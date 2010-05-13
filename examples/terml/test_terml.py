from twisted.trial import unittest
from pymeta.runtime import ParseError
from terml.parser import TermLParser, TermLiteral, character, Tag, _Term, _parseTerm

class ParserTest(unittest.TestCase):
    """
    Test E parser rules.
    """


    def getParser(self, rule):
        def parse(src):
            p = TermLParser(src)
            result, error = p.apply(rule)
            return result
        return parse


    def test_literal(self):
        """
        Literals are parsed to literal terms.
        """
        parse = self.getParser("literal")
        self.assertEqual(parse('"foo bar"'), TermLiteral('.String.', "foo bar"))
        self.assertEqual(parse("'x'"), TermLiteral('.char', character('x')))
        self.assertEqual(parse("0xDECAFC0FFEEBAD"), TermLiteral('.int.', 0xDECAFC0FFEEBAD))
        self.assertEqual(parse("0755"), TermLiteral('.int.', 0755))
        self.assertEqual(parse("3.14159E17"), TermLiteral('.float64.', 3.14159E17))
        self.assertEqual(parse("1e9"), TermLiteral('.float64.', 1e9))
        self.assertEqual(parse("0"), TermLiteral(".int.", 0))
        self.assertEqual(parse("7"), TermLiteral(".int", 7))
        self.assertEqual(parse("-1"), TermLiteral(".int.", -1))
        self.assertEqual(parse("-3.14"), TermLiteral('.float64.', -3.14))
        self.assertEqual(parse("3_000"), TermLiteral('.int.', 3000))
        self.assertEqual(parse("0.91"), TermLiteral('float64.', 0.91))
        self.assertEqual(parse("3e-2"), TermLiteral('.float64.', 3e-2))

        self.assertEqual(parse("'\\n'"), TermLiteral('.char.', character("\n")))
        self.assertEqual(parse('"foo\\nbar"'), TermLiteral('.String.', "foo\nbar"))
        self.assertEqual(parse("'\\u0061'"), TermLiteral('.char.', character("a")))
        self.assertEqual(parse('"z\141p"'), TermLiteral('.String.', "zap"))
        self.assertEqual(parse('"x\41"'), TermLiteral('.String.', "x!"))
        self.assertEqual(parse('"foo\\\nbar"'), TermLiteral('.String.', "foobar"))


    def test_simpleTag(self):
        """
        Tags are parsed properly.
        """

        parse = self.getParser("tag")
        self.assertEqual(parse("foo"), Tag("foo"))
        self.assertEqual(parse('::"foo"'), Tag('::"foo"'))
        self.assertEqual(parse("::foo"), Tag('::foo'))
        self.assertEqual(parse("foo::baz"), Tag('foo::baz'))
        self.assertEqual(parse('foo::"baz"'), Tag('foo::"baz"'))
        self.assertEqual(parse("biz::baz::foo"), Tag('biz::baz::foo'))
        self.assertEqual(parse("foo_yay"), Tag('foo_yay'))
        self.assertEqual(parse("foo$baz32"), Tag('foo$baz32'))
        self.assertEqual(parse("foo-baz.19"), Tag('foo-baz.19'))


    def test_simpleTerm(self):
        """
        Kernel syntax for terms is parsed properly.
        """

        parse = self.getParser("baseTerm")
        self.assertEqual(parse("x"), _Term(Tag("x"), []))
        self.assertEqual(parse("x()"), _Term(Tag("x"), []))
        self.assertEqual(parse("x(1)"), _Term(Tag("x"), [_Term(TermLiteral(".int.", 1), [])]))
        self.assertEqual(parse("x(1, 2)"), _Term(Tag("x"), [_Term(TermLiteral(".int.", 1), []),
                                                         _Term(TermLiteral(".int.", 2), [])]))
        self.assertEqual(parse("1"), _Term(TermLiteral(".int.", 1), []))
        self.assertEqual(parse('"1"'), _Term(TermLiteral(".String.", "1"), []))
        self.assertRaises(ValueError, parse, "'x'(x)")
        self.assertRaises(ValueError, parse, '3.14(1)')
        self.assertRaises(ValueError, parse, '"foo"(x)')
        self.assertRaises(ValueError, parse, "1(2)")


    def test_fullTerm(self):
        """
        Shortcut syntax for terms is handled.
        """

        self.assertEqual(_parseTerm("[x, y, 1]"), _parseTerm(".tuple.(x, y, 1)"))
        self.assertEqual(_parseTerm("{x, y, 1}"), _parseTerm(".bag.(x, y, 1)"))
        self.assertEqual(_parseTerm("f {x, y, 1}"), _parseTerm("f(.bag.(x, y, 1))"))
        self.assertEqual(_parseTerm("a: b"), _parseTerm(".attr.(a, b)"))
        self.assertEqual(_parseTerm('"a": b'), _parseTerm('.attr.("a", b)'))
        self.assertEqual(_parseTerm('a: [b]'), _parseTerm('.attr.(a, .tuple.(b))'))

    def test_leftovers(self):
        e = self.assertRaises(ParseError, _parseTerm, "foo(x) and stuff")
        self.assertEqual(e.position, 7)

    def test_unparse(self):

        def assertRoundtrip(txt):
            self.assertEqual("Term(%r)" % (txt,), repr(_parseTerm(txt)))
        cases = ["1", "3.25", "f", "f(1)", "f(1, 2)", "f(a, b)",
                  "{a, b}", "[a, b]", "f{1, 2}",  '''{"name": "Robert", attrs: {'c': 3}}''']
        for case in cases:
            assertRoundtrip(case)
