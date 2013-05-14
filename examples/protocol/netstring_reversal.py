from twisted.internet.defer import Deferred
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import ServerFactory
from twisted.internet.task import react

from parsley import makeProtocol
from netstrings import grammar, NetstringSender


class NetstringReverserState(object):
    def __init__(self, sender, parser):
        self.sender = sender

    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def netstringReceived(self, string):
        self.sender.sendNetstring(string[::-1])


NetstringReverser = makeProtocol(
    grammar, NetstringSender, NetstringReverserState)


class NetstringReverserFactory(ServerFactory):
    protocol = NetstringReverser


def main(reactor):
    server = TCP4ServerEndpoint(reactor, 1234)
    d = server.listen(NetstringReverserFactory())
    d.addCallback(lambda p: Deferred())
    return d

react(main, [])
