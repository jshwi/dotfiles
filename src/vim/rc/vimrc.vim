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
" =============================================================================
" MODULES
" =============================================================================
source $HOME/.vim/plugins/plugins.vim
source $HOME/.vim/plugins/themes.vim

" =============================================================================
" FILETYPES
" =============================================================================
filetype plugin indent on
au BufNewFile *.html 0r $HOME/.vim/skeletons/html.skel | let IndentStyle = "html"
syntax on
" Filetypes to use bulletpoint rules
let bullets_enabled_file_types = [
    \ 'markdown',
    \ 'text',
    \ 'gitcommit',
    \ 'scratch'
    \]


" =============================================================================
" BEHAVIOUR
" =============================================================================
set shell=zsh
set lines=24 columns=84  "terminal size on open
set nu  "line numbers
set colorcolumn=72,80
set fileformat=unix
set encoding=utf-8
set tags=/usr/bin/ctags
"--- indenting ---
set autoindent  " Auto indent for tabs
set smartindent  " follow prior indent
set tabstop=2
set backspace=indent,eol,start
set softtabstop=2
set wrap
set breakindent  " Rule for wrapping
set linebreak
set foldmethod=indent  " Rule for code folding
set foldlevel=99
set shiftwidth=4
" set textwidth=79
set expandtab
" --- file-locations ---
set backupdir=$HOME/.vim/tmp/
set directory=$HOME/.vim/swp/
set exrc  " allow vim to run commands from file if instructed to
set secure  " mitigates exrc risks somewhat
set splitbelow  " split below buffer when splitting horizontally
set splitright  " split to the right of buffer when splitting vertically
set clipboard=unnamed  " allow access to system clipboard for vim
set showbreak=>\ \ \  " show when a line has been broken
set listchars=tab:▸\ ,eol:¬  " replace the dollar sign for end of line character
set nocompatible  " Turn of Vi compatibility and remain Vi Improved
set mouse=a  " Allow use od mouse within vim like a regular text editor
set cursorline
set hidden
"--- Turn off annoying terminal bell sound ---
set noerrorbells
set visualbell
set vb
set t_vb=".
set viminfo+=n~/.vim/.cache/viminfo

" =============================================================================
" NERDTREE
" =============================================================================
let NERDTreeIgnore = ['\.DAT$', '\.LOG1$', '\.LOG1$']
let NERDTreeHijackNetrw=0
let g:NERDTreeDirArrows = 1
let g:NERDTreeDirArrowExpandable = '▸'
let g:NERDTreeDirArrowCollapsible = '▾'
let g:NERDTreeGlyphReadOnly = "RO"


" =============================================================================
" NERDTREE
" =============================================================================
let tagbar_expand = 1


" =============================================================================
" PYMODE
" =============================================================================
let g:pymode_python = 'python3.8'
let g:pymode_rope = 0
let g:pymode_lint = 0
let python_highlight_all = 1


" =============================================================================
" GUTENTAGS
" =============================================================================
let g:gutentags_cache_dir="~/.tags"


" =============================================================================
" KEY MAPPING
" =============================================================================
nmap <F8> :TagbarToggle<CR>
map <C-n> :NERDTreeToggle<CR>
nnoremap <C-N> :bnext<CR>
nnoremap <C-P> :bprev<CR>
nnoremap <space> za
map <C-T> :ConqueTermSplit zsh<CR><ESC>:resize -10<CR>
map <C-F> :Pydocstring<CR>
vnoremap <c-f> y<ESC>/<c-r>"<CR>


" =============================================================================
" KEY MAPPING
" =============================================================================
autocmd BufWritePre * :%s/\s\+$//e
autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab
autocmd BufNewFile,BufRead * if expand('%:t') !~ '\.' | set syntax=sh | endif
function! TrimWhiteSpace()
    %s/\s\+$//e
endfunction
autocmd BufWritePre     * :call TrimWhiteSpace()
au FileType python setlocal formatprg=autopep8\ -
if has('gui')
    set novb
    set noerrorbells
endif
autocmd Filetype gitcommit setlocal spell textwidth=72
set clipboard+=ideaput

" replace currently selected text with default register
" without yanking it
vnoremap <leader>p "_dP
xnoremap p pgvy
let Tlist_Ctags_Cmd = '/usr/bin/ctags-exuberant'

let g:ycm_server_keep_logfiles = 1
let g:ycm_server_log_level = 'debug'

set viminfo='100,n$HOME/.vim/files/info/viminfo
" autocmd VimEnter * AnsiEsc
