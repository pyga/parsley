import itertools
from types import FunctionType
from compiler import ast, compile as python_compile
from compiler.pycodegen import ExpressionCodeGenerator

class AstBuilder(object):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    def _compileAstMethod(self, name, expr):
        """
        Produce a callable of a single argument with name C{name} that returns
        the value of the given AST.
        """
        f = self.function(name, expr)
        e = ast.Expression(f)
        e.filename = self.name
        c = ExpressionCodeGenerator(e).getCode()
        return FunctionType(c.co_consts[-1], globals())


    def compilePythonExpr(self, name, expr):
        c = python_compile(expr, "<grammar rule %s>" % (name,), "eval")
        return ast.Stmt([
                ast.CallFunc(ast.Name('eval'),
                             [ast.Const(c),
                              ast.Getattr(ast.Name("self"), "globals"),
                              ast.Name('__locals')])])

    def function(self, name, expr):
        """
        Create a function of one argument with the given name returning the
        given expr.
        """

        fexpr = ast.Stmt([ast.Assign([ast.AssName('__locals', 'OP_ASSIGN')],
                                     ast.Dict([(ast.Const('self'), ast.Name('self'))])),
                          ast.Assign([ast.Subscript(ast.Getattr(ast.Name('self'), 'locals'),
                                                    'OP_ASSIGN',
                                                    [ast.Const(name.split('_',1)[1])])],
                                 ast.Name('__locals')),
                          expr])
        f = ast.Lambda(['self'], [], 0, fexpr)
        f.filename = self.name
        return f

    def makeGrammar(self, rules):
        ruleMethods = dict([('rule_'+k, self._compileAstMethod('rule_'+k, v))
                             for (k, v) in rules])

        methodDict = {'locals': {}}
        methodDict.update(ruleMethods)
        return methodDict

    def apply(self, ruleName, codeName=None, *exprs):
        """
        Create a call to self.apply(ruleName, *args).
        """
        args = [self.compilePythonExpr(codeName, arg) for arg in exprs]
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "apply"),
                            [ast.Const(ruleName)] + args,
                        None, None)

    def exactly(self, expr):
        """
        Create a call to self.exactly(expr).
        """
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "exactly"),
                            [ast.Const(expr)],
                            None, None)

    def many(self, expr):
        """
        Create a call to self.many(lambda: expr).
        """
        f = ast.Lambda([], [], 0, expr)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "many"),
                            [f],
                            None, None)

    def many1(self, expr):
        """
        Create a call to self.many((lambda: expr), expr).
        """
        f = ast.Lambda([], [], 0, expr)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "many"),
                            [f, expr],
                            None, None)

    def optional(self, expr):
        """
        Try to parse an expr and continue if it fails.
        """
        return self._or([expr, ast.Const(None)])

    def _or(self, exprs):
        """
        Create a call to
        self._or([lambda: expr1, lambda: expr2, ... , lambda: exprN]).
        """
        fs = []
        for expr in exprs:
            f = ast.Lambda([], [], 0, expr)
            f.filename = self.name
            fs.append(f)
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "_or"),
                            [ast.List(fs)],
                            None, None)

    def _not(self, expr):
        f = ast.Lambda([], [], 0, expr)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "_not"),
                            [f],
                            None, None)


    def lookahead(self, expr):
        f = ast.Lambda([], [], 0, expr)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "lookahead"),
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
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "pred"),
                            [f],
                            None, None)

    def action(self, expr):
        return expr

    def listpattern(self, exprs):
        f = ast.Lambda([], [], 0, exprs)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "listpattern"),
                            [f],
                            None, None)


