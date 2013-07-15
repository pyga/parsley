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
Parsley grammar rules. Before getting started with
:func:`~parsley.makeProtocol`, let's build a grammar for `netstrings`_. The
netstrings protocol is very simple::

  4:spam,4:eggs,

This stream contains two netstrings: ``spam``, and ``eggs``. The data is
prefixed with one or more ASCII digits followed by a ``:``, and suffixed with a
``,``. So, a Parsley grammar to match a netstring would look like::

  nonzeroDigit = digit:x ?(x != '0')
  digits = <'0' | nonzeroDigit digit*>:i -> int(i)

  netstring = digits:length ':' <anything{length}>:string ',' -> string

:func:`~parsley.makeProtocol` takes, in addition to a grammar, a factory for a
"sender" and a factory for a "receiver". In the system of objects managed by
the ``ParserProtocol``, the sender is in charge of writing data to the wire,
and the receiver has methods called on it by the Parsley rules. To demonstrate
it, here is the final piece needed in the Parsley grammar for netstrings::

  initial = netstring:string -> receiver.netstringReceived(string)

The receiver is always available in Parsley rules with the name ``receiver``,
allowing Parsley rules to call methods on it. By default, the
``ParserProtocol`` tries to use a rule named ``initial`` as the starting rule.
If a rule named ``initial`` is not defined in the grammar, and another rule is
not set to be the starting rule before parsing begins (see :ref:`Advanced
parsing <advanced-parsing>` below), parsing will immediately fail. Unless
another starting rule is chosen, the ``ParserProtocol`` will use the starting
rule ``initial`` as the first current rule.

When data is received over the wire, the ``ParserProtocol`` tries to match the
received data against the current rule. If the current rule requires more data
to finish matching, the ``ParserProtocol`` stops and waits until more data
comes in, then tries to continue matching. This repeats until the current rule
is completely matched, and then the ``ParserProtocol`` starts matching any
leftover data against the current rule again.

The current rule can change during parsing. There are two ways to change the
current rule, which are addressed in the :ref:`Advanced parsing
<advanced-parsing>` section. The default behavior is to keep using the same
rule. Since the netstring protocol doesn't change, the default behavior of
continuing to use the same rule is fine for parsing netstrings.

Both the sender factory and receiver factory are constructed when the
``ParserProtocol``'s connection is established. The sender factory is a
one-argument callable which will be passed the ``ParserProtocol``'s
`Transport`_. This allows the sender to send data over the transport. For
example::

  class NetstringSender(object):
      def __init__(self, transport):
          self.transport = transport

      def sendNetstring(self, string):
          self.transport.write('%d:%s,' % (len(string), string))

The receiver factory is a two-argument callable which is passed the constructed
sender and the ``ParserProtocol`` instance. The returned object must at least
have ``prepareParsing`` and ``finishParsing`` methods. ``prepareParsing`` is
called when a connection is established (i.e. in the ``connectionMade`` of the
``ParserProtocol``) and ``finishParsing`` is called when a connection is closed
(i.e. in the ``connectionLost`` of the ``ParserProtocol``).

.. note::
   Both the receiver factory and its returned object's ``prepareParsing`` are
   called at in the ``ParserProtocol``'s ``connectionMade`` method; this
   separation is for ease of testing receivers.

To demonstrate a receiver, here is a simple receiver that receives netstrings
and echos the same netstrings back::

  class NetstringReceiver(object):
      def __init__(self, sender, parser):
          self.sender = sender

      def prepareParsing(self):
          pass

      def finishParsing(self, reason):
          pass

      def netstringReceived(self, string):
          self.sender.sendNetstring(string)

Putting it all together, the Protocol is constructed using the grammar, sender
factory, and receiver factory::

  NetstringProtocol = makeProtocol(
      grammar, NetstringSender, NetstringReceiver)

And finally, a complete example::

  from twisted.internet.defer import Deferred
  from twisted.internet.endpoints import TCP4ServerEndpoint
  from twisted.internet.protocol import Factory
  from twisted.internet.task import react

  from parsley import makeProtocol


  grammar = """

  digit = anything:x ?(x.isdigit())
  nonzeroDigit = anything:x ?(x != '0' and x.isdigit())
  digits = <'0' | nonzeroDigit digit*>:i -> int(i)

  netstring = digits:length ':' <anything{length}>:string ',' -> string

  initial = netstring:string -> receiver.netstringReceived(string)

  """


  class NetstringSender(object):
      def __init__(self, transport):
          self.transport = transport

      def sendNetstring(self, string):
          self.transport.write('%d:%s,' % (len(string), string))


  class NetstringReceiver(object):
      def __init__(self, sender, parser):
          self.sender = sender

      def prepareParsing(self):
          pass

      def finishParsing(self, reason):
          pass

      def netstringReceived(self, string):
          self.sender.sendNetstring(string)


  NetstringProtocol = makeProtocol(
      grammar, NetstringSender, NetstringReceiver)


  class NetstringFactory(Factory):
      protocol = NetstringProtocol


  def main(reactor):
      server = TCP4ServerEndpoint(reactor, 1234)
      d = server.listen(NetstringFactory())
      d.addCallback(lambda p: Deferred())  # listen forever
      return d


  react(main, [])


Intermezzo: error reporting
---------------------------

