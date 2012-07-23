# -*- test-case-name: ometa.test.test_pymeta -*-
"""
Public interface to OMeta, as well as the grammars used to compile grammar
definitions.
"""
import string
from StringIO import StringIO

from terml.parser import TermLParser

from ometa.boot import BootOMetaGrammar
from ometa.builder import TermActionPythonWriter, TermBuilder, moduleFromGrammar, TextWriter
from ometa.runtime import OMetaBase, OMetaGrammarBase, ParseError, EOFError


v1Grammar = r"""
hspace = ' ' | '\t' | ('#' (~vspace anything)*)
vspace = (token("\r\n") | '\r' | '\n')
number = spaces ('-' barenumber:x -> self.builder.exactly(-x)
                    |barenumber:x -> self.builder.exactly(x))
barenumber = '0' (('x'|'X') <hexdigit+>:hs -> int(hs, 16)
                    |<octaldigit+>:ds -> int(ds, 8))
               |<digit+>:ds -> int(ds)
octaldigit = :x ?(x in '01234567' ) -> x
hexdigit = :x ?(x in '0123456789ABCDEFabcdef') -> x

escapedChar = '\\' ('n' -> "\n"
                     |'r' -> "\r"
                     |'t' -> "\t"
                     |'b' -> "\b"
                     |'f' -> "\f"
                     |'"' -> '"'
                     |'\'' -> "'"
                     |'\\' -> "\\")

character = token("'") (escapedChar | anything):c token("'") -> self.builder.exactly(c)

string = token('"') (escapedChar | ~('"') anything)*:c token('"') -> self.builder.exactly(''.join(c))

name = <letter letterOrDigit*>
application = (token('<') spaces name:name
                  (' ' !(self.applicationArgs(finalChar='>')):args '>'
                     -> self.builder.apply(name, self.name, *args)
                  |token('>')
                     -> self.builder.apply(name, self.name)))

expr1 = (application
          |ruleValue
          |semanticPredicate
          |semanticAction
          |number
          |character
          |string
          |token('(') expr:e token(')') -> e
          |token('[') expr:e token(']') -> self.builder.listpattern(e))

expr2 = (token('~') (token('~') expr2:e -> self.builder.lookahead(e)
                       |expr2:e -> self.builder._not(e))
          |expr1)

expr3 = ((expr2:e ('*' -> self.builder.many(e)
                      |'+' -> self.builder.many1(e)
                      |'?' -> self.builder.optional(e)
                      | -> e)):r
           (':' name:n -> self.builder.bind(n, r)
           | -> r)
          |token(':') name:n
           -> self.builder.bind(n, self.builder.apply("anything", self.name)))

expr4 = expr3*:es -> self.builder.sequence(es)

expr = expr4:e (token('|') expr4)*:es
          -> self.builder._or([e] + es)

ruleValue = token("=>") -> self.ruleValueExpr(False)

semanticPredicate = token("?(") -> self.semanticPredicateExpr()

semanticAction = token("!(") -> self.semanticActionExpr()

ruleEnd = (hspace* vspace+) | end
rulePart :requiredName = (spaces name:n ?(n == requiredName)
                            !(setattr(self, "name", n))
                            expr4:args
                            (token("::=") expr:e ruleEnd
                               -> self.builder.sequence([args, e])
                            | ruleEnd -> args))
rule = (spaces ~~(name:n) rulePart(n):r
          (rulePart(n)+:rs -> self.builder.rule(n, self.builder._or([r] + rs))
          |                     -> self.builder.rule(n, r)))

grammar = rule*:rs spaces -> self.builder.makeGrammar(rs)
"""

