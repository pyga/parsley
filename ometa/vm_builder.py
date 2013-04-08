from StringIO import StringIO

import ometa
from terml.nodes import termMaker as t

def writeBytecode(expr):
    from ometa.grammar import TreeTransformerGrammar, loadGrammar
    from ometa.runtime import TreeTransformerBase
    Compiler = loadGrammar(ometa, 'vm', {'t': t},
                           grammar=TreeTransformerGrammar,
                           superclass=TreeTransformerBase)
    return Compiler.transform(expr)[0]


def bytecodeToPython(expr):
    from ometa.grammar import TreeTransformerGrammar, loadGrammar
    from ometa.runtime import TreeTransformerBase
    Emitter = loadGrammar(ometa, 'vm_emit', {'t': t},
                          grammar=TreeTransformerGrammar,
                          superclass=TreeTransformerBase)
    return Emitter.transform(expr)[0]
