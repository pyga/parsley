from textwrap import dedent
from twisted.trial import unittest

from pymeta.builder import TreeBuilder, writePython

def dd(txt):
    return dedent(txt).strip()


class TreeBuilderTests(unittest.TestCase):
    """
    Tests for building an AST from a grammar.
    """


    def setUp(self):
        """
        Create a L{PythonBuilder}.
        """

        self.builder = TreeBuilder()


    def test_exactly(self):
        """
        Test generation of code for the 'exactly' pattern.
        """

        x = self.builder.exactly("x")
        self.assertEqual(writePython(x),
                         dd("""
                            _G_exactly_1 = self.exactly('x')
                            _G_exactly_1
                            """))


    def test_sequence(self):
        """
        Test generation of code for sequence patterns.
        """
        x = self.builder.exactly("x")
        y = self.builder.exactly("y")
        z = self.builder.sequence([x, y])
        self.assertEqual(writePython(z),
                         dd("""
                            _G_exactly_1 = self.exactly('x')
                            _G_exactly_2 = self.exactly('y')
                            _G_exactly_2
                            """))

    def test_apply(self):
        """
        Test generation of code for rule application.
        """

        x = self.builder.apply("foo", "main", "1", "2")
        self.assertEqual(writePython(x),
                         dd("""
                            _G_apply_1 = self.apply("foo", 1, 2)
                            _G_apply_1
                            """))




    def test_superApply(self):
        """
        Test generation of code for calling the superclass' implementation of
        the current rule.
        """

        x = self.builder.apply("super", "main", "1", "2")
        self.assertEqual(writePython(x),
                         dd("""
                            _G_apply_1 = self.superApply("main", 1, 2)
                            _G_apply_1
                            """))


    def test_many(self):
        """
        Test generation of code for matching zero or more instances of
        a pattern.
        """

        xs = self.builder.many(self.builder.exactly("x"))
        self.assertEqual(writePython(xs),
                         dd("""
                            def _G_many_1():
                                _G_exactly_1 = self.exactly('x')
                                return _G_exactly_1
                            _G_many_2 = self.many(_G_many_1)
                            _G_many_2
                            """))

    def test_many1(self):
        """
        Test generation of code for matching one or more instances of
        a pattern.
        """

        xs = self.builder.many1(self.builder.exactly("x"))
        self.assertEqual(writePython(xs),
                         dd("""
                            def _G_many1_1():
                                _G_exactly_1 = self.exactly('x')
                                return _G_exactly_1
                            _G_many1_2 = self.many(_G_many1_1, _G_many1_1())
                            _G_many1_2
                            """))

