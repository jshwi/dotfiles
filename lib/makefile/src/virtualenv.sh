# ======================================================================
#
#          FILE: virtualenv.sh
#
#         USAGE: virtualenv.sh
#
#   DESCRIPTION:
#
#       OPTIONS: ---
#  REQUIREMENTS: python3.8,pipenv
#          BUGS: ---
#         NOTES: This script aims to follow Google's `Shell Style Guide'
#                https://google.github.io/styleguide/shellguide.html
#        AUTHOR: Stephen Whitlock (jshwi), stephen@jshwisolutions.com
#  ORGANIZATION: Jshwi Solutions
#       CREATED: 08/12/20 22:01:41
#      REVISION: 1.0.0
# ======================================================================
# --- location ---
_MAKEFILE="$(dirname "$(cd "$(dirname "$0")" && pwd)")"
_LIB="$(dirname "$_MAKEFILE")"
_REPOPATH="$(dirname "$_LIB")"

# get path to pipenv environment
# if one doesn't exist, create it
PIPENV_IGNORE_VIRTUALENVS=1
cd "$_REPOPATH" || return 1
if ! pipenv --venv >/dev/null 2>&1; then
  pipenv install || return 1
fi
_VENV="$(pipenv --venv)"
_VENV_BIN="${_VENV}/bin"
_VENV_LIB="${_VENV}/lib"
cd - >/dev/null 2>&1 || return 1
OLDPWD="$PWD"

# --- compile PYTHONPATH ---
PYTHONPATH="${PYTHONPATH}:${_REPOPATH}"
PYTHONPATH="${PYTHONPATH}:${_VENV_BIN}"
PYTHONPATH="${PYTHONPATH}:"${_LIB}
PYTHONPATH="${PYTHONPATH}:${_VENV_LIB}/$(ls -t -U "$_VENV_LIB")/site-packages"

# --- compile PATH ---
PATH="${PATH}:${_VENV_BIN}"

# --- export env ---
export PIPENV_IGNORE_VIRTUALENVS
export PYTHONPATH
export PATH
export OLDPWD
