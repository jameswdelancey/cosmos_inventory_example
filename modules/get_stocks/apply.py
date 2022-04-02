import logging
import os
import subprocess

repo_url = os.environ.get("GET_STOCKS_REPO")
config_path = os.environ.get("GET_STOCKS_CONFIG_PATH")  # NOT FULL FILENAME
os.makedirs(config_path, exist_ok=True)
sqlite_path = os.environ.get("GET_STOCKS_DATA_PATH")  # NOT FULL FILENAME
os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("GET_STOCKS_REPO_PATH")
os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/get_stocks/main.py"

# SERVER_NAMES = ["run_collection_server", "run_ui_server", "run_detectors"]
# UNIT_FILE_PAYLOADS = []
# for server in SERVER_NAMES:
#     UNIT_FILE_PAYLOADS.append(
#         """\
# [Unit]
# Description=TimeseriesServer API Server %s
# StartLimitInterval=400
# StartLimitBurst=5
# [Service]
# Type=simple
# EnvironmentFile=/etc/environment
# WorkingDirectory=%s
# ExecStart=/usr/local/bin/poetry run python '%s' '%s'
# Restart=always
# RestartSec=30
# # WatchdogSec=60
# KillMode=process
# User=pi
# Group=pi
# [Install]
# WantedBy=multi-user.target
# """
#         % (server, local_repo_path, local_repo_python_entrypoint_long_fn, server)
#     )
# FILENAMES_FOR_UNITFILES = [f"{server}.service" for server in SERVER_NAMES]
# PATH_FOR_UNITFILE = "/etc/systemd/system"

# unitfile_fullpaths = []
# for fn in FILENAMES_FOR_UNITFILES:
#     unitfile_fullpaths.append("%s/%s" % (PATH_FOR_UNITFILE, fn))


if not os.path.exists(local_repo_path):
    git_output = subprocess.check_output(["git", "clone", repo_url, local_repo_path])
    logging.debug("git clone output: %s", git_output.decode())
else:
    git_output = subprocess.check_output(
        ["git", "-C", local_repo_path, "reset", "--hard"]
    )
    logging.debug("git reset output: %s", git_output.decode())
    git_output = subprocess.check_output(["git", "-C", local_repo_path, "clean", "-fd"])
    logging.debug("git clean output: %s", git_output.decode())
    git_output = subprocess.check_output(["git", "-C", local_repo_path, "pull"])
    logging.debug("git pull output: %s", git_output.decode())


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

    # # reapply unitfile
    # for unitfile_fullpath, payload in zip(unitfile_fullpaths, UNIT_FILE_PAYLOADS):
    #     try:
    #         logging.info("creating unitfile at path %s", unitfile_fullpath)
    #         with open(unitfile_fullpath, "w") as f:
    #             f.write(payload)
    #     except Exception as e:
    #         logging.exception(
    #             "error creating unitfile at path %s with error %s",
    #             unitfile_fullpath,
    #             repr(e),
    #         )

    # # refresh systemd daemon
    # COMMANDS_TO_RUN = [
    #     ["systemctl", "daemon-reload"],
    # ]
    # for fn in FILENAMES_FOR_UNITFILES:
    #     COMMANDS_TO_RUN.extend(
    #         [["systemctl", "restart", fn]]
    #     )
    # for command in COMMANDS_TO_RUN:
    #     logging.info("running command to refresh systemd daemon %s", repr(command))
    #     subprocess.run(command)

    # # restart service
    # COMMANDS_TO_RUN = [["systemctl", "restart", fn] for fn in FILENAMES_FOR_UNITFILES]
    # for command in COMMANDS_TO_RUN:
    #     logging.info("running command to restart services %s", repr(command))
    #     subprocess.check_output(command)
