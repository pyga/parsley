from ometa.interp import TrampolinedGrammarInterpreter, _feed_me

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


    def _setupInterp(self):
        """
        Resets the parser. The parser will begin parsing with the rule named
        'initial'.
        """
        self._interp = TrampolinedGrammarInterpreter(
            grammar=self.grammar, ruleName='initial', callback=None,
            globals=self.bindings)


    def receive(self, data):
        """
        Receive the incoming data and begin parsing. The parser will parse the
        data incrementally according to the 'initial' rule in the grammar.

        @param data: The raw data received.
        """
        while data:
            try:
                status = self._interp.receive(data)
            except Exception as e:
                # maybe we should raise it?
                raise e
            else:
                if status is _feed_me:
                    return
            data = ''.join(self._interp.input.data[self._interp.input.position:])
            self._setupInterp()