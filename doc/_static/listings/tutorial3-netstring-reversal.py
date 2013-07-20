from twisted.internet.defer import Deferred
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.internet.task import react

from parsley import makeProtocol, stack


grammar = """
nonzeroDigit = digit:x ?(x != '0')
digits = <'0' | nonzeroDigit digit*>:i -> int(i)

netstring = digits:length ':' <anything{length}>:string ',' -> string

receiveNetstring = netstring:string -> receiver.netstringReceived(string)
"""


class NetstringReversalWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def sendNetstring(self, string):
        self.wrapped.sendNetstring(string[::-1])


class NetstringSender(object):
    def __init__(self, transport):
        self.transport = transport

    def sendNetstring(self, string):
        self.transport.write('%d:%s,' % (len(string), string))


class NetstringSplittingWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def netstringReceived(self, string):
        splitpoint = len(string) // 2
        self.wrapped.netstringFirstHalfReceived(string[:splitpoint])
        self.wrapped.netstringSecondHalfReceived(string[splitpoint:])

    def __getattr__(self, attr):
        return getattr(self.wrapped, attr)


class SplitNetstringReceiver(object):
    currentRule = 'receiveNetstring'

    def __init__(self, sender):
        self.sender = sender

    def prepareParsing(self, parser):
        pass

    def finishParsing(self, reason):
        pass

    def netstringFirstHalfReceived(self, string):
        self.sender.sendNetstring(string)

    def netstringSecondHalfReceived(self, string):
        pass

pass  # begin protocol definition
NetstringProtocol = makeProtocol(
    grammar,
    stack(NetstringReversalWrapper, NetstringSender),
    stack(NetstringSplittingWrapper, SplitNetstringReceiver))

class NetstringFactory(Factory):
    protocol = NetstringProtocol


def main(reactor):
    server = TCP4ServerEndpoint(reactor, 1234)
    d = server.listen(NetstringFactory())
    d.addCallback(lambda p: Deferred())  # listen forever
    return d


react(main, [])
