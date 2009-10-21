from types import ModuleType as module
import itertools, linecache, sys

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
    def __init__(self, name, grammar, superclass, globals, sourceOnly):
        self.name = name
        self.superclass = superclass
        self.gensymCounter = 0
        self.grammar = grammar
        self.globals = globals
        self.sourceOnly = sourceOnly

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
        return ["lastValue, lastError = " + e,
                "self.considerError(lastError)"]


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
        return [head] + [self._indent(line) for line in self.sequence(body)] + [self._indent(self._return("(lastValue, self.currentError)"))]


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
        if self.sourceOnly:
            return source
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
        return self._expr('(eval(%r, self.globals, _locals), self.currentError)' %(expr,))


    def apply(self, ruleName, codeName=None, *exprs):
        """
        Create a call to self.apply(ruleName, *args).
        """
        args = [self.compilePythonExpr(codeName, arg) for arg in exprs]
        if ruleName == 'super':
            return [self._expr('self.superApply("%s", %s)' % (codeName,
                                                              ', '.join(self.sequence(args))))]
        return [self._expr('self.apply("%s", %s)' % (ruleName, ', '.join(self.sequence(args))))]


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
        exprs = list(exprs)
        def _seq(xs):
            for ex in xs:
                if not ex:
                    continue
                elif isinstance(ex, str):
                    yield ex
                else:
                    for subex in self.sequence(ex):
                        yield subex
        result = list(_seq(exprs))
        return result

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
