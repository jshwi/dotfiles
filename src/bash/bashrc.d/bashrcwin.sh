#!/bin/bash -
# ==================================================================== #
#                             .dotfiles .bashrc                        #
# ==================================================================== #
# shellcheck disable=SC1090
ZSH_GLOBAL="$HOME/.dotfiles/zsh/globals"
# source global variables
GIT_PS1_SHOWDIRTYSTATE=1
GIT_PS1_SHOWUNTRACKEDFILES=1
GIT_PS1_SHOWSTASHSTATE=1
GIT_PS1_SHOWUPSTREAM="auto verbose"
VIMRC="$HOME/.dotfiles/vim/rc/vimwin.vim"
HISTFILE="$HOME/.dotfiles/bash/bash_history"
export ZSH_GLOBAL
export GIT_PS1_SHOWDIRTYSTATE
export GIT_PS1_SHOWUNTRACKEDFILES
export GIT_PS1_SHOWSTASHSTATE
export GIT_PS1_SHOWUPSTREAM
export VIMRC
# MSYSTEM=''
# TITLEPREFIX=''
ETC="$HOME/scoop/apps/git/current/etc"

if [[ -f "$ETC/profile.d/git-sdk.sh" ]]; then
    TITLEPREFIX=SDK-${MSYSTEM#MINGW}
else
    TITLEPREFIX=$MSYSTEM
fi


PS1="\[\033]0;$TITLEPREFIX:$PWD\007\]" # set window title
PS1="$PS1"'\n'  # new line
PS1="$PS1"'\[\033[32m\]'  # change to green
#PS1="$PS1"'\u@\h '  # user@host<space>
#PS1="$PS1"'\[\033[35m\]'  # change to purple
#PS1="$PS1"'$MSYSTEM '  # show MSYSTEM
#PS1="$PS1"'\[\033[33m\]'  # change to brownish yellow
PS1="$PS1"'\W'  # current working directory
if [[ -z "$WINELOADERNOEXEC" ]]; then
    GIT_EXEC_PATH="$(git --exec-path 2>/dev/null)"
    COMPLETION_PATH="${GIT_EXEC_PATH%/libexec/git-core}"
    COMPLETION_PATH="${COMPLETION_PATH%/lib/git-core}"
    COMPLETION_PATH="$COMPLETION_PATH/share/git/completion"
fi
if [[ -f "$COMPLETION_PATH/git-prompt.sh" ]]; then
    # shellcheck disable=SC1090
    source "$COMPLETION_PATH/git-completion.bash"
    # shellcheck disable=SC1090
    source "$COMPLETION_PATH/git-prompt.sh"
    PS1="$PS1"'\[\033[36m\]'  # change color to cyan
    PS1="$PS1"'`__git_ps1`'  # bash function
fi

PS1="$PS1"'\[\033[0m\]'  # change #color
PS1="$PS1"'\n\[\033[35m\]>_\[\033[0m\] '  # new line:

umask 077
DIRCOLORS="$HOME/.dotfiles/zsh/dir_colors"
eval "$(dircolors "$DIRCOLORS")"


wpip ()

{
    pippath="/c/Users/swhitlock/scoop/apps/python/3.8.5/Scripts/pip3.8.exe"
    positional="$1"
    if [[ "$positional" == "install" ]]; then
        shift
        "$pippath" install --trusted-host pypi.org --trusted-host files.pythonhosted.org "$@"
    elif [[ "$#" -ne 0 ]]; then
         "$pippath" "$@"
    else
        "$pippath" --help
    fi
}
#source "$HOME/.opt/liquidprompt/liquidprompt"
alias ws="cd /c/Users/swhitlock/home/stephen"
#alias ls="ls --ignore='.*'"
alias l="ls -al"
alias rm="rm -v"
alias pip="wpip"
source "$HOME/.dotfiles/zsh/aliases"
ws
