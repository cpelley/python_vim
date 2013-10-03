" setup wrapping
setlocal textwidth=79   " width of document
setlocal nowrap  " don't automatically wrap on load
setlocal fo-=t   " don't automatically wrap text when typing

" define plugin script location for relative executing
let s:path = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" Colour column at 80char
if exists('+colorcolumn')
  setlocal colorcolumn=80
else
  autocmd BufWinEnter * let w:m2=matchadd('ErrorMsg', '\%>80v.\+', -1)
endif
highlight ColorColumn ctermbg=241

" Highlight when over line length
highlight OverLength ctermbg=red ctermfg=white guibg=#592929
match OverLength /\%80v.\+/

" Remove trailing whitespace on save
"autocmd BufWritePre * :%s/\s\+$//e

" Setup TABs
setlocal tabstop=4
setlocal softtabstop=4
setlocal shiftwidth=4
setlocal shiftround
setlocal expandtab
setlocal autoindent

" code folding (command: za, zM -foldall zR -infoldall)
setlocal foldignore=
setlocal foldmethod=indent
setlocal foldlevel=99
setlocal foldnestmax=2

" Run python
command Runpython execute "!python %"
command Runpythonint execute "!python -i %"

" Settings for jedi-vim
" " cd ~/.vim/bundle
" " git clone git://github.com/davidhalter/jedi-vim.git
let g:jedi#popup_on_dot = 0 "no automatic popup
let g:jedi#show_call_signatures = "1" "arguments of function, does slow completion down

" shortcut for inserting ipdb debug
map <Leader>b Oimport ipdb; ipdb.set_trace()<ESC>
" remove
map <leader>bd :g/import ipdb; ipdb.set_trace()/d<ESC>:nohl<CR>

" automatically adjust quickfix window height
function! AdjustWindowHeight(minheight, maxheight)
    exe max([min([line("$"), a:maxheight]), a:minheight]) . "wincmd _"
endfunction


" monkeypatched pyflakes for consistent interp.
command Pyflakes :call Pyflakes()
function! Pyflakes()
    cclose
    exe "setlocal makeprg=" . s:path . "/../bin/pyflake_parsed.py\\ %"
    silent make|redraw!
    au FileType qf call AdjustWindowHeight(3, 10)
    cw
    cfirst
endfunction

command Pep8 :call Pep8()
function! Pep8()
    cclose
    setlocal makeprg=pep8\ --repeat\ %
    silent make|redraw!
    au FileType qf call AdjustWindowHeight(3, 10)
    cw
    cfirst
endfunction

command Browse :call Browse()
function! Browse()
    cclose
    exe "setlocal makeprg=" . s:path . "/../bin/python_class_browser.py\\ %" 
    silent make|redraw!
    au FileType qf call AdjustWindowHeight(3, 20)
    cw
    cfirst
endfunction
