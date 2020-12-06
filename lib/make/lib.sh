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
[ -n "$LIBMAKE_ENV" ] && return; LIBMAKE_ENV=0; # pragma once

# --- pipenv env vars ---
PIPENV_IGNORE_VIRTUALENVS=1

# --- repo env ---
LIBMAKE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"  # /lib/make/
PYSHARED="${LIBMAKE}/pyshared"
LIB="$(dirname "$LIBMAKE")"  # /lib/
ENVIRONMENT_TEMPLATES="$LIB/environment"
REPOPATH="$(dirname "$LIB")"  # /
REPONAME="$(basename "$REPOPATH")"  # /<REPONAME>
ENVFILE="${REPOPATH}/.env"  # /.env

# --- / ---
WORKPATH="${REPOPATH}/build"
TESTS="${REPOPATH}/tests"
WHITELIST="${REPOPATH}/whitelist.py"
PYLINTRC="${REPOPATH}/.pylintrc"
COVERAGEXML="${REPOPATH}/coverage.xml"
COVERAGEXML="${REPOPATH}/setup.py"
LOCKPATH="${REPOPATH}/Pipfile.lock"
READMEPATH="${REPOPATH}/README.rst"
SETUP="${REPOPATH}/setup.py"
DISTPATH="${REPOPATH}/dist"
DOCS="${REPOPATH}/docs"
REQUIREMENTS="${REPOPATH}/requirements.txt"
export PIPENV_IGNORE_VIRTUALENVS
export LIBMAKE
export LIB
export REPOPATH
export REQUIREMENTS
export LOCKPATH
export READMEPATH
export DOCS
export WHITELIST
export SETUP
export TESTS

# --- source /lib/make/ ---
source "${LIBMAKE}/colors.sh"
source "${LIBMAKE}/err.sh"
source "${LIBMAKE}/icons.sh"
source "${LIBMAKE}/clean.sh"
source "${LIBMAKE}/virtualenv.sh"

# --- source /.env ---
[ -f "$ENVFILE" ] && source "$ENVFILE"

# --- */**/bin/ ---
if [[ "$EUID" -eq 0 ]]; then
  BIN="/usr/local/bin"
else
  BIN="${HOME}/.local/bin"
fi

# --- install location ---
INSTALLED="${BIN}/${REPONAME}"

# --- */**/<APPNAME>/ ---
if ! APP_PATH="$(python3 "${LIBMAKE}/path.py")"; then
  APP_PATH="${REPOPATH}/${REPONAME}"
fi

# --- */**/<APPNAME>/* ---
MAIN="${APP_PATH}/__main__.py"

# --- / ---
SPECPATH="${APP_PATH}.spec"

# --- /dist ---
COMPILED="${DISTPATH}/${REPONAME}"

# --- /docs ---
DOCSCONF="${DOCS}/conf.py"
DOCSBUILD="${DOCS}/_build"

# --- array of python files and directories ---
PYITEMS=(
  "$APP_PATH"
  "$TESTS"
  "$DOCSCONF"
  "$PYSHARED"
)


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
  items="$1"
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
# Get path to the environment's Python.
# Globals:
#   PYTHON
# Arguments:
#   None
# Outputs:
#   Path to `pipenv' virtualenv Python.
# ======================================================================
get_python () {
  check_reqs >/dev/null 2>&1
  echo "$PYTHON"
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
  items="$1"
  for item in "${items[@]}"; do
    if [ -e "$item" ]; then
      echo "Removing $item"
      rm -rf "$item"
    fi
  done
  unset items
}


# ======================================================================
# Remove the directories and files that result from running Pyinstaller.
# Globals:
#   WORKPATH
#   DISTPATH
#   SPECPATH
#   YELLOW
#   RESET
# Arguments:
#   None
# Outputs:
#   Announces to the user that the file or directory is being removed
# ======================================================================
clean_pyinstaller_build () {
  items=( "$WORKPATH" "$DISTPATH" "$SPECPATH" )
  for item in "${items[@]}"; do
    if [ -e "$item" ]; then
      echo "${YELLOW}removing prior build cache...${RESET}"
      rm_force_recurse "${items[@]}"
      break
    fi
  done
}


