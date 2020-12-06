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

export RED
export GREEN
export YELLOW
export CYAN
export BOLD
export RESET
