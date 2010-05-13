import string
from pymeta.grammar import OMeta

baseGrammar = r"""
spaces ::= (' '|'\t'|'\f'|('#' (~<eol> <anything>)*))*

number ::= <spaces> <barenumber>
barenumber ::= '-'?:sign ('0' (('x'|'X') <hexdigit>*:hs => makeHex(sign, hs)
                    |<floatPart sign '0'>
                    |<octaldigit>*:ds => makeOctal(sign, ds))
               |<decdigits>:ds <floatPart sign ds>
               |<decdigits>:ds => signedInt(sign, join(ds)))


exponent ::= ('e' | 'E'):e ('+' | '-' | => ""):s <decdigits>:ds => concat(e, s, join(ds))


floatPart :sign :ds ::= ('.' <decdigits>:fs <exponent>?:e => makeFloat(sign, ds, fs, e)
                               | <exponent>:e => float((sign or '') + concat(ds, e)))

decdigits ::= <digit>:d ((:x ?(isDigit(x)) => x) | '_' => "")*:ds => concat(d, join(ds))
octaldigit ::= :x ?(isOctDigit(x)) => x
hexdigit ::= :x ?(isHexDigit(x)) => x

string ::= <token '"'> (<escapedChar> | ~('"') <anything>)*:c '"' => join(c)
character ::= <token "'"> (<escapedChar> | ~('\''|'\n'|'\r'|'\\') <anything>):c '\'' => Character(c)
escapedUnicode ::= ('u' <hexdigit>:a <hexdigit>:b <hexdigit>:c <hexdigit>:d => unichr(int(concat(a, b, c, d), 16))
                   |'U' (<hexdigit>:a <hexdigit>:b <hexdigit>:c <hexdigit>:d
                         <hexdigit>:e <hexdigit>:f <hexdigit>:g <hexdigit>:h => unichr(int(concat(a, b, c, d, e, f, g, h), 16))))

escapedOctal ::= ((:a ?(contains("0123", a))) (<octdigit>:b  (<octdigit>:c (=> int(concat(a, b, c), 8)) | (=> int(concat(a, b), 8))| => int(a, 8)))
                 | :a ?(contains("4567", a)) (<octdigit>:b (=> int(concat(a, b), 8)) | => int(a, 8)))

escapedChar ::= '\\' ('n' => '\n'
                     |'r' => '\r'
                     |'t' => '\t'
                     |'b' => '\b'
                     |'f' => '\f'
                     |'"' => '"'
                     |'\'' => '\''
                     |'?' => '?'
                     |'\\' => '\\'
                     | <escapedUnicode>
                     | <escapedOctal>
                     | <spaces> <eol> => "")

eol ::= <spaces> ('\r' '\n'|'\r' | '\n')

uriBody ::= (<letterOrDigit> |';'|'/'|'?'|':'|'@'|'&'|'='|'+'|'$'|','|'-'|'.'|'!'|'~'|'*'|'\''|'('|')'|'%'|'\\'|'|'|'#')+:x => join(x)

"""


def concat(*bits):
    return ''.join(map(str, bits))


def makeFloat(sign, ds, fs, e):
    if e:
        return float((sign or '') + ds+"."+fs+e)
    else:
        return float((sign or '') + ds+"."+fs)

def signedInt(sign, x, base=10):
    return int((sign or '')+x, base)

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

CommonParser = OMeta.makeGrammar(baseGrammar,  globals(), "CommonParser")