# ======================================================================
# Remove existing binary executable from the site or user bin directory.
# Globals:
#   INSTALLED
#   YELLOW
#   RESET
# Arguments
#   None
# Outputs:
#   Announces to the user that the file is being removed
# ======================================================================
rm_exe () {
  if [ -f "$INSTALLED" ]; then
    echo "${YELLOW}removing existing binaries...${RESET}"
    rm_force_recurse "$INSTALLED"
  fi
}


# ======================================================================
# Add and commit the documentation for `gh-pages' deployment. Ensure the
# commit message containing `[ci skip]' - this is all occurring
# automatically during a `Travis CI' build and we do not want to run
# another build for this process which contains no test suite or project
# files. Remove the upstream so we can push to the orphaned remote. Add
# the new orphan remote. Force push (overwrite existing deployments).
# Globals:
#   GH_NAME
#   GH_TOKEN
#   GH_NAME
#   REPONAME
# Arguments:
#   None
# Outputs:
#   Various announcements about the deployment
# Returns:
#   `0' if there are no bugs in the build otherwise potentially `1'
# ======================================================================
commit_docs () {
  url="https://${GH_NAME}:${GH_TOKEN}@github.com/${GH_NAME}/${REPONAME}.git"
  git add .
  git commit -m "[ci skip] Publishes updated documentation"
  git remote rm origin  # separate `gh-pages' branch from `master'
  git remote add origin "$url"  # add the new `gh-pages' orphan
  git push origin gh-pages -f  # overwrite any previous builds with -f
}


