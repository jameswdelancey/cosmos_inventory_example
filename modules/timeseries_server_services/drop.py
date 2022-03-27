import logging
import os
import subprocess

repo_url = os.environ.get("TIMESERIES_SERVER_REPO")
sqlite_path = os.environ.get("TIMESERIES_SERVER_SQLITE_PATH")  # NOT FULL FILENAME
# os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("TIMESERIES_SERVER_REPO_PATH")
# os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/timeseries_server/main.py"

SERVER_NAMES = ["run_collection_server", "run_ui_server", "run_detectors"]
FILENAMES_FOR_UNITFILES = [f"{server}.service" for server in SERVER_NAMES]

# stop services
COMMANDS_TO_RUN = [["systemctl", "stop", fn] for fn in FILENAMES_FOR_UNITFILES]
for command in COMMANDS_TO_RUN:
    logging.info("running command to restart services %s", repr(command))
    subprocess.check_output(command)

# disable services
COMMANDS_TO_RUN = [["systemctl", "disable", fn] for fn in FILENAMES_FOR_UNITFILES]
for command in COMMANDS_TO_RUN:
    logging.info("running command to restart services %s", repr(command))
    subprocess.check_output(command)


# remove unitfiles
PATH_FOR_UNITFILE = "/etc/systemd/system"

unitfile_fullpaths = []
for fn in FILENAMES_FOR_UNITFILES:
    unitfile_fullpaths.append("%s/%s" % (PATH_FOR_UNITFILE, fn))


for unitfile_fullpath in unitfile_fullpaths:
    try:
        logging.info("removing unitfile at path %s", unitfile_fullpath)
        os.unlink(unitfile_fullpath)
    except Exception as e:
        logging.exception(
            "error deleting unitfile at path %s with error %s",
            unitfile_fullpath,
            repr(e),
        )

# refresh systemd daemon
COMMANDS_TO_RUN = [
    ["systemctl", "daemon-reload"],
]
for command in COMMANDS_TO_RUN:
    logging.info("running command to update systemctl daemon reload %s", repr(command))
    subprocess.check_output(command)


# try:
#     shutil.rmtree(local_repo_path)
#     logging.info("removed local repo at path: %s", local_repo_path)
# except Exception as e:
#     logging.exception(
#         "could not remove local repo at path: %s, with error: %s",
#         local_repo_path,
#         repr(e),
#     )
