
================
Parsley Tutorial
================

Parsley is a pattern matching and parsing tool for Python programmers.

Most Python programmers are familiar with regular expressions, as
provided by Python's `re` module. To use it, you provide a string that
describes the pattern you want to match, and your input.

For example::

    >>> import re
    >>> x = re.compile("a(b|c)d+e")
    >>> x.match("abddde")
    <_sre.SRE_Match object at 0x7f587af54af8>


You can do exactly the same sort of thing in Parsley::

    >>> import parsley
    >>> x = parsley.makeGrammar("foo = 'a' ('b' | 'c') 'd'+ 'e'", {})
    >>> x("abdde").foo()
    'e'

From this small example, a couple differences between regular
expressions and Parsley grammars can be seen:

Parsley Grammars Have Named Rules
---------------------------------

A Parsley grammar can have many rules, and each has a name. The
example above has a single rule named `foo`. Rules can call each
other; calling rules in Parsley works like calling functions in
Python. Here is another way to write the grammar above::

    foo = 'a' baz 'd'+ 'e'
    baz = 'b' | 'c'


Parsley Grammars Are Expressions
--------------------------------

Calling `match` for a regular expression returns a match object if the
match succeeds or None if it fails. Parsley parsers return the value
of last expression in the rule. Behind the scenes, Parsley turns each
rule in your grammar into Python methods. In pseudo-Python code, it
looks something like this::

    def foo(self):
        match('a')
        self.baz()
        match_one_or_more('d')
        return match('e')

    def baz(self):
        return match('b') or match('c')

The value of the last expression in the rule is what the rule
returns. This is why our example returns 'e'.

The similarities to regular expressions pretty much end here,
though. Having multiple named rules composed of expressions makes for
a much more powerful tool, and now we're going to look at some more
features that go even further.

Rules Can Embed Python Expressions
----------------------------------

Since these rules just turn into Python code eventually, we can stick
some Python code into them ourselves. This is particularly useful for
changing the return value of a rule. The Parsley expression for this
is `->`. We can also bind the results of expressions to variable names
and use them in Python code. So things like this are possible::

    >>> x = parsley.makeGrammar("""
    foo = 'a':one baz:two 'd'+ 'e' -> (one, two)
    baz = 'b' | 'c'
    """, {})
    >>> x("abdde").foo()
    ('a', 'b')

Literal match expressions like `'a'` return the character they
match. Using a colon and a variable name after an expression is like
assignment in Python. As a result, we can use those names in a Python
expression - in this case, creating a tuple.

Another way to use Python code in a rule is to write custom tests for
matching. Sometimes it's more convenient to write some Python that
determines if a rule matches than to stick to Parsley expressions
alone. For those cases, we can use `?()`. Here, we use the builtin
rule `anything` to match a single character, then a Python predicate
to decide if it's the one we want::

    digit = anything:x ?(x in '0123456789') -> x

This rule `digit` will match any decimal digit. We need the `-> x` on
the end to return the character rather than the value of the predicate
expression, which is just `True`.

Repeated Matches Make Lists
---------------------------

Like regular expressions, Parsley supports repeating matches. You can
match an expression zero or more times with '* ', one or more times
with '+', and a specific number of times with '{n, m}' or just
'{n}'. Since all expressions in Parsley return a value, these
repetition operators return a list containing each match they made.

::

    >>> x = parsley.makeGrammar("""
    digit = anything:x ?(x in '0123456789') -> x
    number = digit+
    """, {})
    >>> x("314159").number()
    ['3', '1', '4', '1', '5', '9']

The `number` rule repeatedly matches `digit` and collects the matches
into a list. This gets us part way to turning a string like `314159`
into an integer. All we need now is to turn the list back into a
string and call `int()`::

    >>> x = parsley.makeGrammar("""
    digit = anything:x ?(x in '0123456789') -> x
    number = digit+:ds -> int(''.join(ds))
    """, {})
    >>> x("8675309").number()
    8675309


If it seemed kind of strange to break our input string up into a list
and then reassemble it into a string using `join`, you're not
alone. Parsley has a shortcut for this since it's a common case: you
can use `<>` around a rule to make it return the slice of input it
consumes, ignoring the actual return value of the rule. For example::

    >>> x = parsley.makeGrammar("""
    digit = anything:x ?(x in '0123456789')
    number = <digit+>:ds -> int(ds)
    """, {})
    >>> x("11235").number()
    11235

Here, `<digit+>` returns the string `"11235"`, since that's the
portion of the input that `digit+` matched. (In this case it's the
entire input, but we'll see some more complex cases soon.) Since it
ignores the list returned by `digit+`, leaving the `-> x` out of
`digit` doesn't change the result.

Now let's look at using these rules in a more complicated parser. We
have support for parsing numbers; let's do addition, as well.

::
    >>> x = parsley.makeGrammar("""
    digit = anything:x ?(x in '0123456789')
    number = <digit+>:ds -> int(ds)
    expr = number:left ( '+' number:right -> left + right
                       | -> left)

    """, {})
    >>> x("17+34").expr()
    51
    >>> x("18").expr()
    18

Parentheses group expressions just like in Python. the '`|`' operator
is like `or` in Python - it short-circuits. It tries each expression
until it finds one that matches. For `"17+34"`, the `number` rule
matches "17", then Parsley tries to match `+` followed by another
`number`. Since "+" and "34" are the next things in the input, those
match, and it then runs the Python expression `left + right` and
returns its value. For the input `"18"` it does the same, but `+` does
not match, so Parsley tries the next thing after `|`. Since this is
just a Python expression, the match succeeds and the number 18 is
returned.

Four function calculator::

    digit = anything:x ?(x in '0123456789')
    number = <digit+>:ds -> int(ds)
    ws = ' '*
    muldiv = value:left ws ('*' value:right -> left * right
                           |'/' value:right -> left / right
                           | -> left)

    expr = muldiv:left ws ('+' muldiv:right -> left + right
                           |'-' muldiv:right -> left - right
                           | -> left)
    parens = '(' ws expr:e ws ')' -> e
    value = ws (number | parens)
