import sys, string
from builder import AstBuilder
from boot import parseGrammar, HandyWrapper
from runtime import OMetaBase, ParseError

class _MetaOMeta(type):
    """
    There is probably some really good joke I could make about this class name
    but I'm not coming up with anything at the moment.
    """
    def __new__(metaclass, name, bases, methodDict):
        grammar = methodDict.get('__doc__', None)
        if grammar:
            rules = parseGrammar(grammar, name)
            rules.update(methodDict)
        else:
            methodDict['__ometa_rules__'] = {}
            rules = methodDict
        grammarClass = type.__new__(metaclass, name, bases, rules)
        grammarClass.globals = sys.modules[grammarClass.__module__].__dict__
        return grammarClass


class _OMetaCallWrapper(OMetaBase):
    def __getattr__(self, name):
        if name in self.__ometa_rules__:
            return lambda: self.apply(name)
        else:
            raise AttributeError

class OMeta(_OMetaCallWrapper):
    __metaclass__ = _MetaOMeta


class OMetaGrammar(OMeta):
    """
    number ::= <spaces> ('-' <barenumber>:x => self.builder.exactly(-x)
                        |<barenumber>:x => self.builder.exactly(x))
    barenumber ::= ('0' (('x'|'X') <hexdigit>*:hs => int(''.join(hs), 16)
                        |<octaldigit>*:ds => int('0'+''.join(ds), 8))
                   |<decdigit>+:ds => int(''.join(ds)))
    octaldigit ::= :x ?(x in string.octdigits) => x
    hexdigit ::= :x ?(x in string.hexdigits) => x
    decdigit ::= :x ?(x in string.digits) => x

    character ::= <token "'"> :c <token "'"> => self.builder.exactly(c)

    name ::= <letter>:x <letterOrDigit>*:xs !(xs.insert(0, x)) => ''.join(xs)

    application ::= (<token '<'> <spaces> <name>:name
                      (' ' !(self.applicationArgs()):args
                         => self.builder.apply(name, self.name, *args)
                      |<token '>'>
                         => self.builder.apply(name)))

    expr1 ::= (<application>
              |<ruleValue>
              |<semanticPredicate>
              |<semanticAction>
              |<number>
              |<character>
              |<token '('> <expr>:e <token ')'> => e
              |<token '['> <expr>:e <token ']'> => self.builder.listpattern(e))

    expr2 ::= (<token '~'> (<token '~'> <expr2>:e => self.builder.lookahead(e)
                           |<expr2>:e => self.builder._not(e))
              |<expr1>)

    expr3 ::= ((<expr2>:e (<token '*'> => self.builder.many(e)
                          |<token '+'> => self.builder.many1(e)
                          | => e)):r
               (':' <name>:n => self.builder.bind(r, n)
               | => r)
              |<token ':'> <name>:n
               => self.builder.bind(self.builder.apply("anything"), n))

    expr4 ::= <expr3>*:es => self.builder.sequence(es)

    expr ::= <expr4>:e (<token '|'> <expr4>)*:es !(es.insert(0, e))
              => self.builder._or(es)

    ruleValue ::= <token "=>"> => self.ruleValueExpr()

    semanticPredicate ::= <token "?("> => self.semanticPredicateExpr()

    semanticAction ::= <token "!("> => self.semanticActionExpr()

    rulePart :requiredName ::= (<spaces> <name>:n ?(n == requiredName)
                                !(setattr(self, "name", n))
                                <expr4>:args
                                (<token "::="> <expr>:e
                                   => self.builder.sequence([args, e])
                                |  => args))
    rule ::= (<spaces> ~~(<name>:n) <rulePart n>:r
              (<rulePart n>+:rs => (n, self.builder._or([r] + rs))
              |                     => (n, r)))

    grammar ::= <rule>*:rs <spaces> => self.builder.makeGrammar(rs)
    """

    def compile(self, name="<grammar>"):
        self.builder = AstBuilder(name, self)
        methodDict = self.apply("grammar")
        x = list(self.input)
        if x:
            try:
                x = repr(''.join(x))
            except TypeError:
                pass
            raise ParseError("Grammar parse failed. Leftover bits: %s" % (x,))
        grammarClass = type(name, (OMetaBase,), methodDict)
        return HandyWrapper(grammarClass)

    def applicationArgs(self):
        args = []
        while True:
            try:
                arg, endchar = self.pythonExpr(" >")
                if not arg:
                    break
                args.append(arg)
                if endchar == '>':
                    break
            except ParseError:
                break
        if args:
            return args
        else:
            raise ParseError()

    def ruleValueExpr(self):
        expr, endchar = self.pythonExpr(endChars="\r\n)]")
        if str(endchar) in ")]":
            self.input.prev()
        return self.builder.compilePythonExpr(self.name, expr)

    def semanticActionExpr(self):
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.action(expr)

    def semanticPredicateExpr(self):
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.pred(expr)

