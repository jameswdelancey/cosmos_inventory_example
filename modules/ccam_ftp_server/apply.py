import logging
import os
import subprocess
import urllib.request

repo_url = os.environ.get("CCAM_WEB_SERVER_REPO_URL")

config_url = os.environ.get("CCAM_WEB_SERVER_DATA_DIR")
os.makedirs(config_url, exist_ok=True)

local_repo_path = os.environ.get("CCAM_WEB_SERVER_REPO_PATH")
local_repo_python_entrypoint_long_fn = local_repo_path + "/ccam_web_server/main.py"

SERVER_NAMES = ["run_ccam_ftp_server"]
UNIT_FILE_PAYLOADS = []
for server in SERVER_NAMES:
    UNIT_FILE_PAYLOADS.append(
        """\
[Unit]
Description=C Camera Recorder Server %s
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
"""
        % (server, local_repo_path, local_repo_python_entrypoint_long_fn, server)
    )
FILENAMES_FOR_UNITFILES = [f"{server}.service" for server in SERVER_NAMES]
PATH_FOR_UNITFILE = "/etc/systemd/system"

unitfile_fullpaths = []
for fn in FILENAMES_FOR_UNITFILES:
    unitfile_fullpaths.append("%s/%s" % (PATH_FOR_UNITFILE, fn))

COMMANDS_TO_START_AND_ENABLE_SERVICE = [
    ["systemctl", "daemon-reload"],
    ["systemctl", "enable", FILENAME_FOR_UNITFILE],
    ["systemctl", "start", FILENAME_FOR_UNITFILE],
]

COMMANDS_TO_RESTART_SERVICE = [
    ["systemctl", "restart", FILENAME_FOR_UNITFILE],
]

if not os.path.exists(unitfile_fullpath):
    logging.info(
        "unitfile_fullpath %s does not exist, continuing with systemd install",
        unitfile_fullpath,
    )
    # copy in binary
    logging.info("copying in binary from url %s", WEB_FILE_PATH)
    urllib.request.urlretrieve(WEB_FILE_PATH, LOCAL_FILE_PATH)

    logging.info("creating unitfile at path %s", unitfile_fullpath)
    # write unit file
    with open(unitfile_fullpath, "w") as f:
        f.write(UNIT_FILE_PAYLOAD)

    # enable unit file
    for command in COMMANDS_TO_START_AND_ENABLE_SERVICE:
        logging.info("running command to start and enable services %s", repr(command))
        subprocess.check_output(command)
