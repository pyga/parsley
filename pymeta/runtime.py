"""
Code needed to run a grammar after it has been compiled.
"""
class ParseError(Exception):
    """
    ?Redo from start
    """

class character(str):
    """
    Type to allow distinguishing characters from strings.
    """

    def __iter__(self):
        """
        Prevent string patterns and list patterns from matching single
        characters.
        """
        raise TypeError("Characters are not iterable")

class unicodeCharacter(unicode):
    """
    Type to distinguish characters from Unicode strings.
    """
    def __iter__(self):
        """
        Prevent string patterns and list patterns from matching single
        characters.
        """
        raise TypeError("Characters are not iterable")

class InputStream(object):
    """
    The basic input mechanism used by OMeta grammars.
    """

    def fromIterable(cls, iterable):
        """
        @param iterable: Any iterable Python object.
        """
        if isinstance(iterable, str):
            data = [character(c) for c in iterable]
        elif isinstance(iterable, unicode):
            data = [unicodeCharacter(c) for c in iterable]
        else:
            data = list(iterable)
        return cls(data, 0)
    fromIterable = classmethod(fromIterable)

    def __init__(self, data, position):
        self.data = data
        self.position = position
        self.memo = {}
        self.tl = None

    def head(self):
        if self.position >= len(self.data):
            raise IndexError("out of range")
        return self.data[self.position]

    def tail(self):
        if self.tl is None:
            self.tl = InputStream(self.data, self.position+1)
        return self.tl

    def prev(self):
        return InputStream(self.data, self.position-1)

    def getMemo(self, name):
        """
        Returns the memo record for the named rule.
        @param name: A rule name.
        """
        return self.memo.get(name, None)


    def setMemo(self, name, rec):
        """
        Store a memo record for the given value and position for the given
        rule.
        @param name: A rule name.
        @param rec: A memo record.
        """
        self.memo[name] = rec
        return rec

class ArgInput(object):
    def __init__(self, arg, parent):
        self.arg = arg
        self.parent = parent
        self.memo = {}

    def head(self):
        return self.arg

    def tail(self):
        return self.parent


    def getMemo(self, name):
        """
        Returns the memo record for the named rule.
        @param name: A rule name.
        """
        return self.memo.get(name, None)


    def setMemo(self, name, rec):
        """
        Store a memo record for the given value and position for the given
        rule.
        @param name: A rule name.
        @param rec: A memo record.
        """
        self.memo[name] = rec
        return rec


class LeftRecursion(object):
    """
    Marker for left recursion in a grammar rule.
    """
    detected = False

