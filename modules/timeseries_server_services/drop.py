import os, logging, subprocess
FILENAME_FOR_UNITFILE = "ccam.service"
PATH_FOR_UNITFILE = "/etc/systemd/system"
unitfile_fullpath = "%s/%s" % (PATH_FOR_UNITFILE, FILENAME_FOR_UNITFILE)

WEB_FILE_PATH = os.environ.get("S3_BUCKET_ARTIFACTS") + "/ccam"
LOCAL_FILE_PATH = "/usr/local/bin/ccam"

COMMANDS_TO_STOP_AND_DISABLE_SERVICE = [
    ["systemctl", "disable", FILENAME_FOR_UNITFILE],
    ["systemctl", "stop", FILENAME_FOR_UNITFILE],
]

COMMANDS_TO_PURGE_SYSTEMD_CONFIG = [
    ["systemctl", "daemon-reload"],
]

# DISABLE unit file
try:
    for command in COMMANDS_TO_STOP_AND_DISABLE_SERVICE:
        logging.info("running command to STOP and DISABLE services %s", repr(command))
        subprocess.check_output(command)
except Exception as e:
    logging.exception(
        "error while stopping and disabling service with error %s", repr(e)
    )

# remove systemd unitfile
try:
    os.unlink(unitfile_fullpath)
except Exception as e:
    logging.exception("error removing systemd unit file with error %s", repr(e))

# PURGE COMMANDS TO SYSTEMD CONFIG
try:
    for command in COMMANDS_TO_PURGE_SYSTEMD_CONFIG:
        logging.info("running command to PURGE UNITFILE FROM SYSTEMD %s", repr(command))
        subprocess.check_output(command)
except Exception as e:
    logging.exception(
        "error while PURGING UNIT FILE FROM SYSTEMD with error %s", repr(e)
    )


# data and config should be under other directories
# set by environment vars, therefore they will not be
# deleted with the following operation to remove the
# repo
try:
    os.unlink(LOCAL_FILE_PATH)
    logging.info("removed local repo at path: %s", LOCAL_FILE_PATH)
except Exception as e:
    logging.exception(
        "could not remove local BINARY at path: %s, with error: %s",
        LOCAL_FILE_PATH,
        repr(e),
    )
