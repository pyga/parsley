from types import ModuleType as module
import itertools, linecache, sys
from types import FunctionType
from compiler import ast, compile as python_compile
from compiler.pycodegen import ExpressionCodeGenerator

class TreeBuilder(object):
    """
    Produce an abstract syntax tree of OMeta operations.
    """
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    def makeGrammar(self, rules):
        return ["Grammar", rules]

    def apply(self, ruleName, codeName=None, *exprs):
        return ["Apply", ruleName, codeName or '', exprs]

    def exactly(self, expr):
        return ["Exactly", expr]

    def many(self, expr):
        return ["Many", expr]

    def many1(self, expr):
        return ["Many1", expr]

    def optional(self, expr):
        return ["Optional", expr]

    def _or(self, exprs):
        return ["Or"] + exprs

    def _not(self, expr):
        return ["Not", expr]

    def lookahead(self, expr):
        return ["Lookahead", expr]

    def sequence(self, exprs):
        return ["And"] + exprs

    def bind(self, expr, name):
        return ["Bind", name, expr]

    def pred(self, expr):
        return ["Predicate", expr]

    def action(self, expr):
        return ["Action", expr]

    def listpattern(self, exprs):
        return ["List", exprs]

    def compilePythonExpr(self, name, expr):
        return ["Python", name, expr]

