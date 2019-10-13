"============================================================================="
"                                VIM PLUGINS                                  "
"============================================================================="
set nocompatible
filetype off
set rtp+=$HOME/.vim/bundle/Vundle.vim/
call vundle#begin('$HOME/.vim/bundle/')
Plugin 'VundleVim/Vundle.vim'

" ADD BELOW
"==========
Plugin 'python-mode/python-mode'
Plugin 'flazz/vim-colorschemes'                     " Colorschemes
Plugin 'vim-syntastic/syntastic'                    " Syntax Highlighting
" Plugin 'tpope/vim-fugitive'                         " Git integration
Plugin 'majutsushi/tagbar'                          " Function buffer
Plugin 'plasticboy/vim-markdown'                    " Syntax for MD files
Plugin 'tpope/vim-surround'                         " Auto surround brackets
Plugin 'rosenfeld/conque-term'                      " VIM shell
Plugin 'dkarter/bullets.vim'                        " Smarter bulletpoints
Plugin 'scrooloose/nerdtree'                        " Ide-like file explorer
Plugin 'vim-scripts/bash-support.vim'               " Bash Ide
Plugin 'Valloric/YouCompleteMe'                     " Autocompletion
Plugin 'Xuyuanp/nerdtree-git-plugin'                " Git info on file explorer
Plugin 'airblade/vim-gitgutter'                     " Git version control info
Plugin 'motemen/git-vim'                            " Git version control info
Plugin 'junegunn/vim-github-dashboard'              " Git version control info
Plugin 'thaerkh/vim-indentguides'                   " Indent guides
Plugin 'universal-ctags/ctags'                      " Exuberant CTags
Plugin 'wakatime/vim-wakatime'                      " User statistics for VIM
Plugin 'tiagofumo/vim-nerdtree-syntax-highlight'    " Syntax for file explorer
Plugin 'ap/vim-buftabline'                          " Info for open buffers
" Plugin 'vim-scripts/Vim-JDE'                        " Java support
Plugin 'alvan/vim-closetag'                         " Surround html tags
Plugin 'tomtom/tcomment_vim'                        " Comment assist
Plugin 'pangloss/vim-javascript'                    " JavaScript support
Plugin 'tmhedberg/SimpylFold'               " Code-folding
Plugin 'vim-scripts/indentpython.vim'       " Auto-Indentation (python)
Plugin 'nvie/vim-flake8'                    " PEP8 checking
Plugin 'kien/ctrlp.vim'                     " Super search Ctrl-P
Plugin 'sk1418/blockit'                     " Easily outline headers
Plugin 'shougo/vimshell.vim'                " Shell command line
Plugin 'DrawIt'                             " ASCII drawingi
Plugin 'vim-python/python-syntax'           " Python syntax highlighting
Plugin 'davidhalter/jedi-vim'               " Python completion
Plugin 'tpope/vim-eunuch'
Plugin 'editorconfig/editorconfig-vim'
Plugin 'w0rp/ale'
Plugin 'jaredpar/VsVim'
Plugin 'vim-scripts/marvim'
Plugin 'chiel92/vim-autoformat'
Plugin 'plytophogy/vim-virtualenv'
Plugin 'craigemery/vim-autotag'
Plugin 'reedes/vim-pencil'
Plugin 'szw/vim-tags'
Plugin 'sudo.vim'
Plugin 'vimwiki/vimwiki'
Plugin 'matze/vim-move'
Plugin 'python.vim'
Plugin 'andrewradev/linediff.vim'
Plugin 'int3/vim-extradite'
Plugin 'wincent/terminus'
Plugin 'severin-lemaignan/vim-minimap'
Plugin 'pbrisbin/vim-mkdir'
Plugin 'ciaranm/detectindent'
Plugin 'chrisbra/sudoedit.vim'
Plugin 'SearchComplete'
Plugin 'ledger/vim-ledger'
Plugin 'christoomey/vim-run-interactive'
Plugin 'Shougo/unite.vim'
Plugin 'neomake/neomake'
Plugin 'guns/xterm-color-table.vim'
Plugin 'artur-shaik/vim-javacomplete2.git'
Plugin 'WolfgangMehner/vim-plugins'
Plugin 'mattn/emmet-vim'
Plugin 'othree/html5.vim'
Plugin 'OmniSharp/omnisharp-vim'
Plugin 'honza/vim-snippets'
Plugin 'SirVer/ultisnips'
Plugin 'mvolkmann/vim-tag-comment'
Plugin 'jiangmiao/auto-pairs'
Plugin 'OrangeT/vim-csharp'
Plugin 'StanAngeloff/php.vim'
" Plugin 'bfredl/nvim-miniyank'
Plugin 'moll/vim-bbye'
Plugin 'tpope/vim-abolish'
Plugin 'amiorin/vim-project'
Plugin 'mhinz/vim-startify'
Plugin 'stephpy/vim-php-cs-fixer'
Plugin 'ncm2/ncm2'
Plugin 'phpactor/ncm2-phpactor'
Plugin 'junegunn/fzf'
Plugin 'BurntSushi/ripgrep'
Plugin 'wincent/ferret'
Plugin 'adoy/vim-php-refactoring-toolbox'
Plugin 'phpactor/phpactor'
Plugin 'mhinz/vim-signify'
Plugin 'joonty/vdebug'
Plugin 'chrisbra/NrrwRgn'
Plugin 'leshill/vim-json'
Plugin 'grvcoelho/vim-javascript-snippets'
Plugin 'tkengo/highway'
Plugin 'monochromegane/the_platinum_searcher'
Plugin 'mattn/jvgrep'
Plugin 'baohaojun/beagrep'
Plugin 'mileszs/ack.vim'
Plugin 'easymotion/vim-easymotion'
Plugin 'tpope/vim-repeat'
Plugin 'prettier/vim-prettier'
Plugin 'waxlamp/jslint.vim'
Plugin 'flowtype/vim-flow'
Plugin 'tell-k/vim-autopep8'
Plugin 'heavenshell/vim-pydocstring.git'
Plugin 'mgedmin/python-imports.vim'
"Plugin 'ludovicchabant/vim-gutentags'
Plugin 'https://github.com/fisadev/vim-isort'
" Plugin 'vim-scripts/Pydiction'
Plugin 'vim-scripts/taglist.vim'
Plugin 'Vimjas/vim-python-pep8-indent'
Plugin 'python-rope/ropevim'
Plugin 'numirias/semshi'
Plugin 'stsewd/isort.nvim'
"==========
" ADD ABOVE

call vundle#end()
filetype plugin indent on
