# -*- test-case-name: pymeta.test.test_grammar -*-
"""
The definition of PyMeta's language is itself a PyMeta grammar, but something
has to be able to read that. Most of the code in this module is generated from
that grammar (in future versions, it will hopefully all be generated).
"""
from pymeta.runtime import OMetaBase, ParseError
import string

class BootOMetaGrammar(OMetaBase):
    """
    The bootstrap grammar, generated from L{pymeta.grammar.OMetaGrammar} via
    L{pymeta.builder.PythonBuilder}.
    """
    globals = globals()

    def __init__(self, input):
        OMetaBase.__init__(self, input)
        self._ruleNames = []


    def parseGrammar(self, name, builder, *args):
        """
        Entry point for converting a grammar to code (of some variety).

        @param name: The name for this grammar.

        @param builder: A class that implements the grammar-building interface
        (interface to be explicitly defined later)
        """
        self.builder = builder(name, self, *args)
        res = self.apply("grammar")
        try:
            x = self.input.head()
        except IndexError:
            pass
        else:
            x = repr(''.join(self.input.data[self.input.position:]))
            raise ValueError("Grammar parse failed. Leftover bits: %s" % (x,))
        return res


    def applicationArgs(self):
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
        if args:
            return args
        else:
            raise ParseError()


    def ruleValueExpr(self):
        expr, endchar = self.pythonExpr(endChars="\r\n)]")
        if str(endchar) in ")]":
            self.input = self.input.prev()
        return self.builder.compilePythonExpr(self.name, expr)


    def semanticActionExpr(self):
        expr = self.builder.compilePythonExpr(self.name,
                                              self.pythonExpr(')')[0])
        return self.builder.action(expr)


    def semanticPredicateExpr(self):
        expr = self.builder.compilePythonExpr(self.name,
                                              self.pythonExpr(')')[0])
        return self.builder.pred(expr)


    def rule_number(self):
        _locals = {'self': self}
        self.locals['number'] = _locals
        lastValue, lastError = self.apply("spaces", )
        self.considerError(lastError)
        def _G__or_1():
            lastValue, lastError = self.exactly('-')
            self.considerError(lastError)
            _locals['x'] = ['lastValue, lastError = self.apply("barenumber", )', 'self.considerError(lastError)']
            lastValue, lastError = _locals['x']
            self.considerError(lastError)
            lastValue, lastError = (eval('self.builder.exactly(-x)', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_2():
            _locals['x'] = ['lastValue, lastError = self.apply("barenumber", )', 'self.considerError(lastError)']
            lastValue, lastError = _locals['x']
            self.considerError(lastError)
            lastValue, lastError = (eval('self.builder.exactly(x)', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_1, _G__or_2])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_barenumber(self):
        _locals = {'self': self}
        self.locals['barenumber'] = _locals
        def _G__or_10():
            lastValue, lastError = self.exactly('0')
            self.considerError(lastError)
            def _G__or_7():
                def _G__or_3():
                    lastValue, lastError = self.exactly('x')
                    self.considerError(lastError)
                    return (lastValue, self.currentError)
                def _G__or_4():
                    lastValue, lastError = self.exactly('X')
                    self.considerError(lastError)
                    return (lastValue, self.currentError)
                lastValue, lastError = self._or([_G__or_3, _G__or_4])
                self.considerError(lastError)
                def _G_many_5():
                    lastValue, lastError = self.apply("hexdigit", )
                    self.considerError(lastError)
                    return (lastValue, self.currentError)
                _locals['hs'] = self.many(_G_many_5)
                lastValue, lastError = _locals['hs']
                self.considerError(lastError)
                lastValue, lastError = (eval("int(''.join(hs), 16)", self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            def _G__or_8():
                def _G_many_6():
                    lastValue, lastError = self.apply("octaldigit", )
                    self.considerError(lastError)
                    return (lastValue, self.currentError)
                _locals['ds'] = self.many(_G_many_6)
                lastValue, lastError = _locals['ds']
                self.considerError(lastError)
                lastValue, lastError = (eval("int('0'+''.join(ds), 8)", self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            lastValue, lastError = self._or([_G__or_7, _G__or_8])
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_11():
            def _G_many_9():
                lastValue, lastError = self.apply("digit", )
                self.considerError(lastError)
                return (lastValue, self.currentError)
            lastValue, lastError = self.many(_G_many_9, _G_many_9())
            _locals['ds'] = self.considerError(lastError)
            lastValue, lastError = _locals['ds']
            self.considerError(lastError)
            lastValue, lastError = (eval("int(''.join(ds))", self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_10, _G__or_11])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_octaldigit(self):
        _locals = {'self': self}
        self.locals['octaldigit'] = _locals
        _locals['x'] = ['lastValue, lastError = self.apply("anything", )', 'self.considerError(lastError)']
        lastValue, lastError = _locals['x']
        self.considerError(lastError)
        def _G_pred_12():
            lastValue, lastError = (eval('x in string.octdigits', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self.pred(_G_pred_12)
        self.considerError(lastError)
        lastValue, lastError = (eval('x', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_hexdigit(self):
        _locals = {'self': self}
        self.locals['hexdigit'] = _locals
        _locals['x'] = ['lastValue, lastError = self.apply("anything", )', 'self.considerError(lastError)']
        lastValue, lastError = _locals['x']
        self.considerError(lastError)
        def _G_pred_13():
            lastValue, lastError = (eval('x in string.hexdigits', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self.pred(_G_pred_13)
        self.considerError(lastError)
        lastValue, lastError = (eval('x', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_escapedChar(self):
        _locals = {'self': self}
        self.locals['escapedChar'] = _locals
        lastValue, lastError = self.exactly('\\')
        self.considerError(lastError)
        def _G__or_14():
            lastValue, lastError = self.exactly('n')
            self.considerError(lastError)
            lastValue, lastError = (eval('"\\n"', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_15():
            lastValue, lastError = self.exactly('r')
            self.considerError(lastError)
            lastValue, lastError = (eval('"\\r"', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_16():
            lastValue, lastError = self.exactly('t')
            self.considerError(lastError)
            lastValue, lastError = (eval('"\\t"', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_17():
            lastValue, lastError = self.exactly('b')
            self.considerError(lastError)
            lastValue, lastError = (eval('"\\b"', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_18():
            lastValue, lastError = self.exactly('f')
            self.considerError(lastError)
            lastValue, lastError = (eval('"\\f"', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_19():
            lastValue, lastError = self.exactly('"')
            self.considerError(lastError)
            lastValue, lastError = (eval('\'"\'', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_20():
            lastValue, lastError = self.exactly("'")
            self.considerError(lastError)
            lastValue, lastError = (eval('"\'"', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_21():
            lastValue, lastError = self.exactly('\\')
            self.considerError(lastError)
            lastValue, lastError = (eval('"\\\\"', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_14, _G__or_15, _G__or_16, _G__or_17, _G__or_18, _G__or_19, _G__or_20, _G__or_21])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_character(self):
        _locals = {'self': self}
        self.locals['character'] = _locals
        lastValue, lastError = self.apply("token", lastValue, lastError = (eval('"\'"', self.globals, _locals), self.currentError), self.considerError(lastError))
        self.considerError(lastError)
        def _G__or_22():
            lastValue, lastError = self.apply("escapedChar", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_23():
            lastValue, lastError = self.apply("anything", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_22, _G__or_23])
        _locals['c'] = self.considerError(lastError)
        lastValue, lastError = _locals['c']
        self.considerError(lastError)
        lastValue, lastError = self.apply("token", lastValue, lastError = (eval('"\'"', self.globals, _locals), self.currentError), self.considerError(lastError))
        self.considerError(lastError)
        lastValue, lastError = (eval('self.builder.exactly(c)', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_string(self):
        _locals = {'self': self}
        self.locals['string'] = _locals
        lastValue, lastError = self.apply("token", lastValue, lastError = (eval('\'"\'', self.globals, _locals), self.currentError), self.considerError(lastError))
        self.considerError(lastError)
        def _G_many_27():
            def _G__or_25():
                lastValue, lastError = self.apply("escapedChar", )
                self.considerError(lastError)
                return (lastValue, self.currentError)
            def _G__or_26():
                def _G__not_24():
                    lastValue, lastError = self.exactly('"')
                    self.considerError(lastError)
                    return (lastValue, self.currentError)
                lastValue, lastError = self._not(_G__not_24)
                self.considerError(lastError)
                lastValue, lastError = self.apply("anything", )
                self.considerError(lastError)
                return (lastValue, self.currentError)
            lastValue, lastError = self._or([_G__or_25, _G__or_26])
            self.considerError(lastError)
            return (lastValue, self.currentError)
        _locals['c'] = self.many(_G_many_27)
        lastValue, lastError = _locals['c']
        self.considerError(lastError)
        lastValue, lastError = self.apply("token", lastValue, lastError = (eval('\'"\'', self.globals, _locals), self.currentError), self.considerError(lastError))
        self.considerError(lastError)
        lastValue, lastError = (eval("self.builder.exactly(''.join(c))", self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_name(self):
        _locals = {'self': self}
        self.locals['name'] = _locals
        _locals['x'] = ['lastValue, lastError = self.apply("letter", )', 'self.considerError(lastError)']
        lastValue, lastError = _locals['x']
        self.considerError(lastError)
        def _G_many_28():
            lastValue, lastError = self.apply("letterOrDigit", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        _locals['xs'] = self.many(_G_many_28)
        lastValue, lastError = _locals['xs']
        self.considerError(lastError)
        lastValue, lastError = (eval('xs.insert(0, x)', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        lastValue, lastError = (eval("''.join(xs)", self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_application(self):
        _locals = {'self': self}
        self.locals['application'] = _locals
        lastValue, lastError = self.apply("token", lastValue, lastError = (eval("'<'", self.globals, _locals), self.currentError), self.considerError(lastError))
        self.considerError(lastError)
        lastValue, lastError = self.apply("spaces", )
        self.considerError(lastError)
        _locals['name'] = ['lastValue, lastError = self.apply("name", )', 'self.considerError(lastError)']
        lastValue, lastError = _locals['name']
        self.considerError(lastError)
        def _G__or_29():
            lastValue, lastError = self.exactly(' ')
            self.considerError(lastError)
            _locals['args'] = ["lastValue, lastError = (eval('self.applicationArgs()', self.globals, _locals), self.currentError)", 'self.considerError(lastError)']
            lastValue, lastError = _locals['args']
            self.considerError(lastError)
            lastValue, lastError = (eval('self.builder.apply(name, self.name, *args)', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_30():
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval("'>'", self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            lastValue, lastError = (eval('self.builder.apply(name, self.name)', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_29, _G__or_30])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_expr1(self):
        _locals = {'self': self}
        self.locals['expr1'] = _locals
        def _G__or_31():
            lastValue, lastError = self.apply("application", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_32():
            lastValue, lastError = self.apply("ruleValue", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_33():
            lastValue, lastError = self.apply("semanticPredicate", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_34():
            lastValue, lastError = self.apply("semanticAction", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_35():
            lastValue, lastError = self.apply("number", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_36():
            lastValue, lastError = self.apply("character", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_37():
            lastValue, lastError = self.apply("string", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_38():
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval("'('", self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            _locals['e'] = ['lastValue, lastError = self.apply("expr", )', 'self.considerError(lastError)']
            lastValue, lastError = _locals['e']
            self.considerError(lastError)
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval("')'", self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            lastValue, lastError = (eval('e', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_39():
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval("'['", self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            _locals['e'] = ['lastValue, lastError = self.apply("expr", )', 'self.considerError(lastError)']
            lastValue, lastError = _locals['e']
            self.considerError(lastError)
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval("']'", self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            lastValue, lastError = (eval('self.builder.listpattern(e)', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_31, _G__or_32, _G__or_33, _G__or_34, _G__or_35, _G__or_36, _G__or_37, _G__or_38, _G__or_39])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_expr2(self):
        _locals = {'self': self}
        self.locals['expr2'] = _locals
        def _G__or_42():
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval("'~'", self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            def _G__or_40():
                lastValue, lastError = self.apply("token", lastValue, lastError = (eval("'~'", self.globals, _locals), self.currentError), self.considerError(lastError))
                self.considerError(lastError)
                _locals['e'] = ['lastValue, lastError = self.apply("expr2", )', 'self.considerError(lastError)']
                lastValue, lastError = _locals['e']
                self.considerError(lastError)
                lastValue, lastError = (eval('self.builder.lookahead(e)', self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            def _G__or_41():
                _locals['e'] = ['lastValue, lastError = self.apply("expr2", )', 'self.considerError(lastError)']
                lastValue, lastError = _locals['e']
                self.considerError(lastError)
                lastValue, lastError = (eval('self.builder._not(e)', self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            lastValue, lastError = self._or([_G__or_40, _G__or_41])
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_43():
            lastValue, lastError = self.apply("expr1", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_42, _G__or_43])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_expr3(self):
        _locals = {'self': self}
        self.locals['expr3'] = _locals
        def _G__or_50():
            _locals['e'] = ['lastValue, lastError = self.apply("expr2", )', 'self.considerError(lastError)']
            lastValue, lastError = _locals['e']
            self.considerError(lastError)
            def _G__or_44():
                lastValue, lastError = self.exactly('*')
                self.considerError(lastError)
                lastValue, lastError = (eval('self.builder.many(e)', self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            def _G__or_45():
                lastValue, lastError = self.exactly('+')
                self.considerError(lastError)
                lastValue, lastError = (eval('self.builder.many1(e)', self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            def _G__or_46():
                lastValue, lastError = self.exactly('?')
                self.considerError(lastError)
                lastValue, lastError = (eval('self.builder.optional(e)', self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            def _G__or_47():
                lastValue, lastError = (eval('e', self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            lastValue, lastError = self._or([_G__or_44, _G__or_45, _G__or_46, _G__or_47])
            _locals['r'] = self.considerError(lastError)
            lastValue, lastError = _locals['r']
            self.considerError(lastError)
            def _G__or_48():
                lastValue, lastError = self.exactly(':')
                self.considerError(lastError)
                _locals['n'] = ['lastValue, lastError = self.apply("name", )', 'self.considerError(lastError)']
                lastValue, lastError = _locals['n']
                self.considerError(lastError)
                lastValue, lastError = (eval('self.builder.bind(r, n)', self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            def _G__or_49():
                lastValue, lastError = (eval('r', self.globals, _locals), self.currentError)
                self.considerError(lastError)
                return (lastValue, self.currentError)
            lastValue, lastError = self._or([_G__or_48, _G__or_49])
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_51():
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval("':'", self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            _locals['n'] = ['lastValue, lastError = self.apply("name", )', 'self.considerError(lastError)']
            lastValue, lastError = _locals['n']
            self.considerError(lastError)
            lastValue, lastError = (eval('self.builder.bind(self.builder.apply("anything", self.name), n)', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_50, _G__or_51])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_expr4(self):
        _locals = {'self': self}
        self.locals['expr4'] = _locals
        def _G_many_52():
            lastValue, lastError = self.apply("expr3", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        _locals['es'] = self.many(_G_many_52)
        lastValue, lastError = _locals['es']
        self.considerError(lastError)
        lastValue, lastError = (eval('self.builder.sequence(es)', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_expr(self):
        _locals = {'self': self}
        self.locals['expr'] = _locals
        _locals['e'] = ['lastValue, lastError = self.apply("expr4", )', 'self.considerError(lastError)']
        lastValue, lastError = _locals['e']
        self.considerError(lastError)
        def _G_many_53():
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval("'|'", self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            lastValue, lastError = self.apply("expr4", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        _locals['es'] = self.many(_G_many_53)
        lastValue, lastError = _locals['es']
        self.considerError(lastError)
        lastValue, lastError = (eval('es.insert(0, e)', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        lastValue, lastError = (eval('self.builder._or(es)', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_ruleValue(self):
        _locals = {'self': self}
        self.locals['ruleValue'] = _locals
        lastValue, lastError = self.apply("token", lastValue, lastError = (eval('"=>"', self.globals, _locals), self.currentError), self.considerError(lastError))
        self.considerError(lastError)
        lastValue, lastError = (eval('self.ruleValueExpr()', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_semanticPredicate(self):
        _locals = {'self': self}
        self.locals['semanticPredicate'] = _locals
        lastValue, lastError = self.apply("token", lastValue, lastError = (eval('"?("', self.globals, _locals), self.currentError), self.considerError(lastError))
        self.considerError(lastError)
        lastValue, lastError = (eval('self.semanticPredicateExpr()', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_semanticAction(self):
        _locals = {'self': self}
        self.locals['semanticAction'] = _locals
        lastValue, lastError = self.apply("token", lastValue, lastError = (eval('"!("', self.globals, _locals), self.currentError), self.considerError(lastError))
        self.considerError(lastError)
        lastValue, lastError = (eval('self.semanticActionExpr()', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_rulePart(self):
        _locals = {'self': self}
        self.locals['rulePart'] = _locals
        _locals['requiredName'] = ['lastValue, lastError = self.apply("anything", )', 'self.considerError(lastError)']
        lastValue, lastError = _locals['requiredName']
        self.considerError(lastError)
        lastValue, lastError = self.apply("spaces", )
        self.considerError(lastError)
        _locals['n'] = ['lastValue, lastError = self.apply("name", )', 'self.considerError(lastError)']
        lastValue, lastError = _locals['n']
        self.considerError(lastError)
        def _G_pred_54():
            lastValue, lastError = (eval('n == requiredName', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self.pred(_G_pred_54)
        self.considerError(lastError)
        lastValue, lastError = (eval('setattr(self, "name", n)', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        _locals['args'] = ['lastValue, lastError = self.apply("expr4", )', 'self.considerError(lastError)']
        lastValue, lastError = _locals['args']
        self.considerError(lastError)
        def _G__or_55():
            lastValue, lastError = self.apply("token", lastValue, lastError = (eval('"::="', self.globals, _locals), self.currentError), self.considerError(lastError))
            self.considerError(lastError)
            _locals['e'] = ['lastValue, lastError = self.apply("expr", )', 'self.considerError(lastError)']
            lastValue, lastError = _locals['e']
            self.considerError(lastError)
            lastValue, lastError = (eval('self.builder.sequence([args, e])', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_56():
            lastValue, lastError = (eval('args', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_55, _G__or_56])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_rule(self):
        _locals = {'self': self}
        self.locals['rule'] = _locals
        lastValue, lastError = self.apply("spaces", )
        self.considerError(lastError)
        def _G_lookahead_57():
            _locals['n'] = ['lastValue, lastError = self.apply("name", )', 'self.considerError(lastError)']
            lastValue, lastError = _locals['n']
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self.lookahead(_G_lookahead_57)
        self.considerError(lastError)
        _locals['r'] = ['lastValue, lastError = self.apply("rulePart", lastValue, lastError = (eval(\'n\', self.globals, _locals), self.currentError), self.considerError(lastError))', 'self.considerError(lastError)']
        lastValue, lastError = _locals['r']
        self.considerError(lastError)
        def _G__or_59():
            def _G_many_58():
                lastValue, lastError = self.apply("rulePart", lastValue, lastError = (eval('n', self.globals, _locals), self.currentError), self.considerError(lastError))
                self.considerError(lastError)
                return (lastValue, self.currentError)
            lastValue, lastError = self.many(_G_many_58, _G_many_58())
            _locals['rs'] = self.considerError(lastError)
            lastValue, lastError = _locals['rs']
            self.considerError(lastError)
            lastValue, lastError = (eval('(n, self.builder._or([r] + rs))', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        def _G__or_60():
            lastValue, lastError = (eval('(n, r)', self.globals, _locals), self.currentError)
            self.considerError(lastError)
            return (lastValue, self.currentError)
        lastValue, lastError = self._or([_G__or_59, _G__or_60])
        self.considerError(lastError)
        return (lastValue, self.currentError)


    def rule_grammar(self):
        _locals = {'self': self}
        self.locals['grammar'] = _locals
        def _G_many_61():
            lastValue, lastError = self.apply("rule", )
            self.considerError(lastError)
            return (lastValue, self.currentError)
        _locals['rs'] = self.many(_G_many_61)
        lastValue, lastError = _locals['rs']
        self.considerError(lastError)
        lastValue, lastError = self.apply("spaces", )
        self.considerError(lastError)
        lastValue, lastError = (eval('self.builder.makeGrammar(rs)', self.globals, _locals), self.currentError)
        self.considerError(lastError)
        return (lastValue, self.currentError)

