from parsley import makeGrammar

calcGrammar = """
ws = ' '*
number = digit+:ds -> int(''.join(ds))
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