class AstBuilder(object):
    """
    Builder of Python code objects via the 'compiler.ast' module.
    """
    def __init__(self, name, grammar):
        """
        @param name: The grammar name.
        @param grammar: A grammar object.
        """
        self.name = name
        self.grammar = grammar

    def _compileAstMethod(self, name, expr):
        """
        Produce a callable of a single argument with name C{name} that returns
        the value of the given AST.

        @param name: The name of the callable.
        @param expr: The AST to compile.
        """
        f = self.function(name, expr)
        e = ast.Expression(f)
        e.filename = self.name
        c = ExpressionCodeGenerator(e).getCode()
        return FunctionType(c.co_consts[-1], globals())


    def compilePythonExpr(self, name, expr):
        """
        Compile an embedded Python expression.

        @param name: The current rule name.
        @param expr: The Python expression to compile.
        """
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

        @param name: The function name.
        @param expr: The AST to insert into the function.
        """

        fexpr = ast.Stmt([ast.Assign([ast.AssName('__locals', 'OP_ASSIGN')],
                                     ast.Dict([(ast.Const('self'),
                                                ast.Name('self'))])),
                          ast.Assign([ast.Subscript(ast.Getattr(
                                                  ast.Name('self'), 'locals'),
                                                    'OP_ASSIGN',
                                                    [ast.Const(
                                                     name.split('_',1)[1])])],
                                     ast.Name('__locals')),
                          expr])
        f = ast.Lambda(['self'], [], 0, fexpr)
        f.filename = self.name
        return f

    def makeGrammar(self, rules):
        """
        Collect a list of (name, ast) tuples into a dict suitable for use as a
        class' method dictionary.
        """
        ruleMethods = dict([('rule_'+k, self._compileAstMethod('rule_'+k, v))
                             for (k, v) in rules])

        methodDict = {'locals': {}}
        methodDict.update(ruleMethods)
        return methodDict

    def apply(self, ruleName, codeName='', *exprs):
        """
        Create a call to self.apply(ruleName, *args).
        """
        args = [self.compilePythonExpr(codeName, arg) for arg in exprs]
        if ruleName == "super":
            return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                            "superApply"),
                                [ast.Const(codeName)] + args,
                                None, None)
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
        """
        Create a call to self._not(lambda: expr).
        """

        f = ast.Lambda([], [], 0, expr)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "_not"),
                            [f],
                            None, None)


    def lookahead(self, expr):
        """
        Create a call to self.lookahead(lambda: expr).
        """

        f = ast.Lambda([], [], 0, expr)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "lookahead"),
                            [f],
                            None, None)


    def sequence(self, exprs):
        """
        Creates a sequence of exprs, returning the value of the last one.
        """
        if len(exprs) > 0:
            stmtExprs = [ast.Discard(e) for e in exprs[:-1]] + [exprs[-1]]
            return ast.Stmt(stmtExprs)
        else:
            return ast.Const(None)

    def bind(self, expr, name):
        """
        Generates code for binding a name to a value in the rule's locals dict.
        """
        return ast.Stmt([
                 ast.Assign([ast.Subscript(ast.Name('__locals'),
                                           'OP_ASSIGN',
                                           [ast.Const(name)])],
                            expr),
                 ast.Subscript(ast.Name('__locals'),
                               'OP_APPLY', [ast.Const(name)])])

    def pred(self, expr):
        """
        Create a call to self.pred(lambda: expr).
        """

        f = ast.Lambda([], [], 0, expr)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "pred"),
                            [f],
                            None, None)

    def action(self, expr):
        """
        Compiled python code is not treated specially if its return value isn't
        important.
        """
        return expr

    def listpattern(self, exprs):
        """
        Create a call to self.listpattern(lambda: exprs).
        """
        f = ast.Lambda([], [], 0, exprs)
        f.filename = self.name
        return ast.CallFunc(ast.Getattr(ast.Name("self"),
                                        "listpattern"),
                            [f],
                            None, None)


class GeneratedCodeLoader(object):
    """
    Object for use as a module's __loader__, to display generated
    source.
    """
    def __init__(self, source):
        self.source = source
    def get_source(self, name):
        return self.source

class PythonBuilder(object):
    """
    Same idea as ASTBuilder but producing literal Python source instead.
    """
    def __init__(self, name, grammar, superclass, globals):
        self.name = name
        self.superclass = superclass
        self.gensymCounter = 0
        self.grammar = grammar
        self.globals = globals

    def _gensym(self, name):
        """
        Produce a unique name for a variable in generated code.
        """
        self.gensymCounter += 1
        return "_G_%s_%s" % (name, self.gensymCounter)

    def _newThunkFor(self, name, expr):
        """
        Define a new function of no arguments.
        @param name: The name of the rule generating this thunk.
        @param expr: A list of lines of Python code.
        """
        fname = self._gensym(name)
        return (self._function("def %s():" % (fname,), expr), fname)

    def _expr(self, e):
        """
        No unique handling of embedded Python expressions, presently.
        """
        return e

    def _indent(self, line):
        """
        Indent a line of code.
        """
        if line.isspace():
            return '\n'
        else:
            return "    " + line

    def _return(self, ex):
        """
        Generate a 'return' statement, if the given line does not contain one.
        """
        if ex.strip().startswith("return"):
            return ex
        else:
            return 'return ' + ex

    def _function(self, head, body):
        """
        Generate a function.
        @param head: The initial line defining the function.
        @param body: A list of lines for the function body.
        """
        body = list(body)
        return [head] + [self._indent(line) for line in body[:-1]] + [self._indent(self._return(body[-1]))]


    def _suite(self, head, body):
        """
        Generate a suite, indenting the body lines.
        @param head: The initial line opening the suite.
        @param body: A list of lines for the suite body.
        """
        body = list(body)
        return [head] + [self._indent(line) for line in body]


    def makeGrammar(self, rules):
        """
        Produce a class from a collection of rules.

        @param rules: A mapping of names to rule bodies.
        """
        lines = list(itertools.chain(*[self._function(
            "def rule_%s(self):" % (name,),
            ["_locals = {'self': self}",
             "self.locals[%r] = _locals" % (name,)] + list(body)) + ['\n\n']
                                       for (name, body) in rules]))
        source = '\n'.join(self._suite(
            "class %s(%s):" %(self.name, self.superclass.__name__),
            lines))
        modname = "pymeta_grammar__"+self.name
        filename = "/pymeta_generated_code/"+modname+".py"
        mod = module(modname)
        mod.__dict__.update(self.globals)
        mod.__name__ = modname
        mod.__dict__[self.superclass.__name__] = self.superclass
        mod.__loader__ = GeneratedCodeLoader(source)
        code = compile(source, filename, "exec")
        eval(code, mod.__dict__)
        mod.__dict__[self.name].globals = self.globals
        sys.modules[modname] = mod
        linecache.getlines(filename, mod.__dict__)
        return mod.__dict__[self.name]

    def compilePythonExpr(self, name, expr):
        """
        Generate code for running embedded Python expressions.
        """
        return self._expr('eval(%r, self.globals, _locals)' %(expr,))


    def apply(self, ruleName, codeName=None, *exprs):
        """
        Create a call to self.apply(ruleName, *args).
        """
        args = [self.compilePythonExpr(codeName, arg) for arg in exprs]
        if ruleName == 'super':
            return [self._expr('self.superApply("%s", %s)' % (codeName,
                                                              ', '.join(args)))]
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
        return self._or([expr, ["None"]])


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
        """
        Create a call to self._not(lambda: expr).
        """
        fn, fname = self._newThunkFor("_not", expr)
        return self.sequence([fn, self._expr("self._not(%s)" %(fname))])


    def lookahead(self, expr):
        """
        Create a call to self.lookahead(lambda: expr).
        """
        fn, fname = self._newThunkFor("lookahead", expr)
        return self.sequence([fn, self._expr("self.lookahead(%s)" %(fname))])


    def sequence(self, exprs):
        """
        Generate code for each statement in order.
        """
        for ex in exprs:
            if not ex:
                continue
            elif isinstance(ex, str):
                yield ex
            else:
                for subex in ex:
                    yield subex

    def bind(self, exprs, name):
        """
        Bind the value of the last expression in 'exprs' to a name in the
        _locals dict.
        """
        bodyExprs = list(exprs)
        finalExpr = bodyExprs[-1]
        bodyExprs = bodyExprs[:-1]
        return self.sequence(bodyExprs + ["_locals['%s'] = %s" %(name, finalExpr), self._expr("_locals['%s']" %(name,))])


    def pred(self, expr):
        """
        Generate a call to self.pred(lambda: expr).
        """

        fn, fname = self._newThunkFor("pred", [expr])
        return self.sequence([fn, self._expr("self.pred(%s)" %(fname))])

    def action(self, expr):
        """
        Generate this embedded Python expression on its own line.
        """
        return [expr]

    def listpattern(self, expr):
        """
        Generate a call to self.listpattern(lambda: expr).
        """
        fn, fname = self._newThunkFor("listpattern", expr)
        return self.sequence([fn, self._expr("self.listpattern(%s)" %(fname))])
