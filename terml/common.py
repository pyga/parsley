import string
from terml.nodes import termMaker

baseGrammar = r"""
horizontal_space = (' '|'\t'|'\f'|('#' (~eol anything)*))
spaces = horizontal_space*

number = spaces barenumber
barenumber = '-'?:sign (('0' ((('x'|'X') hexdigit*:hs -> makeHex(sign, hs))
                    |floatPart(sign '0')
                    |octaldigit*:ds -> makeOctal(sign, ds)))
               |decdigits:ds floatPart(sign, ds)
               |decdigits:ds -> signedInt(sign, ds))


exponent = <('e' | 'E') ('+' | '-')? decdigits>


floatPart :sign :ds = <('.' decdigits exponent?) | exponent>:tail -> makeFloat(sign, ds, tail)

decdigits = digit:d ((:x ?(isDigit(x)) -> x) | '_' -> "")*:ds -> concat(d, join(ds))
octaldigit = :x ?(isOctDigit(x)) -> x
hexdigit = :x ?(isHexDigit(x)) -> x

string = token('"') (escapedChar | ~('"') anything)*:c '"' -> join(c)
character = token("'") (escapedChar | ~('\''|'\n'|'\r'|'\\') anything):c '\'' -> Character(c)
escapedUnicode = ('u' <hexdigit hexdigit hexdigit hexdigit>:hs -> unichr(int(hs, 16))
                   |'U' <hexdigit hexdigit hexdigit hexdigit
                         hexdigit hexdigit hexdigit hexdigit>:hs -> unichr(int(hs, 16)))

escapedOctal = ( <:a ?(contains("0123", a)) octdigit? octdigit?>
                 | <:a ?(contains("4567", a)) octdigit?>):os -> int(os, 8)

escapedChar = '\\' ('n' -> '\n'
                     |'r' -> '\r'
                     |'t' -> '\t'
                     |'b' -> '\b'
                     |'f' -> '\f'
                     |'"' -> '"'
                     |'\'' -> '\''
                     |'?' -> '?'
                     |'\\' -> '\\'
                     | escapedUnicode
                     | escapedOctal
                     | eol -> "")

eol = horizontal_space* ('\r' '\n'|'\r' | '\n')

uriBody = <(letterOrDigit |';'|'/'|'?'|':'|'@'|'&'|'='|'+'|'$'|','|'-'|'.'|'!'|'~'|'*'|'\''|'('|')'|'%'|'\\'|'|'|'#')+>

"""


def concat(*bits):
    return ''.join(map(str, bits))

Character = termMaker.Character

def makeFloat(sign, ds, tail):
        return float((sign or '') + ds + tail)

def signedInt(sign, x, base=10):
    return int(str((sign or '')+x), base)

def join(x):
    return ''.join(x)

def makeHex(sign, hs):
    return int((sign or '') + ''.join(hs), 16)

def makeOctal(sign, ds):
    return int((sign or '') + '0'+''.join(ds), 8)

def isDigit(x):
    return x in string.digits

def isOctDigit(x):
    return x in string.octdigits

def isHexDigit(x):
    return x in string.hexdigits

def contains(container, value):
    return value in container

def cons(first, rest):
    return [first] + rest


def brk(x):
    import pdb; pdb.set_trace()
    return x

try:
    from terml.common_generated import Parser as CommonParser
    CommonParser.globals = globals()
except ImportError:
    from ometa.boot import BootOMetaGrammar
    CommonParser = BootOMetaGrammar.makeGrammar(baseGrammar, globals(),
                                                "CommonParser")