If an exception is raised from within Parsley during parsing, whether it's due
to input not matching the current rule or an exception being raised from code
the grammar calls, the connection will be immediately closed. The traceback
will be captured as a `Failure`_ and passed to the ``finishParsing`` method of
the receiver.

At present, there is no way to recover from failure.


Composing senders and receivers
-------------------------------

The design of senders and receivers is intentional to make composition easy:
no subclassing is required. While the composition is easy enough to do on your
own, Parsley provides two functions: :func:`~parsley.stackSenders` and
:func:`~parsley.stackReceivers`. Both take a base factory followed by zero or
more wrappers.

Their use is extremely simple: ``stackSenders(x, y, z)`` will return a sender
factory which will, when called with a transport, return
``x(y(z(transport)))``. Similarly, ``stackReceivers(x, y, z)`` will return a
receiver factory which, when called with a sender and parser, will return
``x(y(z(sender, parser)))``.

An example of wrapping a sender factory::

  class NetstringReversalWrapper(object):
      def __init__(self, wrapped):
          self.wrapped = wrapped

      def sendNetstring(self, string):
          self.wrapped.sendNetstring(string[::-1])

And then, constructing the Protocol::

  NetstringProtocol = makeProtocol(
      grammar,
      stackSenders(NetstringReversalWrapper, NetstringSender),
      NetstringReceiver)

A wrapper doesn't need to call the same methods on the thing it's wrapping.
Also note that in most cases, it's important to forward unknown methods on to
the wrapped object. An example of wrapping a receiver::

  class NetstringSplittingWrapper(object):
      def __init__(self, wrapped):
          self.wrapped = wrapped

      def netstringReceived(self, string):
          splitpoint = len(string) // 2
          self.wrapped.netstringFirstHalfReceived(string[:splitpoint])
          self.wrapped.netstringSecondHalfReceived(string[splitpoint:])

      def __getattr__(self, attr):
          return getattr(self.wrapped, attr)

The corresponding receiver and again, constructing the Protocol::

  class SplitNetstringReceiver(object):
      def __init__(self, sender, parser):
          self.sender = sender

      def prepareParsing(self):
          pass

      def finishParsing(self, reason):
          pass

      def netstringFirstHalfReceived(self, string):
          self.sender.sendNetstring(string)

      def netstringSecondHalfReceived(self, string):
          pass

  NetstringProtocol = makeProtocol(
      grammar,
      stackSenders(NetstringReversalWrapper, NetstringSender),
      stackReceivers(NetstringSplittingWrapper, SplitNetstringReceiver))


.. _advanced-parsing:

Advanced parsing
----------------

As mentioned before, it's possible to change the current rule. Imagine a
"netstrings2" protocol that looks like this::

  3:foo,3;bar,4:spam,4;eggs,

That is, the protocol alternates between using ``:`` and using ``;`` delimiting
data length and the data. The amended grammar would look something like this::

  nonzeroDigit = digit:x ?(x != '0')
  digits = <'0' | nonzeroDigit digit*>:i -> int(i)

  colon = digits:length ':' <anything{length}>:string ',' -> receiver.netstringReceived(':', string)
  semicolon = digits:length ';' <anything{length}>:string ',' -> receiver.netstringReceived(';', string)

Note that there is no ``initial`` rule. The starting rule can be specified
using the ``setNextRule`` method of a ``ParserProtocol``. Here's the beginning
of a receiver for netstrings2::

  class Netstring2Receiver(object):
      def __init__(self, sender, parser):
          self.sender = sender
          self.parser = parser

      def prepareParsing(self):
          self.parser.setNextRule('colon')

In our case calling ``setNextRule`` is required before parsing begins since
there is no rule named ``initial``. Otherwise, the ``ParserProtocol`` would try
to match against a nonexistant rule and fail.

.. note::

   It doesn't matter if ``setNextRule`` is called in ``__init__`` or
   ``prepareParsing`` to set the starting rule as long as it's called in one of
   them (or something called by one of them).

The other way to change the current rule is to make the current rule evaluate
to a string naming another rule. Since in our grammar the ``colon`` rule
evaluates to the result of calling ``receiver.netstringReceived(...)``, the
``netstringReceived`` method could look like this::

  def netstringReceived(self, delimiter, string):
      self.sender.sendNetstring(string)
      if delimiter == ':':
          return 'semicolon'
      else:
          return 'colon'

The same effect can be achieved with ``setNextRule``::

  def netstringReceived(self, delimiter, string):
      self.sender.sendNetstring(string)
      if delimiter == ':':
          self.parser.setNextRule('semicolon')
      else:
          self.parser.setNextRule('colon')

.. note::

   ``setNextRule`` can be called at any time. However, if ``setNextRule`` is
   called from somewhere other than the receiver factory, its
   ``prepareParsing``, or a method called from the grammar, Parsley will wait
   until the current rule is completely matched before switching rules.


.. _Twisted: http://twistedmatrix.com/trac/
.. _TCP clients: http://twistedmatrix.com/documents/current/core/howto/clients.html
.. _servers: http://twistedmatrix.com/documents/current/core/howto/servers.html
.. _IProtocol: http://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IProtocol.html
.. _netstrings: http://cr.yp.to/proto/netstrings.txt
.. _Transport: http://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.ITransport.html
.. _Failure: http://twistedmatrix.com/documents/current/api/twisted.python.failure.Failure.html