# ======================================================================
# Build documentation and deploy to orphaned `gh-pages' branch.
# Globals:
#   GH_EMAIL
#   GH_NAME
# Arguments:
#   None
# Outputs:
#   Build information
# Return:
#   `0' for a successful build, `1' if build fails
# ======================================================================
master_docs () {
  # unpack docs/html directory into project root
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
  commit_docs
  git checkout "$branch"
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
        master_docs || return "$?"
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

  _pylint_rcfile () {
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
          _pylint_rcfile "$item" || return "$?"
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
  if ls "$TESTS/"*_test.py >/dev/null 2>&1 \
      || ls "$TESTS"/test_*.py >/dev/null 2>&1 ; then
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
  if python "$LIBMAKE/check_tests.py"; then
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
    python3 "${LIBMAKE}/toc.py" || return "$?"
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

  _make_docs () {
    check_reqs sphinx-build --dev
    rm_force_recurse "$DOCSBUILD"
    original="$("python3" "${LIBMAKE}/title.py" --replace "README")"
    sphinx-build -M html "$DOCS" "$DOCSBUILD"
    rc=$?
    python3 "${LIBMAKE}/title.py" --replace "$original" &>/dev/null
    return $rc
  }

  make_toc || return "$?"

  # allow for cleanup before exit in the case that there is an error
  if [ -f "$DOCSCONF" ]; then
    _make_docs || return "$?"
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
      mypy --ignore-missing-imports "$item" || return "$?"
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
    return "$?"
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
whitelist () {
  check_reqs vulture --dev
  python3 "${LIBMAKE}/whitelist.py" \
      --files "${PYITEMS[@]}"
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
pipfile_to_requirements () {
  check_reqs pipfile2req --dev
  python3 "${LIBMAKE}/requirements.py" --executable pipfile2req
}


# ======================================================================
# Check that the bin directory the binary will be placed in exists.
# If the bin directory does not exist then create one. A an executable
# already exists then remove it.
# Globals:
#   BIN
#   INSTALLED
# Arguments:
#   None
# Outputs:
#   Notifies user if a new bin directory has been created and suggests
#   adding it to PATH so the executable can be run without the full-path
#   arg
# ======================================================================
check_exe () {
  if [ ! -d "$BIN" ]; then
    mkdir -p "$BIN";
    echo "created $BIN"
    echo "to run add $BIN to your PATH"
  elif [ -f "$INSTALLED" ]; then
    rm_exe
  fi
}


# ======================================================================
# Run `Pyinstaller' with the arguments suitable for this package. These
# arguments will allow a build to take place from any PWD without
# accidentally polluting the current working directory with build cache.
# Globals:
#   YELLOW
#   RESET
#   PYINSTALLER
#   DISTPATH
#   WORKPATH
#   REPOPATH
#   APPNAME
#   MAIN
# Arguments:
#   None
# Outputs;
#   `Pyinstaller' warnings
# Return:
#   `0' if build succeeds, otherwise non-zero exit code determined by
#   `Pyinstaller' if build fails
# ======================================================================
run_pyinstaller () {
  echo "${YELLOW}compiling package...${RESET}"
  pyinstaller \
      --onefile \
      --distpath "$DISTPATH" \
      --workpath "$WORKPATH" \
      --specpath "$REPOPATH" \
      --log-level ERROR \
      --name "$REPONAME" \
      "$MAIN"
}


# ======================================================================
# Add the package executable to PATH.
# Globals:
#   YELLOW
#   REPONAME
#   RESET
#   COMPILED
#   INSTALLED
#   REPOPATH
# Arguments:
#   None
# Outputs:
#   Notify the user that the executable will be added to PATH and let
#   the user know when this is successful - as well as where the
#   executable has been placed
# ======================================================================
add_to_path () {
  echo "${YELLOW}adding ${REPONAME} to PATH...${RESET}"
  cp "$COMPILED" "$INSTALLED" || return 1
  dexe="${COMPILED/"$REPOPATH"/""}"
  echo "${dexe:1} -> $INSTALLED"
}


# ======================================================================
# Build the portable, compiled, `PyInstaller' executable bundled with
# all dependencies into single executable binary that will then be
# added to PATH.
# Globals:
#   GREEN
#   REPONAME
#   RESET
#   PYINSTALLER
# Arguments:
#   None
# Outputs:
#   Announces to user what is taking place with the build
# Return:
#   `0' if build succeeds, otherwise non-zero exit code (determined
#   by `Pyinstaller') or `1'
# ======================================================================
install_binary () {
  if [ -f "$MAIN" ]; then
    echo "${GREEN}Installing ${REPONAME}${RESET}"
    check_reqs pyinstaller --dev
    clean_pyinstaller_build
    check_exe
    run_pyinstaller || return 1
    add_to_path || return 1
    echo "${GREEN}${REPONAME} successfully installed${RESET}"
  else
    echo "no package found to install"
  fi
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
    install_binary
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
  whitelist || return "$?"
  make_toc || return "$?"
  pipfile_to_requirements || return "$?"
}


# ======================================================================
# List environment variables that are needed for this script
#
# Globals:
#   TEMPLATE_ENV
# Outputs:
#   environment variables needed to run the build
# Returns:
#   `0' if all goes OK
# ======================================================================
list_env_vars () {
  mapfile -t vars < "$ENVIRONMENT_TEMPLATES/env"
  for var in "${vars[@]}"; do
    echo "- $var"
  done
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
  ( make_announce "clean" && make_clean ) || return "$?"
  ( make_announce "format" && make_format ) || return "$?"
  ( make_announce "typecheck" && make_typecheck ) || return "$?"
  ( make_announce "unused" && make_unused ) || return "$?"
  ( make_announce "coverage" && make_coverage ) || return "$?"
  ( make_announce "docs" && make_docs ) || return "$?"
  ( make_announce "lint" && make_lint ) || return "$?"
  ( make_announce "install" && make_install ) || return "$?"
  ( make_announce "deploy-cov'" && make_deploy_cov "$@" ) || return "$?"
  ( make_announce "deploy-docs" && make_deploy_docs "$@" ) || return "$?"
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
which-pipenv () {
  cd "$REPOPATH" || return 1
  if ! command -v pipenv >/dev/null 2>&1; then
    err "${CROSS} \`pipenv' not found"
  else
    echo "${TICK} $(command -v pipenv)"
  fi
}

OLDPWD="$PWD"
export OLDPWD
