# ======================================================================
#
#          FILE: lib.sh
#
#         USAGE: source lib.sh to add global variables and functions to
#                shell
#
#   DESCRIPTION: All environment variables and functions used by this
#                project's Makefile. Alternating variables for site
#                packages and virtual environment packages.
#                Allow for `make' to navigate repository and appropriate
#                bin directory for user or root. Export all variables
#                for other scripts to use.
#
#       OPTIONS: ---
#  REQUIREMENTS: python3.8,pipenv
#          BUGS: ---
#         NOTES: This script aims to follow Google's `Shell Style Guide'
#                https://google.github.io/styleguide/shellguide.html
#        AUTHOR: Stephen Whitlock (jshwi), stephen@jshwisolutions.com
#  ORGANIZATION: Jshwi Solutions
#       CREATED: 05/09/20 11:39:45
#      REVISION: 1.0.0
#
# shellcheck disable=SC1090,SC2153
# ======================================================================
# ---source this script only once ---
[ -n "$MAKEFILE_ENV" ] && return; MAKEFILE_ENV=0; # pragma once
SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export SOURCE
export MAKEFILE

source "${SOURCE}/virtualenv.sh"

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"  # /lib/make/
MAKEFILE="$(dirname "$SOURCE")"
LIB="$(dirname "$MAKEFILE")"  # /lib/
REPOPATH="$(dirname "$LIB")"  # /

export REPOPATH

if git symbolic-ref --short HEAD >/dev/null 2>&1; then
  TRAVIS_BRANCH=$(git symbolic-ref --short HEAD)
else
  TRAVIS_BRANCH=
fi
REPONAME="$(basename "$REPOPATH")"  # /<REPONAME>
ENVFILE="${REPOPATH}/.env"  # /.env
WORKPATH="${REPOPATH}/build"
TESTS="${REPOPATH}/tests"
WHITELIST="${REPOPATH}/whitelist.py"
PYLINTRC="${REPOPATH}/.pylintrc"
COVERAGEXML="${REPOPATH}/coverage.xml"
COVERAGEXML="${REPOPATH}/setup.py"
LOCKPATH="${REPOPATH}/Pipfile.lock"
READMEPATH="${REPOPATH}/README.rst"
SETUP="${REPOPATH}/setup.py"

export REQUIREMENTS
export LOCKPATH
export READMEPATH
export DOCS
export WHITELIST
export SETUP
export TESTS

DISTPATH="${REPOPATH}/dist"
DOCS="${REPOPATH}/docs"
REQUIREMENTS="${REPOPATH}/requirements.txt"
[ -f "$ENVFILE" ] && source "$ENVFILE"
if [[ "$EUID" -eq 0 ]]; then
  BIN="/usr/local/bin"
else
  BIN="${HOME}/.local/bin"
fi
INSTALLED="${BIN}/${REPONAME}"
if ! APP_PATH="$(python3 -c "from src import get_path; get_path()")"; then
  APP_PATH="${REPOPATH}/${REPONAME}"
fi
MAIN="${APP_PATH}/__main__.py"
SPECPATH="${APP_PATH}.spec"
COMPILED="${DISTPATH}/${REPONAME}"
DOCSCONF="${DOCS}/conf.py"
DOCSBUILD="${DOCS}/_build"
PYITEMS=(
  "$APP_PATH"
  "$TESTS"
  "$DOCSCONF"
  "$MAKEFILE"
)

if [ -t 1 ]; then
  RED=$(printf '\033[31m')
  GREEN=$(printf '\033[32m')
  YELLOW=$(printf '\033[33m')
  CYAN=$(printf '\033[36m')
  BOLD=$(printf '\033[1m')
  RESET=$(printf '\033[m')
else
  RED=
  GREEN=
  YELLOW=
  CYAN=
  BOLD=
  RESET=
fi
TICK="${GREEN}✔${RESET}"
CROSS="${RED}✘${RESET}"


# ======================================================================
# Stylize and announce process in cyan
#
# Globals:
#   BOLD
#   CYAN
#   RESET
# Arguments:
#   Announcement as a string
# Outputs:
#   Stylized announcement
# Returns:
#   `0' if all goes OK
# ======================================================================
make_announce () {
  echo
  echo "${BOLD}${CYAN}+ --- make $1 ---${RESET}"
}

