import string
from types import FunctionType
from compiler import ast, compile as python_compile
from compiler.pycodegen import ExpressionCodeGenerator

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
            del buf[-1]
        self.position -= 1
        del self.lastThing

    def push(self, obj):
        self.position -= 1
        self.buffer.append(obj)
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
    def __init__(self, string):
        self.input = IterBuffer(string)


    def hasRule(self, name):
        return (name in self.__ometa_rules__
                or hasattr(self, "rule_"+name))


    def getRule(self, name):
        r = self.__ometa_rules__.get(name, None)
        if r is None and hasattr(self, "rule_"+name):
            return getattr(self, "rule_"+name)
        else:
            return r.__get__(self)


    def apply(self, ruleName, *args):
        rule = self.getRule(ruleName)
        if args:
            for arg in args[::-1]:
                self.input.push(arg)
            return rule()
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
        return ''.join(expr).strip(), c


def compile(grammar, name="<grammar>"):
    """
    Compile an OMeta grammar and return an object whose methods invoke its
    productions on their first argument.
    """

    ab, rules = parseGrammar(grammar, name)
    ruleMethods = dict([(k, ab.compileAstMethod(k, v))
                         for (k, v) in rules.iteritems()])
    methodDict = {'__ometa_rules__': ruleMethods}
    grammarClass = type(name, (OMetaBase,), methodDict)
    return HandyWrapper(grammarClass)

class HandyWrapper(object):
    """
    Convenient grammar wrapper for parsing strings.
    """
    def __init__(self, klass):
        self.klass = klass
    def __getattr__(self, name):
        def doIt(str):
            obj = self.klass(str)
            ret = obj.apply(name)
            extra = list(obj.input)
            if not extra:
                try:
                    return ''.join(ret)
                except TypeError:
                    return ret
            else:
                raise ParseError("trailing garbage in input: %s" % (extra,))
        return doIt

def parseGrammar(grammar, name="<grammar>"):
    ab = AstBuilder(name)
    g = OMetaGrammar(grammar)
    g.ab = ab
    res = g.rule_grammar()
    x = list(g.input)
    if x:
        try:
            x = repr(''.join(x))
        except TypeError:
            pass
        raise ParseError("Grammar parse failed. Leftover bits: %s" % (x,))
    return ab, res

