import logging
import os
import subprocess

repo_url = os.environ.get("TIMESERIES_SERVER_REPO")
sqlite_path = os.environ.get("TIMESERIES_SERVER_DATA_DIR")  # NOT FULL FILENAME
os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("TIMESERIES_SERVER_REPO_PATH")
os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/timeseries_server/main.py"

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


