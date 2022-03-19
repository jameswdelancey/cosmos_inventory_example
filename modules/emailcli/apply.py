import os
import subprocess

repo_url = os.environ.get("EMAILCLI_REPO")
sqlite_path = os.environ.get("EMAILCLI_SQLITE_PATH")
os.makedirs(sqlite_path, exist_ok=True)
local_repo_path = os.environ.get("EMAILCLI_REPO_PATH")
os.makedirs(os.path.dirname(local_repo_path), exist_ok=True)
local_repo_python_entrypoint_long_fn = local_repo_path + "/emailcli/main.py"

if not os.path.exists(local_repo_path):
    subprocess.check_output(["git", "clone", repo_url, local_repo_path])

# subprocess.check_output(["git", "-C", local_repo_path, "pull"])
