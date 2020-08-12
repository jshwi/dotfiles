" ============================================================================"
"                                VIM PLUGINS                                  "
"============================================================================="
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

Plugin 'BurntSushi/ripgrep'
Plugin 'OmniSharp/omnisharp-vim'
Plugin 'OrangeT/vim-csharp'
Plugin 'Shougo/unite.vim'
Plugin 'SirVer/ultisnips'
Plugin 'StanAngeloff/php.vim'
Plugin 'Valloric/YouCompleteMe'
Plugin 'Vimjas/vim-python-pep8-indent'
Plugin 'WolfgangMehner/vim-plugins'
Plugin 'Xuyuanp/nerdtree-git-plugin'
Plugin 'adoy/vim-php-refactoring-toolbox'
Plugin 'airblade/vim-gitgutter'
Plugin 'alvan/vim-closetag'
Plugin 'amiorin/vim-project'
Plugin 'andrewradev/linediff.vim'
Plugin 'ap/vim-buftabline'
Plugin 'artur-shaik/vim-javacomplete2'
Plugin 'baohaojun/beagrep'
Plugin 'chiel92/vim-autoformat'
Plugin 'chrisbra/NrrwRgn'
Plugin 'chrisbra/csv.vim'
Plugin 'chrisbra/sudoedit.vim'
Plugin 'christoomey/vim-run-interactive'
Plugin 'ciaranm/detectindent'
Plugin 'craigemery/vim-autotag'
Plugin 'davidhalter/jedi-vim'
Plugin 'dkarter/bullets.vim'
Plugin 'easymotion/vim-easymotion'
Plugin 'editorconfig/editorconfig-vim'
Plugin 'flazz/vim-colorschemes'
Plugin 'flowtype/vim-flow'
Plugin 'grvcoelho/vim-javascript-snippets'
Plugin 'guns/xterm-color-table.vim'
Plugin 'heavenshell/vim-pydocstring'
Plugin 'honza/vim-snippets'
Plugin 'fisadev/vim-isort'
Plugin 'int3/vim-extradite'
Plugin 'itspriddle/vim-shellcheck'
Plugin 'jaredpar/VsVim'
Plugin 'jiangmiao/auto-pairs'
Plugin 'joonty/vdebug'
Plugin 'junegunn/fzf'
Plugin 'junegunn/vim-github-dashboard'
Plugin 'kien/ctrlp.vim'
Plugin 'koalaman/shellcheck'
Plugin 'ledger/vim-ledger'
Plugin 'leshill/vim-json'
Plugin 'majutsushi/tagbar'
Plugin 'mattn/emmet-vim'
Plugin 'mattn/jvgrep'
Plugin 'matze/vim-move'
Plugin 'mgedmin/python-imports.vim'
Plugin 'mhinz/vim-signify'
Plugin 'mhinz/vim-startify'
Plugin 'mileszs/ack.vim'
Plugin 'moll/vim-bbye'
Plugin 'monochromegane/the_platinum_searcher'
Plugin 'motemen/git-vim'
Plugin 'mvolkmann/vim-tag-comment'
Plugin 'ncm2/ncm2'
Plugin 'neomake/neomake'
Plugin 'nvie/vim-flake8'
Plugin 'othree/html5.vim'
Plugin 'pangloss/vim-javascript'
Plugin 'pbrisbin/vim-mkdir'
Plugin 'phpactor/ncm2-phpactor'
Plugin 'phpactor/phpactor'
Plugin 'plasticboy/vim-markdown'
Plugin 'plytophogy/vim-virtualenv'
Plugin 'prettier/vim-prettier'
Plugin 'python-mode/python-mode'
Plugin 'python-rope/ropevim'
Plugin 'reedes/vim-pencil'
Plugin 'rosenfeld/conque-term'
Plugin 'scrooloose/nerdtree'
Plugin 'severin-lemaignan/vim-minimap'
Plugin 'shougo/vimshell.vim'
Plugin 'sk1418/blockit'
Plugin 'stephpy/vim-php-cs-fixer'
Plugin 'stephpy/vim-yaml'
Plugin 'stsewd/isort.nvim'
Plugin 'szw/vim-tags'
Plugin 'tell-k/vim-autopep8'
Plugin 'thaerkh/vim-indentguides'
Plugin 'tiagofumo/vim-nerdtree-syntax-highlight'
Plugin 'tkengo/highway'
Plugin 'tmhedberg/SimpylFold'
Plugin 'tomtom/tcomment_vim'
Plugin 'tpope/vim-abolish'
Plugin 'tpope/vim-eunuch'
Plugin 'tpope/vim-git'
Plugin 'tpope/vim-repeat'
Plugin 'tpope/vim-surround'
Plugin 'universal-ctags/ctags'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
Plugin 'vim-python/python-syntax'
Plugin 'vim-scripts/DrawIt'
Plugin 'vim-scripts/SearchComplete'
Plugin 'vim-scripts/bash-support.vim'
Plugin 'vim-scripts/crontab.vim'
Plugin 'vim-scripts/indentpython.vim'
Plugin 'vim-scripts/marvim'
Plugin 'vim-scripts/python.vim'
Plugin 'vim-scripts/sudo.vim'
Plugin 'vim-scripts/taglist.vim'
Plugin 'vim-syntastic/syntastic'
Plugin 'vimwiki/vimwiki'
Plugin 'w0rp/ale'
Plugin 'wakatime/vim-wakatime'
Plugin 'waxlamp/jslint.vim'
Plugin 'wincent/ferret'
Plugin 'wincent/terminus'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
