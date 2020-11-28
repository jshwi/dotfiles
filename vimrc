"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""##### ## ## ############ ### ##### #### ####### ######## ######## # #######""
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
source ~/.vim/plugins.vim

" Colorschemes ( '$USER# vthm' to select )
source ~/.vim/themes.vim



" Filetypes
" =========
" Loads ftplugin (filetype plugin) and indent rules for filetypes
filetype plugin indent on

" Source html skeleton
au BufNewFile *.html 0r ~/.vim/skeletons/html.skel | let IndentStyle = "html"



" Default Behaviour
" =================
" Systems default shell
set shell=/usr/bin/zsh

" Default terminal size when opening vim. Gnome terminals default is 24x80.
" This makes room for line numbers
set lines=24 columns=84

" Display line numbers
set nu

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

" Save vim temp files here and don't pollute home directory
set backupdir=~/.vim/tmp/

" Save vim swap files here
set directory=~/.vim/swp/

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
let g:bullets_enabled_file_types = [
    \ 'markdown',
    \ 'text',
    \ 'gitcommit',
    \ 'scratch'
    \]

" Default size for NERDTree
let g:NERDTreeWinSize=20

" Default size for Tagbar
let tagbar_width=25

" Ignore irrelevant files in file explorer
let NERDTreeIgnore = ['\.DAT$', '\.LOG1$', '\.LOG1$']

" Let NERDTree hijack netrw
let g:NERDTreeHijackNetrw=0

" Expand vim for tagbar
let g:tagbar_expand = 1

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



" Automatic Commands
" ==================
" Remove whitespace on save
autocmd VimEnter * wincmd p
autocmd BufWritePre * :%s/\s\+$//e
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
let g:python_highlight_all = 1
