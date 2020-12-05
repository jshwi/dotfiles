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
[ -n "$LIBMAKE_ENV" ] && return; LIBMAKE_ENV=0; # pragma once

LIBMAKE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- source lib/make ---
source "$LIBMAKE/colors.sh"
source "$LIBMAKE/err.sh"
source "$LIBMAKE/icons.sh"

LIB="$(dirname "$LIBMAKE")"

REPOPATH="$(dirname "$LIB")"

ENVFILE="$REPOPATH/.env"

# --- source .env ---
[ -f "$ENVFILE" ] && source "$ENVFILE"

REPONAME="$(basename "$REPOPATH")"

# --- env vars ---
PIPENV_IGNORE_VIRTUALENVS=1
export PIPENV_IGNORE_VIRTUALENVS
source  "$ENVFILE"

# --- */**"/bin/" ---
if [[ "$EUID" -eq 0 ]]; then
  BIN="/usr/local/bin"
else
  BIN="$HOME/.local/bin"
fi

INSTALLED="$BIN/$REPONAME"

# --- */**"/virtalenvs/$REPONAME-*/" ---
if [ "$1" == "--no-install" ]; then
  VIRTUAL_ENV=
else
  cd "$REPOPATH" || return 1
  if ! pipenv --venv >/dev/null 2>&1; then
    pipenv install || return 1
  fi
  VIRTUAL_ENV="$(pipenv --venv)"
fi

PYTHONPATH="${PYTHONPATH}:${VIRTUAL_ENV}/bin"
PYTHONPATH="${PYTHONPATH}:${VIRTUAL_ENV}/lib/python*/site-packages"

# --- "./bin" ---
DEVPY="$LIBMAKE/dev"

# --- "./$APPNAME" ---
if [ -e "$PYTHON" ] && APPNAME="$("$PYTHON" "$DEVPY" name)"; then
  APP_PATH="$REPOPATH/$APPNAME"
else
  APP_PATH="$REPOPATH/$REPONAME"
fi
MAIN="$APP_PATH/__main__.py"
SRC="$APP_PATH/src"

# --- PYTHONPATH ---
PYTHONPATH="$REPOPATH:$APP_PATH:$SRC"
export PYTHONPATH

# --- "./" ---
WORKPATH="$REPOPATH/build"
SPECPATH="${APP_PATH}.spec"
README="$REPOPATH/README.rst"
TESTS="$REPOPATH/tests"
WHITELIST="$REPOPATH/whitelist.py"
PYLINTRC="$REPOPATH/.pylintrc"
COVERAGEXML="$REPOPATH/coverage.xml"
PIPFILELOCK="$REPOPATH/Pipfile.lock"
REQUIREMENTS="$REPOPATH/requirements.txt"
export README
export PIPFILELOCK
export REQUIREMENTS

# --- "./dist" ---
DISTPATH="$REPOPATH/dist"
COMPILED="$DISTPATH/$REPONAME"

# --- "./docs" ---
DOCSOURCE="$REPOPATH/docs"
DOCSCONF="$DOCSOURCE/conf.py"
DOCSBUILD="$DOCSOURCE/_build"

