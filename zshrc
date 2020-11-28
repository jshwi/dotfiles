#-----------------------------------------------------------------------------#
#                                STEPHEN'S ZSH                                #
#-----------------------------------------------------------------------------#

# Basic zsh config.
export PATH=usr/bin:/usr/local/bin:$PATH
export PATH=usr/bin:/home/stephen/.gem/ruby/2.5.0/bin:$PATH
export PATH="$PATH:/sbin"
#export PATH="$PATH:/home/stephen/.vimpkg/bin"
export ZSH="$HOME/.oh-my-zsh"
umask 077
ZDOTDIR="$ZDOTDIR:-$HOME"
ZSHDDIR="${HOME}/.zsh"
HISTFILE="${HOME}/.zsh_history"
HISTSIZE='10000'
SAVEHIST="${HISTSIZE}"
compinit -d "${HOME}/.zshcompdump/zcompdump"
export EDITOR="/usr/bin/vim"
if ! [[ "${PATH}" =~ "^${HOME}/.bin" ]]; then
    export PATH="${HOME}/.local/bin:${PATH}"
export PATH="${HOME}/.bin/pycharm-community-2018.2.2/bin:${PATH}"
fi
export LANG=en_AU.UTF-8                 # language locale
export TERM="xterm-256color"
#export "${HOME}/.local/bin:${PATH}"
#export UPDATE_ZSH_DAYS=13              # change frequency of updates

# Source files
source $HOME/.zsh/theme.list        # select themes from list.
source $HOME/.zsh/plugins.list      # select plugins from this li`st
source $HOME/.zsh/aliases           # apply aliases to this list
source $ZSH/oh-my-zsh.sh                # themes and plugins load from here


# Behaviour
HYPHEN_INSENSITIVE="true"               # turn off correction for hyphens
ENABLE_CORRECTION="true"                # enable correction for commands
COMPLETION_WAITING_DOTS="true"          # load dots for completion
HIST_STAMPS="dd.mm.yyyy"                # format for dates in history

autoload -Uz compinit && compinit       # advanced tab-completion
setopt correctall                       # command completion
autoload -U promptinit && promptinit    # command prompt
# Disable the bell
if [[ $iatest > 0 ]];
then bind "set bell-style visible";
fi
setopt autocd                           # change directory without cd
eval "$(dircolors ~/.dir_colors)"       # colored directories
#LS_COLORS='rs=0:di=01;34:ln=01;36:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:tw=30;42:ow=34;42:st=37;44:ex=01;32:';
#export LS_COLORS

# Comp stuff
zmodload zsh/complist
zstyle :compinstall filename '${HOME}/.zshrc'
zstyle ':completion:*:descriptions' format '%U%B%d%b%u'
zstyle ':completion:*:warnings' format '%BSorry, no matches for: %d%b'
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:kill:*'   force-list always
zstyle ':completion:*:*:killall:*' menu yes select
zstyle ':completion:*:killall:*'   force-list always
unsetopt BEEP
NPM_PACKAGES="${HOME}/.npm-packages"
PATH="$NPM_PACKAGES/bin:$PATH"
# Unset manpath so we can inherit from /etc/manpath via the `manpath` command
unset MANPATH # delete if you already modified MANPATH elsewhere in your config
export MANPATH="$NPM_PACKAGES/share/man:$(manpath)"
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"
# export PATH="/home/stephen/.gem/ruby/2.5.0/bin:$PATH"
