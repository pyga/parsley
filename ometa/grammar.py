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

v2Grammar = r"""
comment = '#' (~'\n' anything)*
hspace = ' ' | '\t' | comment
vspace = token("\r\n") | '\r' | '\n'
emptyline = hspace* vspace
indentation = emptyline* hspace+
noindentation = emptyline* ~~~hspace

number = spaces
               ('-' barenumber:x  -> t.Exactly(-x)
                    |barenumber:x -> t.Exactly(x))
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
                     |'x' <hexdigit hexdigit>:d -> chr(int(d, 16))
                     |'\\' -> "\\")

character = token("'") (~'\'' (escapedChar | anything))+:c
            token("'") -> t.Exactly(''.join(c))

string = token('"') (escapedChar | ~('"') anything)*:c
         token('"') -> t.Token(''.join(c))

name = <letter letterOrDigit*>

application = indentation? name:name
                  ('(' !(self.applicationArgs(finalChar=')')):args ')'
                    -> t.Apply(name, self.rulename, args)
                  | -> t.Apply(name, self.rulename, []))

expr1 = application
          |ruleValue
          |semanticPredicate
          |semanticAction
          |number:n !(self.isTree()) -> n
          |character
          |string
          |token('(') expr:e token(')') -> e
          |token('<') expr:e token('>')
             -> t.ConsumedBy(e)
          |token('[') expr:e token(']') !(self.isTree())
             -> t.List(e)

expr2 = (token('~') (token('~') expr2:e -> t.Lookahead(e)
                    |           expr2:e -> t.Not(e)
                    )
        |expr1)

repeatTimes = (barenumber:x -> int(x)) | name

expr3 = (expr2:e
                      ('*' -> t.Many(e)
                      |'+' -> t.Many1(e)
                      |'?' -> t.Optional(e)
                      |'{' spaces repeatTimes:start spaces (
                      (',' spaces repeatTimes:end spaces '}'
                           -> t.Repeat(start, end, e))
                         | spaces '}'
                           -> t.Repeat(start, start, e))
                      | -> e
)):r
           (':' name:n -> t.Bind(n, r)
           | -> r)
          |token(':') name:n
          -> t.Bind(n, t.Apply("anything", self.rulename, []))

expr4 = expr3*:es -> t.And(es)

expr = expr4:e (token('|') expr4)*:es
          -> t.Or([e] + es)

ruleValue = token("->") -> self.ruleValueExpr(True)

semanticPredicate = token("?(") -> self.semanticPredicateExpr()

semanticAction = token("!(") -> self.semanticActionExpr()

ruleEnd = (hspace* vspace+) | end

rulePart :requiredName = noindentation name:n ?(n == requiredName)
                            !(setattr(self, "rulename", n))
                            expr4:args
                            (token("=") expr:e ruleEnd
                               -> t.And([args, e])
                            | ruleEnd -> args)

rule = noindentation ~~(name:n) rulePart(n)+:rs -> t.Rule(n, t.Or(rs))


grammar = rule*:rs spaces -> t.Grammar(self.name, self.tree, rs)
"""

OMeta = BootOMetaGrammar.makeGrammar(v2Grammar, globals(), name='OMeta',
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


treeTransformerGrammar = r"""
termPattern = indentation? name:name ?(name[0] in string.uppercase)
              '(' expr:patts ')' -> t.TermPattern(name, patts)

subtransform = "@" name:n -> t.Bind(n, t.Apply('transform', self.rulename, []))

expr1 = termPattern
       |subtransform
       |application
       |ruleValue
       |semanticPredicate
       |semanticAction
       |number:n !(self.isTree()) -> n
       |character
       |string
       |token('(') expr:e token(')') -> e
       |token('[') expr:e token(']') -> t.TermPattern(".tuple.", e)


rule = noindentation ~~(name:n) (termRulePart(n)+:rs | rulePart(n)+:rs)  -> t.Rule(n, t.Or(rs))

termRulePart :requiredName = noindentation !(setattr(self, "rulename", requiredName)) 
                             termPattern:t ?(t.tag.name == requiredName) expr4:tail -> t.And([t, tail])
"""

TreeTransformerGrammar = BootOMetaGrammar.makeGrammar(
    treeTransformerGrammar, globals(), name='TreeTransformer',
    superclass=OMeta)
