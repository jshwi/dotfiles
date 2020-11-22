""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"##### ## ## ############ ### ##### #### ####### ######## ######## # #######""
""###### ## ## ############ ### ##### ## ####### ########## ######## # ######""
""####### ## ## ############ ### #####/ ####### ############ ######## # #####""
""########| | ##| |########## (_| )#### ######_#(_)##########_######## # ####""
""########| / __| '_ \ \#/\#/ / |// __|#\ \#/ / | '_ ` _ \| '__/ __|### # ###""
""####| |#| \__ \ |#| \ V  V /| |#\__ \##\ V /| | |#| |#| | |#| (## #### # ##""
""#####\___/|___/_| |_|\_/\_/#|_|#|___/#(_)_/#|_|_|#|_|#|_|_|##\___|##### # #""
""############ ## ## ############  # ####  ##################### ######## #.""
""############# ## ## ########## # ## ### ##09/04/2018############ ######## #""
""############################# # ## ### ###### ################### ########.""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Modultes
" ========
" Plugins ( '$USER# vundles' to select )
<<<<<<< HEAD:vimrc
source $HOME/.vim/plugins.vim

=======
source ~/.vim/plugins.vim
>>>>>>> proxy:vim/vimrc
" Colorschemes ( '$USER# vthm' to select )
source $HOME/.vim/themes.vim

" Filetypes
" =========
" Loads ftplugin (filetype plugin) and indent rules for filetypes
filetype plugin indent on
" Source html skeleton
au BufNewFile *.html 0r ~/.vim/skeletons/html.skel | let IndentStyle = "html"
syntax on

" Default Behaviour
" =================
" Systems default shell
<<<<<<< HEAD:vimrc
set shell=bash

=======
set shell=/usr/bin/zsh
>>>>>>> proxy:vim/vimrc
" Default terminal size when opening vim. Gnome terminals default is 24x80.
" This makes room for line numbers
set lines=24 columns=84
" Display line numbers
set nu
set shell=bash
" Margin for maximum code length
set colorcolumn=80"
" Linux computer here
set fileformat=unix
" utf-8 rule
set encoding=utf-8
" Follow prior indents
set smartindent
" Wrap text
set wrap
" Dont allow vim to slice words over multiple lines
set linebreak
<<<<<<< HEAD:vimrc

let $TMP=expand('~/tmp')

" Save vim temp files here and don't pollute home directory
set backupdir=$HOME/.vim/tmp/

" Save vim swap files here
set directory=$HOME/.vim/swp/

=======
" Save vim temp files here and don't pollute home directory
set backupdir=~/.vim/tmp/
" Save vim swap files here
set directory=~/.vim/swp/
>>>>>>> proxy:vim/vimrc
" Allow vim to run commands from file if instructed to
set exrc
" Mitigates exrc risks somewhat
set secure
" Rule for code folding
set foldmethod=indent
" Opens all folds regardless of method to fold
set foldlevel=99
" Split below original buffer when splitting horizontally
set splitbelow
" Split to the right of original buffer when splitting vertically
set splitright
" Default number of characters for tab
set tabstop=4 softtabstop=4
set shiftwidth=4 textwidth=79
" Auto indent for tabs
set expandtab autoindent
" Allow access to system clipboard for vim
set clipboard=unnamed
" Rule for wrapping
set breakindent
" Show when a line has been broken
set showbreak=>\ \ \
" Change the default dollar sign for end of line character
set listchars=tab:▸\ ,eol:¬
" Turn of Vi compatibility and remain Vi Improved
set nocompatible
" Allow use od mouse within vim like a regular text editor
set mouse=a
" Highlight the current line
set cursorline
" Buffers
set hidden
" Turn off annoying terminal bell sound
set noerrorbells visualbell t_vb=
" Filetypes to use bulletpoint rules
let bullets_enabled_file_types = [
    \ 'markdown',
    \ 'text',
    \ 'gitcommit',
    \ 'scratch'
    \]
" Default size for NERDTree
let NERDTreeWinSize=30
" Default size for Tagbar
let tagbar_width=35
" Ignore irrelevant files in file explorer
let NERDTreeIgnore = ['\.DAT$', '\.LOG1$', '\.LOG1$']
" Let NERDTree hijack netrw
let NERDTreeHijackNetrw=0
" Expand vim for tagbar
let tagbar_expand = 1

" Key Mappings
" ============
" Toggle Tagbar
nmap <F8> :TagbarToggle<CR>
" Toggle NERDTree
map <C-n> :NERDTreeToggle<CR>
" Easily change buffers
nnoremap <C-N> :bnext<CR>
nnoremap <C-P> :bprev<CR>
" Use spacebar to fold text ins visual mode
nnoremap <space> za
" Map ConqueTerm for in vim terminal
map <C-T> :ConqueTermSplit zsh<CR><ESC>:resize -10<CR>

" Auto Commands
" ==================
" Remove whitespace on save
autocmd BufWritePre * :%s/\s\+$//e
let python_highlight_all = 1
" let ale_python_pylint_options = '--load-plugins pylint_django'
" let autopep8_on_save = 1
autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab
" Syntax for files with no extension
autocmd BufNewFile,BufRead * if expand('%:t') !~ '\.' | set syntax=sh | endif
" for gutentags
set tags=/usr/bin/ctags-exuberant
" go the pre-commit hook but still useful
function! TrimWhiteSpace()
    %s/\s\+$//e
endfunction
" don't know which one is the good one
autocmd BufWritePre     * :call TrimWhiteSpace()
" addon for better docstrings
map <C-F> :Pydocstring<CR>
set vb t_vb=".
au FileType python setlocal formatprg=autopep8\ -
if has('gui')
    set novb
    set noerrorbells
endif
" put ctags cache in home dotfile
let g:gutentags_cache_dir="~/.tags"
" for the pymode addon use python3
let g:pymode_python = 'python3'
" don't leave vim open for NERDTree
function! s:CloseIfOnlyNerdTreeLeft()
  if exists("t:NERDTreeBufName")
    if bufwinnr(t:NERDTreeBufName) != -1
      if winnr("$") == 1
        q
      endif
    endif
  endif
endfunction
" ???
autocmd Filetype gitcommit setlocal spell textwidth=72
" ???
autocmd BufWritePre * %s/\s\+$//e
" open NERDTree on startup
au VimEnter *  NERDTree
" open Tagbar on startup
autocmd VimEnter * nested :TagbarOpen
" jump to the main window.
autocmd VimEnter * wincmd p

function! StartUp()
    if 0 == argc()
        NERDTree
    end
endfunction

autocmd VimEnter * call StartUp()
