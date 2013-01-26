from parsley import makeGrammar

jsonGrammar = r"""
object = token('{') members:m token('}') -> dict(m)

members = (pair:first (token(',') pair)*:rest -> [first] + rest)
          | -> []

pair = string:k token(':') value:v -> (k, v)

array = token('[') elements:xs token(']') -> xs
elements = (value:first (token(',') value)*:rest -> [first] + rest)
           | -> []

value = (string | number | object | array
        | token('true')  -> True
        | token('false') -> False
        | token('null')  -> None)

string = token('"') (escapedChar | ~'"' anything)*:c '"' -> ''.join(c)

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

hexdigit = :x ?(x in '0123456789abcdefABCDEF') -> x
escapedUnicode = 'u' <hexdigit{4}>:hs -> unichr(int(hs, 16))

number = spaces ('-' | -> ''):sign (intPart:ds (floatPart(sign ds)
                                               | -> int(sign + ds)))
digit = :x ?(x in '0123456789') -> x
digits = <digit*>
digit1_9 = :x ?(x in '123456789') -> x

intPart = (digit1_9:first digits:rest -> first + rest) | digit
floatPart :sign :ds = <('.' digits exponent?) | exponent>:tail
    		 -> float(sign + ds + tail)
exponent = ('e' | 'E') ('+' | '-')? digits
"""

JSONParser = makeGrammar(jsonGrammar, {})
