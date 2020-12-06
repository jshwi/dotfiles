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
  make_announce "uninstall"
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
make_clean () {
  cd "$DOTFILES" || return 1
  git clean \
      -fdx \
      --exclude=".env" \
      --exclude="instance" \
      --exclude="bundle" \
      --exclude="zsh_history" \
      --exclude="bash_history" \
      --exclude="vimrc" \
      --exclude=".cache"
}
