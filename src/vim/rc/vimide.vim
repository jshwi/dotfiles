source $HOME/.vim/rc/vimrc.vim
" Default size for NERDTree
let NERDTreeWinSize=30
" Default size for Tagbar
let tagbar_width=35
" open NERDTree on startup
au VimEnter *  NERDTree
" open Tagbar on startup
autocmd VimEnter * nested :TagbarOpen
" jump to the main window.
autocmd VimEnter * wincmd p

autocmd BufWritePre * %s/\s\+$//e
" Close all open buffers on entering a window if the only
" buffer that's left is the NERDTree buffer
function! s:CloseIfOnlyNerdTreeLeft()
  if exists("t:NERDTreeBufName")
    if bufwinnr(t:NERDTreeBufName) != -1
      if winnr("$") == 1
        q
      endif
    endif
  endif
endfunction

autocmd Filetype gitcommit setlocal spell textwidth=72