class OMetaBase(object):
    """
    Base class providing implementations of the fundamental OMeta
    operations. Built-in rules are defined here.
    """
    globals = None
    def __init__(self, string, globals=None):
        """
        @param string: The string to be parsed.

        @param globals: A dictionary of names to objects, for use in evaluating
        embedded Python expressions.
        """
        self.input = InputStream.fromIterable(string)
        self.locals = {}
        if self.globals is None:
            if globals is None:
                self.globals = {}
            else:
                self.globals = globals


    def superApply(self, ruleName, *args):
        """
        Apply the named rule as defined on this object's superclass.

        @param ruleName: A rule name.
        """
        r = getattr(super(self.__class__, self), "rule_"+ruleName, None)
        if r is not None:
            self.input.setMemo(ruleName, None)
            return self._apply(r, ruleName, args)
        else:
            raise NameError("No rule named '%s'" %(ruleName,))

    def apply(self, ruleName, *args):
        """
        Apply the named rule, optionally with some arguments.

        @param ruleName: A rule name.
        """
        r = getattr(self, "rule_"+ruleName, None)
        if r is not None:
            return self._apply(r, ruleName, args)

        else:
            raise NameError("No rule named '%s'" %(ruleName,))


    def _apply(self, rule, ruleName, args):
        """
        Apply a rule method to some args.
        @param rule: A method of this object.
        @param ruleName: The name of the rule invoked.
        @param args: A sequence of arguments to it.
        """
        if args:
            if rule.func_code.co_argcount - 1 != len(args):
                for arg in args[::-1]:
                    self.input = ArgInput(arg, self.input)
                return rule()
            else:
                return rule(*args)
        memoRec = self.input.getMemo(ruleName)
        if memoRec is None:
            oldPosition = self.input
            lr = LeftRecursion()
            memoRec = self.input.setMemo(ruleName, lr)

            memoRec = self.input.setMemo(ruleName,
                                         [rule(), self.input])
            if lr.detected:
                sentinel = self.input
                while True:
                    try:
                        self.input = oldPosition
                        ans = rule()
                        if (self.input == sentinel):
                            break

                        memoRec = oldPosition.setMemo(ruleName,
                                                     [ans, self.input])
                    except ParseError:
                        break
            self.input = oldPosition

        elif isinstance(memoRec, LeftRecursion):
            memoRec.detected = True
            raise ParseError()
        self.input = memoRec[1]
        return memoRec[0]


    def rule_anything(self):
        """
        Match a single item from the input of any kind.
        """
        try:
            h = self.input.head()
            self.input = self.input.tail()
            return h
        except IndexError:
            raise ParseError()

    def exactly(self, wanted):
        """
        Match a single item from the input equal to the given specimen.

        @param wanted: What to match.
        """
        i = self.input
        try:
            val = self.input.head()
            self.input = self.input.tail()
        except IndexError:
            raise ParseError()
        if wanted == val:
            return wanted
        else:
            self.input = i
            raise ParseError()

    rule_exactly = exactly

    def many(self, fn, *initial):
        """
        Call C{fn} until it fails to match the input. Collect the resulting
        values into a list.

        @param fn: A callable of no arguments.
        @param initial: Initial values to populate the returned list with.
        """
        ans = list(initial)
        while True:
            try:
                m = self.input
                ans.append(fn())
            except ParseError:
                self.input = m
                break
        return ans

    def _or(self, fns):
        """
        Call each of a list of functions in sequence until one succeeds,
        rewinding the input between each.

        @param fns: A list of no-argument callables.
        """
        for f in fns:
            try:
                m = self.input
                ret = f()
                return ret
            except ParseError:
                self.input = m
        raise ParseError()

    def _not(self, fn):
        """
        Call the given function. Raise ParseError iff it does not.

        @param fn: A callable of no arguments.
        """
        m = self.input
        try:
            fn()
        except ParseError:
            self.input = m
            return True
        else:
            raise ParseError()

    def eatWhitespace(self):
        """
        Consume input until a non-whitespace character is reached.
        """
        while True:
            try:
                c = self.input.head()
            except IndexError:
                break
            t = self.input.tail()
            if c.isspace():
                self.input = t
            else:
                break
        return True
    rule_spaces = eatWhitespace

    def pred(self, expr):
        """
        Call the given function, raising ParseError if it returns false.

        @param expr: A callable of no arguments.
        """
        if not expr():
            raise ParseError()
        else:
            return True

    def listpattern(self, expr):
        """
        Call the given function, treating the next object on the stack as an
        iterable to be used for input.

        @param expr: A callable of no arguments.
        """
        v = self.rule_anything()
        oldInput = self.input
        try:
            self.input = InputStream.fromIterable(v)
        except TypeError:
            raise ParseError()
        r = expr()
        self.end()
        self.input = oldInput
        return v


    def end(self):
        """
        Match the end of the stream.
        """
        return self._not(self.rule_anything)

    rule_end = end

    def lookahead(self, f):
        """
        Execute the given callable, rewinding the stream no matter whether it
        returns successfully or not.

        @param f: A callable of no arguments.
        """
        try:
            m = self.input
            x = f()
            return x
        finally:
            self.input = m


    def token(self, tok):
        """
        Match and return the given string, consuming any preceding whitespace.
        """
        m = self.input
        try:
            self.eatWhitespace()
            for c in tok:
                self.exactly(c)
            return tok
        except ParseError:
            self.input = m
            raise

    rule_token = token

    def letter(self):
        """
        Match a single letter.
        """
        try:
            x = self.input.head()
            if x.isalpha():
                self.input = self.input.tail()
                return x
            else:
                raise ParseError()
        except IndexError:
            raise ParseError()

    rule_letter = letter

    def letterOrDigit(self):
        """
        Match a single alphanumeric character.
        """
        try:
            x = self.input.head()
        except IndexError:
            raise ParseError()
        if x.isalnum() or x == '_':
            self.input = self.input.tail()
            return x
        else:
            raise ParseError()

    rule_letterOrDigit = letterOrDigit

    def digit(self):
        """
        Match a single digit.
        """
        try:
            x = self.input.head()
        except IndexError:
            raise ParseError()
        if x.isdigit():
            self.input = self.input.tail()
            return x
        else:
            raise ParseError()

    rule_digit = digit


    def pythonExpr(self, endChars="\r\n"):
        """
        Extract a Python expression from the input and return it.

        @arg endChars: A set of characters delimiting the end of the expression.
        """
        delimiters = { "(": ")", "[": "]", "{": "}"}
        stack = []
        expr = []
        while True:
            try:
                c = self.rule_anything()
            except ParseError:
                endchar = None
                break
            if c in endChars and len(stack) == 0:
                endchar = c
                break
            else:
                expr.append(c)
                if c in delimiters:
                    stack.append(delimiters[c])
                elif len(stack) > 0 and c == stack[-1]:
                    stack.pop()
                elif c in delimiters.values():
                    raise ParseError()
                elif c in "\"'":
                    while True:
                        strc = self.rule_anything()
                        expr.append(strc)
                        if strc == c:
                            break
        if len(stack) > 0:
            raise ParseError()
        return ''.join(expr).strip(), endchar
