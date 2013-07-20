from twisted.test.proto_helpers import StringTransport

import parsley
import pytest
import netstrings

netstringGrammar = parsley.makeGrammar(netstrings.grammar, {})

def stringParserFromRule(rule):
    def parseString(s):
        return getattr(netstringGrammar(s), rule)()
    return parseString

def test_digits_parsing():
    parse = stringParserFromRule('digits')

    assert parse('0') == 0
    assert parse('1') == 1
    assert parse('1234567890') == 1234567890
    with pytest.raises(parsley.ParseError):
        parse('01')
    with pytest.raises(parsley.ParseError):
        parse('0001')

def test_netstring_parsing():
    parse = stringParserFromRule('netstring')

    assert parse('0:,') == ''
    assert parse('1:x,') == 'x'
    assert parse('10:abcdefghij,') == 'abcdefghij'


def build_testing_sender():
    transport = StringTransport()
    sender = netstrings.NetstringSender(transport)
    return sender, transport

def test_sending_empty_netstring():
    sender, transport = build_testing_sender()
    sender.sendNetstring('')
    assert transport.value() == '0:,'

def test_sending_one_netstring():
    sender, transport = build_testing_sender()
    sender.sendNetstring('foobar')
    assert transport.value() == '6:foobar,'

def test_sending_two_netstrings():
    sender, transport = build_testing_sender()
    sender.sendNetstring('spam')
    sender.sendNetstring('egggs')
    assert transport.value() == '4:spam,5:egggs,'


class FakeReceiver(object):
    currentRule = 'receiveNetstring'

    def __init__(self, sender):
        self.sender = sender
        self.netstrings = []
        self.connected = False
        self.lossReason = None

    def netstringReceived(self, s):
        self.netstrings.append(s)

    def prepareParsing(self, parser):
        self.connected = True

    def finishParsing(self, reason):
        self.lossReason = reason

TestingNetstringProtocol = parsley.makeProtocol(
    netstrings.grammar, netstrings.NetstringSender, FakeReceiver)

def build_testing_protocol():
    protocol = TestingNetstringProtocol()
    transport = StringTransport()
    protocol.makeConnection(transport)
    return protocol, transport

def test_receiving_empty_netstring():
    protocol, transport = build_testing_protocol()
    protocol.dataReceived('0:,')
    assert protocol.receiver.netstrings == ['']

def test_receiving_one_netstring_by_byte():
    protocol, transport = build_testing_protocol()
    for c in '4:spam,':
        protocol.dataReceived(c)
    assert protocol.receiver.netstrings == ['spam']

def test_receiving_two_netstrings_by_byte():
    protocol, transport = build_testing_protocol()
    for c in '4:spam,4:eggs,':
        protocol.dataReceived(c)
    assert protocol.receiver.netstrings == ['spam', 'eggs']

def test_receiving_two_netstrings_in_chunks():
    protocol, transport = build_testing_protocol()
    for c in ['4:', 'spa', 'm,4', ':eg', 'gs,']:
        protocol.dataReceived(c)
    assert protocol.receiver.netstrings == ['spam', 'eggs']

def test_receiving_two_netstrings_at_once():
    protocol, transport = build_testing_protocol()
    protocol.dataReceived('4:spam,4:eggs,')
    assert protocol.receiver.netstrings == ['spam', 'eggs']

def test_establishing_connection():
    assert not FakeReceiver(None).connected
    protocol, transport = build_testing_protocol()
    assert protocol.receiver.connected

def test_losing_connection():
    protocol, transport = build_testing_protocol()
    reason = object()
    protocol.connectionLost(reason)
    assert protocol.receiver.lossReason == reason
