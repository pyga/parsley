
from twisted.trial import unittest
from pymeta.runtime import OMetaBase, ParseError, expected

class RuntimeTests(unittest.TestCase):
    """
    Tests for L{pymeta.runtime}.
    """

    def test_anything(self):
        """
        L{OMetaBase.rule_anything} returns each item from the input along with its position.
        """

        data = "foo"
        o = OMetaBase(data)

        for i, c in enumerate(data):
            self.assertEqual((c, i), o.rule_anything())


    def test_exactly(self):
        """
        L{OMetaBase.rule_exactly} returns the requested item from the input
        string along with its position, if it's there.
        """

        data = "foo"
        o = OMetaBase(data)
        self.assertEqual(o.rule_exactly("f"), ("f", 0))

    def test_exactlyFail(self):
        """
        L{OMetaBase.rule_exactly} raises L{ParseError} when the requested item
        doesn't match the input. The error contains info on what was expected
        and the position.
        """

        data = "foo"
        o = OMetaBase(data)
        e = self.assertRaises(ParseError, o.rule_exactly, "g")
        self.assertEquals(e.error, expected("g"))
        self.assertEquals(e.position, 0)



    def test_token(self):
        """
        L{OMetaBase.rule_token} matches all the characters in the given string
        plus any preceding whitespace.
        """

        data = "  foo bar"
        o = OMetaBase(data)
        v, e = o.rule_token("foo")
        self.assertEqual(v, "foo")
        self.assertEqual(e, 4)
        v, e = o.rule_token("bar")
        self.assertEqual(v, "bar")
        self.assertEqual(e, 8)


    def test_many(self):
        """
        C{OMetaBase.many} returns a list of parsed values and the error that
        caused the end of the loop.
        """

        data = "ooops"
        o  = OMetaBase(data)
        self.assertEqual(o.many(lambda: o.rule_exactly('o')), (['o'] * 3, ParseError(3, expected('o'))))


    def test_or(self):
        """
        C{OMetaBase._or} returns the result of the first of its arguments to succeed.
        """

        data = "a"

        o = OMetaBase(data)
        called = [False, False, False]
        targets = ['b', 'a', 'c']
        matchers = []
        for i, m in enumerate(targets):
            def match(i=i, m=m):
                called[i] = True
                return o.exactly(m)
            matchers.append(match)

        v, e = o._or(matchers)
        self.assertEqual(called, [True, True, False])
        self.assertEqual(v, 'a')
        self.assertEqual(e, 0)