class OMetaGrammar(OMetaBase):
    """
    Grammar parser.
    """
    __ometa_rules__ = {}
    def rule_application(self):
        self.token("<")
        self.eatWhitespace()
        name = self.rule_name()
        try:
            self.exactly(" ")
            args = []
            while True:
                try:
                    arg, endchar = self.pythonExpr(" >")
                    if not arg:
                        break
                    args.append(arg)
                    if endchar == '>':
                        break
                except ParseError:
                    break
            exprs = [self.ab.compilePythonExpr(self.name, arg) for arg in args]
        except ParseError:
            exprs = []
            self.token(">")

        return self.ab.apply(name, *exprs)


    def rule_number(self):
        self.eatWhitespace()
        isHex = 0
        isOctal = 0
        buf = []
        try:
            buf.append(self.exactly("-"))
        except ParseError:
            pass
        d = self.digit()
        buf.append(d)
        if d == '0':
            isOctal = 1
        try:
            try:
                buf.append(self.digit())
            except ParseError:
                if isOctal:
                    try:
                        buf.append(self.exactly('x'))
                    except ParseError:
                        buf.append(self.exactly('X'))
                    isHex = 1
                    isOctal = 0
            while True:
                try:
                    buf.append(self.hexdigit())
                except ParseError:
                    break

        except ParseError:
            pass
        s = ''.join(buf)
        if isHex:
            i = int(s, 16)
        elif isOctal:
            i = int(s, 8)
        else:
            i = int(s)
        return self.ab.exactly(ast.Const(i))
    def rule_character(self):
        self.token("'")
        r = self.apply("anything")
        if (r == "\\"):
            r += self.apply("anything")
        self.token("'")
        return self.ab.exactly(ast.Const(r))


    def rule_name(self):
        x  = self.letter()
        xs = self.many(self.letterOrDigit)
        xs.insert(0, x)
        return ''.join(xs)

    def rule_expr1(self):
        try:
            r = self.apply("application")
        except ParseError:
            try:
                r = self.ab.compilePythonExpr(self.name,
                                              self.apply("ruleValue"))
            except ParseError:
                try:
                    r = self.apply("semanticPredicate")
                except ParseError:
                    try:
                        r = self.apply("number")
                    except ParseError:
                        try:
                            r = self.apply("character")
                        except ParseError:
                            try:
                                self.token("(")
                                r = self.apply("expr")
                                self.token(")")
                            except ParseError:
                                self.token("[")
                                try:
                                    self.token("]")
                                    r = self.ab.listpattern([])
                                except ParseError:
                                    e = self.apply("expr")
                                    self.token("]")
                                    r = self.ab.listpattern(e)
        return r

    def rule_expr2(self):
        try:
            self.token("~")
            r = self.apply("expr2")
            return self.ab._not(r)
        except ParseError:
            pass
        return self.apply("expr1")


    def rule_expr3(self):
        try:
            r = self.apply("expr2")
            try:
                self.token("*")
                r = self.ab.many(r)
            except ParseError:
                try:
                    self.token("+")
                    r = self.ab.many1(r)
                except ParseError:
                    pass
            try:
                self.exactly(":")
                name = self.apply("name")
                r = self.ab.bind(r, name)
            except ParseError:
                pass
            return r
        except ParseError:
            self.token(":")
            name = self.apply("name")
            r = self.ab.apply("anything")
            return self.ab.bind(r, name)

    def rule_expr4(self):
        return self.ab.sequence(self.many(lambda: self.apply("expr3")))


    def rule_expr(self):
        ans = [self.apply("expr4")]
        m = -1
        try:
            while True:
                m = self.input.mark()
                self.token("|")
                ans.append(self.apply("expr4"))
                self.input.unmark(m)
        except ParseError:
            if m >= 0:
                self.input.rewind(m)

        return self.ab._or(ans)

    def rule_ruleValue(self):
        self.token("=>")
        #this feels a bit hackish...
        expr, endchar = self.pythonExpr(endChars="\r\n)]")
        if endchar in ')]':
            self.input.prev()
        return expr

    def rule_semanticPredicate(self):
        self.token("?(")
        expr = self.ab.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.ab.pred(expr)

    def rule_rulePart(self):
        requiredName = self.apply("anything")
        self.eatWhitespace()
        m = self.input.mark()
        name = self.apply("name")
        if (name != requiredName):
            self.input.rewind(m)
            raise ParseError()
        else:
            self.input.unmark(m)

        self.name = name
        argPatterns = self.apply("expr4")
        try:
            self.token("::=")
        except ParseError:
            return argPatterns
        else:
            body = self.ab.sequence([argPatterns, self.apply("expr")])
            return body

    def rule_rule(self):
        self.eatWhitespace()
        name = self.lookahead(lambda: self.apply("name"))
        if self.hasRule(name):
            raise SyntaxError("Multiple definitions of "+name)
        rs = [self.apply("rulePart", name)]
        while True:
            try:
                rs.append(self.apply("rulePart", name))
            except ParseError:
                break
        if len(rs) == 1:
            return (name, rs[0])
        else:
            return (name, self.ab._or(rs))


    def rule_grammar(self):
        return dict(self.many(lambda: self.apply("rule")))