# --- array of python files and directories ---
PYITEMS=(
  "$APP_PATH"
  "$TESTS"
  "$DOCSCONF"
  "$DEVPY"
)


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
  items="$1";
  installed=1
  for item in "${items[@]}"; do
    if [ ! -f "$item" ]; then
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
uninstall () {
  if pipenv --venv >/dev/null 2>&1; then
    VIRTUAL_ENV="$(pipenv --venv)"
  fi
  items=(
    "$(clean_repo 2>&1 | tee /dev/tty)"
    "$([[ "$VIRTUAL_ENV" == "" ]] || pipenv --rm 2>&1 | tee /dev/tty)"
    "$(rm_exe 2>&1 | tee /dev/tty)"
  )
  for item in "${items[@]}"; do
    if [ "$item" != "" ]; then
      echo
      echo "${YELLOW}${REPONAME} uninstalled successfully${RESET}"
      return 0
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
clean_repo () {
  cd "$REPOPATH" || return 1
  git clean \
      -fdx \
      --exclude=".env" \
      --exclude="instance" \
      --exclude "bundle" \
      --exclude "zsh_history" \
      --exclude "secret" \
      --exclude "bash_history" \
      --exclude "vimrc" \
      --exclude ".cache"
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
deploy_docs () {
  branch="${1:-"master"}"
  if [[ "$TRAVIS_BRANCH" =~ ^"$branch"$|^[0-9]+\.[0-9]+\.X$ ]]; then
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
deploy_cov () {
  if [ -f "$COVERAGEXML" ]; then
    check_reqs "$CODECOV"
    "$CODECOV" --file "$COVERAGEXML" --token "$CODECOV_TOKEN" || return "$?"
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
format_py () {
  check_reqs "$BLACK" --dev
  for item in "${PYITEMS[@]}"; do
    if [ -e "$item" ]; then
      "$BLACK" "$item"
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
lint_files () {

  _pylint () {
    "$PYLINT" "$1" --output-format=colorized || return "$?"
  }

  _pylint_rcfile () {
    "$PYLINT" \
        "$1" \
        --output-format=colorized \
        --rcfile="$PYLINTRC" \
        || return "$?"
  }

  check_reqs "$PYLINT" --dev
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
run_tests () {
  if ls "$TESTS/"*_test.py >/dev/null 2>&1 \
      || ls "$TESTS"/test_*.py >/dev/null 2>&1 ; then
    check_reqs "$PYTEST" --dev
    "$PYTEST" --color=yes "$TESTS" -vv || return "$?"
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
run_test_cov () {
  if ls "$TESTS/"*_test.py >/dev/null 2>&1 \
      || ls "$TESTS"/test_*.py >/dev/null 2>&1 ; then
    items=( "$PYTEST" "$COVERAGE" )
    for item in "${items[@]}"; do
      check_reqs "$item" --dev
    done
    "$PYTEST" --color=yes "$TESTS" --cov="$APP_PATH" -vv || return "$?"
    "$COVERAGE" xml
    unset items
  else
    echo "no tests found"
  fi
}


# ======================================================================
# Create <PACKAGENAME>.rst from package directory.
# Globals:
#   DOCSCONF
#   DEVPY
# Returns:
#   `0' if all goes ok
# ======================================================================
make_toc () {
  if [ -f "$DOCSCONF" ]; then
    "$DEVPY" toc || return "$?"
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
#   DEVPY
#   SPHINXBUILD
#   DOCSOURCE
#   DOCSCONF
# Arguments:
#   None
# Outputs:
#   Building process and announce successful completion
# Returns:
#   `0' if the build is successful, non-zero exit code (determined by
#   `Sphinx') if the build fails
# ======================================================================
make_html () {

  _make_html () {
    check_reqs "$SPHINXBUILD" --dev
    rm_force_recurse "$DOCSBUILD"
    original="$("$DEVPY" title --replace "README")"
    "$SPHINXBUILD" -M html "$DOCSOURCE" "$DOCSBUILD"
    rc=$?
    "$DEVPY" title --replace "$original" &>/dev/null
    return $rc
  }

  make_toc || return "$?"

  # allow for cleanup before exit in the case that there is an error
  if [ -f "$DOCSCONF" ]; then
    _make_html || return "$?"
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
inspect_types () {
  check_reqs "$MYPY" --dev
  for item in "${PYITEMS[@]}"; do
    if [ -e "$item" ]; then
      "$MYPY" --ignore-missing-imports "$item" || return "$?"
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
vulture () {

  _vulture () {
    check_reqs "$VULTURE" --dev
    [ -f "$WHITELIST" ] || touch "$WHITELIST"
    for item in "${PYITEMS[@]}"; do
      if [ -e "$item" ]; then
        "$VULTURE" "$item" "$WHITELIST" || return "$?"
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
#   DEVPY
#   VULTURE
#   PYITEMS
# Arguments:
#   None
# Returns:
#   `0' if all goes ok
# ======================================================================
whitelist () {
  check_reqs "$VULTURE" --dev
  "$DEVPY" \
      whitelist \
      --executable "$VULTURE" \
      --files "${PYITEMS[@]}"
}


# ======================================================================
# Convert `Pipfile.lock' to `requirements.txt' (transfer prod and dev
# packages across). Remove the additional information after the `;'
# delim. Sort `requirements.txt' and remove duplicates. Notify user that
# all went well.
# Globals:
#   PIPFILE2REQ
#   DEVPY
#   PYITEMS
# Returns:
#   `0' if all goes ok
# ======================================================================
pipfile_to_requirements () {
  check_reqs "$PIPFILE2REQ" --dev
  "$DEVPY" reqs --executable "$PIPFILE2REQ"
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
  "$PYINSTALLER" \
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
    check_reqs "$PYINSTALLER" --dev
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
install () {
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
  mapfile -t vars < "$TEMPLATE_ENV"
  for var in "${vars[@]}"; do
    echo "- $var"
  done
}


# ======================================================================
# Source the .env file if it exists, otherwise explain error and exit
#
# Globals:
#   ENVFILE
# Outputs:
#   environment variables needed to run the build
# Returns:
#   `0' if all goes OK
# ======================================================================
source_env () {
  if [ -f "$ENVFILE" ]; then
    source "$ENVFILE"
  else
    err \
        "\.env file cannot be found" \
        "cannot continue running with these values:"$'\n'"$(list_env_vars)"
  fi
}


source_symlink () {
  if [ -L "$ENVFILE" ]; then
    echo "${BOLD}${YELLOW}Warning: .env is symlinked to it's template bin/env${RESET}"
    echo "${YELLOW}. do not make any changes to this file as it may be added to version control${RESET}"
    echo "${YELLOW}. remove symlink and copy bin/env to .env${RESET}"
    echo "${YELLOW}. uncomment /.env in .gitignore${RESET}"
  fi
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
build () {
  source_env || return "$?"
  source_symlink
  export TRAVIS_BRANCH
  ( announce "clean" && clean_repo ) || return "$?"
  ( announce "format" && format_py ) || return "$?"
  ( announce "typecheck" && inspect_types ) || return "$?"
  ( announce "unused" && vulture ) || return "$?"
  ( announce "coverage" && run_test_cov ) || return "$?"
  ( announce "docs" && make_html ) || return "$?"
  ( announce "lint" && lint_files ) || return "$?"
  ( announce "install" && install_binary ) || return "$?"
  ( announce "deploy-cov'" && deploy_cov "$@" ) || return "$?"
  ( announce "deploy-docs" && deploy_docs "$@" ) || return "$?"
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
  cd "$DOTFILES" || return 1
  if ! command -v pipenv >/dev/null 2>&1; then
    err "${CROSS} \`pipenv' not found"
  else
    echo "${TICK} $(command -v pipenv)"
  fi
}

OLDPWD="$PWD"
export OLDPWD
