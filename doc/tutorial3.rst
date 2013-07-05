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

With :func:`makeParser`, Parsley can generate a `Twisted`_
`IProtocol`_-implementing class which will match incoming network data using
Parlsey grammar rules. Before getting started with :func:`makeParser`, let's
build a grammar for `netstrings`_. The netstrings protocol is very simple::

  4:spam,4:eggs,

This stream contains two netstrings: ``spam``, and ``eggs``. The data is
prefixed with one or more ASCII digits followed by a ``:``, and suffixed with a
``,``. So, a Parsley grammar to match a netstring would look like::

  nonzeroDigit = digit:x ?(x != '0')
  digits = <'0' | nonzeroDigit digit*>:i -> int(i)

  netstring = digits:length ':' <anything{length}>:string ',' -> string

:func:`makeParser` takes, in addition to a grammar, a factory for a "sender"
and a factory for a "receiver". In the system of objects managed by the
``ParserProtocol``, the sender is in charge of writing data to the wire, and
the receiver has methods called on it by the Parsley rules. To demonstrate it,
here is the final piece needed in the Parsley grammar for netstrings::

  initial = netstring:string -> receiver.netstringReceived(string)

The receiver is always available in Parsley rules with the name ``receiver``,
allowing Parsley rules to call methods on it. This rule is specifically called
``initial`` because ``ParserProtocol`` defaults to matching against this rule
first. There are two ways to change the rule that ``ParserProtocol`` matches
against, which will be addressed later. The default behavior is to keep using
the same rule, which is fine for netstrings.

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
have ``connectionMade`` and ``connectionLost`` methods. These are called at the
same time as the same-named methods on the ``ParserProtocol``.

.. note::
   Both the receiver factory and its returned object's ``connectionMade`` are
   called at in the ``ParserProtocol``'s ``connectionMade`` method; this
   separation is for ease of testing receivers.

To demonstrate a receiver, here is a simple receiver that receives netstrings
and echos the same netstrings back::

  class NetstringReceiver(object):
      def __init__(self, sender, parser):
          self.sender = sender

      def connectionMade(self):
          pass

      def connectionLost(self, reason):
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

      def connectionMade(self):
          pass

      def connectionLost(self, reason):
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
will be captured as a `Failure`_ and passed to the ``connectionLost`` method of
the receiver.

At present, there is no way to recover from failure.


Composing senders and receivers
-------------------------------

The design of senders and receivers is intentional to make composition easy.
While the composition is easy enough to do on your own, Parsley provides two
functions: :func:`stackSenders` and :func:`stackReceivers`. Both take a base
factory followed by zero or more wrappers.

Their use is extremely simple: ``stackSenders(x, y, z)`` will return a sender
factory which will, when called with a transport, return
``z(y(x(transport)))``. Similarly, ``stackReceivers(x, y, z)`` will return a
receiver factory which, when called with a sender and parser, will return
``z(y(x(sender, parser)))``.

An example of wrapping a sender factory::

  class NetstringReversalWrapper(object):
      def __init__(self, wrapped):
          self.wrapped = wrapped

      def sendNetstring(self, string):
          self.wrapped.sendNetstring(string[::-1])

And then, constructing the Protocol::

  NetstringProtocol = makeProtocol(
      grammar,
      stackSenders(NetstringSender, NetstringReversalWrapper),
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

      def connectionMade(self):
          pass

      def connectionLost(self, reason):
          pass

      def netstringFirstHalfReceived(self, string):
          self.sender.sendNetstring(string)

      def netstringSecondHalfReceived(self, string):
          pass

  NetstringProtocol = makeProtocol(
      grammar,
      stackSenders(NetstringSender, NetstringReversalWrapper),
      stackReceivers(SplitNetstringReceiver, NetstringSplittingWrapper))


More advanced parsing
---------------------

As mentioned before, it's possible to switch the rule that the
``ParserProtocol`` uses to match incoming data. Imagine a "netstrings2"
protocol that looks like this::

  3:foo,3;bar,4:spam,4;eggs,

That is, the protocol alternates between using ``:`` and using ``;`` delimiting
data length and the data. The amended grammar would look something like this::

  nonzeroDigit = digit:x ?(x != '0')
  digits = <'0' | nonzeroDigit digit*>:i -> int(i)

  colon = digits:length ':' <anything{length}>:string ',' -> receiver.netstringReceived(':', string)
  semicolon = digits:length ';' <anything{length}>:string ',' -> receiver.netstringReceived(';', string)

Note that there is no ``initial`` rule. The initial rule can be changed using
the ``setNextRule`` method of a ``ParserProtocol``. Here's the beginning of a
receiver for netstrings2::


  class Netstring2Receiver(object):
      def __init__(self, sender, parser):
          self.sender = sender
          self.parser = parser

      def connectionMade(self):
          self.parser.setNextRule('colon')

It doesn't actually matter if ``setNextRule`` is called in ``__init__`` or
``connectionMade`` to set the initial rule as long as it's called in one of
them (or something called by one of them). The other way to change the rule the
``ParserProtocol`` is matching is to make the current rule evaluate to a string
naming another rule. Since in our grammar the ``colon`` rule evaluates to the
result of calling ``receiver.netstringReceived(...)``, the
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
   ``connectionMade``, or a method called from the grammar, Parsley will wait
   until the current rule is completely matched before switching rules.


.. _Twisted: http://twistedmatrix.com/trac/
.. _TCP clients: http://twistedmatrix.com/documents/current/core/howto/clients.html
.. _servers: http://twistedmatrix.com/documents/current/core/howto/servers.html
.. _IProtocol: http://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IProtocol.html
.. _netstrings: http://cr.yp.to/proto/netstrings.txt
.. _Transport: http://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.ITransport.html
.. _Failure: http://twistedmatrix.com/documents/current/api/twisted.python.failure.Failure.html
