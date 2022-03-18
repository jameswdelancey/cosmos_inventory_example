import os
import subprocess
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

COMMANDS_TO_START_AND_ENABLE_SERVICE = [
    ["systemctl", "daemon-reload"],
    ["systemctl", "enable", "ccam.service"],
    ["systemctl", "start", "ccam.service"],
]

COMMANDS_TO_RESTART_SERVICE = [
    ["systemctl", "restart", "ccam.service"],
]

unitfile_fullpath = "%s/%s" % (PATH_FOR_UNITFILE, FILENAME_FOR_UNITFILE)

if not os.path.exists(unitfile_fullpath):
    # copy in binary
    url = os.environ.get("S3_BUCKET_ARTIFACTS") + "/ccam"
    urllib.request.urlretrieve(url, "/usr/local/bin/ccam")

    # write unit file
    with open(unitfile_fullpath, "w") as f:
        f.write(UNIT_FILE_PAYLOAD)

    # enable unit file
    for command in COMMANDS_TO_START_AND_ENABLE_SERVICE:
        subprocess.check_output(command)
