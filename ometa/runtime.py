# -*- test-case-name: ometa.test.test_runtime -*-
"""
Code needed to run a grammar after it has been compiled.
"""
import operator
from textwrap import dedent
from terml.twine import asTwineFrom
from terml.nodes import termMaker as t
from ometa.builder import moduleFromGrammar, writePython

class ParseError(Exception):
    """
    ?Redo from start
    """

    @property
    def position(self):
        return self.args[0]


    @property
    def error(self):
        return self.args[1]


    def __init__(self, input, *a):
        Exception.__init__(self, *a)
        self.input = input
        if len(a) > 2:
            self.message = a[2]


    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return (self.position, self.error) == (other.position, other.error)


    def formatReason(self):
        if self.error is None:
            return "Syntax error"
        if len(self.error) == 1:
            if self.error[0][0] == 'message':
                return self.error[0][1]
            if self.error[0][2] == None:
                return 'expected a ' + self.error[0][1]
            else:
                typ = self.error[0][1]
                if typ is None:
                    if isinstance(self.input, basestring):
                        typ = 'character'
                    else:
                        typ = 'object'
                return 'expected the %s %r' % (typ,
                                               self.error[0][2])
        else:
            bits = []
            for s in self.error:
                if s[2] is None:
                    desc = "a " + s[1]
                else:
                    desc = repr(s[2])
                    if s[1] is not None:
                        desc = "%s %s" % (s[1], desc)
                bits.append(desc)
            bits.sort()
            return "expected one of %s, or %s" % (', '.join(bits[:-1]),
                                                  bits[-1])


    def formatError(self):
        """
        Return a pretty string containing error info about string
        parsing failure.
        """
        #de-twineifying
        lines = str(self.input).split('\n')
        counter = 0
        lineNo = 1
        columnNo = 0
        for line in lines:
            newCounter = counter + len(line)
            if newCounter > self.position:
                columnNo = self.position - counter
                break
            else:
                counter += len(line) + 1
                lineNo += 1
        reason = self.formatReason()
        return ('\n' + line + '\n' + (' ' * columnNo + '^') +
                "\nParse error at line %s, column %s: %s\n" % (lineNo,
                                                               columnNo,
                                                               reason))


    def formatErrorTwine(self):
        """
        Report errors based on position info in Twine input.
        """
        reason = self.formatReason()
        map = self.input.sourceMap
        start = 0
        end = len(map)
        test = end / 2
        for _ in xrange(10):
            candidate = map[test]
            print start, end, test, candidate, self.position
            if (candidate[0][0] <= self.position
                and candidate[0][1] >= self.position):
                span = candidate[1]
                offset = self.position - candidate[0][0]
                lineNo = span.startLine
                columnNo = span.startCol + offset
                line = self.input[candidate[0][0]:candidate[0][1]]
                break
            elif candidate[0][0] > self.position:
                end = test
                test = start + ((end - start) / 2)
            elif candidate[0][1] < self.position:
                start = test
                test = start + ((end - start) / 2)
            elif test < end:
                test += 1
        else:
            span = None

        return ('\n' +  line + (' ' * columnNo+ '^') +
                "\nParse error at line %s, column %s: %s\n" % (lineNo,
                                                               columnNo,
                                                               reason))


    def __str__(self):
        return self.formatError()


class EOFError(ParseError):
    """
    Raised when the end of input is encountered.
    """
    def __init__(self, input, position):
        ParseError.__init__(self, input, position, eof())


def expected(typ, val=None):
    """
    Return an indication of expected input and the position where it was
    expected and not encountered.
    """

    return [("expected", typ, val)]


def eof():
    """
    Return an indication that the end of the input was reached.
    """
    return [("message", "end of input")]