class AstBuilder(object):
    def __init__(self, filename):
        self.filename = filename


    def compileAstMethod(self, name, expr):
        """
        Produce a callable of a single argument with name C{name} that returns
        the value of the given AST.
        """
        f = self.function(name, expr)
        e = ast.Expression(f)
        e.filename = self.filename
        c = ExpressionCodeGenerator(e).getCode()
        return FunctionType(c.co_consts[-1], globals())


    def compilePythonExpr(self, name, expr):
        c = python_compile(expr, "<grammar rule %s>" % (name,), "eval")
        return ast.Stmt([
                ast.CallFunc(ast.Name('eval'),
                             [ast.Const(c),
                              ast.Name('__locals')])])

    def function(self, name, expr):
        """
        Create a function of one argument with the given name returning the
        given expr.
        """

        fexpr = ast.Stmt([ast.Assign([ast.AssName('__locals', 'OP_ASSIGN')],
                                     ast.Dict(())),
                          expr])
        f = ast.Lambda(['self'], [], 0, fexpr)
        f.filename = self.filename
        return f

    def apply(self, ruleName, *args):
        """
        Create a call to self.apply(ruleName, *args).
        """
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "apply"),
                            [ast.Const(ruleName)] + list(args),
                        None, None)

    def exactly(self, expr):
        """
        Create a call to self.exactly(expr).
        """
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "exactly"),
                            [expr],
                            None, None)

    def many(self, expr):
        """
        Create a call to self.many(lambda: expr).
        """
        f = ast.Lambda([], [], 0, expr)
        f.filename = self.filename
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "many"),
                            [f],
                            None, None)

    def many1(self, expr):
        """
        Create a call to self.many((lambda: expr), expr).
        """
        f = ast.Lambda([], [], 0, expr)
        f.filename = self.filename
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "many"),
                            [f, expr],
                            None, None)

    def _or(self, exprs):
        """
        Create a call to
        self._or([lambda: expr1, lambda: expr2, ... , lambda: exprN]).
        """
        fs = []
        for expr in exprs:
            f = ast.Lambda([], [], 0, expr)
            f.filename = self.filename
            fs.append(f)
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "_or"),
                            [ast.List(fs)],
                            None, None)

    def _not(self, expr):
        f = ast.Lambda([], [], 0, expr)
        f.filename = self.filename
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "_not"),
                            [f],
                            None, None)

    def sequence(self, exprs):
        if len(exprs) > 0:
            stmtExprs = [ast.Discard(e) for e in exprs[:-1]] + [exprs[-1]]
            return ast.Stmt(stmtExprs)
        else:
            return ast.Const(None)

    def bind(self, expr, name):
        return ast.Stmt([
                 ast.Assign([ast.Subscript(ast.Name('__locals'),
                                           'OP_ASSIGN',
                                           [ast.Const(name)])],
                            expr),
                 ast.Subscript(ast.Name('__locals'),
                               'OP_APPLY', [ast.Const(name)])])

    def pred(self, expr):
        f = ast.Lambda([], [], 0, expr)
        f.filename = self.filename
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "pred"),
                            [f],
                            None, None)

    def listpattern(self, exprs):
        f = ast.Lambda([], [], 0, exprs)
        f.filename = self.filename
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "listpattern"),
                            [f],
                            None, None)

class _MetaOMeta(type):
    """
    There is probably some really good joke I could make about this class name
    but I'm not coming up with anything at the moment.
    """
    def __new__(metaclass, name, bases, methodDict):
        grammar = methodDict.get('__doc__', None)
        if grammar:
            ab, rules = parseGrammar(grammar, name)
            ruleMethods = dict([(k, ab.compileAstMethod(k, v))
                                for (k, v) in rules.iteritems()])
            methodDict['__ometa_rules__'] = ruleMethods
        else:
            methodDict['__ometa_rules__'] = {}
        grammarClass = type.__new__(metaclass, name, bases, methodDict)
        return grammarClass


class _OMetaCallWrapper(OMetaBase):
    def __getattr__(self, name):
        if name in self.__ometa_rules__:
            return lambda: self.apply(name)
        else:
            raise AttributeError

class OMeta(_OMetaCallWrapper):
    __metaclass__ = _MetaOMeta
