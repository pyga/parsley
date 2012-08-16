from parsley import makeGrammar

calcGrammar = """
digit = anything:x ?(x in '0123456789')
number = <digit+>:ds -> int(ds)
ws = ' '*
parens = '(' ws expr:e ws ')' -> e
value = number | parens
muldiv = ws ('*' ws value
            |'/' ws value:n -> 1.0/n)
expr2 = value:n (muldiv+:vals -> n * reduce(lambda x, y: x * y, vals, 1)
                    | -> n)
addsub = ws ('+' ws expr2
            |'-' ws expr2:n -> -n)
expr = expr2:e (addsub+:vals -> e + sum(vals)
                   | -> e)
"""

Calc = makeGrammar(calcGrammar, {})
