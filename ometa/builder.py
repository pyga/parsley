# -*- test-case-name: ometa.test.test_builder -*-
import os.path
from StringIO import StringIO
from types import ModuleType as module
import itertools, linecache, sys

class TreeBuilder(object):
    """
    Produce an abstract syntax tree of OMeta operations.
    """

    def __init__(self, name, grammar=None, *args):
        self.name = name


    def makeGrammar(self, rules):
        return ["Grammar", self.name, rules]

    def rule(self, name, expr):
        return ["Rule", name, expr]

    def apply(self, ruleName, codeName, *exprs):
        return ["Apply", ruleName, codeName, exprs]

    def exactly(self, expr):
        return ["Exactly", expr]

    def many(self, expr):
        return ["Many", expr]

    def many1(self, expr):
        return ["Many1", expr]

    def optional(self, expr):
        return ["Optional", expr]

    def _or(self, exprs):
        return ["Or", exprs]

    def _not(self, expr):
        return ["Not", expr]

    def lookahead(self, expr):
        return ["Lookahead", expr]

    def sequence(self, exprs):
        return ["And", exprs]

    def bind(self, name, expr):
        return ["Bind", name, expr]

    def pred(self, expr):
        return ["Predicate", expr]

    def action(self, expr):
        return ["Action", expr]

    def expr(self, expr):
        return ["Python", expr]

    def listpattern(self, exprs):
        return ["List", exprs]

    def consumedBy(self, exprs):
        return ["ConsumedBy", exprs]


class TextWriter(object):

    stepSize = 4

    def __init__(self, f, indentSteps=0):
        self.file = f
        self.indentSteps = indentSteps


    def writeln(self, data):
        if data:
            self.file.write(" " * (self.indentSteps * self.stepSize))
            self.file.write(data)
        self.file.write("\n")

    def indent(self):
        return TextWriter(self.file, self.indentSteps + 1)


class PythonWriter(object):
    """
    Converts an OMeta syntax tree into Python source.
    """
    def __init__(self, tree):
        self.takesTreeInput = False
        self.tree = tree
        self.gensymCounter = 0


    def _generate(self, out, expr, retrn=False):
        result = self._generateNode(out, expr)
        if retrn:
            out.writeln("return (%s, self.currentError)" % (result,))
        elif result:
            out.writeln(result)

    def output(self, out):
        self._generate(out, self.tree)


    def _generateNode(self, out, node):
        name = node[0]
        args =  node[1:]
        return getattr(self, "generate_"+name)(out, *args)


    def _gensym(self, name):
        """
        Produce a unique name for a variable in generated code.
        """
        self.gensymCounter += 1
        return "_G_%s_%s" % (name, self.gensymCounter)


    def _newThunkFor(self, out, name, expr):
        """
        Define a new function of no arguments.
        @param name: The name of the rule generating this thunk.
        @param expr: A list of lines of Python code.
        """

        fname = self._gensym(name)
        self._writeFunction(out, fname, (),  expr)
        return fname


    def _expr(self, out, typ, e):
        """
        Generate the code needed to execute the expression, and return the
        variable name bound to its value.
        """
        name = self._gensym(typ)
        out.writeln("%s, lastError = %s" % (name, e))
        out.writeln("self.considerError(lastError)")
        return name


    def _writeFunction(self, out, fname, arglist, expr):
        """
        Generate a function.
        @param head: The initial line defining the function.
        @param body: A list of lines for the function body.
        """

        out.writeln("def %s(%s):" % (fname, ", ".join(arglist)))
        self._generate(out.indent(), expr, retrn=True)
        return fname


    def compilePythonExpr(self, out, expr):
        """
        Generate code for running embedded Python expressions.
        """
        return self._expr(out, 'python', 'eval(%r, self.globals, _locals), None' %(expr,))

    def _convertArgs(self, out, rawArgs):
        return [self._generateNode(out, x) for x in rawArgs]


    def generate_Apply(self, out, ruleName, codeName, rawArgs):
        """
        Create a call to self.apply(ruleName, *args).
        """
        args = self._convertArgs(out, rawArgs)
        if ruleName == 'super':
            return self._expr(out, 'apply', 'self.superApply("%s", %s)' % (codeName,
                                                              ', '.join(args)))
        return self._expr(out, 'apply', 'self._apply(self.rule_%s, "%s", [%s])' % (ruleName,
                                                                              ruleName,
                                                             ', '.join(args)))

    def generate_Exactly(self, out, literal):
        """
        Create a call to self.exactly(expr).
        """
        if not isinstance(literal, basestring):
            self.takesTreeInput = True
        return self._expr(out, 'exactly', 'self.exactly(%r)' % (literal,))


    def generate_Many(self, out, expr):
        """
        Create a call to self.many(lambda: expr).
        """
        fname = self._newThunkFor(out, "many", expr)
        return self._expr(out, 'many', 'self.many(%s)' % (fname,))


    def generate_Many1(self, out, expr):
        """
        Create a call to self.many(lambda: expr).
        """
        fname = self._newThunkFor(out, "many1", expr)
        return self._expr(out, 'many1', 'self.many(%s, %s())' % (fname, fname))


    def generate_Optional(self, out, expr):
        """
        Try to parse an expr and continue if it fails.
        """
        realf = self._newThunkFor(out, "optional", expr)
        passf = self._gensym("optional")
        out.writeln("def %s():" % (passf,))
        out.indent().writeln("return (None, self.input.nullError())")
        return self._expr(out, 'or', 'self._or([%s])' % (', '.join([realf, passf])))


    def generate_Or(self, out, exprs):
        """
        Create a call to
        self._or([lambda: expr1, lambda: expr2, ... , lambda: exprN]).
        """
        if len(exprs) > 1:
            fnames = [self._newThunkFor(out, "or", expr) for expr in exprs]
            return self._expr(out, 'or', 'self._or([%s])' % (', '.join(fnames)))
        else:
            return self._generateNode(out, exprs[0])


    def generate_Not(self, out, expr):
        """
        Create a call to self._not(lambda: expr).
        """
        fname = self._newThunkFor(out, "not", expr)
        return self._expr(out, "not", "self._not(%s)" % (fname,))


    def generate_Lookahead(self, out, expr):
        """
        Create a call to self.lookahead(lambda: expr).
        """
        fname = self._newThunkFor(out, "lookahead", expr)
        return self._expr(out, "lookahead", "self.lookahead(%s)" %(fname,))


    def generate_And(self, out, exprs):
        """
        Generate code for each statement in order.
        """
        v = None
        for ex in exprs:
            v = self._generateNode(out, ex)
        return v


    def generate_Bind(self, out, name, expr):
        """
        Bind the value of 'expr' to a name in the _locals dict.
        """
        v = self._generateNode(out, expr)
        ref = "_locals['%s']" % (name,)
        out.writeln("%s = %s" %(ref, v))
        return ref


    def generate_Predicate(self, out, expr):
        """
        Generate a call to self.pred(lambda: expr).
        """

        fname = self._newThunkFor(out, "pred", expr)
        return self._expr(out, "pred", "self.pred(%s)" %(fname,))


    def generate_Action(self, out, expr):
        """
        Generate this embedded Python expression on its own line.
        """
        return self.compilePythonExpr(out, expr)


    def generate_Python(self, out, expr):
        """
        Generate this embedded Python expression on its own line.
        """
        return self.compilePythonExpr(out, expr)


    def generate_List(self, out, expr):
        """
        Generate a call to self.listpattern(lambda: expr).
        """
        self.takesTreeInput = True
        fname = self._newThunkFor(out, "listpattern", expr)
        return  self._expr(out, "listpattern", "self.listpattern(%s)" %(fname,))


    def generate_ConsumedBy(self, out, expr):
        """
        Generate a call to self.consumedBy(lambda: expr).
        """
        fname = self._newThunkFor(out, "consumedby", expr)
        return  self._expr(out, "consumedby", "self.consumedby(%s)" %(fname,))


    def generate_Rule(self, prevOut, name, expr):
        prevOut.writeln("def rule_%s(self):" % (name,))
        out = prevOut.indent()
        out.writeln("_locals = {'self': self}")
        out.writeln("self.locals[%r] = _locals" % (name,))
        self._generate(prevOut.indent(), expr, retrn=True)

    def generate_Grammar(self, out, name, rules):
        out.writeln("class %s(GrammarBase):" % (name,))
        out = out.indent()
        for rule in rules:
            self._generateNode(out, rule)
            out.writeln("")
            out.writeln("")
        if self.takesTreeInput:
            out.writeln("tree = True")


