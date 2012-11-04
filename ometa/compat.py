from ometa.runtime import OMetaGrammarBase
from ometa.boot import BootOMetaGrammar
from terml.nodes import termMaker as t

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
          |number:n !(self.isTree()) -> n
          |character
          |string
          |token('(') expr:e token(')') -> e
          |(!(self.startSpan()):s token('[') expr:e token(']') !(self.isTree())
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

grammar = rule*:rs spaces -> t.Grammar(self.name, self.tree, rs)
"""

OMeta1 = BootOMetaGrammar.makeGrammar(v1Grammar, globals(), name='OMeta1',
                                      superclass=OMetaGrammarBase)

