from ometa.runtime import character, ParseError, EOFError
from terml.common import CommonParser
from terml.nodes import Tag, Term

termLGrammar = r"""
literal = (string:x -> Term(Tag(".String."), x, None, None)
            | character:x -> Term(Tag(".char."), x, None, None)
            | number:x -> Term(Tag(numberType(x)), x, None, None))

tag = (segment:seg1 (':' ':' sos)*:segs -> makeTag(cons(seg1, segs))
        | (':' ':' sos)+:segs -> prefixedTag(segs))

sos = segment | (string:s -> tagString(s))

segment = ident | special | uri

ident = segStart:i1 segPart*:ibits -> join(cons(i1, ibits))

segStart = letter | '_' | '$'

segPart = letterOrDigit | '_' | '.' | '-' | '$'

special = '.':a ident:b -> concat(a, b)

uri = '<' uriBody*:uriChars '>' -> concat(b, uriChars, e)

functor = spaces (literal | tag:t)
baseTerm = functor:f ('(' argList:a spaces ')' -> makeTerm(f, a)
                           | -> makeTerm(f))

argList = ((term:t (',' term)*:ts ','?) -> cons(t, ts)
            | -> [])

tupleTerm = token('[') argList:a token(']') -> Tuple(a)

bagTerm = token('{') argList:a token('}') -> Bag(a)

labelledBagTerm = functor:f bagTerm:b -> LabelledBag(f, b)

extraTerm = tupleTerm | labelledBagTerm  | bagTerm | baseTerm

attrTerm = extraTerm:k token(':') extraTerm:v -> Attr(k, v)

term =  attrTerm | extraTerm

"""

## Functions called from grammar actions

def Character(char):
    return character(char)

def makeTag(nameSegs):
    return Tag('::'.join(nameSegs))

def prefixedTag(tagnameSegs):
    return makeTag([''] + tagnameSegs)

def tagString(string):
    return '"' + string + '"'

def numberType(n):
    if isinstance(n, float):
        return ".float64."
    elif isinstance(n, (long, int)):
        return ".int."
    raise ValueError("wtf")


def makeTerm(t, args=None):
    if isinstance(t, Term):
        if args:
            raise ValueError("Literal terms do not take arguments")
        return t
    return Term(t, None, args, None)


def Tuple(args):
    return Term(Tag(".tuple."), None, args, None)

def Bag(args):
    return Term(Tag(".bag."), None, args, None)

def LabelledBag(f, arg):
    return Term(f, None, [arg], None)

def Attr(k, v):
    return Term(Tag(".attr."), None, [k, v], None)

try:
    from terml.parser_generated import Parser as BaseTermLParser
    BaseTermLParser.globals = globals()
except ImportError:
    from ometa.boot import BootOMetaGrammar
    BaseTermLParser = BootOMetaGrammar.makeGrammar(termLGrammar, globals(),
                                                   "TermLParser")

class TermLParser(BaseTermLParser, CommonParser):
    pass
TermLParser.globals.update(CommonParser.globals)

def _parseTerm(termString):
    """
    Parser frontend for term strings.
    """
    p = TermLParser(termString)
    result, error = p.apply("term")
    try:
        p.input.head()
    except EOFError:
        pass
    else:
        raise error
    return result


def parseTerm(termString):
    """
    Friendly interface for parsing.
    """
    try:
        return _parseTerm(termString)
    except ParseError, e:
        print e.formatError(termString)
        raise
