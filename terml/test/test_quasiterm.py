
from unittest import TestCase
from terml.parser import parseTerm as term
from terml.quasiterm import quasiterm

class QuasiTermMatchTests(TestCase):

    def test_basic(self):
        x = quasiterm("foo($x, $y)").substitute({"x": 1, "y": term("baz")})
        self.assertEqual(x, term("foo(1, baz)"))
        y = quasiterm("foo($0, ${1})").substitute([1, term("baz")])
        self.assertEqual(y, term("foo(1, baz)"))


    def test_withArgs(self):
        x = quasiterm("$x(3)").substitute({"x": term("foo")})
        self.assertEqual(x, term("foo(3)"))
        self.assertRaises(TypeError, quasiterm("$x(3)").substitute,
                          {"x": term("foo(3)")})

    # def test_lessgreedy(self):

    #     result = quasiterm("[@x*, @y, @z]").match(term("[4, 5, 6, 7, 8]"))
    #     self.assertEqual(result, {"x": [term("4"), term("5"), term("6")], "y": term("7"),
    #                               "z": term("8")})
