from ometa.grammar import OMeta
from ometa.runtime import ParseError, EOFError, OMetaBase, expected
from terml.parser import parseTerm as term
from terml.nodes import termMaker
from terml.quasiterm import quasiterm

__version__ = '1.1'


def wrapGrammar(g, tracefunc=None):
    def makeParser(input):
        """
        Creates a parser for the given input, with methods for
        invoking each rule.

        :param input: The string you want to parse.
        """
        fastParser = g._fastGrammar(input)
        parser = g(input)
        if tracefunc:
            parser._trace = tracefunc
        return _GrammarWrapper(fastParser, parser, input)
    makeParser._grammarClass = g
    return makeParser


def makeGrammar(source, bindings, name='Grammar', unwrap=False,
                extends=wrapGrammar(OMetaBase), tracefunc=None):
    """
    Create a class from a Parsley grammar.

    :param source: A grammar, as a string.
    :param bindings: A mapping of variable names to objects.
    :param name: Name used for the generated class.

    :param unwrap: If True, return a parser class suitable for
                   subclassing. If False, return a wrapper with the
                   friendly API.
    :param extends: The superclass for the generated parser class.

    :param tracefunc: A 3-arg function which takes a fragment of
    grammar source, the start/end indexes in the grammar of this
    fragment, and a position in the input. Invoked for terminals and
    rule applications.
    """
    g = OMeta.makeGrammar(source, name).createParserClass(
        unwrapGrammar(extends), bindings)
    if unwrap:
        return g
    else:
        return wrapGrammar(g, tracefunc=tracefunc)


def unwrapGrammar(w):
    """
    Access the internal parser class for a Parsley grammar object.
    """
    return getattr(w, '_grammarClass', None) or w


class _GrammarWrapper(object):
    """
    A wrapper for Parsley grammar instances.

    To invoke a Parsley rule, invoke a method with that name -- this
    turns x(input).foo() calls into grammar.apply("foo") calls.
    """
    def __init__(self, fastParser, parser, input):
        self._fastParser = fastParser
        self._parser = parser
        self._input = input
        #so pydoc doesn't get trapped in the __getattr__
        self.__name__ = _GrammarWrapper.__name__

    def __getattr__(self, name):
        """
        Return a function that will instantiate a grammar and invoke the named
        rule.
        :param name: Rule name.
        """
        def _invokeRule( *args, **kwargs):
            """
            Invoke a Parsley rule. Passes any positional args to the rule.
            """
            print "PARSE FAILED. Re-running to collect debug info..."
            try:
                ret, err = self._parser.apply(name, *args)
            except ParseError, e:
                self._parser.considerError(e)
                err = self._parser.currentError
            else:
                try:
                    extra, _ = self._parser.input.head()
                except EOFError:
                    return ret
                else:
                    # problem is that input remains, so:
                    err = ParseError(err.input, err.position + 1,
                                     [["message", "expected EOF"]], err.trail)
            raise err

        def _fastInvokeRule( *args, **kwargs):
            """
            Invoke a Parsley rule. Passes any positional args to the rule.
            """
            try:
                ret, _ = self._fastParser.apply(name, *args)
            except ParseError, e:
                return _invokeRule(*args, **kwargs)
            else:
                try:
                    extra, _ = self._fastParser.input.head()
                except EOFError:
                    return ret
            return _invokeRule(*args, **kwargs)


        return _fastInvokeRule

__all__ = ['makeGrammar', 'wrapGrammar', 'unwrapGrammar', 'term', 'quasiterm']







