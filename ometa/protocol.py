from twisted.internet.protocol import Protocol
from twisted.python.failure import Failure

from ometa.interp import TrampolinedGrammarInterpreter, _feed_me

class ParserProtocol(Protocol):
    currentRule = 'initial'

    def __init__(self, grammar, senderFactory, receiverFactory, bindings):
        self.grammar = grammar
        self.bindings = dict(bindings)
        self.senderFactory = senderFactory
        self.receiverFactory = receiverFactory
        self.disconnecting = False

    def setNextRule(self, rule):
        self.currentRule = rule

    def connectionMade(self):
        self.sender = self.senderFactory(self.transport)
        self.bindings['receiver'] = self.receiver = self.receiverFactory(
            self.sender, self)
        self.receiver.connectionMade()
        self._setupInterp()

    def _setupInterp(self):
        self._interp = TrampolinedGrammarInterpreter(
            self.grammar, self.currentRule, callback=self._parsedRule,
            globals=self.bindings)

    def _parsedRule(self, nextRule, position):
        if nextRule is not None:
            self.currentRule = nextRule

    def dataReceived(self, data):
        if self.disconnecting:
            return

        while data:
            try:
                status = self._interp.receive(data)
            except Exception:
                self.connectionLost(Failure())
                self.transport.abortConnection()
                return
            else:
                if status is _feed_me:
                    return
            data = ''.join(self._interp.input.data[self._interp.input.position:])
            self._setupInterp()

    def connectionLost(self, reason):
        if self.disconnecting:
            return
        self.receiver.connectionLost(reason)
        self.disconnecting = True
