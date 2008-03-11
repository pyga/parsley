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
    rules = parseGrammar(grammar)
    ruleMethods = dict([("rule_"+k, compileAstMethod("rule_"+k, v, name))
                         for (k, v) in rules.iteritems()])
    grammarClass = type(name, (StringOMeta,), ruleMethods)
    return HandyWrapper(grammarClass)

class HandyWrapper(object):
    def __init__(self, klass):
        self.klass = klass
    def __getattr__(self, name):
        def doIt(str):
            obj = self.klass(str)
            return getattr(obj, "rule_"+name)()
        return doIt

def parseGrammar(grammar):
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
    return {name: ast_exactly(ast.Const(char))}

def compileAstMethod(name, expr, filename="<grammar>"):
    """
    Produce a callable of a single argument with name C{name} that returns the
    value of the given AST.
    """
    fe = ast_function(name, filename, expr)
    c = ExpressionCodeGenerator(fe).getCode()
    return eval(c)

def ast_function(name, filename, expr):
    """
    Create a function of no arguments with the given name returning the given
    expr.
    """
    f = ast.Lambda(['self'], [], 0, expr)
    f.filename = filename
    e = ast.Expression(f)
    e.filename = filename
    return e

def ast_apply(ruleName, *args):
    """
    Create a call to self.apply(ruleName, *args).
    """
    return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                    "apply"),
                        [ast.Const(ruleName)] + list(args),
                        None, None)

def ast_exactly(expr):
    """
    Create a call to self.exactly(expr).
    """
    return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                    "exactly"),
                        [expr],
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

    def __iter__(self):
        return self

    def next(self):
        if self.buffer:
            return self.buffer.pop()
        else:
            return self.iterable.next()

    def push(self, obj):
        self.buffer.append(obj)



class OMeta(object):
    """
    Abstract class providing implementations of the basic OMeta operations.
    """
    def apply(self, ruleName, *args):
        for arg in args[::-1]:
            self.input.push(arg)
        return getattr(self, "rule_"+ruleName)()

    def rule_anything(self):
        return self.input.next()

    def exactly(self, wanted):
        if wanted == self.apply("anything"):
            return wanted
        else:
            raise ParseError()

class StringOMeta(OMeta):
    """
    Simple OMeta backend for parsing strings.
    """
    def __init__(self, string):
        self.input = IterBuffer(string)
