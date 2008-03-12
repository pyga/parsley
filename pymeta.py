from types import FunctionType
from compiler import ast
from compiler.pycodegen import ExpressionCodeGenerator

class ParseError(Exception):
    """
    ?Redo from start
    """


def pyExpr(bits):
    """
    Extract a Python expression from the beginning of a string and return it.
    """

class IterBuffer(object):
    """
    Wrapper for an iterable that allows pushing items onto it.
    """

    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.buffer = []
        self.markBuffers = []
        self.lastMark = -1
    def __iter__(self):
        return self


    def next(self):
        if self.buffer:
            val = self.buffer.pop()
        else:
            val = self.iterable.next()
        for buf in self.markBuffers:
            buf.append(val)
        self.lastThing = val
        return val


    def prev(self):
        self.buffer.append(self.lastThing)
        for buf in self.markBuffers:
            del buf[-1]
        del self.lastThing

    def push(self, obj):
        self.buffer.append(obj)


    def mark(self):
        self.lastMark += 1
        self.markBuffers.append([])
        return self.lastMark


    def unmark(self, mark):
        del self.markBuffers[mark:]
        self.lastMark = mark-1


    def rewind(self, mark):
        saved = self.markBuffers[mark][::-1]
        self.buffer.extend(saved)
        del self.markBuffers[mark:]
        for buf in self.markBuffers:
            del buf[-len(saved):]
        self.lastMark = mark-1

class OMeta(object):
    """
    Abstract class providing implementations of the basic OMeta operations.
    """
    def apply(self, ruleName, *args):
        for arg in args[::-1]:
            self.input.push(arg)
        return getattr(self, "rule_"+ruleName)()


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
        try:
            while True:
                m = self.input.mark()
                ans.append(fn())
                self.input.unmark(m)
        except ParseError:
                self.input.rewind(m)
        return ans

    def eatWhitespace(self):
        for c in self.input:
            if not c.isspace():
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
        x = self.input.next()
        if x.isalnum():
            return x
        else:
            self.input.prev()
            raise ParseError()

class StringOMeta(OMeta):
    """
    Simple OMeta backend for parsing strings.
    """
    def __init__(self, string):
        self.input = IterBuffer(string)

def compile(grammar, name="<grammar>"):
    """
    Compile an OMeta grammar and return an object whose methods invoke its
    productions on their first argument.
    """

    ab, rules = parseGrammar(grammar, name)
    ruleMethods = dict([("rule_"+k, ab.compileAstMethod("rule_"+k, v))
                         for (k, v) in rules.iteritems()])
    grammarClass = type(name, (StringOMeta,), ruleMethods)
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
            ret = getattr(obj, "rule_"+name)()
            try:
                obj.input.next()
            except StopIteration:
                try:
                    return ''.join(ret)
                except TypeError:
                    return ret
            else:
                raise ParseError("trailing garbage in input")
        return doIt

def parseGrammar(grammar, name="<grammar>"):
    ab = AstBuilder(name)
    g = OMetaGrammar(grammar)
    g.ab = ab
    return ab, g.rule_grammar()

class OMetaGrammar(StringOMeta):
    """
    Grammar parser.
    """

    def rule_character(self):
        self.token("'")
        r = self.apply("anything")
        self.token("'")
        return self.ab.exactly(ast.Const(r))


    def rule_name(self):
        x  = self.letter()
        xs = self.many(self.letterOrDigit)
        xs.insert(0, x)
        return ''.join(xs)

    def rule_expr1(self):
        return self.apply("character")

    def rule_expr2(self):
        return self.apply("expr1")


    def rule_expr3(self):
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
        return r


    def rule_expr4(self):
        return ast.Subscript(ast.Tuple(self.many(lambda: self.apply("expr3"))),
                             "OP_APPLY", [ast.Const(-1)])

    def rule_expr(self):
        x = self.apply("expr4")
        return x

    def rule_rulePart(self):
        name = self.apply("name")
        self.token("::=")
        body = self.apply("expr")
        return (name, body)

    def rule_rule(self):
        self.eatWhitespace()
        return self.apply("rulePart")

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
        return eval(c)


    def function(self, name, expr):
        """
        Create a function of one argument with the given name returning the
        given expr.
        """
        f = ast.Lambda(['self'], [], 0, expr)
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
