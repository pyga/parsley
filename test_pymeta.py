from twisted.trial import unittest
from compiler import parse as python_parse
from pymeta import compile, ParseError, pyExpr, compileAstMethod
class OMetaTestCase(unittest.TestCase):
    """
    Tests of OMeta grammar compilation.
    """
    def test_literals(self):
        """
        Input matches can be made on literal characters.
        """
        g = compile("digit ::= '1'")
        self.assertEqual(g.digit("1"), "1")
        self.assertRaises(ParseError, g.digit, "4")


    def test_star(self):
        """
        Input matches can be made on zero or more repetitions of a pattern.
        """
        g = compile("xs ::= 'x'*")
        self.assertEqual(g.xs(""), "")
        self.assertEqual(g.xs("x"), "x")
        self.assertEqual(g.xs("xxxx"), "xxxx")
        self.assertRaises(ParseError, g.xs, "xy")


    def test_plus(self):
        """
        Input matches can be made on one or more repetitions of a pattern.
        """
        g = compile("xs ::= 'x'+")
        self.assertEqual(g.xs("x"), "x")
        self.assertEqual(g.xs("xxxx"), "xxxx")
        self.assertRaises(ParseError, g.xs, "xy")
        self.assertRaises(ParseError, g.xs, "")


    def test_sequencing(self):
        """
        Input matches can be made on a sequence of patterns.
        """
        g = compile("twelve ::= '1' '2';")
        self.assertEqual(g.twelve("12"), "12");
        self.assertRaises(ParseError, g.twelve, "1")


    def test_alternatives(self):
        """
        Input matches can be made on one of a set of alternatives.
        """
        g = compile("digit ::= '0' | '1' | '2'")
        self.assertEqual(g.digit("0"), "0")
        self.assertEqual(g.digit("1"), "1")
        self.assertEqual(g.digit("2"), "2")
        self.assertRaises(ParseError, g.digit, "3")


    def test_apply(self):
        """
        Other productions can be invoked from within a production.
        """
        g = compile("digit ::= '0' | '1'; bits ::= <digit>+")
        self.assertEqual(g.bits('0110110'), '0110110')

    def test_negate(self):
        """
        Input can be matched based on its failure to match a pattern.
        """
        g = compile("foo ::= ~'0';")
        self.assertEqual(g.foo("1"),True)
        self.assertRaises(ParseError, g.foo, "0")


    def test_action(self):
        """
        Productions can specify a Python expression that provides the result
        of the parse.
        """
        g = compile("foo ::= '1' | '2' => 7")
        self.assertEqual(g.foo('1'), 7)


    def test_binding(self):
        """
        The result of a parsing expression can be bound to a name.
        """
        g = compile("foo ::= '1':x => x * 2")
        self.assertEqual(g.foo("1"), 2)


    def test_predicate(self):
        """
        Python expressions can be used to determine the success or failure of a
        parse.
        """
        g = compile("""
              digit ::= '0' | '1'
              double_bits ::= <digit>:a <digit>:b ?(a == b) => int(b)
           """)
        self.assertEqual(g.double_bits("00"), 0)
        self.assertEqual(g.double_bits("11"), 1)
        self.assertRaises(ParseError, g.double_bits, "10")
        self.assertRaises(ParseError, g.double_bits, "01")


    def test_parens(self):
        """
        Parens can be used to group subpatterns.
        """
        g = compile("foo ::= 'a' ('b' | 'c')")
        self.assertEqual(g.foo("ab"), "ab")
        self.assertEqual(g.foo("ac"), "ac")


    def test_args(self):
        """
        Productions can take arguments.
        """
        g = compile("""
              digit ::= ('0' | '1' | '2'):d => int(d)
              foo :x ::= (?(x > 1) '9' | ?(x <= 1) '8'):d => int(d)
              baz ::= <digit>:a <foo a>
            """)
        self.assertEqual(g.foo("18"), [1, 8])
        self.assertEqual(g.foo("08"), [0, 8])
        self.assertEqual(g.foo("29"), [2, 9])
        self.assertRaises(ParseError, g.foo, "28")


    def test_patternMatch(self):
        """
        Productions can pattern-match on arguments.
        Also, multiple definitions of a rule can be done in sequence.
        """
        g = compile("""
              fact 0                       => 1
              fact :n ::= <fact (n - 1)>:m => n * m
           """)
        self.assertEqual(g.foo(3), 6)


    def test_listpattern(self):
        """
        Brackets can be used to match contents of lists.
        """
        g = compile("""
             interp ::= :x ?(x.isdigit())           => x
                      | [<interp>:x "+" <interp>:y] => x + y
                      | [<interp>:x "+" <interp>:y] => x * y
           """)
        self.assertEqual(g.interp([3, '+', [5, '*', 2]]), 13)



class PyExtractorTest(unittest.TestCase):
    """
    Tests for finding Python expressions in OMeta grammars.
    """
    def findInGrammar(self, expr):
        """
        C{pyExpr} can extract a single Python expression from a string,
        ignoring the text following it.
        """
        self.assertEqual(pyExpr(expr + "\nbaz ::= ...\n"), expr)
    def test_expressions(self):
        """
        C{pyExpr} can recognize various paired delimiters properly and include
        newlines in expressions where appropriate.
        """
        self.findInGrammar("x")
        self.findInGrammar("(x + 1)")
        self.findInGrammar("{x: (y)}")
        self.findInGrammar("x, '('")
        self.findInGrammar('x, "("')
        self.findInGrammar('x, """("""')
        self.findInGrammar('(x +\n 1)')
        self.findInGrammar('[x, "]",\n 1]')
        self.findInGrammar('{x: "]",\ny: "["}')



class CodeGenTest(unittest.TestCase):
    """
    Tests for creating Python functions and classes.
    """

    def test_method(self):
        """
        C{compileAstMethod} creates a function with a single 'self' arg that
        returns the value of the given expression.
        """
        expr = python_parse("self[1] + 3", mode="eval").asList()[0]
        f = compileAstMethod("f", expr)
        self.assertEqual(f([0, 2]), 5)
