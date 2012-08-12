from parsley import makeGrammar

jsonGrammar = r"""
escapedChar = '\\' ('"' -> '"'
                   |'\\' -> '\\'
                   |'/' -> '/'
                   |'b' -> '\b'
                   |'f' -> '\f'
                   |'n' -> '\n'
                   |'r' -> '\r'
                   |'t' -> '\t'
                   |'\'' -> '\''
                   | escapedUnicode)
ws = (' ' | '\t' | '\r' | '\n')*
object = '{' ws members:m ws '}' -> dict(m)
members = (pair:first (ws ',' ws pair)*:rest -> [first] + rest)
          | -> []
pair = string:k ws ':' ws value:v -> (k, v)
array = '[' ws elements:xs ws ']' -> xs
elements = (value:first (ws ',' ws value)*:rest -> [first] + rest)
           | -> []
value = ws (string | number | object | array
           | token('true')  -> True
           | token('false') -> False
           | token('null')  -> None)

string = '"' (escapedChar | ~('"') anything)*:c '"' -> ''.join(c)
number = ('-' | -> ''):sign (intPart:ds floatPart(sign ds)
                            |intPart:ds -> int(sign + ds))
intPart = (digit1_9:first digits:rest -> first + rest) | digit

exponent = <('e' | 'E') ('+' | '-')? digits>
floatPart :sign :ds = <('.' digits exponent?) | exponent>:tail
                     -> float(sign + ds + tail)

digit = :x ?(x in '0123456789') -> x
digits = digit*:ds -> ''.join(ds)
digit1_9 = :x ?(x in '123456789') -> x
digits1_9 = digit1_9*:ds -> ''.join(ds)

hexdigit = :x ?(x in '0123456789abcdefABCDEF') -> x
escapedUnicode = 'u' <hexdigit{4}>:hs -> unichr(int(hs, 16))
"""

JSONParser = makeGrammar(jsonGrammar, {})
