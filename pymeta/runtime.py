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

class IterBuffer(object):
    """
    Wrapper for an iterable that allows pushing items onto it.
    """

    def __init__(self, iterable):
        """
        @param iterable: Any iterable Python object.
        """
        self.original = iterable
        if isinstance(iterable, str):
            self.iterable = (character(c) for c in iterable)
        elif isinstance(iterable, unicode):
            self.iterable = (unicodeCharacter(c) for c in iterable)
        else:
            self.iterable = iter(iterable)
        self.buffer = []
        self.markBuffers = []
        self.markPositions = []
        self.position = 0
        self.memo = {}
        self.args = []


    def getMemo(self, name):
        """
        Returns the memo record for the named rule.
        @param name: A rule name.
        """
        m = self.memo.get(self.position, None)
        if m:
            return m.get(name, None)


    def setMemo(self, pos, name, rec):
        """
        Store a memo record for the given value and position for the given
        rule.
        @param pos: A position in the input.
        @param name: A rule name.
        @param rec: A memo record.
        """
        self.memo.setdefault(pos, {})[name] = rec
        return rec


    def __iter__(self):
        return self


    def next(self):
        """
        Fetch the next item in the stream.
        """
        if self.args:
            val = self.args.pop()
        else:
            if self.buffer:
                val = self.buffer.pop()
            else:
                val = self.iterable.next()
            for buf in self.markBuffers:
                buf.append(val)
        self.position += 1
        self.lastThing = val
        return val


    def prev(self):
        """
        Rewind by a single item.
        """
        self.buffer.append(self.lastThing)
        for buf in self.markBuffers:
            if buf:
                del buf[-1]
        self.position -= 1
        del self.lastThing

    def push(self, obj):
        """
        Push an object onto the stream, such that it will be returned on the
        next call to next().
        """
        self.position -= 1
        self.args.append(obj)
        if self.position in self.memo:
            self.memo[self.position] = {}

    def mark(self):
        """
        Mark a position in the stream.
        """
        self.markPositions.append(self.position)
        self.markBuffers.append([])
        return len(self.markBuffers)-1


    def unmark(self, mark):
        """
        Register disinterest in returning to a previously marked stream
        position.
        """
        del self.markBuffers[mark:]
        del self.markPositions[mark:]


    def rewind(self, mark):
        """
        Return to a previously marked position in the stream.
        """
        saved = self.markBuffers[mark][::-1]
        self.buffer.extend(saved)
        self.position = self.markPositions[mark]
        self.unmark(mark)
        if len(saved) > 0:
            for buf in self.markBuffers:
                del buf[-len(saved):]


    def seekForwardTo(self, position):
        """
        Advance until the input reaches the requested position.
        """
        while position > self.position:
            self.next()

class LeftRecursion(object):
    """
    Marker for left recursion in a grammar rule.
    """
    detected = False

class OMetaBase(object):
    """
    Base class providing implementations of the fundamental OMeta operations.
    """
    globals = None
    def __init__(self, string, globals=None):
        """
        @param string: The string to be parsed.

        @param globals: A dictionary of names to objects, for use in evaluating
        embedded Python expressions.
        """
        self.input = IterBuffer(string)
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
                    self.input.push(arg)
                return rule()
            else:
                return rule(*args)
        memoRec = self.input.getMemo(ruleName)
        if memoRec is None:
            m = self.input.mark()
            oldPosition = self.input.position
            lr = LeftRecursion()
            memoRec = self.input.setMemo(self.input.position, ruleName, lr)

            memoRec = self.input.setMemo(self.input.position, ruleName,
                                         [rule(), self.input.position])
            if lr.detected:
                sentinel = self.input.position
                self.input.rewind(m)
                while True:
                    try:
                        m = self.input.mark()
                        ans = rule()
                        if (self.input.position == sentinel):
                            break

                        memoRec = self.input.setMemo(oldPosition, ruleName,
                                                     [ans, self.input.position])
                        self.input.rewind(m)
                    except ParseError:
                        break
            self.input.unmark(m)

        elif isinstance(memoRec, LeftRecursion):
            memoRec.detected = True
            raise ParseError()
        self.input.seekForwardTo(memoRec[1])
        return memoRec[0]


    def rule_anything(self):
        """
        Match a single item from the input of any kind.
        """
        try:
            return self.input.next()
        except StopIteration:
            raise ParseError()

    def exactly(self, wanted):
        """
        Match a single item from the input equal to the given specimen.

        @param wanted: What to match.
        """
        try:
            val = self.input.next()
        except StopIteration:
            raise ParseError()
        if wanted == val:
            return wanted
        else:
            self.input.prev()
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
                m = self.input.mark()
                ans.append(fn())
            except ParseError:
                self.input.rewind(m)
                break
            else:
                self.input.unmark(m)
        return ans

    def _or(self, fns):
        """
        Call each of a list of functions in sequence until one succeeds,
        rewinding the input between each.

        @param fns: A list of no-argument callables.
        """
        for f in fns:
            try:
                m = self.input.mark()
                ret = f()
                self.input.unmark(m)
                return ret
            except ParseError:
                self.input.rewind(m)
        raise ParseError()

    def _not(self, fn):
        """
        Call the given function. Raise ParseError iff it does not.

        @param fn: A callable of no arguments.
        """
        try:
            fn()
        except ParseError:
            return True
        else:
            raise ParseError()

    def eatWhitespace(self):
        """
        Consume input until a non-whitespace character is reached.
        """
        for c in self.input:
            if not c.isspace():
                self.input.prev()
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
        oldInput = self.input
        m = self.input.mark()
        try:
            try:
                list = IterBuffer(self.rule_anything())
                self.input = list
            except TypeError:
                oldInput.rewind(m)
                raise ParseError()
            else:
                oldInput.unmark(m)
            r = expr()
            self.end()
        finally:
            self.input = oldInput
        return r


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
            m = self.input.mark()
            x = f()
            return x
        finally:
            self.input.rewind(m)


    def token(self, tok):
        """
        Match and return the given string, consuming any preceding whitespace.
        """
        m = self.input.mark()
        try:
            self.eatWhitespace()
            for c in tok:
                self.exactly(c)
            self.input.unmark(m)
            return tok
        except ParseError:
            self.input.rewind(m)
            raise

    rule_token = token

    def letter(self):
        """
        Match a single letter.
        """
        try:
            x = self.input.next()
            if x.isalpha():
                return x
            else:
                self.input.prev()
                raise ParseError
        except StopIteration:
            raise ParseError

    rule_letter = letter

    def letterOrDigit(self):
        """
        Match a single alphanumeric character.
        """
        try:
            x = self.input.next()
        except StopIteration:
            raise ParseError()
        if x.isalnum() or x == '_':
            return x
        else:
            self.input.prev()
            raise ParseError()

    rule_letterOrDigit = letterOrDigit

    def digit(self):
        """
        Match a single digit.
        """
        try:
            x = self.input.next()
        except StopIteration:
            raise ParseError()
        if x.isdigit():
            return x
        else:
            self.input.prev()
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
        for c in self.input:
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
                    for strc in self.input:
                        expr.append(strc)
                        if strc == c:
                            break
        else:
            endchar = None
        if len(stack) > 0:
            raise ParseError()
        return ''.join(expr).strip(), endchar
