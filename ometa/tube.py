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
        self._interp = self._makeInterp()


    def _makeInterp(self):
        return TrampolinedGrammarInterpreter(
            grammar=self.grammar, rule=self.receiver.currentRule,
            callback=None, globals=self.bindings)


    def receive(self, data):
        """
        Receive the incoming data and begin parsing. The parser will parse the
        data incrementally according to the 'initial' rule in the grammar.

        @param data: The raw data received.
        """
        self._interp = _pumpInterpreter(self._makeInterp, data, self._interp)



def _pumpInterpreter(interpFactory, dataChunk, interp=None, end=False):
    if interp is None:
        interp = interpFactory()
    while dataChunk:
        status = interp.receive(dataChunk)
        if status is _feed_me:
            break
        dataChunk = ''.join(interp.input.data[interp.input.position:])
        interp = interpFactory()
    if end and not interp.ended:
        interp.end()
    return interp



def iterGrammar(grammar, bindings, rule, input_stream, end=False):
    """
    Repeatedly apply rule to an input stream, and yield matches.

    @param grammar: An ometa grammar.
    @param bindings: Bindings for the grammar.
    @param rule: The name of the rule to match.  Matches will be yielded.
    @param input_stream: The stream to read.  Will be read incrementally.
    @param end: Whether to tell the grammar that no more input will arrive
        when the stream is exhausted.
    """
    tokens = []  # Should really be an explicit queue.
    def append(token, error):
        if error.error:
            raise error
        tokens.append(token)

    def makeInterpreter():
        return TrampolinedGrammarInterpreter(
            grammar, rule, callback=append, globals=bindings)

    while True:
        data = input_stream.read()
        if not data:
            break
        _pumpInterpreter(makeInterpreter, data, end=end)
        for token in tokens:
            yield token
        tokens[:] = []
