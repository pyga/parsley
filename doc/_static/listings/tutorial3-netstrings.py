from twisted.internet.defer import Deferred
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.internet.task import react

from parsley import makeProtocol


grammar = """
nonzeroDigit = digit:x ?(x != '0')
digits = <'0' | nonzeroDigit digit*>:i -> int(i)

netstring = digits:length ':' <anything{length}>:string ',' -> string
receiveNetstring = netstring:string -> receiver.netstringReceived(string)
"""


class NetstringSender(object):
    def __init__(self, transport):
        self.transport = transport

    def sendNetstring(self, string):
        self.transport.write('%d:%s,' % (len(string), string))


class NetstringReceiver(object):
    currentRule = 'receiveNetstring'

    def __init__(self, sender):
        self.sender = sender

    def prepareParsing(self, parser):
        pass

    def finishParsing(self, reason):
        pass

    def netstringReceived(self, string):
        self.sender.sendNetstring(string)


NetstringProtocol = makeProtocol(
    grammar, NetstringSender, NetstringReceiver)


class NetstringFactory(Factory):
    protocol = NetstringProtocol


def main(reactor):
    server = TCP4ServerEndpoint(reactor, 1234)
    d = server.listen(NetstringFactory())
    d.addCallback(lambda p: Deferred())  # listen forever
    return d


react(main, [])
