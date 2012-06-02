from pymeta.grammar import OMeta
from pymeta.runtime import character, ParseError, EOFError
from terml.common import CommonParser

termLGrammar = r"""
literal ::= (<string>:x => TermLiteral(".String.", x)
            | <character>:x => TermLiteral(".char.", x)
            | <number>:x => TermLiteral(numberType(x), x))

tag ::= (<segment>:seg1 (':' ':' <sos>)*:segs => makeTag(cons(seg1, segs))
        | (':' ':' <sos>)+:segs => prefixedTag(segs))

sos ::= <segment> | (<string>:s => tagString(s))

segment ::= <ident> | <special> | <uri>

ident ::= <segStart>:i1 <segPart>*:ibits => join(cons(i1, ibits))

segStart ::= <letter> | '_' | '$'

segPart ::= <letterOrDigit> | '_' | '.' | '-' | '$'

special ::= '.':a <ident>:b => concat(a, b)

uri ::= '<' <uriBody>*:uriChars '>' => concat(b, uriChars, e)

functor ::= <spaces> (<literal> | <tag>:t (<functorHole>:h => taggedHole(t, h)
                                          | => t)
                     | <functorHole>)

functorHole ::= ((<token "${"> <decdigits>:n '}' => ValueHole(n))
                |(<token "$"> <decdigits>:n  => ValueHole(n))
                |(<token "$"> <tag>:t => NamedValueHole(t))
                |(<token "@{"> <decdigits>:n '}' => PatternHole(n))
                |(<token "@"> <decdigits>:n  => PatternHole(n))
                |(<token "@"> <tag>:t => NamedPatternHole(t)))

baseTerm ::= <functor>:f ('(' <argList>:a ')' => Term(f, a)
                     | => Term(f, emptyList()))

argList ::= ((<term>:t (',' <term>)*:ts ) => cons(t, ts)
            | => emptyList())

tupleTerm ::= <token '['> <argList>:a <token ']'> => Tuple(a)

bagTerm ::= <token '{'> <argList>:a <token '}'> => Bag(a)

labelledBagTerm ::= <functor>:f <bagTerm>:b => LabelledBag(f, b)

extraTerm ::= <tupleTerm> | <labelledBagTerm>  | <bagTerm> | <baseTerm>

attrTerm ::= <extraTerm>:k <token ':'> <extraTerm>:v => Attr(k, v)

term ::=  <attrTerm> | <extraTerm>

"""

class _Term(object):

    def __init__(self, functor, arglist):
        self.functor = functor
        self.arglist = arglist
        assert len(arglist) >= 0


    def __eq__(self, other):
        return (self.functor, self.arglist) == (other.functor, other.arglist)


    def __repr__(self):
        return "Term(%r)" % (self._unparse())


    def _unparse(self):
        if len(self.arglist) == 0:
            return self.functor._unparse()
        args = ', '.join([a._unparse() for a in self.arglist])
        if self.functor.name == '.tuple.':
            return "[%s]" % (args,)
        elif self.functor.name == '.attr.':
            return "%s: %s" % (self.arglist[0]._unparse(), self.arglist[1]._unparse())
        elif self.functor.name == '.bag.':
            return "{%s}" % (args,)
        elif len(self.arglist) == 1 and self.arglist[0].functor.name == '.bag.':
            return "%s%s" % (self.functor._unparse(), args)
        else:
            return "%s(%s)" % (self.functor._unparse(), args)



class TermLiteral(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.data == other.data

    def __repr__(self):
        return "TermLiteral(%r)" % (self.data,)

    def _unparse(self):
        if self.name == '.String.':
            return '"%s"' % self.data
        elif self.name == '.char.':
            return "'%s'" % self.data
        else:
            return str(self.data)



class Tag(object):
    def __init__(self, name):
        if name[0] == '':
            import pdb; pdb.set_trace()
        self.name = name

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.name == other.name

    def __repr__(self):
        return "Tag(%r)" % (self.name,)

    def _unparse(self):
        return self.name





## Functions called from grammar actions

def Character(char):
    return character(char)

def makeTag(nameSegs):
    return Tag('::'.join(nameSegs))

def prefixedTag(tagnameSegs):
    return makeTag([''] + tagnameSegs)

def tagString(string):
    return '"' + string + '"'

def emptyList():
    return []

def Term(functor, argList):
    if isinstance(functor, TermLiteral) and len(argList) > 0:
        raise ValueError("Term %s can't have both data and children" % (functor.name,))
    return _Term(functor, argList)

def numberType(n):
    if isinstance(n, float):
        return ".float64."
    elif isinstance(n, (long, int)):
        return ".int."
    raise ValueError("wtf")


def Tuple(args):
    return _Term(Tag(".tuple."), args)

def Bag(args):
    return _Term(Tag(".bag."), args)

def LabelledBag(f, arg):
    return _Term(f, [arg])

def Attr(k, v):
    return _Term(Tag(".attr."), [k, v])


BaseTermLParser = OMeta.makeGrammar(termLGrammar, globals(), "TermLParser")

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
