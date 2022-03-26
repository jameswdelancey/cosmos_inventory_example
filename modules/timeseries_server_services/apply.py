import logging
import os
import subprocess

local_repo_path = os.environ.get("TIMESERIES_SERVER_REPO_PATH")
os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/timeseries_server/main.py"
sqlite_path = os.environ.get("TIMESERIES_SERVER_DATA_DIR")  # NOT FULL FILENAME
os.makedirs(sqlite_path, exist_ok=True)

SERVER_NAMES = ["run_collection_server", "run_ui_server", "run_detectors"]
UNIT_FILE_PAYLOADS = []
for server in SERVER_NAMES:
    UNIT_FILE_PAYLOADS.append(
        """\
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
"""
        % (server, local_repo_path, local_repo_python_entrypoint_long_fn, server)
    )
FILENAMES_FOR_UNITFILES = [f"{server}.service" for server in SERVER_NAMES]
PATH_FOR_UNITFILE = "/etc/systemd/system"

unitfile_fullpaths = []
for fn in FILENAMES_FOR_UNITFILES:
    unitfile_fullpaths.append("%s/%s" % (PATH_FOR_UNITFILE, fn))

UNIT_FILE_PAYLOADS_existing = []
for fn in unitfile_fullpaths:
    try:
        with open(fn) as f:
            UNIT_FILE_PAYLOADS_existing.apply(f.read())
    except Exception as e:
        logging.exception("error looking at current files with error %s", repr(e))
        UNIT_FILE_PAYLOADS_existing.apply("")


if UNIT_FILE_PAYLOADS != UNIT_FILE_PAYLOADS_existing:
    # reapply unitfile
    for unitfile_fullpath, payload in zip(unitfile_fullpaths, UNIT_FILE_PAYLOADS):
        try:
            logging.info("creating unitfile at path %s", unitfile_fullpath)
            with open(unitfile_fullpath, "w") as f:
                f.write(payload)
        except Exception as e:
            logging.exception(
                "error creating unitfile at path %s with error %s",
                unitfile_fullpath,
                repr(e),
            )

    # refresh systemd daemon
    COMMANDS_TO_RUN = [
        ["systemctl", "daemon-reload"],
    ]
    for fn in FILENAMES_FOR_UNITFILES:
        COMMANDS_TO_RUN.extend(
            [["systemctl", "enable", fn], ["systemctl", "start", fn]]
        )
    for command in COMMANDS_TO_RUN:
        logging.info("running command to refresh systemd daemon %s", repr(command))
        subprocess.check_output(command)

    # restart service
    COMMANDS_TO_RUN = [["systemctl", "restart", fn] for fn in FILENAMES_FOR_UNITFILES]
    for command in COMMANDS_TO_RUN:
        logging.info("running command to restart services %s", repr(command))
        subprocess.check_output(command)
