from ometa.runtime import character, ParseError, EOFError
from terml.common import CommonParser
from terml.nodes import Tag, Term
from terml.twine import spanCover

termLGrammar = r"""
spaces = ('\r' '\n'|'\r' | '\n' | horizontal_space)*
literal =  !(self.startSpan()):s (
              string:x -> Term(Tag(".String."), x, None, self.span(s))
            | character:x -> Term(Tag(".char."), x, None, self.span(s))
            | number:x -> Term(Tag(numberType(x)), x, None, self.span(s)))

tag =  (
          segment:seg1 (':' ':' sos)*:segs -> makeTag(cons(seg1, segs))
        | (':' ':' sos)+:segs -> prefixedTag(segs))

sos = segment | (string:s -> tagString(s))

segment = ident | special | uri

ident = segStart:i1 segPart*:ibits -> join(cons(i1, ibits))

segStart = letter | '_' | '$'

segPart = letterOrDigit | '_' | '.' | '-' | '$'

special = '.':a ident:b -> concat(a, b)

uri = '<' uriBody*:uriChars '>' -> concat(b, uriChars, e)

functor = spaces (literal | tag:t)
baseTerm = !(self.startSpan()):s functor:f (
                             '(' argList:a spaces ')' -> makeTerm(f, a, self.span(s))
                           | -> makeTerm(f, None, self.span(s)))

arg = term

argList = ((arg:t (token(',') arg)*:ts token(',')?) -> cons(t, ts)
            | -> [])

tupleTerm = !(self.startSpan()):s token('[') argList:a token(']') -> Tuple(a, self.span(s))

bagTerm = !(self.startSpan()):s token('{') argList:a token('}') -> Bag(a, self.span(s))

labelledBagTerm = !(self.startSpan()):s functor:f bagTerm:b -> LabelledBag(f, b, self.span(s))

extraTerm = tupleTerm | labelledBagTerm  | bagTerm | baseTerm

attrTerm = !(self.startSpan()):s extraTerm:k token(':') extraTerm:v -> Attr(k, v, self.span(s))

term =  spaces (attrTerm | extraTerm)

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


def makeTerm(t, args=None, span=None):
    if isinstance(t, Term):
        if args:
            raise ValueError("Literal terms do not take arguments")
        return t
    return Term(t, None, args and tuple(args), span)


def Tuple(args, span):
    return Term(Tag(".tuple."), None, tuple(args), span)

def Bag(args, span):
    return Term(Tag(".bag."), None, tuple(args), span)

def LabelledBag(f, arg, span):
    return Term(f, None, (arg,), span)

def Attr(k, v, span):
    return Term(Tag(".attr."), None, (k, v), span)



try:
    from terml.terml_generated import Parser as BaseTermLParser
    BaseTermLParser.globals = globals()
except ImportError:
    from ometa.boot import BootOMetaGrammar
    BaseTermLParser = BootOMetaGrammar.makeGrammar(termLGrammar, globals(),
                                                   "TermLParser")

class TermLParser(BaseTermLParser, CommonParser):

    def startSpan(self):
        return self.input.position

    def span(self, start):
        end = self.input.position
        return self.input.data[start:end].span



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
