#!/bin/bash -
#=======================================================================
#
#          FILE: err.sh
#
#         USAGE: source err.sh
#
#   DESCRIPTION: Source and use as an echo for errors
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: This script aims to follow Google's `Shell Style Guide'
#                https://google.github.io/styleguide/shellguide.html
#        AUTHOR: Stephen Whitlock (jshwi), stephen@jshwisolutions.com
#  ORGANIZATION: Jshwi Solutions
#       CREATED: 08/09/20 10:58:32
#      REVISION: 1.0.0
#
# shellcheck disable=SC1090
#=======================================================================
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