# ======================================================================
# Pass the path to expected executable for this function. If the file
# does not exist then install the project development dependencies from
# `Pipfile.lock'.
# Globals:
#   REPOPATH
# Arguments:
#   Expected path to executable
#   Optional --dev flag for development installations
# Outputs:
#   Installation information from `pipenv'
# Returns:
#   `0' if everything works as should, `1' if for some reason the
#   repository cannot be entered
# ======================================================================
check_reqs () {
  items=( "$1" )
  installed=1
  for item in "${items[@]}"; do
    if ! command -v "$item" >/dev/null 2>&1; then
      installed=0
      break
    fi
  done
  unset items
  if [ "$installed" -eq 0 ]; then
    cd "$REPOPATH" || return 1
    if [ "$2" == "--dev" ]; then
      pipenv install --dev
    else
      pipenv install
    fi
  fi
}


# ======================================================================
# Announce error and return exit code 1
# Arguments:
#   Error message
# Outputs:
#   Error message as stderr with datetime
# Returns:
#   An exit code of 1
# ======================================================================
err() {
  echo "$*" >&2
  return 1
}


# ======================================================================
# Remove an array of files or directories if they exist. Announce this
# to the user if the file or directory exists. If the item does not
# exist as either then exit silently. Unset the array so every
# invocation of this function begins with a fresh array.
# Arguments:
#   An array of files/ directories
# Outputs:
#   Announces to the user that the file or directory is being removed
# ======================================================================
rm_force_recurse() {
  items=( "$1" )
  for item in "${items[@]}"; do
    if [ -e "$item" ]; then
      echo "Removing $item"
      rm -rf "$item"
    fi
  done
  unset items
}


