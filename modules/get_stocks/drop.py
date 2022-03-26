import logging
import os
import shutil
import subprocess

repo_url = os.environ.get("GET_STOCKS_REPO")
sqlite_path = os.environ.get("GET_STOCKS_SQLITE_PATH")  # NOT FULL FILENAME
# os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("GET_STOCKS_REPO_PATH")
# os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/get_stocks/main.py"

# data and config should be under other directories
# set by environment vars, therefore they will not be
# deleted with the following operation to remove the
# repo
try:
    shutil.rmtree(local_repo_path)
    logging.info("removed local repo at path: %s", local_repo_path)
except Exception as e:
    logging.exception(
        "could not remove local repo at path: %s, with error: %s",
        local_repo_path,
        repr(e),
    )
