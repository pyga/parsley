from unittest import TestCase
from terml.twine import SourceSpan, Twine

class SourceSpanTests(TestCase):

    def test_creation(self):
        ss = SourceSpan("http://example.org/t", True, 1, 0, 1, 9)
        self.assertEqual(ss,
                         SourceSpan("http://example.org/t", True, 1, 0, 1, 9))
        self.assertEqual(list(ss), ["http://example.org/t", True, 1, 0, 1, 9])
        self.assertEqual(ss.uri, "http://example.org/t")
        self.assertEqual(ss.isOneToOne, True)
        self.assertEqual(ss.startLine, 1)
        self.assertEqual(ss.startCol, 0)
        self.assertEqual(ss.endLine, 1)
        self.assertEqual(ss.endCol, 9)


    def test_oneToOne(self):
        ss = SourceSpan("http://example.org/t", True, 1, 0, 1, 9)
        self.assertEqual(list(ss.notOneToOne()),
                         ["http://example.org/t", False, 1, 0, 1, 9])
        self.assertRaises(ValueError, SourceSpan,
                          "http://example.org/t", True, 1, 0, 2, 7)


class TwineTests(TestCase):

    def test_creation(self):
        ss = SourceSpan("http://example.org/t", True, 1, 0, 1, 9)
        t = Twine(u"foo baz")
        self.assertEqual(t.span, None)
        ss2 = ss.notOneToOne()
        t = Twine(u"foo baz", ss2)
        self.assertEqual(t.span, ss2)


    def test_asFrom(self):
        t = Twine(u"foo baz").asFrom("test.txt")
        self.assertEqual(t.span, SourceSpan("test.txt", True, 1, 0, 1, 6))

        self.assertEqual(Twine(u"abc\ndef").asFrom("test.txt").span,
                         SourceSpan("test.txt", False, 1, 0, 2, 2))

        self.assertEqual(Twine(u"abc\ndef").asFrom("test.txt", 3, 10).span,
                         SourceSpan("test.txt", False, 3, 10, 4, 2))

        self.assertEqual(Twine(u"abcdef").asFrom("test.txt").span,
                         SourceSpan("test.txt", True, 1, 0, 1, 5))

        self.assertEqual(Twine(u"abcdef\n").asFrom("test.txt").span,
                         SourceSpan("test.txt", True, 1, 0, 1, 6))

        self.assertEqual(Twine(u"abcdef\nghijkl").asFrom("test.txt").span,
                         SourceSpan("test.txt", False, 1, 0, 2, 5))

        self.assertEqual(Twine(u"abcdef\nghijkl").asFrom("test.txt")[:6].span,
                         SourceSpan("test.txt", True, 1, 0, 1, 5))

        self.assertEqual(Twine(u"").asFrom("test.txt").span, None)

        self.assertEqual(Twine(u"\n").asFrom("test.txt").span,
                         SourceSpan("test.txt", True, 1, 0, 1, 0))

        self.assertEqual(Twine(u"\n\n").asFrom("test.txt").span,
                         SourceSpan("test.txt", False, 1, 0, 2, 0))

        self.assertEqual(Twine(u"abcdef\n\n").asFrom("test.txt").span,
                         SourceSpan("test.txt", False, 1, 0, 2, 0))

        self.assertEqual(Twine(u"abcdef\ng\n").asFrom("test.txt").span,
                         SourceSpan("test.txt", False, 1, 0, 2, 1))

        self.assertEqual(Twine(u"abcdef\ng").asFrom("test.txt").span,
                         SourceSpan("test.txt", False, 1, 0, 2, 0))


    def test_slice(self):
        t = Twine(u"abcdef").asFrom("foo:bar")
        self.assertEqual(t[1], u"b")
        self.assertEqual(t[1].span, SourceSpan("foo:bar", True, 1, 1, 1, 1))
        self.assertEqual(t[:3], u"abc")
        self.assertEqual(t[:3].span,
                         SourceSpan("foo:bar", True, 1, 0, 1, 2))
        self.assertEqual(list(t), list(u"abcdef"))
        t = Twine(u"abc\ndef\n\nghij\n\n").asFrom("foo:bar")

        self.assertEqual(t[:3].span,
                         SourceSpan("foo:bar", True, 1, 0, 1, 2))
        self.assertEqual(t[2:6].span,
                         SourceSpan("foo:bar", False, 1, 2, 2, 1))
        self.assertEqual(t[2].span,
                         SourceSpan("foo:bar", True, 1, 2, 1, 2))
        self.assertEqual(t[14].span,
                         SourceSpan("foo:bar", True, 5, 0, 5, 0))
        self.assertEqual(t[-1].span,
                         SourceSpan("foo:bar", True, 5, 0, 5, 0))


    def test_split(self):
        t = Twine(u"abc\ndef\n\nghij\n\n").asFrom("foo:bar")
        self.assertEqual([x.span for x in t.split('\n')],
                         [SourceSpan("foo:bar", True, 1, 0, 1, 2),
                          SourceSpan("foo:bar", True, 2, 0, 2, 2),
                          None,
                          SourceSpan("foo:bar", True, 4, 0, 4, 3),
                          None,
                          None])


    def test_rsplit(self):
        t = Twine(u"abc\ndef\n\nghij\n\n").asFrom("foo:bar")
        self.assertEqual([x.span for x in t.rsplit('\n')],
                         [SourceSpan("foo:bar", True, 1, 0, 1, 2),
                          SourceSpan("foo:bar", True, 2, 0, 2, 2),
                          None,
                          SourceSpan("foo:bar", True, 4, 0, 4, 3),
                          None,
                          None])


    def test_concat(self):
        t1 = Twine(u"foo ", SourceSpan("foo:bar", True, 1, 0, 1, 3))
        t2 = Twine(u"baz", SourceSpan("foo:bar", True, 1, 3, 1, 5))
        self.assertEqual((t1 + t2).span,
                         SourceSpan("foo:bar", True, 1, 0, 1, 5))

        self.assertEqual((t1 + t2).parts,
                         (t1, t2))

        t1 = Twine(u"foo\nbaz").asFrom("foo:bar")
        t2 = Twine(u" boz").asFrom("foo:bar", 1, 6)
        self.assertEqual((t1 + t2).parts, ("foo\n", "baz", " boz"))


    def test_eq(self):
        t1 = Twine(u"foo ", SourceSpan("foo:bar", True, 1, 0, 1, 3))
        self.assertEqual(t1,
                         Twine(u"foo ", SourceSpan("foo:bar", True, 1, 0, 1, 3)))
        self.assertEqual(t1, u"foo ")

        t1 = Twine(u"9ab\ncdefg").asFrom("foo:bar")
        self.assertEqual(t1,
                         Twine(u"9ab\ncdefg"))
        self.assertEqual(t1, u"9ab\ncdefg")


    def test_join(self):
        ts = Twine(u'one two three').asFrom("foo:bar")
        words = ts.split(u' ')
        t = Twine(u', ').join(words)
        self.assertEqual(t.span, None)
        self.assertEqual(t.parts,
                         (u'one', u', ', u'two', u', ', u'three'))
        self.assertEqual(t.sourceMap,
                         (((0, 3), SourceSpan("foo:bar", True, 1, 0, 1, 2)),
                          ((5, 8), SourceSpan("foo:bar", True, 1, 4, 1, 6)),
                          ((10, 15), SourceSpan("foo:bar", True, 1, 8, 1, 12))))


    def test_replace(self):
        t = Twine(u'one two three').asFrom("foo:bar")
        t2 = t.replace(u'two', u'eleventy')
        self.assertEqual(t2.parts, (u'one ', u'eleventy', u' three'))
        self.assertEqual(t2.span, SourceSpan("foo:bar", False, 1, 0, 1, 12))
        self.assertEqual(t2.sourceMap,
                         (((0, 4), SourceSpan("foo:bar", True, 1, 0, 1, 3)),
                          ((4, 12), SourceSpan("foo:bar", False, 1, 4, 1, 6)),
                          ((12, 18), SourceSpan("foo:bar", True, 1, 7, 1, 12))))




#    def test_format(self):
#        pass

#    def test_mod(self):
#        pass

