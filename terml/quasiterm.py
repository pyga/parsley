from ometa.boot import BootOMetaGrammar
from ometa.runtime import ParseError, EOFError
from terml.parser import TermLParser
from terml.qnodes import ValueHole, PatternHole, QTerm, QSome, QFunctor

quasitermGrammar = """
schema = production+:ps -> schema(ps)
production = tag:t token('::=') argList:a token(';') -> production(t, a)

functor = (spaces ( (functorHole functorHole !(reserved("hole-tagged-hole")))
                  | ('.'? functorHole)
                  | (tag:t functorHole:h) -> taggedHole(t, h)))
          | super

arg = interleave:l (token('|') interleave)*:r -> _or(l, *r)
interleave = action:l (token('&') action)*:r -> interleave(l, *r)
action = pred:l (token('->') pred:r -> action(l, *r)
                |                   -> l)
pred = some | (token('!') some:x -> not(x))
some = (quant:q -> some(None, q)
       | ( prim:l ( (token('**') prim:r -> matchSeparatedSequence(l, r))
                  | (token('++') prim:r -> matchSeparatedSequence1(l, r))
                  )?:seq
           quant?:q -> some(seq or l, q)))
quant = token('?') | token('+') | token('*')
prim = term
     | ('.' -> any())
     | (literal:l token('..') literal:r -> range(l, r))
     | token('^') string:s -> anyOf(s)
     | token('(') argList:l token(')') -> l

simpleint = decdigits:ds -> int(ds)
functorHole = '$'        (simpleint:i | '{' simpleint:i '}' | (tag:t -> t.name):i) -> dollarHole(i)
            |('@' | '=') (simpleint:i | '{' simpleint:i '}' | (tag:t -> t.name):i) -> patternHole(i)

"""

def interleave(l, *r):
    if r:
        raise NotImplementedError()
    return l

def _or(l, *r):
    if r:
        raise NotImplementedError()
    return l

def some(value, quant):
    if quant:
        return QSome(value, quant)
    else:
        return value

def dollarHole(i):
    return ValueHole(None, i, False)

def patternHole(i):
    return PatternHole(None, i, False)

def taggedHole(t, h):
    return h.__class__(t, h.name, h.isFunctorHole)

def leafInternal(tag, data, span):
    return QFunctor(tag, data, span)


def makeTerm(t, args=None, span=None):
    if args is None:
        return t
    else:
        if isinstance(t, QTerm):
            if t.data:
                if not args:
                    return t
                else:
                    raise ValueError("Literal terms can't have arguments")
    return QTerm(t.asFunctor(), None, args and tuple(args), span)


QTermParser = BootOMetaGrammar.makeGrammar(quasitermGrammar,
                                           TermLParser.globals,
                                           "QTermParser", TermLParser)
QTermParser.globals.update(globals())




def quasiterm(termString):
    """
    Build a quasiterm from a string.
    """
    p = QTermParser(termString)
    result, error = p.apply("term")
    try:
        p.input.head()
    except EOFError:
        pass
    else:
        raise error
    return result