class PythonBuilder(object):
    def __init__(self, name, grammar):
        self.name = name
        self.gensymCounter = 0
        self.grammar = grammar

    def _gensym(self, name):
        self.gensymCounter += 1
        return "_G_%s_%s" % (name, self.gensymCounter)

    def _newThunkFor(self, name, expr):
        fname = self._gensym(name)
        return (self._function("def %s():" % (fname,), expr), fname)

    def _expr(self, e):
        return e

    def _indent(self, line):
        if line.isspace():
            return '\n'
        else:
            return "    " + line

    def _return(self, ex):
        if ex.strip().startswith("return"):
            return ex
        else:
            return 'return ' + ex

    def _function(self, head, body):
        body = list(body)
        return [head] + [self._indent(line) for line in body[:-1]] + [self._indent(self._return(body[-1]))]


    def _suite(self, head, body):
        body = list(body)
        return [head] + [self._indent(line) for line in body]


    def makeGrammar(self, rules):
        lines = list(itertools.chain(*[self._function("def rule_%s(self):"%(name,),
                                                      ["_locals = {'self': self}", "self.locals[%s] = _locals" % (name,)] + list(body)) + ['\n\n']
                                       for (name, body) in rules]))
        code = '\n'.join(self._suite("class %s(%s):" %(self.name, self.grammar.__class__.__name__), lines))
        module = "from %s import %s\n" % (self.grammar.__class__.__module__, self.grammar.__class__.__name__) + code
        return module

    def compilePythonExpr(self, name, expr):
        return self._expr('eval(%r, self.globals, _locals)' %(expr,))


    def apply(self, ruleName, codeName=None, *exprs):
        """
        Create a call to self.apply(ruleName, *args).
        """
        args = [self.compilePythonExpr(codeName, arg) for arg in exprs]
        return [self._expr('self.apply("%s", %s)' % (ruleName, ', '.join(args)))]


    def exactly(self, literal):
        """
        Create a call to self.exactly(expr).
        """
        return [self._expr('self.exactly(%r)' % (literal,))]


    def many(self, expr):
        """
        Create a call to self.many(lambda: expr).
        """
        fn, fname = self._newThunkFor("many", expr)
        return self.sequence([fn, "self.many(%s)" %(fname,)])


    def many1(self, expr):
        """
        Create a call to self.many((lambda: expr), expr).
        """
        fn, fname = self._newThunkFor("many", expr)
        return self.sequence([fn, self._expr("self.many(%s, %s())" %(fname, fname))])

    def optional(self, expr):
        """
        Try to parse an expr and continue if it fails.
        """
        return self._or([expr, "True"])


    def _or(self, exprs):
        """
        Create a call to
        self._or([lambda: expr1, lambda: expr2, ... , lambda: exprN]).
        """
        if len(exprs) > 1:
            fs, fnames = zip(*[self._newThunkFor("_or", expr) for expr in exprs])
            return self.sequence(list(fs) + [self._expr("self._or([%s])" %(', '.join(fnames)))])
        else:
            return exprs[0]


    def _not(self, expr):
        fn, fname = self._newThunkFor("_not", expr)
        return self.sequence([fn, self._expr("self._not(%s)" %(fname))])


    def lookahead(self, expr):
        fn, fname = self._newThunkFor("lookahead", expr)
        return self.sequence([fn, self._expr("self.lookahead(%s)" %(fname))])


    def sequence(self, exprs):
        for ex in exprs:
            if not ex:
                continue
            elif isinstance(ex, str):
                yield ex
            else:
                for subex in ex:
                    yield subex

    def bind(self, exprs, name):
        bodyExprs = list(exprs)
        finalExpr = bodyExprs[-1]
        bodyExprs = bodyExprs[:-1]
        return self.sequence(bodyExprs + ["_locals['%s'] = %s" %(name, finalExpr), self._expr("_locals['%s']" %(name,))])


    def pred(self, expr):
        fn, fname = self._newThunkFor("pred", [expr])
        return self.sequence([fn, self._expr("self.pred(%s)" %(fname))])

    def action(self, expr):
        return [expr]

    def listpattern(self, expr):
        fn, fname = self._newThunkFor("listpattern", expr)
        return self.sequence([fn, self._expr("self.listpattern(%s)" %(fname))])
