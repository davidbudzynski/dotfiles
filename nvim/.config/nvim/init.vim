set tabstop=4 softtabstop=4
set shiftwidth=4
set expandtab
set smartindent
set relativenumber
set nu
set noerrorbells
set nowrap
set noswapfile
set incsearch
set scrolloff=8
set signcolumn=yes
set colorcolumn=80
set history=10000
set noshowmode

call plug#begin()
Plug 'gruvbox-community/gruvbox'
Plug 'itchyny/lightline.vim'
call plug#end()

colorscheme gruvbox
highlight Normal guibg=none

let g:lightline = {
      \ 'colorscheme': 'jellybeans',
      \ }