_go = False
def joinErrors(errors):
    """
    Return the error from the branch that matched the most of the input.
    """
    errors.sort(reverse=True, key=operator.itemgetter(0))
    results = set()
    pos = errors[0][0]
    for err in errors:
        if pos == err[0]:
            e = err[1]
            if e is not None:
                for item in e:
                        results.add(item)
        else:
            break

    return [pos, list(results) or None]


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
        if isinstance(iterable, (character, unicodeCharacter)):
            raise TypeError("Characters are not iterable")
        if isinstance(iterable, str):
            return WrappedValueInputStream(iterable, 0, wrapper=character)
        elif isinstance(iterable, unicode):
            return WrappedValueInputStream(iterable, 0,
                                           wrapper=unicodeCharacter)
        else:
            return cls(list(iterable), 0)
    fromIterable = classmethod(fromIterable)


    def fromFile(cls, f, encoding='utf-8'):
        if getattr(f, 'seek', None) and gettattr(f, 'tell', None):
            position = f.tell()
            f.seek(0)
        else:
            position = 0
        t = asTwineFrom(f.read(), getattr(f, 'name', repr(f)))
        return cls(t, 0)
    fromFile = classmethod(fromFile)


    def fromText(cls, t, name="<string>"):
        if getattr(t, 'span', None):
            return cls(t, 0)
        return cls(asTwineFrom(t, name), 0)
    fromText = classmethod(fromText)


    def __init__(self, data, position):
        self.data = data
        self.position = position
        self.memo = {}
        self.tl = None

    def head(self):
        if self.position >= len(self.data):
            raise EOFError(self, self.position)
        return self.data[self.position], [self.position, None]

    def nullError(self):
        return [self.position, None]

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

    def __cmp__(self, other):
        return cmp((self.data, self.position), (other.data, other.position))


class WrappedValueInputStream(InputStream):

    def __init__(self, data, position, wrapper=None):
        InputStream.__init__(self, data, position)
        self.wrapper = wrapper

    def head(self):
        v, e = InputStream.head(self)
        return self.wrapper(v), e

    def tail(self):
        if self.tl is None:
            self.tl = WrappedValueInputStream(self.data, self.position+1,
                                              self.wrapper)
        return self.tl