v2Grammar = r"""
hspace  = (' ' | '\t')
vspace = (token("\r\n") | '\r' | '\n')
emptyline = hspace* vspace
indentation = emptyline* hspace+
noindentation = emptyline* ~~~hspace

number = spaces ('-' barenumber:x -> self.builder.exactly(-x)
                    |barenumber:x -> self.builder.exactly(x))
barenumber = '0' (('x'|'X') <hexdigit+>:hs -> int(hs, 16)
                    |<octaldigit+>:ds -> int(ds, 8))
               |<digit+>:ds -> int(ds)
octaldigit = :x ?(x in '01234567' ) -> x
hexdigit = :x ?(x in '0123456789ABCDEFabcdef') -> x

escapedChar = '\\' ('n' -> "\n"
                     |'r' -> "\r"
                     |'t' -> "\t"
                     |'b' -> "\b"
                     |'f' -> "\f"
                     |'"' -> '"'
                     |'\'' -> "'"
                     |'\\' -> "\\")

character = token("'") (escapedChar | anything):c token("'") -> self.builder.exactly(c)

string = token('"') (escapedChar | ~('"') anything)*:c token('"') -> self.builder.exactly(''.join(c))

name = <letter letterOrDigit*>

application = indentation? name:name
                  ('(' !(self.applicationArgs(finalChar=')')):args ')'
                    -> self.builder.apply(name, self.name, *args)
                  | -> self.builder.apply(name, self.name))

expr1 = application
          |ruleValue
          |semanticPredicate
          |semanticAction
          |number
          |character
          |string
          |token('(') expr:e token(')') -> e
          |token('<') expr:e token('>') -> self.builder.consumedBy(e)
          |token('[') expr:e token(']') -> self.builder.listpattern(e)

expr2 = (token('~') (token('~') expr2:e -> self.builder.lookahead(e)
                       |expr2:e -> self.builder._not(e)
          )
          |expr1)

expr3 = (expr2:e ('*' -> self.builder.many(e)
                      |'+' -> self.builder.many1(e)
                      |'?' -> self.builder.optional(e)
                      | -> e
)):r
           (':' name:n -> self.builder.bind(n, r)
           | -> r)
          |token(':') name:n
           -> self.builder.bind(n, self.builder.apply("anything", self.name))

expr4 = expr3*:es -> self.builder.sequence(es)

expr = expr4:e (token('|') expr4)*:es
          -> self.builder._or([e] + es)

ruleValue = token("->") -> self.ruleValueExpr(True)

semanticPredicate = token("?(") -> self.semanticPredicateExpr()

semanticAction = token("!(") -> self.semanticActionExpr()

ruleEnd = (hspace* vspace+) | end

rulePart :requiredName = noindentation name:n ?(n == requiredName)
                            !(setattr(self, "name", n))
                            expr4:args
                            (token("=") expr:e ruleEnd
                               -> self.builder.sequence([args, e])
                            | ruleEnd -> args)

rule = noindentation ~~(name:n) rulePart(n):r
          (rulePart(n)+:rs -> self.builder.rule(n, self.builder._or([r] + rs))
          |                -> self.builder.rule(n, r))

grammar = rule*:rs spaces -> self.builder.makeGrammar(rs)
"""
OMeta = BootOMetaGrammar.makeGrammar(v2Grammar, globals(), name='OMeta',
                                      superclass=OMetaGrammarBase)

OMeta1 = BootOMetaGrammar.makeGrammar(v1Grammar, globals(), name='OMeta1',
                                      superclass=OMetaGrammarBase)


termOMeta2Grammar = """
ruleValue = token("->") term:t -> self.builder.action(t)

semanticPredicate = token("?(") term:t token(")") -> self.builder.pred(t)

semanticAction = token("!(") term:t token(")") -> self.builder.action(t)

application = indentation? name:name ('(' term_arglist:args ')'
                    -> self.builder.apply(name, self.name, *args)
                  | -> self.builder.apply(name, self.name))
"""

class TermOMeta(BootOMetaGrammar.makeGrammar(
        termOMeta2Grammar,
        globals(), name='TermOMeta2', superclass=OMeta)):

    @classmethod
    def makeGrammar(cls, grammar, globals, name='Grammar', superclass=None):
        """
        Define a new parser class with the rules in the given grammar.

        @param grammar: A string containing a PyMeta grammar.
        @param globals: A dict of names that should be accessible by this
        grammar.
        @param name: The name of the class to be generated.
        @param superclass: The class the generated class is a child of.
        """
        g = cls(grammar)
        tree = g.parseGrammar(name, TermBuilder)
        return moduleFromGrammar(
            tree, name, superclass or OMetaBase,
            globals, writer=g.writeTerm)


    def writeTerm(self, term):
        f = StringIO()
        pw = TermActionPythonWriter(term)
        out = TextWriter(f)
        pw.output(out)
        return f.getvalue().strip()


    def rule_term(self):
        tp = TermLParser('')
        tp.input = self.input
        self.input.setMemo('term', None)
        val, err = tp.apply('term')
        self.input = tp.input
        return val, err

    def rule_term_arglist(self):
        tp = TermLParser('')
        tp.input = self.input
        val, err = tp.apply('argList')
        self.input = tp.input
        return val, err