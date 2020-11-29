"""
pyfunctions.env
===============
"""
import datetime
import os
import pathlib

HOME = str(pathlib.Path.home())
DATE = datetime.date.today().strftime("%Y/%m/%d")
TIME = datetime.datetime.now().strftime("%H:%M:%S")
GNUPG_PASSPHRASE = os.environ.get("GNUPG_PASSPHRASE", "")
PIPFILELOCK = "Pipfile.lock"
README = "README.rst"
REQUIREMENTS = "requirements.txt"
WHITELIST = "whitelist.py"
PACKAGE = os.path.dirname(os.path.realpath(__file__))
PYLIB = os.path.dirname(PACKAGE)
LIB = os.path.dirname(PYLIB)
REPOPATH = os.path.dirname(LIB)
DOCS = os.path.join(REPOPATH, "docs")
LOCKPATH = os.path.join(REPOPATH, PIPFILELOCK)
PACKAGENAME = os.path.basename(REPOPATH)
READMEPATH = os.path.join(REPOPATH, README)
REQPATH = os.path.join(REPOPATH, REQUIREMENTS)
WHITELISTPATH = os.path.join(REPOPATH, WHITELIST)
