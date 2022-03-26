import logging
import os
import shutil
import subprocess

repo_url = os.environ.get("TIMESERIES_SERVER_REPO")
sqlite_path = os.environ.get("TIMESERIES_SERVER_SQLITE_PATH")  # NOT FULL FILENAME
# os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("TIMESERIES_SERVER_REPO_PATH")
# os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/timeseries_server/main.py"


try:
    shutil.rmtree(local_repo_path)
    logging.info("removed local repo at path: %s", local_repo_path)
except Exception as e:
    logging.exception(
        "could not remove local repo at path: %s, with error: %s",
        local_repo_path,
        repr(e),
    )
