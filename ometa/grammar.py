# -*- test-case-name: ometa.test.test_pymeta -*-
"""
Public interface to OMeta, as well as the grammars used to compile grammar
definitions.
"""
import string
from StringIO import StringIO

from terml.parser import TermLParser
from terml.nodes import termMaker as t
from ometa.boot import BootOMetaGrammar
from ometa.builder import TermActionPythonWriter, moduleFromGrammar, TextWriter
from ometa.runtime import OMetaBase, OMetaGrammarBase

v1Grammar = r"""
comment = '#' (~'\n' anything)*
hspace = ' ' | '\t' | comment
vspace = token("\r\n") | '\r' | '\n'
number = spaces !(self.startSpan()):s
                   ('-' barenumber:x -> t.Exactly(-x, span=self.span(s))
                    |barenumber:x -> t.Exactly(x, span=self.span(s)))
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

character = !(self.startSpan()):s token("'") (escapedChar | anything):c
            token("'") -> t.Exactly(c, span=self.span(s))

string = !(self.startSpan()):s token('"') (escapedChar | ~('"') anything)*:c
            token('"') -> t.Exactly(''.join(c))

name = <letter letterOrDigit*>
application = !(self.startSpan()):s (token('<') spaces name:name
                  (' ' !(self.applicationArgs(finalChar='>')):args '>'
                     -> t.Apply(name, self.rulename, args, span=self.span(s))
                  |token('>')
                     -> t.Apply(name, self.rulename, [], span=self.span(s))))

expr1 = (application
          |ruleValue
          |semanticPredicate
          |semanticAction
          |number
          |character
          |string
          |token('(') expr:e token(')') -> e
          |(!(self.startSpan()):s token('[') expr:e token(']')
              -> t.List(e, span=self.span(s))))

expr2 = (!(self.startSpan()):s token('~') (token('~') expr2:e
                                 -> t.Lookahead(e, span=self.span(s))
                                          |expr2:e
                                           -> t.Not(e, span=self.span(s)))
                              |expr1)

expr3 = !(self.startSpan()):s (
            (expr2:e !(self.startSpan()):s
              ('*' -> t.Many(e, span=self.span(s))
              |'+' -> t.Many1(e, span=self.span(s))
              |'?' -> t.Optional(e, span=self.span(s))
              | -> e)):r
           (':' name:n -> t.Bind(n, r, span=self.span(s))
           | -> r)
          | (!(self.startSpan()):s token(':') name:n
              -> t.Bind(n, t.Apply("anything", self.rulename, [],
                        span=self.span(s)))))

expr4 = !(self.startSpan()):s expr3*:es -> t.And(es, span=self.span(s))

expr = !(self.startSpan()):s expr4:e (token('|') expr4)*:es
          -> t.Or([e] + es, span=self.span(s))

ruleValue = !(self.startSpan()):s token("=>")
              -> self.ruleValueExpr(False, span=self.span(s))

semanticPredicate = !(self.startSpan()):s token("?(")
                      -> self.semanticPredicateExpr(span=self.span(s))

semanticAction = token("!(") -> self.semanticActionExpr()

ruleEnd = (hspace* vspace+) | end
rulePart :requiredName = (spaces name:n ?(n == requiredName)
                            !(setattr(self, "rulename", n))
                            expr4:args
                            (token("::=") expr:e ruleEnd
                               -> t.And([args, e])
                            | ruleEnd -> args))
rule = !(self.startSpan()):s (spaces ~~(name:n) rulePart(n):r
          (rulePart(n)+:rs -> t.Rule(n, t.Or([r] + rs), span=self.span(s))
          |                     -> t.Rule(n, r, span=self.span(s))))

grammar = rule*:rs spaces -> t.Grammar(self.name, rs)
"""

