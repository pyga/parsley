import unittest

from ometa.grammar import OMeta
from ometa.protocol import ParserProtocol


testingGrammarSource = """

someA = ('a' 'a') -> state('a')
someB = ('b' 'b') -> state('b')

initial = someA

"""
testGrammar = OMeta(testingGrammarSource).parseGrammar('testGrammar')


class SenderFactory(object):
    def __init__(self, transport):
        self.transport = transport


class StateFactory(object):
    def __init__(self, sender):
        self.sender = sender
        self.calls = []
        self.returnMap = {}
        self.lossReason = None

    def __call__(self, v):
        self.calls.append(v)
        return self.returnMap.get(v)

    def connectionLost(self, reason):
        self.lossReason = reason


class ParserProtocolTestCase(unittest.TestCase):
    def setUp(self):
        self.protocol = ParserProtocol(
            testGrammar, SenderFactory, StateFactory, {})

    def test_transportPassed(self):
        """The sender is passed the transport recieved by the protocol."""
        transport = object()
        self.protocol.makeConnection(transport)
        self.assertEqual(transport, self.protocol.sender.transport)

    def test_senderPassed(self):
        """The sender is passed to the state."""
        self.protocol.makeConnection(None)
        self.assertEqual(self.protocol.sender, self.protocol.state.sender)

    def test_basicParsing(self):
        """Rules can be parsed multiple times for the same effect."""
        self.protocol.makeConnection(None)
        self.protocol.dataReceived('aa')
        self.assertEqual(self.protocol.state.calls, ['a'])
        self.protocol.dataReceived('aa')
        self.assertEqual(self.protocol.state.calls, ['a', 'a'])

    def test_parsingChunks(self):
        """Any number of rules can be called from one dataRecived."""
        self.protocol.makeConnection(None)
        self.protocol.dataReceived('a')
        self.assertEqual(self.protocol.state.calls, [])
        self.protocol.dataReceived('aa')
        self.assertEqual(self.protocol.state.calls, ['a'])
        self.protocol.dataReceived('aaa')
        self.assertEqual(self.protocol.state.calls, ['a', 'a', 'a'])

    def test_ruleSwitching(self):
        """The rule being parsed can specify the next rule to be parsed."""
        self.protocol.makeConnection(None)
        self.protocol.state.returnMap.update(dict(a='someB', b='someA'))
        self.protocol.dataReceived('aa')
        self.assertEqual(self.protocol.state.calls, ['a'])
        self.protocol.dataReceived('bb')
        self.assertEqual(self.protocol.state.calls, ['a', 'b'])
        self.protocol.dataReceived('aa')
        self.assertEqual(self.protocol.state.calls, ['a', 'b', 'a'])

    def test_ruleSwitchingWithChunks(self):
        """Any number of rules can be called even during rule switching."""
        self.protocol.makeConnection(None)
        self.protocol.state.returnMap.update(dict(a='someB', b='someA'))
        self.protocol.dataReceived('a')
        self.assertEqual(self.protocol.state.calls, [])
        self.protocol.dataReceived('ab')
        self.assertEqual(self.protocol.state.calls, ['a'])
        self.protocol.dataReceived('baa')
        self.assertEqual(self.protocol.state.calls, ['a', 'b', 'a'])

    def test_connectionLoss(self):
        """The reason for connection loss is forwarded to the state."""
        self.protocol.makeConnection(None)
        reason = object()
        self.protocol.connectionLost(reason)
        self.assertEqual(self.protocol.state.lossReason, reason)
