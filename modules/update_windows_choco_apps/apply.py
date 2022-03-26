import datetime

# import os
import logging
import subprocess

out = subprocess.check_output(
    ["choco", "feature", "enable", "-n=allowGlobalConfirmation"]
)
logging.debug("choco feature enable allowGlobalConfirmation output: %s", out.decode())

if datetime.datetime.now().hour == 12:
    out = subprocess.check_output(["choco", "update", "all"])
    logging.debug("choco upgrade all output: %s", out.decode())
