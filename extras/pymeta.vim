" Vim syntax file
" Language:         PyMeta
" Maintainer:       Cory Dodt
" Last Change:      $Date: 2009/10/04 14:42:09 $
" Version:          $Id: pymeta.vim,v 1.1 2009/10/04 14:42:09 cdodt Exp $    

" Quit when a syntax file was already loaded
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

hi link pymetaExec NONE
hi link pymetaFilter NONE
hi link subExpression NONE
hi link pymetaTerminal NONE
hi link pymetaIdentifier NONE
hi link pymetaSeparator NONE
hi link pymetaReturns NONE
hi link pymetaOptional NONE
hi link pymetaMultiple NONE
hi link pymetaNot NONE
hi link pymetaVariable NONE
hi link pymetaChoice NONE
hi link pymetaOp NONE
hi link cddComment NONE
hi link pymetaChrLiteral NONE

syn region pymetaVariable start=/:/ end=/[^A-Za-z0-9_]/

syn match pymetaIdentifier /[A-Za-z0-9_]/
syn match pymetaOp         /\(::=\||\|=>\|[|?*+~]\)/
syn match pymetaOpNohl     /[()]/ " don't highlight parens - gets annoying

syn region subExpression  start=/(/ end=/)/ contained
syn region pymetaTerminal start=/</ end=/>/
syn region pymetaExec     start=/!(/ end=/)/ contains=subExpression
syn region pymetaFilter   start=/?(/ end=/)/ contains=subExpression
syn region cddComment     start=/COMMENT::=!("""/ end=/""")/
syn region pymetaChrLiteral start=/'/ end=/'/

hi link pymetaExec       Special
hi link pymetaFilter     Special
hi link subExpression    Special
hi link pymetaTerminal   Constant
" hi link pymetaIdentifier Identifier
hi link pymetaOp         Operator
hi link pymetaVariable   Identifier
hi link cddComment       Comment
hi link pymetaChrLiteral String
