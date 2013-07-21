.. _protocol-parsing:

===============================================
Parsley Tutorial Part III: Parsing Network Data
===============================================

This tutorial assumes basic knowledge of writing `Twisted`_ `TCP clients`_ or
`servers`_.


Basic parsing
-------------

Parsing data that comes in over the network can be difficult due to that there
is no guarantee of receiving whole messages. Buffering is often complicated by
protocols switching between using fixed-width messages and delimiters for
framing. Fortunately, Parsley can remove all of this tedium.

With :func:`parsley.makeProtocol`, Parsley can generate a `Twisted`_
`IProtocol`_-implementing class which will match incoming network data using
Parsley grammar rules. Before getting started with :func:`.makeProtocol`, let's
build a grammar for `netstrings`_. The netstrings protocol is very simple::

  4:spam,4:eggs,

This stream contains two netstrings: ``spam``, and ``eggs``. The data is
prefixed with one or more ASCII digits followed by a ``:``, and suffixed with a
``,``. So, a Parsley grammar to match a netstring would look like:

.. literalinclude:: _static/listings/tutorial3-netstrings.py
   :start-after: grammar =
   :end-before: receiveNetstring

:func:`.makeProtocol` takes, in addition to a grammar, a factory for a "sender"
and a factory for a "receiver". In the system of objects managed by the
:class:`.ParserProtocol`, the sender is in charge of writing data to the wire,
and the receiver has methods called on it by the Parsley rules. To demonstrate
it, here is the final piece needed in the Parsley grammar for netstrings:

.. literalinclude:: _static/listings/tutorial3-netstrings.py
   :start-after: netstring =
   :end-before: """

The receiver is always available in Parsley rules with the name ``receiver``,
allowing Parsley rules to call methods on it.

When data is received over the wire, the :class:`.ParserProtocol` tries to
match the received data against the current rule. If the current rule requires
more data to finish matching, the :class:`.ParserProtocol` stops and waits
until more data comes in, then tries to continue matching. This repeats until
the current rule is completely matched, and then the :class:`.ParserProtocol`
starts matching any leftover data against the current rule again.

One specifies the current rule by setting a :attr:`.currentRule` attribute on
the receiver, which the :class:`.ParserProtocol` looks at before doing any
parsing. Changing the current rule is addressed in the :ref:`Switching rules
<switching-rules>` section.

Since the :class:`.ParserProtocol` will never modify the :attr:`.currentRule`
attribute itself, the default behavior is to keep using the same rule. Parsing
netstrings doesn't require any rule changing, so, the default behavior of
continuing to use the same rule is fine.

Both the sender factory and receiver factory are constructed when the
:class:`.ParserProtocol`'s connection is established. The sender factory is a
one-argument callable which will be passed the :class:`.ParserProtocol`'s
`Transport`_. This allows the sender to send data over the transport. For
example:

.. literalinclude:: _static/listings/tutorial3-netstrings.py
   :pyobject: NetstringSender

The receiver factory is another one-argument callable which is passed the
constructed sender. The returned object must at least have
:meth:`.prepareParsing` and :meth:`.finishParsing` methods.
:meth:`.prepareParsing` is called with the :class:`.ParserProtocol` instance
when a connection is established (i.e. in the ``connectionMade`` of the
:class:`.ParserProtocol`) and :meth:`.finishParsing` is called when a
connection is closed (i.e. in the ``connectionLost`` of the
:class:`.ParserProtocol`).

.. note::
   Both the receiver factory and its returned object's :meth:`.prepareParsing`
   are called at in the :class:`.ParserProtocol`'s ``connectionMade`` method;
   this separation is for ease of testing receivers.

To demonstrate a receiver, here is a simple receiver that receives netstrings
and echos the same netstrings back:

.. literalinclude:: _static/listings/tutorial3-netstrings.py
   :pyobject: NetstringReceiver

Putting it all together, the Protocol is constructed using the grammar, sender
factory, and receiver factory:

.. literalinclude:: _static/listings/tutorial3-netstrings.py
   :start-after: self.sender.sendNetstring
   :end-before: class

:download:`The complete script is also available for download.
<_static/listings/tutorial3-netstrings.py>`


Intermezzo: error reporting
---------------------------

If an exception is raised from within Parsley during parsing, whether it's due
to input not matching the current rule or an exception being raised from code
the grammar calls, the connection will be immediately closed. The traceback
will be captured as a `Failure`_ and passed to the :meth:`.finishParsing`
method of the receiver.

At present, there is no way to recover from failure.


Composing senders and receivers
-------------------------------

The design of senders and receivers is intentional to make composition easy: no
subclassing is required. While the composition is easy enough to do on your
own, Parsley provides a function: :func:`.stack`. It takes a base factory
followed by zero or more wrappers.

Its use is extremely simple: ``stack(x, y, z)`` will return a callable suitable
either as a sender or receiver factory which will, when called with an
argument, return ``x(y(z(argument)))``.

An example of wrapping a sender factory:

.. literalinclude:: _static/listings/tutorial3-netstring-reversal.py
   :pyobject: NetstringReversalWrapper

And then, constructing the Protocol::

  NetstringProtocol = makeProtocol(
      grammar,
      stack(NetstringReversalWrapper, NetstringSender),
      NetstringReceiver)

A wrapper doesn't need to call the same methods on the thing it's wrapping.
Also note that in most cases, it's important to forward unknown methods on to
the wrapped object. An example of wrapping a receiver:

.. literalinclude:: _static/listings/tutorial3-netstring-reversal.py
   :pyobject: NetstringSplittingWrapper

The corresponding receiver and again, constructing the Protocol:

.. literalinclude:: _static/listings/tutorial3-netstring-reversal.py
   :pyobject: SplitNetstringReceiver

.. literalinclude:: _static/listings/tutorial3-netstring-reversal.py
   :start-after: begin protocol definition
   :end-before: SplitNetstringReceiver

:download:`The complete script is also available for download.
<_static/listings/tutorial3-netstring-reversal.py>`


.. _switching-rules:

Switching rules
---------------

As mentioned before, it's possible to change the current rule. Imagine a
"netstrings2" protocol that looks like this::

  3:foo,3;bar,4:spam,4;eggs,

That is, the protocol alternates between using ``:`` and using ``;`` delimiting
data length and the data. The amended grammar would look something like this:

.. literalinclude:: _static/listings/tutorial3-netstrings2.py
   :start-after: grammar =
   :end-before: """

Changing the current rule is as simple as changing the :attr:`.currentRule`
attribute on the receiver. So, the ``netstringReceived`` method could look like
this:

.. literalinclude:: _static/listings/tutorial3-netstrings2.py
   :pyobject: NetstringReceiver.netstringReceived

While changing the :attr:`.currentRule` attribute can be done at any time, the
:class:`.ParserProtocol` only examines the :attr:`.currentRule` at the
beginning of parsing and after a rule has finished matching. As a result, if
the :attr:`.currentRule` changes, the :class:`.ParserProtocol` will wait until
the current rule is completely matched before switching rules.

:download:`The complete script is also available for download.
<_static/listings/tutorial3-netstrings2.py>`


.. _Twisted: http://twistedmatrix.com/trac/
.. _TCP clients: http://twistedmatrix.com/documents/current/core/howto/clients.html
.. _servers: http://twistedmatrix.com/documents/current/core/howto/servers.html
.. _IProtocol: http://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IProtocol.html
.. _netstrings: http://cr.yp.to/proto/netstrings.txt
.. _Transport: http://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.ITransport.html
.. _Failure: http://twistedmatrix.com/documents/current/api/twisted.python.failure.Failure.html