class ArgInput(object):
    def __init__(self, arg, parent):
        self.arg = arg
        self.parent = parent
        self.memo = {}
        self.err = parent.nullError()

    @property
    def data(self):
        return self.parent.data

    def head(self):
        return self.arg, self.err

    def tail(self):
        return self.parent



    def nullError(self):
        return self.parent.nullError()


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
    tree = False
    def __init__(self, string, globals=None, name='<string>', tree=False):
        """
        @param string: The string to be parsed.

        @param globals: A dictionary of names to objects, for use in evaluating
        embedded Python expressions.

        @param tree: Whether the input should be treated as part of a
        tree of nested iterables, rather than being a standalone
        string.
        """
        if self.tree or tree:
            self.input = InputStream.fromIterable(string)
        else:
            self.input = InputStream.fromText(string)
        self.locals = {}
        if self.globals is None:
            if globals is None:
                self.globals = {}
            else:
                self.globals = globals

        self.currentError = self.input.nullError()

    def considerError(self, error):
        if error:
            if error[0] > self.currentError[0]:
                self.currentError = error
            elif error[0] == self.currentError[0]:
                self.currentError = joinErrors([error, self.currentError])


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
            val, err = self._apply(r, ruleName, args)
            return val, ParseError(self.input.data, *err)

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
            if ((not getattr(rule, 'func_code', None))
                 or rule.func_code.co_argcount - 1 != len(args)):
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

            #print "Calling", ruleName
            try:
                memoRec = self.input.setMemo(ruleName,
                                             [rule(), self.input])
            except ParseError:
                #print "Failed", rule
                raise
            #print "Success", ruleName, memoRec
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
            raise ParseError(self.input.data, *self.input.nullError())
        self.input = memoRec[1]
        return memoRec[0]


    def exactly(self, wanted):
        """
        Match a single item from the input equal to the given specimen.

        @param wanted: What to match.
        """
        i = self.input
        val, p = self.input.head()
        self.input = self.input.tail()
        if wanted == val:
            return val, p
        else:
            self.input = i
            raise ParseError(self.input.data, p[0], expected(None, wanted))


    def many(self, fn, *initial):
        """
        Call C{fn} until it fails to match the input. Collect the resulting
        values into a list.

        @param fn: A callable of no arguments.
        @param initial: Initial values to populate the returned list with.
        """
        ans = []
        for x, e in initial:
            ans.append(x)
        while True:
            try:
                m = self.input
                v, _ = fn()
                ans.append(v)
            except ParseError, e:
                self.input = m
                break
        return ans, e


    def repeat(self, min, max, fn):
        """
        Call C{fn} C{max} times or until it fails to match the
        input. Fail if less than C{min} matches were made.
        Collect the results into a list.
        """
        ans = []
        for i in range(min):
            v, e = fn()
            ans.append(v)

        for i in range(min, max):
            try:
                m = self.input
                v, e = fn()
                ans.append(v)
            except ParseError, e:
                self.input = m
                break
        return ans, e

    def _or(self, fns):
        """
        Call each of a list of functions in sequence until one succeeds,
        rewinding the input between each.

        @param fns: A list of no-argument callables.
        """
        errors = []
        for f in fns:
            try:
                m = self.input
                ret, err = f()
                errors.append(err)
                return ret, joinErrors(errors)
            except ParseError, e:
                errors.append(e)
                self.input = m
        raise ParseError(self.input.data, *joinErrors(errors))


    def _not(self, fn):
        """
        Call the given function. Raise ParseError iff it does not.

        @param fn: A callable of no arguments.
        """
        m = self.input
        try:
            fn()
        except ParseError, e:
            self.input = m
            return True, self.input.nullError()
        else:
            raise ParseError(self.input.data, *self.input.nullError())


    def eatWhitespace(self):
        """
        Consume input until a non-whitespace character is reached.
        """
        while True:
            try:
                c, e = self.input.head()
            except EOFError, e:
                break
            t = self.input.tail()
            if c.isspace():
                self.input = t
            else:
                break
        return True, e


    def pred(self, expr):
        """
        Call the given function, raising ParseError if it returns false.

        @param expr: A callable of no arguments.
        """
        val, e = expr()
        if not val:
            raise ParseError(self.input.data, *e)
        else:
            return True, e


    def listpattern(self, expr):
        """
        Call the given function, treating the next object on the stack as an
        iterable to be used for input.

        @param expr: A callable of no arguments.
        """
        v, e = self.rule_anything()
        oldInput = self.input
        try:
            self.input = InputStream.fromIterable(v)
        except TypeError:
            e = self.input.nullError()
            e[1] = expected("an iterable")
            raise ParseError(self.input.data, *e)
        expr()
        self.end()
        self.input = oldInput
        return v, e


    def consumedby(self, expr):
        oldInput = self.input
        _, e = expr()
        slice = oldInput.data[oldInput.position:self.input.position]
        return slice, e


    def end(self):
        """
        Match the end of the stream.
        """
        return self._not(self.rule_anything)


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
                v, e = self.exactly(c)
            return tok, e
        except ParseError, e:
            self.input = m

            raise ParseError(self.input.data, e[0], expected("token", tok))


    def letter(self):
        """
        Match a single letter.
        """
        x, e = self.rule_anything()
        if x.isalpha():
            return x, e
        else:
            e[1] = expected("letter")
            raise ParseError(self.input.data, *e)


    def letterOrDigit(self):
        """
        Match a single alphanumeric character.
        """
        x, e = self.rule_anything()
        if x.isalnum() or x == '_':
            return x, e
        else:
            e[1] = expected("letter or digit")
            raise ParseError(self.input.data, *e)


    def digit(self):
        """
        Match a single digit.
        """
        x, e = self.rule_anything()
        if x.isdigit():
            return x, e
        else:
            e[1] = expected("digit")
            raise ParseError(self.input.data, *e)

    rule_digit = digit

    rule_letterOrDigit = letterOrDigit
    rule_letter = letter
    rule_token = token
    rule_end = end
    rule_spaces = eatWhitespace
    rule_exactly = exactly


    def rule_anything(self):
        """
        Match a single item from the input of any kind.
        """
        h, p = self.input.head()
        self.input = self.input.tail()
        return h, p