class TermActionPythonWriter(PythonWriter):

    def _convertArgs(self, out, termArgs):
        return [self._termAsPython(out, a) for a in termArgs]


    def generate_Predicate(self, out, term):
        """
        Generate a call to self.pred(lambda: expr).
        """

        fname = self._newThunkFor(out, "pred", ["Action", term])
        return self._expr(out, "pred", "self.pred(%s)" %(fname,))

    def generate_Action(self, out, term):
        return self._termAsPython(out, term)

    generate_Python = generate_Action

    def _termAsPython(self, out, term):
        lines = []
        class Term2PythonAction(object):
            def leafData(bldr, data, span):
                return repr(data)

            def leafTag(bldr, tag, span):
                return tag.name

            def empty(bldr):
                return []

            def seq(bldr, args, arg):
                args.append(arg)
                return args

            def term(bldr, tag, args):
                if not args:
                    return tag
                if tag == '.tuple.':
                    return "[%s]" % (', '.join(args),)
                elif tag == '.attr.':
                    return "(%s)" % (', '.join(args),)
                elif tag == '.bag.':
                    return "dict(%s)" % (', '.join(args),)
                return "%s(%s)" % (tag, ', '.join(args))
        if not term.args:
            if term.data is None:
                return self.compilePythonExpr(out, term.tag.name)
            else:
                name = self._gensym("literal")
                out.writeln("%s = %r" % (name, term.data))
                return name
        else:
            return self.compilePythonExpr(out, term.build(Term2PythonAction()))


def writePython(tree):
    f = StringIO()
    out = TextWriter(f)
    pw = PythonWriter(tree)
    pw.output(out)
    return f.getvalue().strip()


class GeneratedCodeLoader(object):
    """
    Object for use as a module's __loader__, to display generated
    source.
    """
    def __init__(self, source):
        self.source = source
    def get_source(self, name):
        return self.source



def moduleFromGrammar(tree, className, superclass, globalsDict, writer=writePython):
    source = writer(tree)
    modname = "pymeta_grammar__" + className
    filename = "/pymeta_generated_code/" + modname + ".py"
    mod = module(modname)
    mod.__dict__.update(globalsDict)
    mod.__name__ = modname
    mod.__dict__[superclass.__name__] = superclass
    mod.__dict__["GrammarBase"] = superclass
    mod.__loader__ = GeneratedCodeLoader(source)
    code = compile(source, filename, "exec")
    eval(code, mod.__dict__)
    fullGlobals = dict(getattr(mod.__dict__[className], "globals", None) or {})
    fullGlobals.update(globalsDict)
    mod.__dict__[className].globals = fullGlobals
    sys.modules[modname] = mod
    linecache.getlines(filename, mod.__dict__)
    return mod.__dict__[className]
