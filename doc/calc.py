from parsley import makeGrammar

calcGrammar = """
ws = ' '*
digit = anything:x ?(x in '0123456789')
number = <digit+>:ds -> int(ds))
parens = '(' ws expr:e ws ')' -> e
value = ws (number | parens)
expr = muldiv:left ws ('+' muldiv:right -> left + right
                        |'-' muldiv:right -> left - right
                        | -> left)
muldiv = value:left ws ('*' value:right -> left * right
                       |'/' value:right -> left / right
                       | -> left)
"""

Calc = makeGrammar(calcGrammar, {})