class OMetaGrammarBase(OMetaBase):
    """
    Common methods for the OMeta grammar parser itself, and its variants.
    """

    @classmethod
    def makeGrammar(cls, grammar, globals, name='Grammar', superclass=None):
        """
        Define a new parser class with the rules in the given grammar.

        @param grammar: A string containing a PyMeta grammar.
        @param globals: A dict of names that should be accessible by this
        grammar.
        @param name: The name of the class to be generated.
        @param superclass: The class the generated class is a child of.
        """
        g = cls(grammar)
        tree = g.parseGrammar(name)
        modname = "pymeta_grammar__" + name
        filename = "/pymeta_generated_code/" + modname + ".py"
        source = writePython(tree)

        return moduleFromGrammar(source, name, superclass or OMetaBase, globals,
                                 modname, filename)


    def __init__(self, grammar, *a, **kw):
        OMetaBase.__init__(self, dedent(grammar), *a, **kw)


    def parseGrammar(self, name):
        """
        Entry point for converting a grammar to code (of some variety).

        @param name: The name for this grammar.

        @param builder: A class that implements the grammar-building interface
        (interface to be explicitly defined later)
        """
        self.name = name
        res, err = self.apply("grammar")
        try:
            x = self.input.head()
        except EOFError:
            pass
        else:
            raise err
        return res


    def applicationArgs(self, finalChar):
        """
        Collect rule arguments, a list of Python expressions separated by
        spaces.
        """
        args = []
        while True:
            try:
                (arg, endchar), err = self.pythonExpr(" " + finalChar)
                if not arg:
                    break
                args.append(t.Action(arg))
                if endchar == finalChar:
                    break
                if endchar == ' ':
                    self.rule_anything()
            except ParseError:
                break
        if args:
            return args
        else:
            raise ParseError(self.input.data, )

    def ruleValueExpr(self, singleLine, span=None):
        """
        Find and generate code for a Python expression terminated by a close
        paren/brace or end of line.
        """
        (expr, endchar), err = self.pythonExpr(endChars="\r\n)]")
        # if str(endchar) in ")]" or (singleLine and endchar):
        #     self.input = self.input.prev()
        return t.Action(expr, span=span)

    def semanticActionExpr(self, span=None):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value is ignored.
        """
        val = t.Action(self.pythonExpr(')')[0][0], span=span)
        self.exactly(')')
        return val

    def semanticPredicateExpr(self, span=None):
        """
        Find and generate code for a Python expression terminated by a
        close-paren, whose return value determines the success of the pattern
        it's in.
        """
        expr = t.Action(self.pythonExpr(')')[0][0], span=span)
        self.exactly(')')
        return t.Predicate(expr, span=span)


    def eatWhitespace(self):
        """
        Consume input until a non-whitespace character is reached.
        """
        consumingComment = False
        while True:
            try:
                c, e = self.input.head()
            except EOFError, e:
                break
            t = self.input.tail()
            if c.isspace() or consumingComment:
                self.input = t
                if c == '\n':
                    consumingComment = False
            elif c == '#':
                consumingComment = True
            else:
                break
        return True, e
    rule_spaces = eatWhitespace


    def pythonExpr(self, endChars="\r\n"):
        """
        Extract a Python expression from the input and return it.

        @arg endChars: A set of characters delimiting the end of the expression.
        """
        delimiters = { "(": ")", "[": "]", "{": "}"}
        stack = []
        expr = []
        endchar = None
        while True:
            try:
                c, e = self.rule_anything()
                endchar = c
            except ParseError, e:
                endchar = None
                break
            if c in endChars and len(stack) == 0:
                self.input = self.input.prev()
                break
            else:
                expr.append(c)
                if c in delimiters:
                    stack.append(delimiters[c])
                elif len(stack) > 0 and c == stack[-1]:
                    stack.pop()
                elif c in delimiters.values():
                    raise ParseError(self.input.data, self.input.position,
                                     expected("Python expression"))
                elif c in "\"'":
                    while True:
                        strc, stre = self.rule_anything()
                        expr.append(strc)
                        slashcount = 0
                        while strc == '\\':
                            strc, stre = self.rule_anything()
                            expr.append(strc)
                            slashcount += 1
                        if strc == c and slashcount % 2 == 0:
                            break

        if len(stack) > 0:
            raise ParseError(self.input.data, self.input.position,
                             expected("Python expression"))
        return (''.join(expr).strip(), endchar), e


    def startSpan(self):
        return self.input.position

    def span(self, start):
        end = self.input.position
        return self.input.data[start:end].span
