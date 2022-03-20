import os
import logging
import subprocess

repo_url = os.environ.get("GET_STOCKS_REPO")
sqlite_path = os.environ.get("GET_STOCKS_SQLITE_PATH") # NOT FULL FILENAME
os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("GET_STOCKS_REPO_PATH")
os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/get_stocks/main.py"

# I dont want to use systemd for everything because it will not
# work on windows but we can do something that works on both
# 
# timer_unit_file_full_fn = "/etc/systemd/system/ccam.timer"
# service_unit_file_full_fn = "/etc/systemd/system/ccam.service"


if not os.path.exists(local_repo_path):
    subprocess.check_output(["git", "clone", repo_url, local_repo_path])

git_output = subprocess.check_output(
    ["git", "-C", local_repo_path, "reset", "--hard"]
)
logging.debug("git reset output: %s", git_output.decode())
git_output = subprocess.check_output(
    ["git", "-C", local_repo_path, "clean", "-fd"]
)
logging.debug("git clean output: %s", git_output.decode())
git_output = subprocess.check_output(
    ["git", "-C", local_repo_path, "pull"]
)
logging.debug("git pull output: %s", git_output.decode())

# if not os.path.exists(timer_unit_file_full_fn):
#     git_output = subprocess.check_output(
#         ["systemctl", "daemon-reload"]
#     )
#     logging.debug("systemctl daemon-reload : %s", git_output.decode())
#     git_output = subprocess.check_output(
#         ["systemctl", "enable", "ccam.service"]
#     )
#     logging.debug("systemctl enable ccam.service: %s", git_output.decode())
#     git_output = subprocess.check_output(
#         ["systemctl", "start", "ccam.service"]
#     )
#     logging.debug("systemctl start ccam.service: %s", git_output.decode())
#     git_output = subprocess.check_output(
#         ["systemctl", "status", "ccam.service"]
#     )
#     logging.debug("systemctl status ccam.service: %s", git_output.decode())

# if "Already up to date." not in git_output.decode():
#     git_output = subprocess.check_output(
#         ["systemctl", "daemon-reload"]
#     )
#     logging.debug("systemctl daemon-reload : %s", git_output.decode())
#     git_output = subprocess.check_output(
#         ["systemctl", "restart", "ccam.service"]
#     )
#     logging.debug("systemctl restart ccam.service: %s", git_output.decode())