v2Grammar = r"""
comment = '#' (~'\n' anything)*
hspace = ' ' | '\t' | comment
vspace = token("\r\n") | '\r' | '\n'
emptyline = hspace* vspace
indentation = emptyline* hspace+
noindentation = emptyline* ~~~hspace

number = spaces !(self.startSpan()):s
               ('-' barenumber:x -> t.Exactly(-x, span=self.span(s))
                    |barenumber:x -> t.Exactly(x, span=self.span(s)))
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

character = !(self.startSpan()):s token("'") (escapedChar | anything):c
            token("'") -> t.Exactly(c, span=self.span(s))

string = !(self.startSpan()):s token('"') (escapedChar | ~('"') anything)*:c
         token('"') -> t.Exactly(''.join(c), span=self.span(s))

name = <letter letterOrDigit*>

application = indentation? !(self.startSpan()):s name:name
                  ('(' !(self.applicationArgs(finalChar=')')):args ')'
                    -> t.Apply(name, self.rulename, args, span=self.span(s))
                  | -> t.Apply(name, self.rulename, [], span=self.span(s)))

expr1 = application
          |ruleValue
          |semanticPredicate
          |semanticAction
          |number
          |character
          |string
          |token('(') expr:e token(')') -> e
          |!(self.startSpan()):s token('<') expr:e token('>')
             -> t.ConsumedBy(e, s=self.span(s))
          |!(self.startSpan()):s token('[') expr:e token(']')
             -> t.List(e, s=self.span(s))

expr2 = !(self.startSpan()):s (token('~') (token('~') expr2:e
                                           -> t.Lookahead(e, span=self.span(s))
                       |expr2:e -> t.Not(e, span=self.span(s))
          )
          |expr1)

repeatTimes = (barenumber:x -> int(x)) | name

expr3 = !(self.startSpan()):s (expr2:e
                      ('*' -> t.Many(e, span=self.span(s))
                      |'+' -> t.Many1(e, span=self.span(s))
                      |'?' -> t.Optional(e, span=self.span(s))
                      |'{' spaces repeatTimes:start spaces (
                      (',' spaces repeatTimes:end spaces '}'
                           -> t.Repeat(start, end, e, span=self.span(s)))
                         | spaces '}'
                           -> t.Repeat(start, start, e, span=self.span(s)))
                      | -> e
)):r
           (':' name:n -> t.Bind(n, r, span=self.span(s))
           | -> r)
          |token(':') name:n
           -> t.Bind(n, t.Apply("anything", self.rulename, []),
                     span=self.span(s))

expr4 = !(self.startSpan()):s expr3*:es -> t.And(es, span=self.span(s))

expr = !(self.startSpan()):s expr4:e (token('|') expr4)*:es
          -> t.Or([e] + es, span=self.span(s))

ruleValue = !(self.startSpan()):s token("->")
             -> self.ruleValueExpr(True, span=self.span(s))

semanticPredicate = !(self.startSpan()):s token("?(")
                    -> self.semanticPredicateExpr(span=self.span(s))

semanticAction = !(self.startSpan()):s token("!(")
                    -> self.semanticActionExpr(span=self.span(s))

ruleEnd = (hspace* vspace+) | end

rulePart :requiredName = noindentation name:n ?(n == requiredName)
                            !(setattr(self, "rulename", n))
                            expr4:args
                            (token("=") expr:e ruleEnd
                               -> t.And([args, e])
                            | ruleEnd -> args)

rule = noindentation ~~(name:n) !(self.startSpan()):s rulePart(n):r
          (rulePart(n)+:rs -> t.Rule(n, t.Or([r] + rs), span=self.span(s))
          |                -> t.Rule(n, r, span=self.span(s)))

grammar = rule*:rs spaces -> t.Grammar(self.name, rs)
"""
OMeta = BootOMetaGrammar.makeGrammar(v2Grammar, globals(), name='OMeta',
                                      superclass=OMetaGrammarBase)

OMeta1 = BootOMetaGrammar.makeGrammar(v1Grammar, globals(), name='OMeta1',
                                      superclass=OMetaGrammarBase)


termOMeta2Grammar = """
ruleValue = !(self.startSpan()):s token("->") term:tt
            -> t.Action(tt, span=self.span(s))

semanticPredicate = !(self.startSpan()):s token("?(") term:tt token(")")
                    -> t.Predicate(tt, span=self.span(s))

semanticAction = !(self.startSpan()):s token("!(") term:tt token(")")
                    -> t.Action(tt, span=self.span(s))

application = indentation? !(self.startSpan()):s name:name
                  ('(' term_arglist:args ')'
                    -> t.Apply(name, self.rulename, args, span=self.span(s))
                  | -> t.Apply(name, self.rulename, [], span=self.span(s)))
"""

class TermOMeta(BootOMetaGrammar.makeGrammar(
        termOMeta2Grammar,
        globals(), name='TermOMeta2', superclass=OMeta)):

    _writer = TermActionPythonWriter

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
        tree = g.parseGrammar(name)
        modname = "pymeta_grammar__" + name
        filename = "/pymeta_generated_code/" + modname + ".py"
        source = g.writeTerm(tree)
        return moduleFromGrammar(source, name, superclass or OMetaBase, globals,
                                 modname, filename)



    def writeTerm(self, term):
        f = StringIO()
        pw = self._writer(term)
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
