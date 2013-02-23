# -*- test-case-name: ometa.test.test_pymeta -*-
"""
Public interface to OMeta, as well as the grammars used to compile grammar
definitions.
"""
import os.path
import string
from StringIO import StringIO

from terml.parser import TermLParser
from terml.nodes import termMaker as t
from ometa.boot import BootOMetaGrammar
from ometa.builder import TermActionPythonWriter, moduleFromGrammar, TextWriter
from ometa.runtime import OMetaBase, OMetaGrammarBase

def loadGrammar(name):
    return open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), name)).read()


OMeta = BootOMetaGrammar.makeGrammar(loadGrammar("parsley.parsley"),
                                                 globals(), name='OMeta',
                                                 superclass=OMetaGrammarBase)

class TermOMeta(BootOMetaGrammar.makeGrammar(
        loadGrammar("parsley_termactions.parsley"),
        globals(), name='TermOMeta2', superclass=OMeta)):

    _writer = TermActionPythonWriter

    @classmethod
    def makeGrammar(cls, grammar, globals, name='Grammar', superclass=None):
        """
        Define a new parser class with the rules in the given grammar.

        @param grammar: A string containing a PyMeta grammar.
        @param globals: A dict of names that should be accessible by this
        grammar.
        @param name: The name of the class to be generated.
        @param superclass: The class the generated class is a child of.
        """
        g = cls(grammar)
        tree = g.parseGrammar(name)
        modname = "pymeta_grammar__" + name
        filename = "/pymeta_generated_code/" + modname + ".py"
        source = g.writeTerm(tree)
        return moduleFromGrammar(source, name, superclass or OMetaBase, globals,
                                 modname, filename)



    def writeTerm(self, term):
        f = StringIO()
        pw = self._writer(term)
        out = TextWriter(f)
        pw.output(out)
        return f.getvalue().strip()


    def rule_term(self):
        tp = TermLParser('')
        tp.input = self.input
        self.input.setMemo('term', None)
        val, err = tp.apply('term')
        self.input = tp.input
        return val, err

    def rule_term_arglist(self):
        tp = TermLParser('')
        tp.input = self.input
        val, err = tp.apply('argList')
        self.input = tp.input
        return val, err


TreeTransformerGrammar = OMeta.makeGrammar(
    loadGrammar("parsley_tree_transformer.parsley"),
    globals(), name='TreeTransformer',
    superclass=OMeta)
