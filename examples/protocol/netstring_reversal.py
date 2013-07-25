from twisted.internet.defer import Deferred
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import ServerFactory
from twisted.internet.task import react

from parsley import makeProtocol
from netstrings import grammar, NetstringSender


class NetstringReverserReceiver(object):
    currentRule = 'receiveNetstring'

    def __init__(self, sender):
        self.sender = sender

    def prepareParsing(self, parser):
        pass

    def finishParsing(self, reason):
        pass

    def netstringReceived(self, string):
        self.sender.sendNetstring(string[::-1])


NetstringReverser = makeProtocol(
    grammar, NetstringSender, NetstringReverserReceiver)


class NetstringReverserFactory(ServerFactory):
    protocol = NetstringReverser


def main(reactor):
    server = TCP4ServerEndpoint(reactor, 1234)
    d = server.listen(NetstringReverserFactory())
    d.addCallback(lambda p: Deferred())
    return d

react(main, [])
