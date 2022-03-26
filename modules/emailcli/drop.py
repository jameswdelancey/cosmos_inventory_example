import os
import logging
import subprocess
import shutil

repo_url = os.environ.get("EMAILCLI_REPO")
sqlite_path = os.environ.get("EMAILCLI_SQLITE_PATH") # NOT FULL FILENAME
# os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("EMAILCLI_REPO_PATH")
# os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/emailcli/main.py"

# data and config should be under other directories
# set by environment vars, therefore they will not be
# deleted with the following operation to remove the
# repo
try:
    shutil.rmtree(local_repo_path)
    logging.info("removed local repo at path: %s", local_repo_path)
except Exception as e:
    logging.exception("could not remove local repo at path: %s, with error: %s", local_repo_path, repr(e))
