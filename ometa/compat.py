from ometa.runtime import OMetaGrammarBase
from ometa.boot import BootOMetaGrammar
from ometa.grammar import loadGrammar
from terml.nodes import termMaker as t

OMeta1 = BootOMetaGrammar.makeGrammar(
    loadGrammar("pymeta_v1.parsley"),
    globals(), name='OMeta1',
    superclass=OMetaGrammarBase)
