Parsley Reference
-----------------

Basic syntax
~~~~~~~~~~~~
``foo = ....``:
   Define a rule named foo.

``expr1 expr2``:
   Match expr1, and then match expr2 if it succeeds, returning the value of
   expr2. Like Python's ``and``.

``expr1 | expr2``:
  Try to match ``expr1`` --- if it fails, match ``expr2`` instead. Like Python's
  ``or``.

``expr*``:
  Match ``expr`` zero or more times, returning a list of matches.

``expr+``:
  Match ``expr`` one or more times, returning a list of matches.

``expr?``:
  Try to match ``expr``. Returns ``None`` if it fails to match.

``expr{n, m}``:
  Match ``expr`` at least ``n`` times, and no more than ``m`` times.

``expr{n}``:
  Match ``expr`` ``n`` times exactly.

``~expr``:
  Negative lookahead. Fails if the next item in the input matches
  ``expr``. Consumes no input.

``~~expr``:
  Positive lookahead. Fails if the next item in the input does *not*
  match ``expr``. Consumes no input.

``ruleName`` or ``ruleName(arg1 arg2 etc)``:
  Call the rule ``ruleName``, possibly with args.

``'x'``:
  Match the literal character 'x'.

``<expr>``:
  Returns the string consumed by matching ``expr``. Good for tokenizing rules.

``expr:name``:
  Bind the result of expr to the local variable ``name``.

``-> pythonExpression``:
  Evaluate the given Python expression and return its result. Can be
  used inside parentheses too!

``!(pythonExpression)``:
  Invoke a Python expression as an action.

``?(pythonExpression)``:
  Fail if the Python expression is false, Returns True otherwise.

``expr ^(CustomLabel)``:
  If the expr fails, the exception raised will contain CustomLabel.
  Good for providing more context when a rule is broken.
  CustomLabel can contain any character other than "(" and ")".

Comments like Python comments are supported as well, starting with #
and extending to the end of the line.


Python API
~~~~~~~~~~
.. automodule:: parsley
   :members:


Protocol parsing API
====================

.. py:module:: ometa.protocol

.. py:class:: ParserProtocol

   The Twisted ``Protocol`` subclass used for :ref:`parsing stream protocols
   using Parsley <protocol-parsing>`. It has two public attributes:

   .. py:attribute:: sender

      After the connection is established, this attribute will refer to the
      sender created by the sender factory of the :class:`ParserProtocol`.

   .. py:attribute:: receiver

      After the connection is established, this attribute will refer to the
      receiver created by the receiver factory of the :class:`ParserProtocol`.

   It's common to also add a ``factory`` attribute to the
   :class:`ParserProtocol` from its factory's ``buildProtocol`` method, but
   this isn't strictly required or guaranteed to be present.

   Subclassing or instantiating :class:`ParserProtocol` is not necessary;
   :func:`~parsley.makeProtocol` is sufficient and requires less boilerplate.

.. _receivers:

.. py:class:: Receiver

   :class:`Receiver` is not a real class but is used here for demonstration
   purposes to indicate the required API.

   .. py:attribute:: currentRule

      :class:`ParserProtocol` examines the :attr:`currentRule` attribute at the
      beginning of parsing as well as after every time a rule has completely
      matched. At these times, the rule with the same name as the value of
      :attr:`currentRule` will be selected to start parsing the incoming stream
      of data.

   .. py:method:: prepareParsing(parserProtocol)

      :meth:`prepareParsing` is called after the :class:`.ParserProtocol` has
      established a connection, and is passed the :class:`.ParserProtocol`
      instance itself.

      :param parserProtocol: An instance of :class:`.ProtocolParser`.

   .. py:method:: finishParsing(reason)

      :meth:`finishParsing` is called if an exception was raised during
      parsing, or when the :class:`.ParserProtocol` has lost its connection,
      whichever comes first. It will only be called once.

      An exception raised during parsing can be due to incoming data that
      doesn't match the current rule or an exception raised calling python code
      during matching.

      :param reason: A `Failure`_ encapsulating the reason parsing has ended.

.. _senders:

Senders do not have any required API as :class:`ParserProtocol` will never call
methods on a sender.


Built-in Parsley Rules
~~~~~~~~~~~~~~~~~~~~~~

``anything``:
    Matches a single character from the input.

``letter``:
    Matches a single ASCII letter.

``digit``:
    Matches a decimal digit.

``letterOrDigit``:
    Combines the above.

``end``:
    Matches the end of input.

``ws``:
    Matches zero or more spaces, tabs, or newlines.

``exactly(char)``:
   Matches the character `char`.


.. _Failure: http://twistedmatrix.com/documents/current/api/twisted.python.failure.Failure.html
