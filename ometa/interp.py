from ometa.runtime import (InputStream, OMetaBase, ParseError, EOFError,
                           joinErrors, expected, LeftRecursion)

def decomposeGrammar(grammar):
    rules = {}
    #XXX remove all these asserts once we have quasiterms
    assert grammar.tag.name == 'Grammar'
    for rule in grammar.args[1].args:
        assert rule.tag.name == 'Rule'
        rules[rule.args[0].data] = rule.args[1]
    return rules

# after 12, i'm worse than a gremlin
_feed_me = object()


class TrampolinedGrammarInterpreter(object):
    def __init__(self, grammar, ruleName, callback=None, globals=None):
        self.grammar = grammar
        self.position = 0
        self.callback = callback
        self.globals = globals or {}
        self.rules = decomposeGrammar(grammar)
        self.next = self.parse_Apply(ruleName, None, ())
        self._localsStack = []
        self.currentResult = None
        self.input = InputStream([], 0)


    def receive(self, buf):
        self.input.data.extend(buf)
        for x in self.next:
            if x is _feed_me:
                return x
        self.callback(*x)


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
                g = rule()
            else:
                g = rule(*args)
            for x in rule():
                if x is _feed_me:
                    yield x
            yield x
            return
        memoRec = self.input.getMemo(ruleName)
        if memoRec is None:
            oldPosition = self.input
            lr = LeftRecursion()
            memoRec = self.input.setMemo(ruleName, lr)

            try:
                for x in rule():
                    if x is _feed_me:
                        yield x
                memoRec = self.input.setMemo(ruleName, [x, self.input])
            except ParseError:
                raise
            if lr.detected:
                sentinel = self.input
                while True:
                    try:
                        self.input = oldPosition
                        for x in rule():
                            if x is _feed_me:
                                yield x
                        ans = x
                        if (self.input == sentinel):
                            break

                        memoRec = oldPosition.setMemo(ruleName,
                                                     [ans, self.input])
                    except ParseError:
                        break
            self.input = oldPosition

        elif isinstance(memoRec, LeftRecursion):
            memoRec.detected = True
            raise ParseError(None, None)
        self.input = memoRec[1]
        yield memoRec[0]


    def _eval(self, expr):
        return getattr(self, "parse_" + expr.tag.name)(*expr.args)


    def parse_Apply(self, ruleName, codeName, args):
        argvals = []
        for a in args:
            for x in self._eval(a):
                if x is _feed_me:
                    yield x
            argvals.append(x[0])
        _locals = {}
        self._localsStack.append(_locals)
        try:
            #XXX super
            rul = self.rules.get(ruleName)
            if rul:
                def f():
                    return self._eval(rul)
            else:
                f = getattr(self, 'rule_' + ruleName)
            for x in self._apply(f, ruleName, argvals):
                if x is _feed_me:
                    yield x
            yield x
        finally:
            self._localsStack.pop()


    def parse_Exactly(self, spec):
        wanted = spec.data
        try:
            val, p = self.input.head()
        except EOFError:
            yield _feed_me
            val, p = self.input.head()
        if val == wanted:
            self.input = self.input.tail()
            yield val, p
        else:
            raise ParseError(val, expected(None, wanted))


    def parse_And(self, expr):
        seq = expr.args
        val = None, self.input.nullError()
        for subexpr in seq:
            for val in self._eval(subexpr):
                if val is _feed_me:
                    yield val
            self.currentError = val[1]
        yield val


    def parse_Or(self, expr):
        errors = []
        i = self.input
        for subexpr in expr.args:
            try:
                for x in self._eval(subexpr):
                    if x is _feed_me:
                        yield x
                val, p = x
                errors.append(p)
                self.currentError = joinErrors(errors)
                yield x
                return
            except ParseError, err:
                errors.append(err)
                self.input = i
        raise ParseError(*joinErrors(errors))


    def parse_Many(self, expr, ans=None):
        ans = ans or []
        while True:
            try:
                m = self.input
                for x in self._eval(expr):
                    if x is _feed_me:
                        yield _feed_me
                ans.append(x[0])
                self.currentError = x[1]
            except ParseError, err:
                self.input = m
                break
        yield ans, err

    def parse_Many1(self, expr):
        for x in self._eval(expr):
            if x is _feed_me:
                yield _feed_me
        for x in self.parse_Many(expr, ans=[x[0]]):
            if x is _feed_me:
                yield _feed_me
        yield x


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
        self.rules = decomposeGrammar(grammar)


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
