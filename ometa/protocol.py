from twisted.internet.protocol import Protocol
from twisted.python.failure import Failure

from ometa.tube import TrampolinedParser


class ParserProtocol(Protocol):
    """
    A Twisted ``Protocol`` subclass for parsing stream protocols.
    """


    def __init__(self, grammar, senderFactory, receiverFactory, bindings):
        """
        Initialize the parser.

        :param grammar: An OMeta grammar to use for parsing.
        :param senderFactory: A unary callable that returns a sender given a
                              transport.
        :param receiverFactory: A unary callable that returns a receiver given
                                a sender.
        :param bindings: A dict of additional globals for the grammar rules.
        """

        self.grammar = grammar
        self.bindings = dict(bindings)
        self.senderFactory = senderFactory
        self.receiverFactory = receiverFactory
        self.disconnecting = False

    def connectionMade(self):
        """
        Start parsing, since the connection has been established.
        """

        self.sender = self.senderFactory(self.transport)
        self.receiver = self.receiverFactory(self.sender)
        self.receiver.prepareParsing(self)
        self.parser = TrampolinedParser(
            self.grammar, self.receiver, self.bindings)

    def dataReceived(self, data):
        """
        Receive and parse some data.

        :param data: A ``str`` from Twisted.
        """

        if self.disconnecting:
            return

        try:
            self.parser.receive(data)
        except Exception:
            self.connectionLost(Failure())
            self.transport.abortConnection()
            return

    def connectionLost(self, reason):
        """
        Stop parsing, since the connection has been lost.

        :param reason: A ``Failure`` instance from Twisted.
        """

        if self.disconnecting:
            return
        self.receiver.finishParsing(reason)
        self.disconnecting = True
