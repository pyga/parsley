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

Parsing Terms
=============

Parsley can parse terms from streams. Terms can contain any kind of parseable
data, including other terms. Returning to the ubiquitous calculator example::

    add = Add(:x, :y) -> x + y

Here this rule matches a term called `Add` which has two components, bind
those components to a couple of names (`x` and `y`), and return their sum. If
this rule were applied to a term like `Add(3, 5)`, it would return 8.

Terms can be nested, too. Here's an example that performs a slightly contrived
match on a negated term inside an addition::

    add_negate = Add(:x, Negate(:y)) -> x - y
