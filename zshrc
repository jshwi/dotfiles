#-----------------------------------------------------------------------------#
#                                STEPHEN'S ZSH                                #
#-----------------------------------------------------------------------------#

# Behaviour
ZDOTDIR="$ZDOTDIR:-$HOME"
ZSHDDIR="${HOME}/.zsh"
HISTFILE="${HOME}/.zsh_history"
HISTSIZE='10000'
SAVEHIST="${HISTSIZE}"
HYPHEN_INSENSITIVE="true"               # turn off correction for hyphens
ENABLE_CORRECTION="true"                # enable correction for commands
COMPLETION_WAITING_DOTS="true"          # load dots for completion
HIST_STAMPS="dd.mm.yyyy"                # format for dates in history
NPM_PACKAGES="$HOME"/.npm-packages

# Exports
export PATH=usr/bin:/usr/local/bin:$PATH
export PATH=usr/bin:/$HOME/.local/bin:$PATH
export PATH=usr/bin:/$HOME/.gem/ruby/2.5.0/bin:$PATH
export PATH=usr/bin:/"$HOME"/.rbenv/bin:$PATH
export PATH=usr/bin:/"$NPM_PACKAGES"/bin:$PATH
export ZSH="$HOME"/.oh-my-zsh
export LANG=en_AU.UTF-8                     # language locale
export TERM="xterm-256color"
export MANPATH="$NPM_PACKAGES"/share/man:$(manpath)
export UPDATE_ZSH_DAYS=13                   # change frequency of updates

# Source files
source $HOME/.zsh/themes/theme.list                # select themes from list.
source $HOME/.zsh/plugins              # select plugins from this li`st
source $HOME/.zsh/aliases                   # apply aliases to this list
source $ZSH/oh-my-zsh.sh                    # themes and plugins load from here
# source $(dirname $(gem which colorls))/tab_complete.sh

# Autoload
autoload -Uz compinit && compinit           # advanced tab-completion
autoload -U promptinit && promptinit        # command prompt

# Setopt
setopt correctall                           # command completion
setopt autocd                               # change directory without cd

# Dir Colors
eval "$(dircolors ~/.dir_colors)"           # colored directories
eval "$(rbenv init -)"

# Zstyle
zstyle :compinstall filename '${HOME}/.zshrc'
zstyle ':completion:*:descriptions' format '%U%B%d%b%u'
zstyle ':completion:*:warnings' format '%BSorry, no matches for: %d%b'
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:kill:*'   force-list always
zstyle ':completion:*:*:killall:*' menu yes select
zstyle ':completion:*:killall:*'   force-list always

zmodload zsh/complist

umask 077

# Comp stuff
unsetopt BEEP

# Unset manpath so we can inherit from /etc/manpath via the `manpath` command
unset MANPATH # delete if you already modified MANPATH elsewhere in your config

