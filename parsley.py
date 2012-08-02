from ometa.grammar import OMeta
from ometa.runtime import ParseError, EOFError

def makeGrammar(source, bindings, name='Grammar'):
    """
    Create a class from a Parsley grammar.
    """
    try:
        g = OMeta.makeGrammar(source, bindings, name=name)
    except ParseError, p:
        print p.formatError(source)
        raise
    return _makeWrappedGrammar(g)

def _makeWrappedGrammar(g):
    def makeParser(input):
        return _GrammarWrapper(g(input), input)
    return makeParser

class _GrammarWrapper(object):
    def __init__(self, grammar, input):
        self._grammar = grammar
        self._input = input

    def __getattr__(self, name):
        """
        Return a function that will instantiate a grammar and invoke the named
        rule.
        @param: Rule name.
        """
        def doIt(debug=False):
            try:
                ret, err = self._grammar.apply(name)
            except ParseError, e:
                err = e
            else:
                try:
                    extra, _ = self._grammar.input.head()
                except EOFError:
                    return ret

            if debug:
                print err.formatError(self._input)
                raise ParseError()
            else:
                raise err
        return doIt

