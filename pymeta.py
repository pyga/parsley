from types import FunctionType
from compiler import ast
from compiler.pycodegen import ExpressionCodeGenerator

class ParseError(Exception):
    """
    ?Redo from start
    """

parseFailed = object()

def compile(grammar, name="<grammar>"):
    """
    Compile an OMeta grammar and return an object whose methods invoke its
    productions on their first argument.
    """
    ab = AstBuilder("<grammar>")
    rules = parseGrammar(ab, grammar)
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

def parseGrammar(ab, grammar):
    """
    Interim grammar parser.
    """
    line = 1
    col = 0
    name_, rule_ = grammar.split('::=')
    name = name_.strip()
    rule = rule_.strip()
    if rule[0] == "'":
        char = rule[1]
        if rule[2] != "'":
            raise SyntaxError("invalid syntax", ("<grammar>", 1,
                                                 len(name_) + len(rule_), + 5,
                                                 grammar))
        if len(rule) > 3:
            if rule[3] == '*':
                return {name: ab.many(ab.exactly(ast.Const(char)))}
            if rule[3] == '+':
                return {name: ab.many1(ab.exactly(ast.Const(char)))}
    return {name: ab.exactly(ast.Const(char))}


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
        return val


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
        if wanted == self.apply("anything"):
            return wanted
        else:
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

class StringOMeta(OMeta):
    """
    Simple OMeta backend for parsing strings.
    """
    def __init__(self, string):
        self.input = IterBuffer(string)
