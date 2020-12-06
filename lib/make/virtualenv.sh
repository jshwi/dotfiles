# --- */**/virtalenvs/<REPONAME>-*/ ---
cd "$REPOPATH" || return 1
if ! pipenv --venv >/dev/null 2>&1; then
  pipenv install || return 1
fi
_VIRTUAL_ENV="$(pipenv --venv)"
cd - >/dev/null 2>&1 || return 1

# --- */**/virtalenvs/<REPONAME>-*/* ---
VIRTUAL_ENV_BIN="${_VIRTUAL_ENV}/bin"
VIRTUAL_ENV_LIB="${_VIRTUAL_ENV}/lib"
SITE_PACKAGES="${VIRTUAL_ENV_LIB}/$(ls -t -U "$VIRTUAL_ENV_LIB")/site-packages"

# --- PYTHONPATH ---
PYTHONPATH="${PYTHONPATH}:${REPOPATH}"
PYTHONPATH="${PYTHONPATH}:${VIRTUAL_ENV_LIB}"
PYTHONPATH="${PYTHONPATH}:${VIRTUAL_ENV_BIN}"
PYTHONPATH="${PYTHONPATH}:${SITE_PACKAGES}"
PYTHONPATH="${PYTHONPATH}:${LIBMAKE}"
export PYTHONPATH

# --- PATH ---
PATH="${PATH}:${VIRTUAL_ENV_BIN}"
export PATH

OLDPWD="$PWD"
export OLDPWD
