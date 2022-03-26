import os
import logging
import subprocess

sqlite_path = os.environ.get("TIMESERIES_SERVER_DATA_DIR") # NOT FULL FILENAME
os.makedirs(sqlite_path, exist_ok=True)

SERVER_NAMES = ["run_collection_server", "run_ui_server", "run_detectors"]
UNIT_FILE_PAYLOADS = []
for server in SERVER_NAMES:
    UNIT_FILE_PAYLOADS.append("""\
[Unit]
Description=TimeseriesServer API Server %s
StartLimitInterval=400
StartLimitBurst=5
[Service]
Type=simple
EnvironmentFile=/etc/environment
WorkingDirectory=%s
ExecStart=/usr/local/bin/poetry run python '%s' '%s'
Restart=always
RestartSec=30
# WatchdogSec=60
KillMode=process
User=pi
Group=pi
[Install]
WantedBy=multi-user.target
""" % (server, local_repo_path, local_repo_python_entrypoint_long_fn, server))
FILENAMES_FOR_UNITFILES = [f"{server}.service" for server in SERVER_NAMES]
PATH_FOR_UNITFILE = "/etc/systemd/system"

unitfile_fullpaths = []
for fn in FILENAMES_FOR_UNITFILES:
    unitfile_fullpaths.append("%s/%s" % (PATH_FOR_UNITFILE, fn))

# update local if repo changed
repo_changed = "Already up to date." not in git_output.decode()

if repo_changed:
    os.chdir(local_repo_path)

    # install poetry
    COMMANDS_TO_RUN = [
        ["apt", "install", "-y", "python3-pip"],
        ["pip3", "install", "poetry"],
    ]
    for command in COMMANDS_TO_RUN:
        logging.info("running command to install poetry %s", repr(command))
        subprocess.run(command)

    # refresh poetry requirements
    COMMANDS_TO_RUN = [
        ["poetry", "install"],
        ["chown", "-R", "pi:pi", local_repo_path],
        ["chown", "-R", "pi:pi", sqlite_path],
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
    ]
    for fn in FILENAMES_FOR_UNITFILES:
        COMMANDS_TO_RUN.extend([["systemctl", "enable", fn],
                                ["systemctl", "start", fn]])
    for command in COMMANDS_TO_RUN:
        logging.info("running command to refresh systemd daemon %s", repr(command))
        subprocess.check_output(command)

    # restart service
    COMMANDS_TO_RUN = [
        ["systemctl", "restart", fn]
        for fn in FILENAMES_FOR_UNITFILES
    ]
    for command in COMMANDS_TO_RUN:
        logging.info("running command to restart services %s", repr(command))
        subprocess.check_output(command)