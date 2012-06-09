from ometa.runtime import OMetaGrammarBase as GrammarBase
class BootOMetaGrammar(GrammarBase):
    def rule_hspace(self):
        _locals = {'self': self}
        self.locals['hspace'] = _locals
        def _G_or_1():
            _G_exactly_1, lastError = self.exactly(' ')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('\t')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)


    def rule_vspace(self):
        _locals = {'self': self}
        self.locals['vspace'] = _locals
        def _G_or_1():
            _G_python_1, lastError = eval('"\\r\\n"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            return (_G_apply_2, self.currentError)
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('\r')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        def _G_or_3():
            _G_exactly_1, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        _G_or_4, lastError = self._or([_G_or_1, _G_or_2, _G_or_3])
        self.considerError(lastError)
        return (_G_or_4, self.currentError)


    def rule_emptyline(self):
        _locals = {'self': self}
        self.locals['emptyline'] = _locals
        def _G_many_1():
            _G_apply_1, lastError = self._apply(self.rule_hspace, "hspace", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_many_2, lastError = self.many(_G_many_1)
        self.considerError(lastError)
        _G_apply_3, lastError = self._apply(self.rule_vspace, "vspace", [])
        self.considerError(lastError)
        return (_G_apply_3, self.currentError)


    def rule_indentation(self):
        _locals = {'self': self}
        self.locals['indentation'] = _locals
        def _G_many_1():
            _G_apply_1, lastError = self._apply(self.rule_emptyline, "emptyline", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_many_2, lastError = self.many(_G_many_1)
        self.considerError(lastError)
        def _G_many1_3():
            _G_apply_1, lastError = self._apply(self.rule_hspace, "hspace", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_many1_4, lastError = self.many(_G_many1_3, _G_many1_3())
        self.considerError(lastError)
        return (_G_many1_4, self.currentError)


    def rule_noindentation(self):
        _locals = {'self': self}
        self.locals['noindentation'] = _locals
        def _G_many_1():
            _G_apply_1, lastError = self._apply(self.rule_emptyline, "emptyline", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_many_2, lastError = self.many(_G_many_1)
        self.considerError(lastError)
        def _G_lookahead_3():
            def _G_not_1():
                _G_apply_1, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError)
                return (_G_apply_1, self.currentError)
            _G_not_2, lastError = self._not(_G_not_1)
            self.considerError(lastError)
            return (_G_not_2, self.currentError)
        _G_lookahead_4, lastError = self.lookahead(_G_lookahead_3)
        self.considerError(lastError)
        return (_G_lookahead_4, self.currentError)


    def rule_number(self):
        _locals = {'self': self}
        self.locals['number'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('-')
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_2
            _G_python_3, lastError = eval('self.builder.exactly(-x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_3, self.currentError)
        def _G_or_3():
            _G_apply_1, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_1
            _G_python_2, lastError = eval('self.builder.exactly(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        _G_or_4, lastError = self._or([_G_or_2, _G_or_3])
        self.considerError(lastError)
        return (_G_or_4, self.currentError)


    def rule_barenumber(self):
        _locals = {'self': self}
        self.locals['barenumber'] = _locals
        def _G_or_1():
            _G_exactly_1, lastError = self.exactly('0')
            self.considerError(lastError)
            def _G_or_2():
                def _G_or_1():
                    _G_exactly_1, lastError = self.exactly('x')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_2():
                    _G_exactly_1, lastError = self.exactly('X')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
                self.considerError(lastError)
                def _G_consumedby_4():
                    def _G_many1_1():
                        _G_apply_1, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                        self.considerError(lastError)
                        return (_G_apply_1, self.currentError)
                    _G_many1_2, lastError = self.many(_G_many1_1, _G_many1_1())
                    self.considerError(lastError)
                    return (_G_many1_2, self.currentError)
                _G_consumedby_5, lastError = self.consumedby(_G_consumedby_4)
                self.considerError(lastError)
                _locals['hs'] = _G_consumedby_5
                _G_python_6, lastError = eval('int(hs, 16)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_6, self.currentError)
            def _G_or_3():
                def _G_consumedby_1():
                    def _G_many1_1():
                        _G_apply_1, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                        self.considerError(lastError)
                        return (_G_apply_1, self.currentError)
                    _G_many1_2, lastError = self.many(_G_many1_1, _G_many1_1())
                    self.considerError(lastError)
                    return (_G_many1_2, self.currentError)
                _G_consumedby_2, lastError = self.consumedby(_G_consumedby_1)
                self.considerError(lastError)
                _locals['ds'] = _G_consumedby_2
                _G_python_3, lastError = eval('int(ds, 8)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_3, self.currentError)
            _G_or_4, lastError = self._or([_G_or_2, _G_or_3])
            self.considerError(lastError)
            return (_G_or_4, self.currentError)
        def _G_or_2():
            def _G_consumedby_1():
                def _G_many1_1():
                    _G_apply_1, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError)
                    return (_G_apply_1, self.currentError)
                _G_many1_2, lastError = self.many(_G_many1_1, _G_many1_1())
                self.considerError(lastError)
                return (_G_many1_2, self.currentError)
            _G_consumedby_2, lastError = self.consumedby(_G_consumedby_1)
            self.considerError(lastError)
            _locals['ds'] = _G_consumedby_2
            _G_python_3, lastError = eval('int(ds)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_3, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)


    def rule_octaldigit(self):
        _locals = {'self': self}
        self.locals['octaldigit'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_1
        def _G_pred_2():
            _G_python_1, lastError = eval("x in '01234567'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_pred_3, lastError = self.pred(_G_pred_2)
        self.considerError(lastError)
        _G_python_4, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_4, self.currentError)


    def rule_hexdigit(self):
        _locals = {'self': self}
        self.locals['hexdigit'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_1
        def _G_pred_2():
            _G_python_1, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_pred_3, lastError = self.pred(_G_pred_2)
        self.considerError(lastError)
        _G_python_4, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_4, self.currentError)


    def rule_escapedChar(self):
        _locals = {'self': self}
        self.locals['escapedChar'] = _locals
        _G_exactly_1, lastError = self.exactly('\\')
        self.considerError(lastError)
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('n')
            self.considerError(lastError)
            _G_python_2, lastError = eval('"\\n"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_3():
            _G_exactly_1, lastError = self.exactly('r')
            self.considerError(lastError)
            _G_python_2, lastError = eval('"\\r"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_4():
            _G_exactly_1, lastError = self.exactly('t')
            self.considerError(lastError)
            _G_python_2, lastError = eval('"\\t"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_5():
            _G_exactly_1, lastError = self.exactly('b')
            self.considerError(lastError)
            _G_python_2, lastError = eval('"\\b"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_6():
            _G_exactly_1, lastError = self.exactly('f')
            self.considerError(lastError)
            _G_python_2, lastError = eval('"\\f"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_7():
            _G_exactly_1, lastError = self.exactly('"')
            self.considerError(lastError)
            _G_python_2, lastError = eval('\'"\'', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_8():
            _G_exactly_1, lastError = self.exactly("'")
            self.considerError(lastError)
            _G_python_2, lastError = eval('"\'"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_9():
            _G_exactly_1, lastError = self.exactly('\\')
            self.considerError(lastError)
            _G_python_2, lastError = eval('"\\\\"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        _G_or_10, lastError = self._or([_G_or_2, _G_or_3, _G_or_4, _G_or_5, _G_or_6, _G_or_7, _G_or_8, _G_or_9])
        self.considerError(lastError)
        return (_G_or_10, self.currentError)


    def rule_character(self):
        _locals = {'self': self}
        self.locals['character'] = _locals
        _G_python_1, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
        self.considerError(lastError)
        def _G_or_3():
            _G_apply_1, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_4():
            _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_or_5, lastError = self._or([_G_or_3, _G_or_4])
        self.considerError(lastError)
        _locals['c'] = _G_or_5
        _G_python_6, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_7, lastError = self._apply(self.rule_token, "token", [_G_python_6])
        self.considerError(lastError)
        _G_python_8, lastError = eval('self.builder.exactly(c)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_8, self.currentError)


    def rule_string(self):
        _locals = {'self': self}
        self.locals['string'] = _locals
        _G_python_1, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
        self.considerError(lastError)
        def _G_many_3():
            def _G_or_1():
                _G_apply_1, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                self.considerError(lastError)
                return (_G_apply_1, self.currentError)
            def _G_or_2():
                def _G_not_1():
                    _G_exactly_1, lastError = self.exactly('"')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                _G_not_2, lastError = self._not(_G_not_1)
                self.considerError(lastError)
                _G_apply_3, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                return (_G_apply_3, self.currentError)
            _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
            self.considerError(lastError)
            return (_G_or_3, self.currentError)
        _G_many_4, lastError = self.many(_G_many_3)
        self.considerError(lastError)
        _locals['c'] = _G_many_4
        _G_python_5, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_6, lastError = self._apply(self.rule_token, "token", [_G_python_5])
        self.considerError(lastError)
        _G_python_7, lastError = eval("self.builder.exactly(''.join(c))", self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_7, self.currentError)


    def rule_name(self):
        _locals = {'self': self}
        self.locals['name'] = _locals
        def _G_consumedby_1():
            _G_apply_1, lastError = self._apply(self.rule_letter, "letter", [])
            self.considerError(lastError)
            def _G_many_2():
                _G_apply_1, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                self.considerError(lastError)
                return (_G_apply_1, self.currentError)
            _G_many_3, lastError = self.many(_G_many_2)
            self.considerError(lastError)
            return (_G_many_3, self.currentError)
        _G_consumedby_2, lastError = self.consumedby(_G_consumedby_1)
        self.considerError(lastError)
        return (_G_consumedby_2, self.currentError)


    def rule_application(self):
        _locals = {'self': self}
        self.locals['application'] = _locals
        def _G_optional_1():
            _G_apply_1, lastError = self._apply(self.rule_indentation, "indentation", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_optional_2():
            return (None, self.input.nullError())
        _G_or_3, lastError = self._or([_G_optional_1, _G_optional_2])
        self.considerError(lastError)
        _G_apply_4, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['name'] = _G_apply_4
        def _G_or_5():
            _G_exactly_1, lastError = self.exactly('(')
            self.considerError(lastError)
            _G_python_2, lastError = eval("self.applicationArgs(finalChar=')')", self.globals, _locals), None
            self.considerError(lastError)
            _locals['args'] = _G_python_2
            _G_python_3, lastError = eval('self.builder.apply(name, self.name, *args)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_3, self.currentError)
        def _G_or_6():
            _G_python_1, lastError = eval('self.builder.apply(name, self.name)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_or_7, lastError = self._or([_G_or_5, _G_or_6])
        self.considerError(lastError)
        return (_G_or_7, self.currentError)


    def rule_expr1(self):
        _locals = {'self': self}
        self.locals['expr1'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_application, "application", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_2():
            _G_apply_1, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_3():
            _G_apply_1, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_4():
            _G_apply_1, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_5():
            _G_apply_1, lastError = self._apply(self.rule_number, "number", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_6():
            _G_apply_1, lastError = self._apply(self.rule_character, "character", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_7():
            _G_apply_1, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_8():
            _G_python_1, lastError = eval("'('", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_3
            _G_python_4, lastError = eval("')'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_5, lastError = self._apply(self.rule_token, "token", [_G_python_4])
            self.considerError(lastError)
            _G_python_6, lastError = eval('e', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_6, self.currentError)
        def _G_or_9():
            _G_python_1, lastError = eval("'<'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_3
            _G_python_4, lastError = eval("'>'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_5, lastError = self._apply(self.rule_token, "token", [_G_python_4])
            self.considerError(lastError)
            _G_python_6, lastError = eval('self.builder.consumedBy(e)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_6, self.currentError)
        def _G_or_10():
            _G_python_1, lastError = eval("'['", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_3
            _G_python_4, lastError = eval("']'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_5, lastError = self._apply(self.rule_token, "token", [_G_python_4])
            self.considerError(lastError)
            _G_python_6, lastError = eval('self.builder.listpattern(e)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_6, self.currentError)
        _G_or_11, lastError = self._or([_G_or_1, _G_or_2, _G_or_3, _G_or_4, _G_or_5, _G_or_6, _G_or_7, _G_or_8, _G_or_9, _G_or_10])
        self.considerError(lastError)
        return (_G_or_11, self.currentError)


    def rule_expr2(self):
        _locals = {'self': self}
        self.locals['expr2'] = _locals
        def _G_or_1():
            _G_python_1, lastError = eval("'~'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            def _G_or_3():
                _G_python_1, lastError = eval("'~'", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
                self.considerError(lastError)
                _G_apply_3, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_3
                _G_python_4, lastError = eval('self.builder.lookahead(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_4, self.currentError)
            def _G_or_4():
                _G_apply_1, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_1
                _G_python_2, lastError = eval('self.builder._not(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_2, self.currentError)
            _G_or_5, lastError = self._or([_G_or_3, _G_or_4])
            self.considerError(lastError)
            return (_G_or_5, self.currentError)
        def _G_or_2():
            _G_apply_1, lastError = self._apply(self.rule_expr1, "expr1", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)


    def rule_expr3(self):
        _locals = {'self': self}
        self.locals['expr3'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_expr2, "expr2", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_1
            def _G_or_2():
                _G_exactly_1, lastError = self.exactly('*')
                self.considerError(lastError)
                _G_python_2, lastError = eval('self.builder.many(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_2, self.currentError)
            def _G_or_3():
                _G_exactly_1, lastError = self.exactly('+')
                self.considerError(lastError)
                _G_python_2, lastError = eval('self.builder.many1(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_2, self.currentError)
            def _G_or_4():
                _G_exactly_1, lastError = self.exactly('?')
                self.considerError(lastError)
                _G_python_2, lastError = eval('self.builder.optional(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_2, self.currentError)
            def _G_or_5():
                _G_python_1, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_1, self.currentError)
            _G_or_6, lastError = self._or([_G_or_2, _G_or_3, _G_or_4, _G_or_5])
            self.considerError(lastError)
            _locals['r'] = _G_or_6
            def _G_or_7():
                _G_exactly_1, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_2, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError)
                _locals['n'] = _G_apply_2
                _G_python_3, lastError = eval('self.builder.bind(r, n)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_3, self.currentError)
            def _G_or_8():
                _G_python_1, lastError = eval('r', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_1, self.currentError)
            _G_or_9, lastError = self._or([_G_or_7, _G_or_8])
            self.considerError(lastError)
            return (_G_or_9, self.currentError)
        def _G_or_2():
            _G_python_1, lastError = eval("':'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_3
            _G_python_4, lastError = eval('self.builder.bind(self.builder.apply("anything", self.name), n)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)


    def rule_expr4(self):
        _locals = {'self': self}
        self.locals['expr4'] = _locals
        def _G_many_1():
            _G_apply_1, lastError = self._apply(self.rule_expr3, "expr3", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_many_2, lastError = self.many(_G_many_1)
        self.considerError(lastError)
        _locals['es'] = _G_many_2
        _G_python_3, lastError = eval('self.builder.sequence(es)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_3, self.currentError)


    def rule_expr(self):
        _locals = {'self': self}
        self.locals['expr'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['e'] = _G_apply_1
        def _G_many_2():
            _G_python_1, lastError = eval("'|'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError)
            return (_G_apply_3, self.currentError)
        _G_many_3, lastError = self.many(_G_many_2)
        self.considerError(lastError)
        _locals['es'] = _G_many_3
        _G_python_4, lastError = eval('self.builder._or([e] + es)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_4, self.currentError)


    def rule_ruleValue(self):
        _locals = {'self': self}
        self.locals['ruleValue'] = _locals
        _G_python_1, lastError = eval('"->"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
        self.considerError(lastError)
        _G_python_3, lastError = eval('self.ruleValueExpr(True)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_3, self.currentError)


    def rule_semanticPredicate(self):
        _locals = {'self': self}
        self.locals['semanticPredicate'] = _locals
        _G_python_1, lastError = eval('"?("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
        self.considerError(lastError)
        _G_python_3, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_3, self.currentError)


    def rule_semanticAction(self):
        _locals = {'self': self}
        self.locals['semanticAction'] = _locals
        _G_python_1, lastError = eval('"!("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
        self.considerError(lastError)
        _G_python_3, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_3, self.currentError)


    def rule_rulePart(self):
        _locals = {'self': self}
        self.locals['rulePart'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['requiredName'] = _G_apply_1
        _G_apply_2, lastError = self._apply(self.rule_noindentation, "noindentation", [])
        self.considerError(lastError)
        _G_apply_3, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['n'] = _G_apply_3
        def _G_pred_4():
            _G_python_1, lastError = eval('n == requiredName', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_pred_5, lastError = self.pred(_G_pred_4)
        self.considerError(lastError)
        _G_python_6, lastError = eval('setattr(self, "name", n)', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_7, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['args'] = _G_apply_7
        def _G_or_8():
            _G_python_1, lastError = eval('"="', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_3
            _G_python_4, lastError = eval('self.builder.sequence([args, e])', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        def _G_or_9():
            _G_python_1, lastError = eval('args', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_or_10, lastError = self._or([_G_or_8, _G_or_9])
        self.considerError(lastError)
        return (_G_or_10, self.currentError)


    def rule_rule(self):
        _locals = {'self': self}
        self.locals['rule'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_noindentation, "noindentation", [])
        self.considerError(lastError)
        def _G_lookahead_2():
            _G_apply_1, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_1
            return (_locals['n'], self.currentError)
        _G_lookahead_3, lastError = self.lookahead(_G_lookahead_2)
        self.considerError(lastError)
        _G_python_4, lastError = eval('n', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_5, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_4])
        self.considerError(lastError)
        _locals['r'] = _G_apply_5
        def _G_or_6():
            def _G_many1_1():
                _G_python_1, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_2, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_1])
                self.considerError(lastError)
                return (_G_apply_2, self.currentError)
            _G_many1_2, lastError = self.many(_G_many1_1, _G_many1_1())
            self.considerError(lastError)
            _locals['rs'] = _G_many1_2
            _G_python_3, lastError = eval('self.builder.rule(n, self.builder._or([r] + rs))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_3, self.currentError)
        def _G_or_7():
            _G_python_1, lastError = eval('self.builder.rule(n, r)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_or_8, lastError = self._or([_G_or_6, _G_or_7])
        self.considerError(lastError)
        return (_G_or_8, self.currentError)


    def rule_grammar(self):
        _locals = {'self': self}
        self.locals['grammar'] = _locals
        def _G_many_1():
            _G_apply_1, lastError = self._apply(self.rule_rule, "rule", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_many_2, lastError = self.many(_G_many_1)
        self.considerError(lastError)
        _locals['rs'] = _G_many_2
        _G_apply_3, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_python_4, lastError = eval('self.builder.makeGrammar(rs)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_4, self.currentError)
