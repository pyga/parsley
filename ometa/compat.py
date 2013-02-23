import ometa
from ometa.runtime import OMetaGrammarBase
from ometa.boot import BootOMetaGrammar
from ometa.grammar import loadGrammar
from terml.nodes import termMaker as t

OMeta1 = loadGrammar(ometa, "pymeta_v1",
                     globals(), OMetaGrammarBase)
