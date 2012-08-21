==================================
Extending Grammars and Inheritance
==================================

:warning: Unfinished

Another feature taken from OMeta is *grammar inheritance*. We can
write a grammar with rules that override ones in a parent::

    import math
    calcGrammarEx = """
    value = super | constant
    constant = "pi" -> math.pi
             | "e" -> math.e
    """
    CalcEx = OMeta.makeGrammar(calcGrammar, {"math": math}, superclass=Calc)