# ======================================================================
# Check that the branch is being pushed as master (or other branch for
# tests). If the correct branch is the one in use deploy `gh-pages' to
# the orphaned branch - otherwise do nothing and announce.
# Globals:
#   TRAVIS_BRANCH
#   GREEN
#   RESET
# Arguments:
#   Optional argument for alternative branch, otherwise the value will
#   remain `master'
# Outputs:
#   Build information or announces that no deployment is taking place
#   if not pushing as master
# Returns:
#   `0' if the build succeeds or documentation is skipped, `1' if the
#   build fails
# ======================================================================
make_deploy_docs () {
  branch="${1:-"master"}"
  if [[ "$TRAVIS_BRANCH" =~ ^("$branch"$|^[0-9]+\.[0-9]+\.X)$ ]]; then
      if [[ -n "$GH_NAME" && -n "$GH_EMAIL" ]]; then
        mv docs/_build/html .
        cp README.rst html
        git stash

        # checkout to root commit
        git checkout "$(git rev-list --max-parents=0 HEAD | tail -n 1)"
        git checkout --orphan gh-pages

        # set `Travis CI' env variables in build's global gitconfig
        git config --global user.email "$GH_EMAIL"
        git config --global user.name "$GH_NAME"

        rm_force_recurse docs  # remove empty docs dir
        git rm -rf .  # versioned
        git clean -fdx --exclude="/html"

        touch ".nojekyll"  # submitting `html' documentation, not `jekyll'
        mv html/* .  # unpack html contents into root of project
        rm_force_recurse html  # remove empty html dir
        url="https://${GH_NAME}:${GH_TOKEN}@github.com/${GH_NAME}/${REPONAME}.git"
        git add .
        git commit -m "[ci skip] Publishes updated documentation"
        git remote rm origin  # separate `gh-pages' branch from `master'
        git remote add origin "$url"  # add the new `gh-pages' orphan
        git push origin gh-pages -f  # overwrite any previous builds with -f
        git checkout "$branch"
      else
        echo "GH_NAME and GH_EMAIL env variables not set"
        echo "+ pushing skipped"
      fi
  else
    echo "${GREEN}+ Documentation not for ${branch}${RESET}"
    echo "+ pushing skipped"
  fi
}


# ======================================================================
# Upload coverage data to `codecov'
# Globals:
#   COVERAGEXML
#   CODECOV
#   CODECOV_TOKEN
# Arguments:
#   API token
# ======================================================================
make_deploy_cov () {
  if [ -f "$COVERAGEXML" ]; then
    check_reqs codecov
    codecov --file "$COVERAGEXML" --token "$CODECOV_TOKEN" || return "$?"
  else
    echo "no coverage report found"
  fi
}


# ======================================================================
# Make sure `Black' is installed. Call `Black' to format python files
# and directories if they exist.
# Globals:
#   BLACK
#   PYITEMS
# Arguments:
#   None
# Outputs:
#   Information about what files were and were not formatted from
#   `Black'
# Returns:
#   `0' if formatting succeeds or there is nothing to format, non-zero
#   exit code (determined by `Black') if there is a parse error in any
#   of the python files
# ======================================================================
make_format () {
  check_reqs black --dev
  for item in "${PYITEMS[@]}"; do
    if [ -e "$item" ]; then
      black "$item"
    fi
  done
  unset items
}


# ======================================================================
# Ensure `pylint' is installed. If not then install development
# dependencies with `pipenv'.
# Lint all python files with `pylint'.
# Globals:
#   PYLINT
#   PYLINTRC
#   PYITEMS
# Arguments:
#   None
# Outputs:
#   Colored linting output with `pylint'
# Returns:
#   `0' if the linting executes as should, non-zero exit code
#   (determined by `pylint') if `pylint' is unable to parse `.pylintrc'
#   file or is unable to find the sources root
# ======================================================================
make_lint () {
  _pylint () {
    pylint "$1" --output-format=colorized || return "$?"
  }

  _rcfile () {
    pylint \
        "$1" \
        --output-format=colorized \
        --rcfile="$PYLINTRC" \
        || return "$?"
  }

  check_reqs pylint --dev
  for item in "${PYITEMS[@]}"; do
    if [ -e "$item" ]; then
      if [ -f "$PYLINTRC" ]; then
          _rcfile "$item" || return "$?"
      else
        _pylint "$item" || return "$?"
      fi
    fi
  done
  unset items
}


# ======================================================================
# Ensure `pytest' is installed. If it is not then install development
# dependencies with `pipenv'. Run the package unit-tests with `pytest'.
# Globals:
#   TESTS
#   PYTEST
# Arguments:
#   None
# Outputs:
#   Test results
# Returns:
#   `0' if the tests pass, non-zero if they fail (determined by
#   `pytest')
# ======================================================================
make_tests () {
  if python -c "from src import check_tests; check_tests()"; then
    check_reqs pytest --dev
    pytest --color=yes "$TESTS" -vv || return "$?"
  else
    echo "no tests found"
  fi
}


# ======================================================================
# Ensure `pytest' and `coverage' are installed. If it is not then
# install development dependencies with `pipenv'. Run the package
# unittests with `pytest' and `coverage'.
# Globals:
#   TESTS
#   PYTEST
#   COVERAGE
#   APP_PATH
# Arguments:
#   None
# Outputs:
#   Test results and coverage information
# Returns:
#   `0' if the tests pass, non-zero if they fail (determined by
#   `pytest')
# ======================================================================
make_coverage () {
  if python -c "from src import check_tests; check_tests()"; then
    items=( pytest coverage )
    for item in "${items[@]}"; do
      check_reqs "$item" --dev
    done
    pytest --color=yes --cov=. "$TESTS" -vv || return "$?"
    coverage xml
    unset items
  else
    echo "no tests found"
  fi
}


# ======================================================================
# Create <PACKAGENAME>.rst from package directory.
# Globals:
#   DOCSCONF
#   LIBMAKE
# Returns:
#   `0' if all goes ok
# ======================================================================
make_toc () {
  if [ -f "$DOCSCONF" ]; then
    python -c "from src import make_toc; make_toc()" || return "$?"
  fi
}


# ======================================================================
# Clean any prior existing builds. Check that there is a path to
# `sphinx-build - if not install development dependencies (which will
# include the `Sphinx' meta-package where `sphinx-build' is found).
# Replace the title of `README.rst' with `README' so the hyperlink isn't
# exactly the same as the package documentation. Run `make html' to
# build the `Sphinx' html documentation. Return the README's title to
# what it originally was (the name of the package).
# Globals:
#   SPHINXBUILD
#   DOCSBUILD
#   LIBMAKE
#   SPHINXBUILD
#   DOCS
#   DOCSCONF
# Arguments:
#   None
# Outputs:
#   Building process and announce successful completion
# Returns:
#   `0' if the build is successful, non-zero exit code (determined by
#   `Sphinx') if the build fails
# ======================================================================
make_docs () {

  "${MAKEFILE}/toc" || exit"$?"

  # allow for cleanup before exit in the case that there is an error
  if [ -f "$DOCSCONF" ]; then
    check_reqs sphinx-build --dev
    rm_force_recurse "$DOCSBUILD"
    original="$(python3 -c "from src import make_title; make_title('README')")"
    sphinx-build -M html "$DOCS" "$DOCSBUILD"
    rc=$?
    python3 \
        -c \
        "from src import make_title; make_title(${original})" &>/dev/null
    exit $rc
  else
    echo "no docs found"
  fi
}


# ======================================================================
# Run `mypy' on all python files to check that there are no errors
# between the files and their stub-files.
# Globals:
#   MYPY
#   PYITEMS
# Arguments:
#   None
# Outputs:
#   Results yielded by `mypy'
# Returns:
#   `0' if everything checks out - possible non-zero exit code if there
#   are errors in the stub-files (determined by `mypy'
# ======================================================================
make_typecheck () {
  check_reqs mypy --dev
  for item in "${PYITEMS[@]}"; do
    if [ -e "$item" ]; then
      mypy --ignore-missing-imports "$item" || exit "$?"
    fi
  done
  unset items
}


# ======================================================================
# Run `vulture' on all python files to inspect them for unused code
# Run the nested function and send stdout / stderr to /dev/tty so output
# can be captured through second stream. Notify user that there are no
# problems rather than just displaying nothing which can looks as though
# nothing has occurred.
# Globals:
#   VULTURE
#   WHITELIST
#   PYITEMS
# Arguments:
#   None
# Outputs:
#   Unused code from `vulture' or a message indicating nothing was found
# Returns:
#   `0' if all non-whitelisted code is used, possibly non-zero
#   (determined by `vulture') for code that isn't
# ======================================================================
make_unused () {

  _vulture () {
    check_reqs vulture --dev
    [ -f "$WHITELIST" ] || touch "$WHITELIST"
    for item in "${PYITEMS[@]}"; do
      if [ -e "$item" ]; then
        vulture "$item" "$WHITELIST" || return "$?"
      fi
    done
    unset items
  }

  if _vulture; then
    echo "vulture found no problems"
  else
    exit "$?"
  fi
}


# ======================================================================
# Update vulture whitelist for all python files.
# Globals:
#   LIBMAKE
#   VULTURE
#   PYITEMS
# Arguments:
#   None
# Returns:
#   `0' if all goes ok
# ======================================================================
make_whitelist () {
  check_reqs vulture --dev
  python3 -c "from src import make_whitelist; make_whitelist('${PYITEMS[*]}')"
}


# ======================================================================
# Convert `Pipfile.lock' to `requirements.txt' (transfer prod and dev
# packages across). Remove the additional information after the `;'
# delim. Sort `requirements.txt' and remove duplicates. Notify user that
# all went well.
# Globals:
#   PIPFILE2REQ
#   LIBMAKE
#   PYITEMS
# Returns:
#   `0' if all goes ok
# ======================================================================
make_requirements () {
  check_reqs pipfile2req --dev
  python3 -c "from src import make_requirements; make_requirements()"
}


# ======================================================================
# If a non-default install mechanism is preferred then the
# ``INSTALL_SCRIPT`` env variable may be set. The variable should be the
# path to the script relative to the Makefile. If the variable exists
# then the script will be executed by ``make install``. No arguments can
# be provided when installing with this method.
# Globals:
#   INSTALL_SCRIPT
# Arguments:
#   None
# Outputs:
#   Announces to user what is taking place with the build
# Return:
#   `0' if build succeeds, otherwise non-zero exit code (determined
#   by `Pyinstaller') or `1'
# ======================================================================
make_install () {
  if [ -n "$INSTALL_SCRIPT" ]; then
    script_path="$REPOPATH/$INSTALL_SCRIPT"
    if [ -e "$script_path" ]; then
      "$script_path"
    fi
  else
    if [ -f "$MAIN" ]; then
      echo "${GREEN}Installing ${REPONAME}${RESET}"
      check_reqs pyinstaller --dev
      items=( "$WORKPATH" "$DISTPATH" "$SPECPATH" )
      for item in "${items[@]}"; do
        if [ -e "$item" ]; then
          echo "${YELLOW}removing prior build cache...${RESET}"
          rm_force_recurse "${items[@]}"
          break
        fi
      done
      if [ ! -d "$BIN" ]; then
        mkdir -p "$BIN";
        echo "created $BIN"
        echo "to run add $BIN to your PATH"
      elif [ -f "$INSTALLED" ]; then
        echo "${YELLOW}removing existing binaries...${RESET}"
        rm_force_recurse "$INSTALLED"
      fi
      echo "${YELLOW}compiling package...${RESET}"
      pyinstaller \
          --onefile \
          --distpath "$DISTPATH" \
          --workpath "$WORKPATH" \
          --specpath "$REPOPATH" \
          --log-level ERROR \
          --name "$REPONAME" \
          "$MAIN"
      echo "${YELLOW}adding ${REPONAME} to PATH...${RESET}"
      cp "$COMPILED" "$INSTALLED" || exit 1
      dexe="${COMPILED/"$REPOPATH"/""}"
      echo "${dexe:1} -> $INSTALLED"
      echo "${GREEN}${REPONAME} successfully installed${RESET}"
    else
      echo "no package found to install"
    fi
  fi
}


# ======================================================================
# Build all the project files one after the other. This will prevent
# checking that a `pipenv' executable is present every time.
# Arguments:
#   None
# Outputs:
#   Announces to user whether files have been updated or whether
#   updating wasn't necessary
# Return:
#   `0' if everything is OK
# =====================================================================
make_files () {
  "${MAKEFILE}/whitelist"     || return "$?"
  "${MAKEFILE}/toc"           || return "$?"
  "${MAKEFILE}/requirements"  || return "$?"
}


# ======================================================================
# Stylize and announce process in cyan
#
# Globals:
#   BOLD
#   CYAN
#   RESET
# Arguments:
#   Announcement as a string
# Outputs:
#   Stylized announcement
# Returns:
#   `0' if all goes OK
# ======================================================================
announce () {
  echo
  echo "${BOLD}${CYAN}+ --- make $1 ---${RESET}"
}


# ======================================================================
# Run the main functions in this package to confirm quality of repo and
# build
#
# Outputs:
#   Various process announcements called from lib functions
# Returns:
#   `0' if all goes OK
# ======================================================================
make_build () {
  ( announce "clean"        && "${MAKEFILE}/clean"            ) || exit "$?"
  ( announce "format"       && "${MAKEFILE}/format"           ) || exit "$?"
  ( announce "typecheck"    && "${MAKEFILE}/typecheck"        ) || exit "$?"
  ( announce "unused"       && "${MAKEFILE}/unused"           ) || exit "$?"
  ( announce "coverage"     && "${MAKEFILE}/coverage"         ) || exit "$?"
  ( announce "docs"         && "${MAKEFILE}/docs"             ) || exit "$?"
  ( announce "lint"         && "${MAKEFILE}/lint"             ) || exit "$?"
  ( announce "install"      && "${MAKEFILE}/install"          ) || exit "$?"
  ( announce "deploy-cov'"  && "${MAKEFILE}/deploy-cov" "$@"  ) || exit "$?"
  ( announce "deploy-docs"  && "${MAKEFILE}/deploy-docs" "$@" ) || exit "$?"
}


# ======================================================================
# Determine if `pipenv' installed or exit with a non-zero exit code
# Globals:
#   REPO
#   CROSS
#   TICK
# Arguments:
#   None
# Outputs:
#   Whether `pipenv' installed or not
# Returns:
#   Return `1' if pipenv installation not found
#   `0' if everything works as should, `1' if for some reason the
#   repository cannot be entered
# ======================================================================
make_which () {
  cd "$REPOPATH" || exit 1
  if ! command -v pipenv >/dev/null 2>&1; then
    err "${CROSS} \`pipenv' not found"
  else
    echo "${TICK} $(command -v pipenv)"
  fi
}

# ======================================================================
# Remove every build element from repository and remove installed binary
# from site or user bin directory.
# Instruct `pipenv' to destroy the repository's virtual environment.
# Create an array of the command outputs to find out if there was a
# result whilst still displaying output by directing the stream to
# /dev/tty
# If there was no output then the package was not installed so notify
# the user
# Globals:
#   VIRTUAL_ENV
#   YELLOW
#   REPONAME
#   RESET
# Arguments:
#   None
# Outputs:
#   Announces to the user that files and directories are being removed
#   or announces that nothing took place
# ======================================================================
make_uninstall () {
  if pipenv --venv >/dev/null 2>&1; then
    VIRTUAL_ENV="$(pipenv --venv)"
  fi
  items=(
    "$(make_clean 2>&1 | tee /dev/tty)"
    "$([[ "$VIRTUAL_ENV" == "" ]] || pipenv --rm 2>&1 | tee /dev/tty)"
    "$(rm_exe 2>&1 | tee /dev/tty)"
  )
  for item in "${items[@]}"; do
    if [ "$item" != "" ]; then
      echo
      echo "${YELLOW}${REPONAME} uninstalled successfully${RESET}"
      exit 0
    fi
  done
  echo "${REPONAME} is not installed"
}


# ======================================================================
# Remove all unversioned directories and files with `git'.
# Globals:
#   REPOPATH
# Arguments:
#   None
# Outputs:
#   Files and directories removed by git
# Returns:
#   None-zero exit code if function fails to entry repository otherwise
#   zero
# ======================================================================
make_clean () {
  cd "$REPOPATH" || exit 1
  git clean \
      -fdx \
      --exclude=".env" \
      --exclude="instance" \
      --exclude="bundle" \
      --exclude="zsh_history" \
      --exclude="bash_history" \
      --exclude="vimrc" \
      --exclude=".cache"
  cd - >/dev/null 2>&1 || exit 1
}
