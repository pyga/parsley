"""
Public interface to OMeta, as well as the grammars used to compile grammar
definitions.
"""
import sys, string
from builder import PythonBuilder
from boot import BootOMetaGrammar
from runtime import OMetaBase, ParseError

class OMeta(OMetaBase):
    """
    Base class for grammar definitions.
    """
    metagrammarClass = BootOMetaGrammar
    def makeGrammar(cls, grammar, globals, name="Grammar"):
        """
        Define a new subclass with the rules in the given grammar.

        @param grammar: A string containing a PyMeta grammar.
        @param globals: A dict of names that should be accessible by this
        grammar.
        @param name: The name of the class to be generated.
        """
        g = cls.metagrammarClass(grammar)
        return g.parseGrammar(name, PythonBuilder, cls, globals)
    makeGrammar = classmethod(makeGrammar)

ometaGrammar = r"""
number ::= <spaces> ('-' <barenumber>:x => self.builder.exactly(-x)
                    |<barenumber>:x => self.builder.exactly(x))
barenumber ::= ('0' (('x'|'X') <hexdigit>*:hs => int(''.join(hs), 16)
                    |<octaldigit>*:ds => int('0'+''.join(ds), 8))
               |<digit>+:ds => int(''.join(ds)))
octaldigit ::= :x ?(x in string.octdigits) => x
hexdigit ::= :x ?(x in string.hexdigits) => x

escapedChar ::= '\\' ('n' => "\n"
                     |'r' => "\r"
                     |'t' => "\t"
                     |'b' => "\b"
                     |'f' => "\f"
                     |'"' => '"'
                     |'\'' => "'"
                     |'\\' => "\\")

character ::= <token "'"> (<escapedChar> | <anything>):c <token "'"> => self.builder.exactly(c)

string ::= <token '"'> (<escapedChar> | ~('"') <anything>)*:c <token '"'> => self.builder.exactly(''.join(c))

name ::= <letter>:x <letterOrDigit>*:xs !(xs.insert(0, x)) => ''.join(xs)

application ::= (<token '<'> <spaces> <name>:name
                  (' ' !(self.applicationArgs()):args
                     => self.builder.apply(name, self.name, *args)
                  |<token '>'>
                     => self.builder.apply(name, self.name)))

expr1 ::= (<application>
          |<ruleValue>
          |<semanticPredicate>
          |<semanticAction>
          |<number>
          |<character>
          |<string>
          |<token '('> <expr>:e <token ')'> => e
          |<token '['> <expr>:e <token ']'> => self.builder.listpattern(e))

expr2 ::= (<token '~'> (<token '~'> <expr2>:e => self.builder.lookahead(e)
                       |<expr2>:e => self.builder._not(e))
          |<expr1>)

expr3 ::= ((<expr2>:e ('*' => self.builder.many(e)
                      |'+' => self.builder.many1(e)
                      |'?' => self.builder.optional(e)
                      | => e)):r
           (':' <name>:n => self.builder.bind(r, n)
           | => r)
          |<token ':'> <name>:n
           => self.builder.bind(self.builder.apply("anything", self.name), n))

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
#don't be confused, emacs

class OMetaGrammar(OMeta.makeGrammar(ometaGrammar, globals())):
    """
    The base grammar for parsing grammar definitions.
    """
    def parseGrammar(self, name, builder, *args):
        """
        Entry point for converting a grammar to code (of some variety).

        @param name: The name for this grammar.

        @param builder: A class that implements the grammar-building interface
        (interface to be explicitly defined later)
        """
        self.builder = builder(name, self, *args)
        res = self.apply("grammar")
        try:
            x = self.input.head()
        except IndexError:
            pass
        else:
            x = repr(''.join(self.input.data[self.input.position:]))
            raise ParseError("Grammar parse failed. Leftover bits: %s" % (x,))
        return res


    def applicationArgs(self):
        """
        Collect rule arguments, a list of Python expressions separated by
        spaces.
        """
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
        """
        Find and generate code for a Python expression terminated by a close
        paren/brace or end of line.
        """
        expr, endchar = self.pythonExpr(endChars="\r\n)]")
        if str(endchar) in ")]":
            self.input = self.input.prev()
        return self.builder.compilePythonExpr(self.name, expr)

    def semanticActionExpr(self):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value is ignored.
        """
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.action(expr)

    def semanticPredicateExpr(self):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value determines the success of the pattern
        it's in.
        """
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.pred(expr)

OMeta.metagrammarClass = OMetaGrammar

nullOptimizationGrammar = """

opt ::= ( ["Apply" :ruleName :codeName [<anything>*:exprs]] => self.builder.apply(ruleName, codeName, *exprs)
        | ["Exactly" :expr] => self.builder.exactly(expr)
        | ["Many" <opt>:expr] => self.builder.many(expr)
        | ["Many1" <opt>:expr] => self.builder.many1(expr)
        | ["Optional" <opt>:expr] => self.builder.optional(expr)
        | ["Or" <opt>*:exprs] => self.builder._or(exprs)
        | ["And" <opt>*:exprs] => self.builder.sequence(exprs)
        | ["Not" <opt>:expr]  => self.builder._not(expr)
        | ["Lookahead" <opt>:expr] => self.builder.lookahead(expr)
        | ["Bind" :name <opt>:expr] => self.builder.bind(expr, name)
        | ["Predicate" <opt>:expr] => self.builder.pred(expr)
        | ["Action" <opt>:expr] => self.builder.action(expr)
        | ["Python" :name :code] => self.builder.compilePythonExpr(name, code)
        | ["List" <opt>:exprs] => self.builder.listpattern(exprs)
        )
grammar ::= ["Grammar" [<rulePair>*:rs]] => self.builder.makeGrammar(rs)
rulePair ::= [:name <opt>:rule] => (name, rule)

"""

NullOptimizer = OMeta.makeGrammar(nullOptimizationGrammar, {})
