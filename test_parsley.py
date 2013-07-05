import unittest

import parsley


def wrapperFactory(addition):
    def wrapper(wrapped):
        return addition, wrapped
    return wrapper

def nullFactory(*args):
    return args


class StackSendersTestCase(unittest.TestCase):
    def test_onlyBase(self):
        "stackSenders can be called with no wrappers."
        fac = parsley.stackSenders(nullFactory)
        self.assertEqual(fac('a'), ('a',))

    def test_oneWrapper(self):
        "stackSenders can be called with one wrapper."
        fac = parsley.stackSenders(nullFactory, wrapperFactory(0))
        self.assertEqual(fac('a'), (0, ('a',)))

    def test_tenWrappers(self):
        "stackSenders can be called with ten wrappers."
        wrappers = []
        result = 'a',
        for x in xrange(10):
            wrappers.append(wrapperFactory(x))
            result = x, result
        fac = parsley.stackSenders(nullFactory, *wrappers)
        self.assertEqual(fac('a'), result)

    def test_failsWithNoBaseSender(self):
        "stackSenders does require at least the base sender factory."
        self.assertRaises(TypeError, parsley.stackSenders)

    def test_senderFactoriesTakeOneArgument(self):
        "The callable returned by stackSenders takes exactly one argument."
        fac = parsley.stackSenders(nullFactory)
        self.assertRaises(TypeError, fac)
        self.assertRaises(TypeError, fac, 'a', 'b')


class StackReceiversTestCase(unittest.TestCase):
    def test_onlyBase(self):
        "stackReceivers can be called with no wrappers."
        fac = parsley.stackReceivers(nullFactory)
        self.assertEqual(fac('a', 'b'), ('a', 'b'))

    def test_oneWrapper(self):
        "stackReceivers can be called with one wrapper."
        fac = parsley.stackReceivers(nullFactory, wrapperFactory(0))
        self.assertEqual(fac('a', 'b'), (0, ('a', 'b')))

    def test_tenWrappers(self):
        "stackReceivers can be called with ten wrappers."
        wrappers = []
        result = 'a', 'b'
        for x in xrange(10):
            wrappers.append(wrapperFactory(x))
            result = x, result
        fac = parsley.stackReceivers(nullFactory, *wrappers)
        self.assertEqual(fac('a', 'b'), result)

    def test_failsWithNoBaseReceiver(self):
        "stackReceivers does require at least the base receiver factory."
        self.assertRaises(TypeError, parsley.stackReceivers)

    def test_receiverFactoriesTakeOneArgument(self):
        "The callable returned by stackReceivers takes exactly two arguments."
        fac = parsley.stackReceivers(nullFactory)
        self.assertRaises(TypeError, fac)
        self.assertRaises(TypeError, fac, 'a')
        self.assertRaises(TypeError, fac, 'a', 'b', 'c')
