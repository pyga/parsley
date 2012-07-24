from ometa.runtime import (InputStream, OMetaBase, ParseError,
                           joinErrors, expected)

class GrammarInterpreter(object):

    def __init__(self, grammar, base, globals=None):
        """
        grammar: A term tree representing a grammar.
        """
        self.grammar = grammar
        self.base = base
        self.rules = {}
        self._localsStack = []
        self._globals = globals or {}
        #XXX remove all these asserts once we have quasiterms
        assert grammar.tag.name == 'Grammar'
        for rule in grammar.args[1].args:
            assert rule.tag.name == 'Rule'
            self.rules[rule.args[0].data] = rule.args[1]


    def apply(self, input, rulename, tree=False):
        run = self.base(input, self._globals, tree=tree)
        v, err = self._apply(run, rulename, ())
        return run.input, v, ParseError(*err)


    def _apply(self, run, ruleName, args):
        argvals = [self._eval(run, a)[0] for a in args]
        _locals = {}
        self._localsStack.append(_locals)
        try:
            if ruleName == 'super':
                return run.superApply(ruleName, argvals)
            else:
                rul = self.rules.get(ruleName)
                if rul:
                    return run._apply(
                        (lambda: self._eval(run, rul)),
                        ruleName, argvals)
                else:
                    x = run._apply(getattr(run, 'rule_' + ruleName), ruleName, argvals)
                    return x
        finally:
            self._localsStack.pop()


    def _eval(self, run, expr):
        name = expr.tag.name
        args = expr.args
        if name == "Apply":
            ruleName = args[0].data
            return self._apply(run, ruleName, args[2].args)

        elif name == "Exactly":
            return run.exactly(args[0].data)

        elif name in ("Many", "Many1"):
            ans = [self._eval(run, args[0])[0]] if name == "Many1" else []
            while True:
                try:
                    m = run.input
                    v, _ = self._eval(run, args[0])
                    ans.append(v)
                except ParseError, err:
                    run.input = m
                    break
            return ans, err

        elif name == "Optional":
            try:
                return self._eval(run, args[0])
            except ParseError:
                return (None, run.input.nullError())

        elif name == "Or":
            errors = []
            for e in args[0].args:
                try:
                    m = run.input
                    x = self._eval(run, e)
                    ret, err = x
                    errors.append(err)
                    return ret, joinErrors(errors)
                except ParseError, err:
                    errors.append(err)
                    run.input = m
            raise ParseError(*joinErrors(errors))


        elif name == "Not":
            m = run.input
            try:
                self._eval(run, args[0])
            except ParseError, err:
                run.input = m
                return True, run.input.nullError()
            else:
                raise ParseError(*run.input.nullError())


        elif name == "Lookahead":
            try:
                m = run.input
                return self._eval(run, args[0])
            finally:
                run.input = m

        elif name == "And":
            v = None, run.input.nullError()
            for e in args[0].args:
                v = self._eval(run, e)
            return v

        elif name == "Bind":
            v, err =  self._eval(run, args[1])
            self._localsStack[-1][args[0].data] = v
            return v, err

        elif name == "Predicate":
            val, err = self._eval(run, args[0])
            if not val:
                raise ParseError(*err)
            else:
                return True, err

        elif name == "List":
            v, e = run.rule_anything()
            oldInput = run.input
            try:
                run.input = InputStream.fromIterable(v)
            except TypeError:
                e = run.input.nullError()
                e[1] = expected("an iterable")
                raise ParseError(*e)
            self._eval(run, args[0])
            run.end()
            run.input = oldInput
            return v, e

        elif name in ("Action", "Python"):
            lo = self._localsStack[-1]
            val = eval(args[0].data, self._globals, lo)
            return (val, run.input.nullError())

        elif name == "ConsumedBy":
            oldInput = run.input
            _, err = self._eval(run, args[0])
            slice = oldInput.data[oldInput.position:run.input.position]
            return slice, err

        else:
            raise ValueError("Unrecognized term: %r" % (name,))
