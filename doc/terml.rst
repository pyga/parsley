=====
TermL
=====

TermL ("term-ell") is the Term Language, a small expression-based language for
representing arbitrary data in a simple structured format. It is ideal for
expressing abstract syntax trees (ASTs) and other kinds of primitive data
trees.

Creating Terms
==============

::

    >>> from terml.nodes import termMaker as t
    >>> t.Term()
    term('Term')

That's it! We've created an empty term, `Term`, with nothing inside.

::

    >>> t.Num(1)
    term('Num(1)')
    >>> t.Outer(t.Inner())
    term('Outer(Inner)')


We can see that terms are not just `namedtuple` lookalikes. They have their
own internals and store data in a slightly different and more structured way
than a normal tuple.
