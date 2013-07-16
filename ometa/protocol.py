from twisted.internet.protocol import Protocol
from twisted.python.failure import Failure

from ometa.tube import TrampolinedParser


class ParserProtocol(Protocol):
    def __init__(self, grammar, senderFactory, receiverFactory, bindings):
        self.grammar = grammar
        self.bindings = dict(bindings)
        self.senderFactory = senderFactory
        self.receiverFactory = receiverFactory
        self.disconnecting = False

    def connectionMade(self):
        self.sender = self.senderFactory(self.transport)
        self.receiver = self.receiverFactory(self.sender)
        self.receiver.prepareParsing()
        self.parser = TrampolinedParser(
            self.grammar, self.receiver, self.bindings)

    def dataReceived(self, data):
        if self.disconnecting:
            return

        try:
            self.parser.receive(data)
        except Exception:
            self.connectionLost(Failure())
            self.transport.abortConnection()
            return

    def connectionLost(self, reason):
        if self.disconnecting:
            return
        self.receiver.finishParsing(reason)
        self.disconnecting = True
