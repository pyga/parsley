from ometa.interp import TrampolinedGrammarInterpreter, _feed_me, _paused

class TrampolinedParser:
    """
    A parser that incrementally parses incoming data.
    """
    def __init__(self, grammar, receiver, bindings):
        """
        Initializes the parser.

        @param grammar: The grammar used to parse the incoming data.
        @param receiver: Responsible for logic operation on the parsed data.
            Typically, the logic operation will be invoked inside the grammar,
            e.g., rule = expr1 expr2 (-> receiver.doSomeStuff())
        @param bindings: The namespace that can be accessed inside the grammar.
        """
        self.grammar = grammar
        self.bindings = dict(bindings)
        self.bindings['receiver'] = self.receiver = receiver
        self._setupInterp()


    def _setupInterp(self, paused=False):
        """
        Resets the parser. The parser will begin parsing with the rule named
        'initial'.
        """
        self._interp = TrampolinedGrammarInterpreter(
            grammar=self.grammar, rule=self.receiver.currentRule,
            callback=None, globals=self.bindings, paused=paused)


    def receive(self, data):
        """
        Receive the incoming data and begin parsing. The parser will parse the
        data incrementally according to the 'initial' rule in the grammar.

        @param data: The raw data received.
        """
        while data or self._interp.hasPendingData():
            status = self._interp.receive(data)
            if status in (_feed_me, _paused):
                return
            data = ''.join(self._interp.input.data[self._interp.input.position:])
            self._setupInterp(self._interp.paused)

    def pauseProducing(self):
        self._interp.paused = True
        self.receiver.transport.pauseProducing()

    def resumeProducing(self):
        self._interp.paused = False
        self.receiver.transport.resumeProducing()
        self.receiver.dataReceived(b'')

    def stopProducing(self):
        self._interp.paused = True
        self.receiver.transport.stopProducing()
