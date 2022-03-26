import os
import logging
import subprocess
repo_url = os.environ.get("TIMESERIES_SERVER_REPO")
sqlite_path = os.environ.get("TIMESERIES_SERVER_SQLITE_PATH") # NOT FULL FILENAME
os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("TIMESERIES_SERVER_REPO_PATH")
os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/timeseries_server/main.py"

SERVER_NAMES = ["run_collection_server", "run_ui_server", "run_detectors"]
UNIT_FILE_PAYLOADS = [f"""\
[Unit]
Description=TimeseriesServer API Server {servers}
StartLimitInterval=400
StartLimitBurst=5
[Service]
Type=simple
ExecStart=/usr/bin/python3 {local_repo_python_entrypoint_long_fn} {servers}
Restart=always
RestartSec=30
# WatchdogSec=60
KillMode=process
User=pi
Group=pi
[Install]
WantedBy=multi-user.target
""" for servers in SERVER_NAMES]
FILENAMES_FOR_UNITFILES = [f"{}.service" for servers in SERVER_NAMES]
PATH_FOR_UNITFILE = "/etc/systemd/system"
unitfile_fullpaths = ["%s/%s" % (PATH_FOR_UNITFILE, fn) for fn in FILENAMES_FOR_UNITFILES]


# I dont want to use systemd for everything because it will not
# work on windows but we can do something that works on both
# 
# timer_unit_file_full_fn = "/etc/systemd/system/ccam.timer"
# service_unit_file_full_fn = "/etc/systemd/system/ccam.service"


if not os.path.exists(local_repo_path):
    git_output = subprocess.check_output(["git", "clone", repo_url, local_repo_path])
    logging.debug("git clone output: %s", git_output.decode())

git_output = subprocess.check_output(
    ["git", "-C", local_repo_path, "reset", "--hard"]
)
logging.debug("git reset output: %s", git_output.decode())
git_output = subprocess.check_output(
    ["git", "-C", local_repo_path, "clean", "-fd"]
)
logging.debug("git clean output: %s", git_output.decode())
git_output = subprocess.check_output(
    ["git", "-C", local_repo_path, "pull"]
)
logging.debug("git pull output: %s", git_output.decode())


# update local if repo changed
repo_changed = "Already up to date." not in git_output.decode()

if repo_changed:
    os.chdir(local_repo_path)

    # refresh poetry requirements
    COMMANDS_TO_RUN = [
        ["poetry", "install"],
    ]
    for command in COMMANDS_TO_RUN:
        logging.info("running command to refresh poetry %s", repr(command))
        subprocess.check_output(command)
    
    # reapply unitfile
    for unitfile_fullpath, payload in zip(unitfile_fullpaths, UNIT_FILE_PAYLOADS):
        try:
            logging.info("creating unitfile at path %s", unitfile_fullpath)
            with open(unitfile_fullpath, "w") as f:
                f.write(payload)
        except Exception as e:
            logging.exception("error creating unitfile at path %s with error %s", unitfile_fullpath, repr(e))

    # refresh systemd daemon
    COMMANDS_TO_RUN = [
        ["systemctl", "daemon-reload"],
    ] + [
        ["systemctl", "enable", fn],
        ["systemctl", "start", fn],
        for fn in FILENAMES_FOR_UNITFILES
    ]
    for command in COMMANDS_TO_RUN:
        logging.info("running command to refresh systemd daemon %s", repr(command))
        subprocess.check_output(command)

    # restart service
    COMMANDS_TO_RUN = [
        ["systemctl", "restart", fn],
        for fn in FILENAMES_FOR_UNITFILES
    ]
    for command in COMMANDS_TO_RUN:
        logging.info("running command to restart services %s", repr(command))
        subprocess.check_output(command)