#
# # Set to this to use case-sensitive completion
# # CASE_SENSITIVE="true"
#
# # Comment this out to disable weekly auto-update checks
# DISABLE_AUTO_UPDATE="false"
#
# # Uncomment following line if you want to disable colors in ls
#   DISABLE_LS_COLORS="true"
#
# # Uncomment following line if you want to disable autosetting terminal title.
# # DISABLE_AUTO_TITLE="true"
#
# # Uncomment following line if you want red dots to be displayed while waiting for completion
# COMPLETION_WAITING_DOTS="true"
#
# # Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# # Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# # Example format: plugins=(rails git textmate ruby lighthouse)
# plugins=(git dirhistory brew dircycle gitfast git-extras jsontools node npm osx repo sudo urltools web-search dirpersist history-substring-search last-working-dir safe-paste yarn)
#
# source $ZSH/oh-my-zsh.sh
#
# # Timing
# PROMPT_TITLE='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/~}\007"'
# export PROMPT_COMMAND="${PROMPT_COMMAND} ${PROMPT_TITLE}; "
#
# ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern cursor)
#
# # Declare the variable
# typeset -A ZSH_HIGHLIGHT_STYLES
#
# # To differentiate aliases from other command types
# ZSH_HIGHLIGHT_STYLES[alias]='fg=cyan,bold'
#
# # To have paths colored instead of underlined
# ZSH_HIGHLIGHT_STYLES[path]='fg=magenta'
#
# ZSH_HIGHLIGHT_STYLES[cursor]='bg=pink'
#
# # To define styles for nested brackets up to level 4
# ZSH_HIGHLIGHT_STYLES[bracket-level-1]='fg=blue,bold'
# ZSH_HIGHLIGHT_STYLES[bracket-level-2]='fg=red,bold'
# ZSH_HIGHLIGHT_STYLES[bracket-level-3]='fg=yellow,bold'
# ZSH_HIGHLIGHT_STYLES[bracket-level-4]='fg=magenta,bold'
#
# ZSH_HIGHLIGHT_STYLES[root]='bg=red'
#
# # List of accounts to read the last tweet from, comma separated
# # The first in the list is read by the party parrot.
# export TTC_BOTS='tinycarebot,selfcare_bot,magicrealismbot'
#
# # Git Repos Refresh
# export TTC_GITBOT='gitlog'
# # export TTC_REPOS_DEPTH=2
# export TTC_SAY_BOX='parrot'
#
# # Location/zip code to check the weather for. Both 90210 and "San Francisco, CA"
# # _should_ be ok (the zip code doesn't always work -- use a location
# # first, if you can). It's using weather.service.msn.com behind the curtains.
# export TTC_WEATHER='Pittsburgh'
#
# # Set to false if you're an imperial savage. <3
# export TTC_CELSIUS=false
#
# # Unset this if you _don't_ want to use Twitter keys and want to
# # use web scraping instead.
# export TTC_APIKEYS=true
#
# # Refresh the dashboard every 20 minutes.
# export TTC_UPDATE_INTERVAL=10
#
#
# # Note: in tiny-terminal-care < 1.0.7, the recommended variables for the Twitter
# # API keys were the ones before. As of 1.0.8, they are deprecated
# # (because the names are too generic), but will still be supported
# # until the next major version.
# # export CONSUMER_KEY='...'
# # export CONSUMER_SECRET='...'
# # export ACCESS_TOKEN='...'
# # export ACCESS_TOKEN_SECRET='...'
#
#  # ------------------------------------------------------------------
#  # Go Paths
#  # ------------------------------------------------------------------
#
# export GOROOT=$HOME/golang/go
# export PATH=$PATH:$GOROOT/bin
# export GOPATH=$HOME/Desktop/Git_Repositories
#
# #--------------------------------------------------------------------
# # Ruby Path fixes
# #--------------------------------------------------------------------
#
# # export PATH=$(brew --prefix)/opt/openssl/bin:$PATH
# # export LDFLAGS=-L/usr/local/opt/openssl/lib
# # export CPPFLAGS=-I/usr/local/opt/openssl/include
# # export PKG_CONFIG_PATH=$(brew --prefix)/opt/openssl/lib/pkgconfig
#
# # -------------------------------------------------------------------
# # Git aliases
# # -------------------------------------------------------------------
#
# alias gaa='git add -A'
# alias gp='git push'
# alias gl='git log'
# alias gs='git status'
# alias gd='git diff'
# alias gmsg='git commit -m'
# alias gmsga='git commit -am'
# alias gb='git branch'
# alias gc='git checkout'
# alias gra='git remote add'
# alias grr='git remote rm'
# alias git_down='git pull'
# alias gcl='git clone'
# alias gta='git tag -a -m'
# alias gf='git reflog'
# alias gfa='git fetch --all'
# # alias git='hub'
#
# # leverage an alias from the ~/.gitconfig
# alias gh='git hist'
# alias glg1='git lg1'
# alias glg2='git lg2'
# alias glg='git lg'
#
# # -------------------------------------------------------------------
# # Capistrano aliases
# # -------------------------------------------------------------------
#
# alias capd='cap deploy'
#
# # -------------------------------------------------------------------
# # Symfony aliases
# # -------------------------------------------------------------------
#
# # -------------------------------------------------------------------
# # OTHER aliases
# # -------------------------------------------------------------------
#
# alias cl='clear'
# alias bi= 'bundle install'
# alias bl= 'bower list'
# alias bs= 'bower search'
# alias npming='npm install -g'
# alias ying='yarn install -g'
# alias npms='npm search'
# alias h='history'
# alias help='man'
# alias whereami='display_info'
# alias did="vim +'normal Go' +'r!date' ~/did.txt"
# # alias javaide='open -a /Applications/IntelliJ\ IDEA.app'
# # alias phpide='open -a /Applications/PHPStorm.app'
# # alias atom='open -a /Applications/Atom.app'
# alias code='open -a /Applications/Visual\ Studio\ Code.app'
# alias webide='open -a /Applications/WebStorm.app'
# alias apmi='apm install'
# alias hypin="hpm install"
# alias brewi='brew install'
# alias brupg='brew upgrade'
# alias brupd='brew update'
# alias szsh='source ~/.zshrc'
# alias srg='surge'
# alias jb='jekyll build'
# alias netd='netlify deploy'
# alias git_up='git standup'
# alias addup='git remote add upstream'
# alias getup='git fetch upstream'
# alias chkmast='git checkout master'
# alias gst='git stash'
# alias gitsta='git stash apply'
# alias hero='git push heroku master'
# alias takecare='tiny-care-terminal'
# alias bsync='browser-sync start --server'
# alias breload='browser-sync reload'
# alias jopt='jpeg-recompress --accurate --quality medium --min 40'
# alias popt='pngcrush -brute'
# alias jekstw='bundle exec jekyll serve --host 0.0.0.0'
# alias jeksth='bundle exec jekyll serve --port 4001 --host 0.0.0.0'
# alias jeksd='bundle exec jekyll serve --port 4002 --host 0.0.0.0'
# alias gitor='git remote add origin'
# alias pushit='git push -u origin master'
# alias free='git pull --rebase upstream staging'
# alias slate='./deploy.sh'
# alias start='torus run bin/rails server'
# alias console='torus run bin/rails console'
# alias killpry='lsof -wni tcp:3000'
# alias git=hub
# alias lint='./node_modules/.bin/eslint --init'
# alias gac="ga . && gcmsg"
# alias gpo="gp && go"
# alias gundo="git undo"
#
#
# # push my changes to my github master branch and open the page
# # The commit message will always be "push from terminal" since I'll probably just be adding more resources or checking things off when using this
# alias pg-gh='cd ~/Desktop/Git_Repositories/personal-goals &&
#   git add -A &&
#   git commit -m "updates goals" &&
#   git push &&
#   open http://github.com/twhite96/personal-goals'
# # exa file list
# alias la="exa --git --color=automatic -x"
# # `cat` with beautiful colors. requires: pip install -U Pygments
# alias c='pygmentize -O style=borland -f console256 -g'
#
# alias myip='curl ip.appspot.com'
# #   memHogsTop, memHogsPs:  Find memory hogs
# #   -----------------------------------------------------
# alias memHogsTop='top -l 1 -o rsize | head -20'
# alias memHogsPs='ps wwaxm -o pid,stat,vsize,rss,time,command | head -10'
#
# #   cpuHogs:  Find CPU hogs
# #   -----------------------------------------------------
# alias cpu_hogs='ps wwaxr -o pid,stat,%cpu,time,command | head -10'
# alias flushDNS='dscacheutil -flushcache'
#
# # Reload dns
# alias reloaddns="dscacheutil -flushcache && sudo killall -HUP mDNSResponder"
#
# # Empty the Trash on all mounted volumes and the main HDD.
# # Also, clear Apple’s System Logs to improve shell startup speed.
# # Finally, clear download history from quarantine. https://mths.be/bum
# alias emptytrash="sudo rm -rfv /Volumes/*/.Trashes; sudo rm -rfv ~/.Trash; sudo rm -rfv /private/var/log/asl/*.asl; sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV* 'delete from LSQuarantineEvent'"
#
#
# #   finderShowHidden:   Show hidden files in Finder
# #   finderHideHidden:   Hide hidden files in Finder
# #   -------------------------------------------------------------------
# alias finderShowHidden='defaults write com.apple.finder ShowAllFiles TRUE'
# alias finderHideHidden='defaults write com.apple.finder ShowAllFiles FALSE'
#
# alias l="exa -l"
# alias copyssh="pbcopy < $HOME/.ssh/id_rsa.pub"
# alias alz="alias | fzf"
#
#
# ########################
# # Terminalizer Aliases #
# ########################
#
# alias trex='terminalizer record'
# alias tconfig='terminalizer config'
# alias tren='terminalizer render'
# alias tplay='terminalizer play'
# alias tgen='terminalizer generate'
# alias tshare='terminalizer share'
#
#
# ###################
# # BUILDING PROMPT #
# ###################
#
# # username --> %n
# # machine name --> %m
# # current location --> %~
#
# # Main prompt (left)
# # PROMPT='╭─$(nvm_prompt_info) $fg[magenta]$(get_pwd)%b
# # ╰───$_SYMBOL'
#
# # Main prompt (right)
# # RPROMPT='$(check_git_prompt_info)'
#
# # #############
# # EMOJI BITS #
# # #############
#
# # Get more options:
# # http://getemoji.com/
# # https://unicode.org/emoji/charts/full-emoji-list.html
# # Ctrl + Cmd + Space on Mac to open up the emoji keyboard
# # EMOJI=(💩 👻 💀 ☠ 👽 👾 🤖 🐶 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐒 🦉 🦄 🐌 🐢 🦑 🐙 🐠 🐟 🐡 🐬 🦈 🐳 🐄 🐘 🍄 🌻 ☃️ ⛄️ ❄️ 🔥 🍌 🍍 🍓 🥝 🍭 🎨 🚀 🏖 🏝 💻 📚 🖌 🖍 📓 😜 🙄 🤓 👩🏻‍💻 👩🏻‍🚀 👸🏼 💃 🛀🏻 🤺 🖕🏻 ✌🏻 🤘🏻 👊🏻 👟 🎩 🐥 🦆 )
# # function random_emoji {
# #   echo -n "$EMOJI[$RANDOM%$#EMOJI+1] "
# # }
#
#
#
# # Prompt symbols
# # ➭ ✔ ✈ ✭ ✗ ➦ ✂ ✱
# # _SYMBOL="%{$fg[red]%}➭%{$fg[yellow]%}➭%{$fg[cyan]%}➭ "
# # _SYMBOL="<< $(random_emoji) >> "
#
#
#
# # #####################
# # Git Prompt Builder #
# # #####################
#
# # ZSH_THEME_GIT_PROMPT_PREFIX="["
# # ZSH_THEME_GIT_PROMPT_SUFFIX="%{$fg[white]%}]"
# # ZSH_THEME_GIT_PROMPT_UNTRACKED="%{$fg[red]%} ✗"
# # ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[green]%} ✔"
#
#
#
# # Git sometimes goes into a detached head state. git_prompt_info doesn't
# # return anything in this case. So wrap it in another function and check
# # for an empty string.
# # function check_git_prompt_info() {
# #   if git rev-parse --git-dir > /dev/null 2>&1; then
# #       if [[ -z $(git_prompt_info) ]]; then
# #           echo "%{$fg[magenta]%}detached-head%{$reset_color%})"
# #       else
# #           echo "$(git_prompt_info)"
# #       fi
# #   fi
# # }
#
#
# ######################
# # NVM Prompt Builder #
# ######################
#
# # ZSH_THEME_NVM_PROMPT_PREFIX="%{$fg[green]%}⬡ %{$fg[white]%}"
# # ZSH_THEME_NVM_PROMPT_SUFFIX="%{$fg[white]%}"
#
#
# ########################
# # Location Path Setter #
# ########################
#
# # function get_pwd(){
# #   git_root=$PWD
# #   while [[ $git_root != / && ! -e $git_root/.git ]]; do
# #     git_root=$git_root:h
# #   done
# #   if [[ $git_root = / ]]; then
# #     unset git_root
# #     prompt_short_dir=%~
# #   else
# #     parent=${git_root%\/*}
# #     prompt_short_dir=${PWD#$parent/}
# #   fi
# #   echo $prompt_short_dir
# # }
#
# function acp() {
#   git add .
#   git commit -m "$1"
#   git push
# }
#
# #   extract:  Extract most know archives with one command
# #   ---------------------------------------------------------
#     extract () {
#         if [ -f $1 ] ; then
#           case $1 in
#             *.tar.bz2)   tar xjf $1     ;;
#             *.tar.gz)    tar xzf $1     ;;
#             *.bz2)       bunzip2 $1     ;;
#             *.rar)       unrar e $1     ;;
#             *.gz)        gunzip $1      ;;
#             *.tar)       tar xf $1      ;;
#             *.tbz2)      tar xjf $1     ;;
#             *.tgz)       tar xzf $1     ;;
#             *.zip)       unzip $1       ;;
#             *.Z)         uncompress $1  ;;
#             *.7z)        7z x $1        ;;
#             *)     echo "'$1' cannot be extracted via extract()" ;;
#              esac
#          else
#              echo "'$1' is not a valid file"
#          fi
#     }
#
# export NVM_DIR="$HOME/.nvm"
# [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
# [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
# source /Users/tiffanywhite/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
#
# # Angular CLI fix
#
# EDITOR=Code; export EDITOR
#
# eval "$(hub alias -s)"
# export GITHUB_TOKEN=$token
#
# # Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
# # echo 'export PATH="/usr/local/opt/openssl/bin:$PATH"' >> ~/.zshrc
# #
#
# # export CPPFLAGS="-I/usr/local/opt/openssl/include -I/usr/local/opt/readline/include"
# # export LDFLAGS="-L/usr/local/opt/openssl/lib -L/usr/local/opt/readline/lib"
#
# # export RBENV_ROOT=/usr/local/var/rbenv
# # if which rbenv > /dev/null; then eval "$(rbenv init -)"; fi
#
# # echo -e "\033]6;1;bg;red;brightness;23\a"
# # echo -e "\033]6;1;bg;green;brightness;52\a"
# # echo -e "\033]6;1;bg;blue;brightness;72\a"
NPM_PACKAGES="${HOME}/.npm-packages"
export PATH="$NPM_PACKAGES/bin:$PATH"

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
#eval $(thefuck --alias)
source $HOME/.zshenv
ZSH_THEME="spaceship" in your .zshrc.

eval "$(ssh-agent -s)" &> /dev/null
ssh-add ~/.ssh/id_rsa_github &> /dev/null

