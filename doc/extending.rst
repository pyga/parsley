==================================
Extending Grammars and Inheritance
==================================

:warning: Unfinished

Another feature taken from OMeta is *grammar inheritance*. We can
write a grammar with rules that override ones in a parent. If we load
the grammar from our calculator tutorial as ``Calc``, we can extend it
with some constants::

    from ometa.grammar import OMeta
    import math
    calcGrammarEx = """
    value = super | constant
    constant = "pi" -> math.pi
             | "e" -> math.e
    """
    CalcEx = OMeta.makeGrammar(calcGrammar, {"math": math}, superclass=Calc)
