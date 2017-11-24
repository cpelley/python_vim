" setup wrapping
setlocal textwidth=79   " width of document
setlocal nowrap  " don't automatically wrap on load
setlocal fo-=t   " don't automatically wrap text when typing

" define plugin script location for relative executing
let s:path = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" syntax highlight from the very beginning of the file (required due to large
" docstrings)
autocmd BufEnter * :syntax sync fromstart

" Colour column at 80char
if exists('+colorcolumn')
  setlocal colorcolumn=79
else
  autocmd BufWinEnter * let w:m2=matchadd('ErrorMsg', '\%>79v.\+', -1)
endif
highlight ColorColumn ctermbg=241

"" Highlight when over line length
"highlight OverLength ctermbg=red ctermfg=white guibg=#592929
"match OverLength /\%80v.\+/

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
command! Runpython execute "!python2.7 %"
command! Runpythonint execute "!python2.7 -i %"

" Settings for jedi-vim
" " cd ~/.vim/bundle
" " git clone --recursive https://github.com/davidhalter/jedi-vim.git ~/.vim/bundle/jedi-vim
"
" Add the virtualenv's site-packages to vim path (for jedi-vim)
if has('python')
py << EOF
import site
site.addsitedir('/home/h05/cpelley/.local/lib/python2.7/site-packages')
site.addsitedir('/project/atk/_dev/environments/latest/lib/python2.7/site-packages')
EOF
endif

let g:jedi#popup_on_dot = 0 "no automatic popup
let g:jedi#show_call_signatures = "1" "arguments of function, does slow completion down

" shortcut for inserting ipdb debug
map <Leader>b Oimport pdb; pdb.set_trace()<ESC>
" remove
map <leader>bd :g/import pdb; pdb.set_trace()/d<ESC>:nohl<CR>

" automatically adjust quickfix window height
function! AdjustWindowHeight(minheight, maxheight)
    exe max([min([line("$"), a:maxheight]), a:minheight]) . "wincmd _"
endfunction


" monkeypatched pyflakes for consistent interp.
command! Pyflakes :call Pyflakes()
function! Pyflakes()
    cclose
    exe "setlocal makeprg=" . s:path . "/../bin/pyflake_parsed.py\\ %"
    silent make|redraw!
    au FileType qf call AdjustWindowHeight(10, 10)
    cw
    cfirst
endfunction

command! Pep8 :call Pep8()
function! Pep8()
    cclose
    setlocal makeprg=pep8\ --repeat\ %
    silent make|redraw!
    au FileType qf call AdjustWindowHeight(10, 10)
    cw
    cfirst
endfunction

command! Browse :call Browse()
function! Browse()
    cclose
    exe "setlocal makeprg=" . s:path . "/../bin/python_class_browser.py\\ %" 
    silent make|redraw!
    au FileType qf call AdjustWindowHeight(10, 20)
    cw
    cfirst
endfunction

command! -nargs=1 Comment :call Comment(<f-args>)
function! Comment(tcom)
    :silent execute ":!" s:path . "/../bin/inline_code_comment.py" expand('%') line('.') a:tcom ">>" . expand('%') . ".comment" | redraw!
endfunction
