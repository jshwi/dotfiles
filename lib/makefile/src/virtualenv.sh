SOURCE="$(cd "$(dirname "$0")" && pwd)"  # /lib/make/
MAKEFILE="$(dirname "$SOURCE")"
LIB="$(dirname "$MAKEFILE")"  # /lib/
REPOPATH="$(dirname "$LIB")"  # /
PIPENV_IGNORE_VIRTUALENVS=1
export PIPENV_IGNORE_VIRTUALENVS
cd "$REPOPATH" || return 1
if ! pipenv --venv >/dev/null 2>&1; then
  pipenv install || return 1
fi
_VIRTUAL_ENV="$(pipenv --venv)"
cd - >/dev/null 2>&1 || return 1
VIRTUAL_ENV_BIN="${_VIRTUAL_ENV}/bin"
VIRTUAL_ENV_LIB="${_VIRTUAL_ENV}/lib"
SITE_PACKAGES="${VIRTUAL_ENV_LIB}/$(ls -t -U "$VIRTUAL_ENV_LIB")/site-packages"
PYTHONPATH="${PYTHONPATH}:${REPOPATH}"
PYTHONPATH="${PYTHONPATH}:${VIRTUAL_ENV_LIB}"
PYTHONPATH="${PYTHONPATH}:${VIRTUAL_ENV_BIN}"
PYTHONPATH="${PYTHONPATH}:${SITE_PACKAGES}"
PYTHONPATH="${PYTHONPATH}:${MAKEFILE}"
PATH="${PATH}:${VIRTUAL_ENV_BIN}"
OLDPWD="$PWD"
export PIPENV_IGNORE_VIRTUALENVS
export export PIPENV_IGNORE_VIRTUALENVS
export VIRTUAL_ENV_BIN
export VIRTUAL_ENV_LIB
export SITE_PACKAGES
export PYTHONPATH
export PATH
export OLDPWD
