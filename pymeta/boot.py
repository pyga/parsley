from pymeta.runtime import OMetaBase, ParseError
import string
from pymeta.builder import AstBuilder

class BootOMetaGrammar(OMetaBase):
    globals = globals()

    def __init__(self, input):
        OMetaBase.__init__(self, input)
        self._ruleNames = []
        self.__ometa_rules__ = {}


    def parseGrammar(self, name="Grammar", builder=AstBuilder):
        self.builder = builder(name, self)
        res = self.apply("grammar")
        x = list(self.input)
        if x:
            try:
                x = repr(''.join(x))
            except TypeError:
                pass
            raise ParseError("Grammar parse failed. Leftover bits: %s" % (x,))
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
            self.input.prev()
        return self.builder.compilePythonExpr(self.name, expr)


    def semanticActionExpr(self):
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.action(expr)


    def semanticPredicateExpr(self):
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.pred(expr)


    def rule_number(self):
        _locals = {'self': self}
        self.apply("spaces", )
        def _G__or_1():
            self.exactly('-')
            _locals['x'] = self.apply("barenumber", )
            _locals['x']
            return eval('self.builder.exactly(-x)', self.globals, _locals)
        def _G__or_2():
            _locals['x'] = self.apply("barenumber", )
            _locals['x']
            return eval('self.builder.exactly(x)', self.globals, _locals)
        return self._or([_G__or_1, _G__or_2])


    def rule_barenumber(self):
        _locals = {'self': self}
        def _G__or_10():
            self.exactly('0')
            def _G__or_7():
                def _G__or_3():
                    return self.exactly('x')
                def _G__or_4():
                    return self.exactly('X')
                self._or([_G__or_3, _G__or_4])
                def _G_many_5():
                    return self.apply("hexdigit", )
                _locals['hs'] = self.many(_G_many_5)
                _locals['hs']
                return eval("int(''.join(hs), 16)", self.globals, _locals)
            def _G__or_8():
                def _G_many_6():
                    return self.apply("octaldigit", )
                _locals['ds'] = self.many(_G_many_6)
                _locals['ds']
                return eval("int('0'+''.join(ds), 8)", self.globals, _locals)
            return self._or([_G__or_7, _G__or_8])
        def _G__or_11():
            def _G_many_9():
                return self.apply("decdigit", )
            _locals['ds'] = self.many(_G_many_9, _G_many_9())
            _locals['ds']
            return eval("int(''.join(ds))", self.globals, _locals)
        return self._or([_G__or_10, _G__or_11])


    def rule_octaldigit(self):
        _locals = {'self': self}
        _locals['x'] = self.apply("anything", )
        _locals['x']
        def _G_pred_12():
            return eval('x in string.octdigits', self.globals, _locals)
        self.pred(_G_pred_12)
        return eval('x', self.globals, _locals)


    def rule_hexdigit(self):
        _locals = {'self': self}
        _locals['x'] = self.apply("anything", )
        _locals['x']
        def _G_pred_13():
            return eval('x in string.hexdigits', self.globals, _locals)
        self.pred(_G_pred_13)
        return eval('x', self.globals, _locals)


    def rule_decdigit(self):
        _locals = {'self': self}
        _locals['x'] = self.apply("anything", )
        _locals['x']
        def _G_pred_14():
            return eval('x in string.digits', self.globals, _locals)
        self.pred(_G_pred_14)
        return eval('x', self.globals, _locals)


    def rule_character(self):
        _locals = {'self': self}
        self.apply("token", eval('"\'"', self.globals, _locals))
        _locals['c'] = self.apply("anything", )
        _locals['c']
        self.apply("token", eval('"\'"', self.globals, _locals))
        return eval('self.builder.exactly(c)', self.globals, _locals)


    def rule_name(self):
        _locals = {'self': self}
        _locals['x'] = self.apply("letter", )
        _locals['x']
        def _G_many_15():
            return self.apply("letterOrDigit", )
        _locals['xs'] = self.many(_G_many_15)
        _locals['xs']
        eval('xs.insert(0, x)', self.globals, _locals)
        return eval("''.join(xs)", self.globals, _locals)


    def rule_application(self):
        _locals = {'self': self}
        self.apply("token", eval("'<'", self.globals, _locals))
        self.apply("spaces", )
        _locals['name'] = self.apply("name", )
        _locals['name']
        def _G__or_16():
            self.exactly(' ')
            _locals['args'] = eval('self.applicationArgs()', self.globals, _locals)
            _locals['args']
            return eval('self.builder.apply(name, self.name, *args)', self.globals, _locals)
        def _G__or_17():
            self.apply("token", eval("'>'", self.globals, _locals))
            return eval('self.builder.apply(name)', self.globals, _locals)
        return self._or([_G__or_16, _G__or_17])


    def rule_expr1(self):
        _locals = {'self': self}
        def _G__or_18():
            return self.apply("application", )
        def _G__or_19():
            return self.apply("ruleValue", )
        def _G__or_20():
            return self.apply("semanticPredicate", )
        def _G__or_21():
            return self.apply("semanticAction", )
        def _G__or_22():
            return self.apply("number", )
        def _G__or_23():
            return self.apply("character", )
        def _G__or_24():
            self.apply("token", eval("'('", self.globals, _locals))
            _locals['e'] = self.apply("expr", )
            _locals['e']
            self.apply("token", eval("')'", self.globals, _locals))
            return eval('e', self.globals, _locals)
        def _G__or_25():
            self.apply("token", eval("'['", self.globals, _locals))
            _locals['e'] = self.apply("expr", )
            _locals['e']
            self.apply("token", eval("']'", self.globals, _locals))
            return eval('self.builder.listpattern(e)', self.globals, _locals)
        return self._or([_G__or_18, _G__or_19, _G__or_20, _G__or_21, _G__or_22, _G__or_23, _G__or_24, _G__or_25])


    def rule_expr2(self):
        _locals = {'self': self}
        def _G__or_28():
            self.apply("token", eval("'~'", self.globals, _locals))
            def _G__or_26():
                self.apply("token", eval("'~'", self.globals, _locals))
                _locals['e'] = self.apply("expr2", )
                _locals['e']
                return eval('self.builder.lookahead(e)', self.globals, _locals)
            def _G__or_27():
                _locals['e'] = self.apply("expr2", )
                _locals['e']
                return eval('self.builder._not(e)', self.globals, _locals)
            return self._or([_G__or_26, _G__or_27])
        def _G__or_29():
            return self.apply("expr1", )
        return self._or([_G__or_28, _G__or_29])


    def rule_expr3(self):
        _locals = {'self': self}
        def _G__or_36():
            _locals['e'] = self.apply("expr2", )
            _locals['e']
            def _G__or_30():
                self.apply("token", eval("'*'", self.globals, _locals))
                return eval('self.builder.many(e)', self.globals, _locals)
            def _G__or_31():
                self.apply("token", eval("'+'", self.globals, _locals))
                return eval('self.builder.many1(e)', self.globals, _locals)
            def _G__or_32():
                self.apply("token", eval("'?'", self.globals, _locals))
                return eval('self.builder.optional(e)', self.globals, _locals)
            def _G__or_33():
                return eval('e', self.globals, _locals)
            _locals['r'] = self._or([_G__or_30, _G__or_31, _G__or_32, _G__or_33])
            _locals['r']
            def _G__or_34():
                self.exactly(':')
                _locals['n'] = self.apply("name", )
                _locals['n']
                return eval('self.builder.bind(r, n)', self.globals, _locals)
            def _G__or_35():
                return eval('r', self.globals, _locals)
            return self._or([_G__or_34, _G__or_35])
        def _G__or_37():
            self.apply("token", eval("':'", self.globals, _locals))
            _locals['n'] = self.apply("name", )
            _locals['n']
            return eval('self.builder.bind(self.builder.apply("anything"), n)', self.globals, _locals)
        return self._or([_G__or_36, _G__or_37])


    def rule_expr4(self):
        _locals = {'self': self}
        def _G_many_38():
            return self.apply("expr3", )
        _locals['es'] = self.many(_G_many_38)
        _locals['es']
        return eval('self.builder.sequence(es)', self.globals, _locals)


    def rule_expr(self):
        _locals = {'self': self}
        _locals['e'] = self.apply("expr4", )
        _locals['e']
        def _G_many_39():
            self.apply("token", eval("'|'", self.globals, _locals))
            return self.apply("expr4", )
        _locals['es'] = self.many(_G_many_39)
        _locals['es']
        eval('es.insert(0, e)', self.globals, _locals)
        return eval('self.builder._or(es)', self.globals, _locals)


    def rule_ruleValue(self):
        _locals = {'self': self}
        self.apply("token", eval('"=>"', self.globals, _locals))
        return eval('self.ruleValueExpr()', self.globals, _locals)


    def rule_semanticPredicate(self):
        _locals = {'self': self}
        self.apply("token", eval('"?("', self.globals, _locals))
        return eval('self.semanticPredicateExpr()', self.globals, _locals)


    def rule_semanticAction(self):
        _locals = {'self': self}
        self.apply("token", eval('"!("', self.globals, _locals))
        return eval('self.semanticActionExpr()', self.globals, _locals)


    def rule_rulePart(self):
        _locals = {'self': self}
        _locals['requiredName'] = self.apply("anything", )
        _locals['requiredName']
        self.apply("spaces", )
        _locals['n'] = self.apply("name", )
        _locals['n']
        def _G_pred_40():
            return eval('n == requiredName', self.globals, _locals)
        self.pred(_G_pred_40)
        eval('setattr(self, "name", n)', self.globals, _locals)
        _locals['args'] = self.apply("expr4", )
        _locals['args']
        def _G__or_41():
            self.apply("token", eval('"::="', self.globals, _locals))
            _locals['e'] = self.apply("expr", )
            _locals['e']
            return eval('self.builder.sequence([args, e])', self.globals, _locals)
        def _G__or_42():
            return eval('args', self.globals, _locals)
        return self._or([_G__or_41, _G__or_42])


    def rule_rule(self):
        _locals = {'self': self}
        self.apply("spaces", )
        def _G_lookahead_43():
            _locals['n'] = self.apply("name", )
            return _locals['n']
        self.lookahead(_G_lookahead_43)
        _locals['r'] = self.apply("rulePart", eval('n', self.globals, _locals))
        _locals['r']
        def _G__or_45():
            def _G_many_44():
                return self.apply("rulePart", eval('n', self.globals, _locals))
            _locals['rs'] = self.many(_G_many_44, _G_many_44())
            _locals['rs']
            return eval('(n, self.builder._or([r] + rs))', self.globals, _locals)
        def _G__or_46():
            return eval('(n, r)', self.globals, _locals)
        return self._or([_G__or_45, _G__or_46])


    def rule_grammar(self):
        _locals = {'self': self}
        def _G_many_47():
            return self.apply("rule", )
        _locals['rs'] = self.many(_G_many_47)
        _locals['rs']
        self.apply("spaces", )
        return eval('self.builder.makeGrammar(rs)', self.globals, _locals)

