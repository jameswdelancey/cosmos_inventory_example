import os
import subprocess
import logging
import urllib.request

UNIT_FILE_PAYLOAD = """\
[Unit]
Description=C Camera Recorder Service
StartLimitInterval=400
StartLimitBurst=5
[Service]
Type=simple
ExecStart=/usr/local/bin/ccam
Restart=always
RestartSec=30
WatchdogSec=60
KillMode=process
User=pi
Group=pi
[Install]
WantedBy=multi-user.target
"""

FILENAME_FOR_UNITFILE = "ccam.service"
PATH_FOR_UNITFILE = "/etc/systemd/system"
unitfile_fullpath = "%s/%s" % (PATH_FOR_UNITFILE, FILENAME_FOR_UNITFILE)

WEB_FILE_PATH = os.environ.get("S3_BUCKET_ARTIFACTS") + "/ccam"
LOCAL_FILE_PATH = "/usr/local/bin/ccam"

COMMANDS_TO_START_AND_ENABLE_SERVICE = [
    ["systemctl", "daemon-reload"],
    ["systemctl", "enable", FILENAME_FOR_UNITFILE],
    ["systemctl", "start", FILENAME_FOR_UNITFILE],
]

COMMANDS_TO_RESTART_SERVICE = [
    ["systemctl", "restart", FILENAME_FOR_UNITFILE],
]

if not os.path.exists(unitfile_fullpath):
    logging.info("unitfile_fullpath %s does not exist, continuing with systemd install", unitfile_fullpath)
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
