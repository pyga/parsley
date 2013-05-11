from twisted.internet.protocol import Protocol

from ometa.interp import TrampolinedGrammarInterpreter, _feed_me

class ParserProtocol(Protocol):
    currentRule = 'initial'

    def __init__(self, grammar, senderFactory, stateFactory, bindings):
        self.grammar = grammar
        self.bindings = dict(bindings)
        self.senderFactory = senderFactory
        self.stateFactory = stateFactory

    def connectionMade(self):
        self.sender = self.senderFactory(self.transport)
        self.bindings['state'] = self.state = self.stateFactory(self.sender)
        self._setupInterp()

    def _setupInterp(self):
        self._interp = TrampolinedGrammarInterpreter(
            self.grammar, self.currentRule, callback=self._parsedRule,
            globals=self.bindings)

    def _parsedRule(self, nextRule, position):
        if nextRule is not None:
            self.currentRule = nextRule

    def dataReceived(self, data):
        while data:
            if self._interp.receive(data) is _feed_me:
                return
            data = ''.join(self._interp.input.data[self._interp.input.position:])
            self._setupInterp()

    def connectionLost(self, reason):
        self.state.connectionLost(reason)
