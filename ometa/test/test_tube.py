from __future__ import absolute_import

import io
from StringIO import StringIO

from twisted.trial import unittest
from twisted.python.compat import iterbytes


from ometa.grammar import OMeta
from ometa.tube import iterGrammar, TrampolinedParser


class TrampolinedReceiver():
    """
    Receive and store the passed in data.
    """

    currentRule = 'initial'

    def __init__(self):
        self.received = []

    def receive(self, data):
        self.received.append(data)


class TrampolinedParserTestCase(unittest.SynchronousTestCase):
    """
    Tests for L{ometa.tube.TrampolinedParser}
    """

    def _parseGrammar(self, grammar, name="Grammar"):
        return OMeta(grammar).parseGrammar(name)

    def setUp(self):
        _grammar =  r"""
            delimiter = '\r\n'
            initial = <(~delimiter anything)*>:val delimiter -> receiver.receive(val)
            witharg :arg1 :arg2 = <(~delimiter anything)*>:a delimiter -> receiver.receive(arg1+arg2+a)
        """
        self.grammar = self._parseGrammar(_grammar)

    def test_dataNotFullyReceived(self):
        """
        Since the initial rule inside the grammar is not matched, the receiver
        shouldn't receive any byte.
        """
        receiver = TrampolinedReceiver()
        trampolinedParser = TrampolinedParser(self.grammar, receiver, {})
        buf = b'foobarandnotreachdelimiter'
        for c in iterbytes(buf):
            trampolinedParser.receive(c)
        self.assertEqual(receiver.received, [])


    def test_dataFullyReceived(self):
        """
        The receiver should receive the data according to the grammar.
        """
        receiver = TrampolinedReceiver()
        trampolinedParser = TrampolinedParser(self.grammar, receiver, {})
        buf = b'\r\n'.join((b'foo', b'bar', b'foo', b'bar'))
        for c in iterbytes(buf):
            trampolinedParser.receive(c)
        self.assertEqual(receiver.received, [b'foo', b'bar', b'foo'])
        trampolinedParser.receive('\r\n')
        self.assertEqual(receiver.received, [b'foo', b'bar', b'foo', b'bar'])


    def test_bindings(self):
        """
        The passed-in bindings should be accessible inside the grammar.
        """
        receiver = TrampolinedReceiver()
        grammar = r"""
            initial = digit:d (-> int(d)+SMALL_INT):val -> receiver.receive(val)
        """
        bindings = {'SMALL_INT': 3}
        TrampolinedParser(self._parseGrammar(grammar), receiver, bindings).receive('0')
        self.assertEqual(receiver.received, [3])


    def test_currentRuleWithArgs(self):
        """
        TrampolinedParser should be able to invoke curruent rule with args.
        """
        receiver = TrampolinedReceiver()
        receiver.currentRule = "witharg", "nice ", "day"
        trampolinedParser = TrampolinedParser(self.grammar, receiver, {})
        buf = b' oh yes\r\n'
        for c in iterbytes(buf):
            trampolinedParser.receive(c)
        self.assertEqual(receiver.received, ["nice day oh yes"])



class TestIterGrammmar(unittest.SynchronousTestCase):
    """
    Tests for L{ometa.tube.iterGrammar}.
    """

    def makeGrammar(self):
        grammar =  r"""
            delimiter = ':'
            initial = <(~delimiter anything)*>:val delimiter? -> val
        """
        return OMeta(grammar).parseGrammar('Grammar')


    def test_wholeThing(self):
        """
        iterGrammar repeatedly applies a rule, returning matches until the
        input stream is exhausted.
        """
        grammar = self.makeGrammar()
        input_data = 'foo:bar:baz:'
        self.assertEqual(
            ['foo', 'bar', 'baz'],
            list(iterGrammar(grammar, 'initial', StringIO(input_data))))


    def test_byteAtATime(self):
        """
        iterGrammar properly handles data that comes in slowly, only yielding
        when a rule is finally matched.
        """
        grammar = self.makeGrammar()
        input_data = 'foo:bar:baz:'
        stream = io.BufferedReader(io.BytesIO(input_data), 1)
        self.assertEqual(
            ['foo', 'bar', 'baz'],
            list(iterGrammar(grammar, 'initial', stream)))


    def test_optionalBehaviour(self):
        """
        If streamEndsGrammar=True is passed to iterGrammar, it will tell the
        grammar to expect no more input after the stream is exhausted.
        """
        grammar = self.makeGrammar()
        input_data = 'foo:bar:baz:qux'
        stream = io.BufferedReader(io.BytesIO(input_data), 5)
        self.assertEqual(
            ['foo', 'bar', 'baz', 'qux'],
            list(iterGrammar(grammar, 'initial', stream,
                             streamEndsGrammar=True)))


    def test_actuallyIterates(self):
        """
        iterGrammar returns an iterator that implements the standard iter()
        interface.
        """
        grammar = self.makeGrammar()
        input_data = 'foo:bar:baz:'
        output = iterGrammar(grammar, 'initial', StringIO(input_data))
        self.assertEqual('foo', output.next())
        self.assertEqual('bar', output.next())
        self.assertEqual('baz', output.next())
        self.assertRaises(StopIteration, output.next)
