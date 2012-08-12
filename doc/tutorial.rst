
================
Parsley Tutorial
================

Four function calculator::

    digit = anything:x ?(x in '0123456789')
    number = <digit+>:ds -> int(ds))
    number = digit+:ds -> int(''.join(ds))
    ws = ' '*
    muldiv = value:left ws ('*' value:right -> left * right
                           |'/' value:right -> left / right
                           | -> left)

    expr = muldiv:left ws ('+' muldiv:right -> left + right
                            |'-' muldiv:right -> left - right
                            | -> left)
    parens = '(' ws expr:e ws ')' -> e
    value = ws (number | parens)
