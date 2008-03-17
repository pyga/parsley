import string
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
        self.original = iterable
        if isinstance(iterable, str):
            self.iterable = (character(c) for c in iterable)
        else:
            self.iterable = iter(iterable)
        self.buffer = []
        self.markBuffers = []
        self.markPositions = []
        self.position = 0
        self.memo = {}
        self.args = []

    def getMemo(self, name):
        m = self.memo.get(self.position, None)
        if m:
            return m.get(name, None)

    def setMemo(self, pos, name, rec):
        self.memo.setdefault(pos, {})[name] = rec
        return rec

    def __iter__(self):
        return self


    def next(self):
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
        self.buffer.append(self.lastThing)
        for buf in self.markBuffers:
            if buf:
                del buf[-1]
        self.position -= 1
        del self.lastThing

    def push(self, obj):
        self.position -= 1
        self.args.append(obj)
        if self.position in self.memo:
            self.memo[self.position] = {}

    def mark(self):
        self.markPositions.append(self.position)
        self.markBuffers.append([])
        return len(self.markBuffers)-1


    def unmark(self, mark):
        del self.markBuffers[mark:]
        del self.markPositions[mark:]


    def rewind(self, mark):
        saved = self.markBuffers[mark][::-1]
        self.buffer.extend(saved)
        self.position = self.markPositions[mark]
        self.unmark(mark)
        if len(saved) > 0:
            for buf in self.markBuffers:
                del buf[-len(saved):]


    def seekTo(self, position):
        if position > self.position:
            while position > self.position:
                self.next()
            return
        elif position < self.position:
            try:
                i = self.markPositions.index(position)
            except ValueError:
                raise RuntimeError("Tried to seek to an unsaved position", position)
            self.rewind(i)


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
        self.input = IterBuffer(string)
        if self.globals is None:
            if globals is None:
                self.globals = {}
            else:
                self.globals = globals

    def hasRule(self, name):
        return (name in self.__ometa_rules__
                or hasattr(self, "rule_"+name))


    def getRule(self, name):
        r = self.__ometa_rules__.get(name, None)
        if r is None:
            if hasattr(self, "rule_"+name):
                return getattr(self, "rule_"+name)
            else:
                raise NameError("No rule named '%s'" %(name,))
        else:
            return r.__get__(self)


    def apply(self, ruleName, *args):
        rule = self.getRule(ruleName)
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
                pass
            self.input.unmark(m)

        elif isinstance(memoRec, LeftRecursion):
            memoRec.detected = True
            raise ParseError()
        self.input.seekTo(memoRec[1])
        return memoRec[0]


    def rule_anything(self):
        try:
            return self.input.next()
        except StopIteration:
            raise ParseError()

    def exactly(self, wanted):
        try:
            val = self.input.next()
        except StopIteration:
            raise ParseError()
        if wanted == val:
            return wanted
        else:
            self.input.prev()
            raise ParseError()


    def many(self, fn, *initial):
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
        try:
            fn()
        except ParseError:
            return True
        else:
            raise ParseError()

    def eatWhitespace(self):
        for c in self.input:
            if not c.isspace():
                self.input.prev()
                break
        return True
    rule_spaces = eatWhitespace

    def pred(self, expr):
        if not expr():
            raise ParseError()
        else:
            return True

    def listpattern(self, expr):
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
        return self._not(self.rule_anything)


    def lookahead(self, f):
        try:
            m = self.input.mark()
            x = f()
            return x
        finally:
            self.input.rewind(m)


    def newline(self):
        for c in self.input:
            if c in '\r\n':
                break
            if not c.isspace():
                self.input.prev()
                raise ParseError()
        for c in self.input:
            if c not in '\r\n':
                self.input.prev()
                break
        return True


    def token(self, tok):
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
        try:
            x = self.input.next()
        except StopIteration:
            raise ParseError()
        if x.isdigit():
            return x
        else:
            self.input.prev()
            raise ParseError()

    def hexdigit(self):
        try:
            x = self.input.next()
        except StopIteration:
            raise ParseError()
        if x in string.hexdigits:
            return x
        else:
            self.input.prev()
            raise ParseError()


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
