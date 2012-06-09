from ometa.runtime import OMetaGrammarBase as GrammarBase
class Parser(GrammarBase):
    def rule_spaces(self):
        _locals = {'self': self}
        self.locals['spaces'] = _locals
        def _G_many_1():
            def _G_or_1():
                _G_exactly_1, lastError = self.exactly(' ')
                self.considerError(lastError)
                return (_G_exactly_1, self.currentError)
            def _G_or_2():
                _G_exactly_1, lastError = self.exactly('\t')
                self.considerError(lastError)
                return (_G_exactly_1, self.currentError)
            def _G_or_3():
                _G_exactly_1, lastError = self.exactly('\x0c')
                self.considerError(lastError)
                return (_G_exactly_1, self.currentError)
            def _G_or_4():
                _G_exactly_1, lastError = self.exactly('#')
                self.considerError(lastError)
                def _G_many_2():
                    def _G_not_1():
                        _G_apply_1, lastError = self._apply(self.rule_eol, "eol", [])
                        self.considerError(lastError)
                        return (_G_apply_1, self.currentError)
                    _G_not_2, lastError = self._not(_G_not_1)
                    self.considerError(lastError)
                    _G_apply_3, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError)
                    return (_G_apply_3, self.currentError)
                _G_many_3, lastError = self.many(_G_many_2)
                self.considerError(lastError)
                return (_G_many_3, self.currentError)
            _G_or_5, lastError = self._or([_G_or_1, _G_or_2, _G_or_3, _G_or_4])
            self.considerError(lastError)
            return (_G_or_5, self.currentError)
        _G_many_2, lastError = self.many(_G_many_1)
        self.considerError(lastError)
        return (_G_many_2, self.currentError)


    def rule_number(self):
        _locals = {'self': self}
        self.locals['number'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_apply_2, lastError = self._apply(self.rule_barenumber, "barenumber", [])
        self.considerError(lastError)
        return (_G_apply_2, self.currentError)


    def rule_barenumber(self):
        _locals = {'self': self}
        self.locals['barenumber'] = _locals
        def _G_optional_1():
            _G_exactly_1, lastError = self.exactly('-')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        def _G_optional_2():
            return (None, self.input.nullError())
        _G_or_3, lastError = self._or([_G_optional_1, _G_optional_2])
        self.considerError(lastError)
        _locals['sign'] = _G_or_3
        def _G_or_4():
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
                def _G_many_4():
                    _G_apply_1, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                    self.considerError(lastError)
                    return (_G_apply_1, self.currentError)
                _G_many_5, lastError = self.many(_G_many_4)
                self.considerError(lastError)
                _locals['hs'] = _G_many_5
                _G_python_6, lastError = eval('makeHex(sign, hs)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_6, self.currentError)
            def _G_or_3():
                _G_python_1, lastError = eval('sign', self.globals, _locals), None
                self.considerError(lastError)
                _G_python_2, lastError = eval("'0'", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_3, lastError = self._apply(self.rule_floatPart, "floatPart", [_G_python_1, _G_python_2])
                self.considerError(lastError)
                return (_G_apply_3, self.currentError)
            def _G_or_4():
                def _G_many_1():
                    _G_apply_1, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                    self.considerError(lastError)
                    return (_G_apply_1, self.currentError)
                _G_many_2, lastError = self.many(_G_many_1)
                self.considerError(lastError)
                _locals['ds'] = _G_many_2
                _G_python_3, lastError = eval('makeOctal(sign, ds)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_3, self.currentError)
            _G_or_5, lastError = self._or([_G_or_2, _G_or_3, _G_or_4])
            self.considerError(lastError)
            return (_G_or_5, self.currentError)
        def _G_or_5():
            _G_apply_1, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            _locals['ds'] = _G_apply_1
            _G_python_2, lastError = eval('sign', self.globals, _locals), None
            self.considerError(lastError)
            _G_python_3, lastError = eval('ds', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_4, lastError = self._apply(self.rule_floatPart, "floatPart", [_G_python_2, _G_python_3])
            self.considerError(lastError)
            return (_G_apply_4, self.currentError)
        def _G_or_6():
            _G_apply_1, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            _locals['ds'] = _G_apply_1
            _G_python_2, lastError = eval('signedInt(sign, ds)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        _G_or_7, lastError = self._or([_G_or_4, _G_or_5, _G_or_6])
        self.considerError(lastError)
        return (_G_or_7, self.currentError)


    def rule_exponent(self):
        _locals = {'self': self}
        self.locals['exponent'] = _locals
        def _G_consumedby_1():
            def _G_or_1():
                _G_exactly_1, lastError = self.exactly('e')
                self.considerError(lastError)
                return (_G_exactly_1, self.currentError)
            def _G_or_2():
                _G_exactly_1, lastError = self.exactly('E')
                self.considerError(lastError)
                return (_G_exactly_1, self.currentError)
            _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
            self.considerError(lastError)
            def _G_optional_4():
                def _G_or_1():
                    _G_exactly_1, lastError = self.exactly('+')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_2():
                    _G_exactly_1, lastError = self.exactly('-')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
                self.considerError(lastError)
                return (_G_or_3, self.currentError)
            def _G_optional_5():
                return (None, self.input.nullError())
            _G_or_6, lastError = self._or([_G_optional_4, _G_optional_5])
            self.considerError(lastError)
            _G_apply_7, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            return (_G_apply_7, self.currentError)
        _G_consumedby_2, lastError = self.consumedby(_G_consumedby_1)
        self.considerError(lastError)
        return (_G_consumedby_2, self.currentError)


    def rule_floatPart(self):
        _locals = {'self': self}
        self.locals['floatPart'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['sign'] = _G_apply_1
        _G_apply_2, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['ds'] = _G_apply_2
        def _G_consumedby_3():
            def _G_or_1():
                _G_exactly_1, lastError = self.exactly('.')
                self.considerError(lastError)
                _G_apply_2, lastError = self._apply(self.rule_decdigits, "decdigits", [])
                self.considerError(lastError)
                def _G_optional_3():
                    _G_apply_1, lastError = self._apply(self.rule_exponent, "exponent", [])
                    self.considerError(lastError)
                    return (_G_apply_1, self.currentError)
                def _G_optional_4():
                    return (None, self.input.nullError())
                _G_or_5, lastError = self._or([_G_optional_3, _G_optional_4])
                self.considerError(lastError)
                return (_G_or_5, self.currentError)
            def _G_or_2():
                _G_apply_1, lastError = self._apply(self.rule_exponent, "exponent", [])
                self.considerError(lastError)
                return (_G_apply_1, self.currentError)
            _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
            self.considerError(lastError)
            return (_G_or_3, self.currentError)
        _G_consumedby_4, lastError = self.consumedby(_G_consumedby_3)
        self.considerError(lastError)
        _locals['tail'] = _G_consumedby_4
        _G_python_5, lastError = eval('makeFloat(sign, ds, tail)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_5, self.currentError)


    def rule_decdigits(self):
        _locals = {'self': self}
        self.locals['decdigits'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_digit, "digit", [])
        self.considerError(lastError)
        _locals['d'] = _G_apply_1
        def _G_many_2():
            def _G_or_1():
                _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                _locals['x'] = _G_apply_1
                def _G_pred_2():
                    _G_python_1, lastError = eval('isDigit(x)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_1, self.currentError)
                _G_pred_3, lastError = self.pred(_G_pred_2)
                self.considerError(lastError)
                _G_python_4, lastError = eval('x', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_4, self.currentError)
            def _G_or_2():
                _G_exactly_1, lastError = self.exactly('_')
                self.considerError(lastError)
                _G_python_2, lastError = eval('""', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_2, self.currentError)
            _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
            self.considerError(lastError)
            return (_G_or_3, self.currentError)
        _G_many_3, lastError = self.many(_G_many_2)
        self.considerError(lastError)
        _locals['ds'] = _G_many_3
        _G_python_4, lastError = eval('concat(d, join(ds))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_4, self.currentError)


    def rule_octaldigit(self):
        _locals = {'self': self}
        self.locals['octaldigit'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_1
        def _G_pred_2():
            _G_python_1, lastError = eval('isOctDigit(x)', self.globals, _locals), None
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
            _G_python_1, lastError = eval('isHexDigit(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_pred_3, lastError = self.pred(_G_pred_2)
        self.considerError(lastError)
        _G_python_4, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_4, self.currentError)


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
        _G_exactly_5, lastError = self.exactly('"')
        self.considerError(lastError)
        _G_python_6, lastError = eval('join(c)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_6, self.currentError)


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
            def _G_not_1():
                def _G_or_1():
                    _G_exactly_1, lastError = self.exactly("'")
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_2():
                    _G_exactly_1, lastError = self.exactly('\n')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_3():
                    _G_exactly_1, lastError = self.exactly('\r')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_4():
                    _G_exactly_1, lastError = self.exactly('\\')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                _G_or_5, lastError = self._or([_G_or_1, _G_or_2, _G_or_3, _G_or_4])
                self.considerError(lastError)
                return (_G_or_5, self.currentError)
            _G_not_2, lastError = self._not(_G_not_1)
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError)
            return (_G_apply_3, self.currentError)
        _G_or_5, lastError = self._or([_G_or_3, _G_or_4])
        self.considerError(lastError)
        _locals['c'] = _G_or_5
        _G_exactly_6, lastError = self.exactly("'")
        self.considerError(lastError)
        _G_python_7, lastError = eval('Character(c)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_7, self.currentError)


    def rule_escapedUnicode(self):
        _locals = {'self': self}
        self.locals['escapedUnicode'] = _locals
        def _G_or_1():
            _G_exactly_1, lastError = self.exactly('u')
            self.considerError(lastError)
            def _G_consumedby_2():
                _G_apply_1, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_2, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_3, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_4, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                return (_G_apply_4, self.currentError)
            _G_consumedby_3, lastError = self.consumedby(_G_consumedby_2)
            self.considerError(lastError)
            _locals['hs'] = _G_consumedby_3
            _G_python_4, lastError = eval('unichr(int(hs, 16))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('U')
            self.considerError(lastError)
            def _G_consumedby_2():
                _G_apply_1, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_2, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_3, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_4, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_5, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_6, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_7, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_8, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                return (_G_apply_8, self.currentError)
            _G_consumedby_3, lastError = self.consumedby(_G_consumedby_2)
            self.considerError(lastError)
            _locals['hs'] = _G_consumedby_3
            _G_python_4, lastError = eval('unichr(int(hs, 16))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)


    def rule_escapedOctal(self):
        _locals = {'self': self}
        self.locals['escapedOctal'] = _locals
        def _G_or_1():
            def _G_consumedby_1():
                _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                _locals['a'] = _G_apply_1
                def _G_pred_2():
                    _G_python_1, lastError = eval('contains("0123", a)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_1, self.currentError)
                _G_pred_3, lastError = self.pred(_G_pred_2)
                self.considerError(lastError)
                def _G_optional_4():
                    _G_apply_1, lastError = self._apply(self.rule_octdigit, "octdigit", [])
                    self.considerError(lastError)
                    return (_G_apply_1, self.currentError)
                def _G_optional_5():
                    return (None, self.input.nullError())
                _G_or_6, lastError = self._or([_G_optional_4, _G_optional_5])
                self.considerError(lastError)
                def _G_optional_7():
                    _G_apply_1, lastError = self._apply(self.rule_octdigit, "octdigit", [])
                    self.considerError(lastError)
                    return (_G_apply_1, self.currentError)
                def _G_optional_8():
                    return (None, self.input.nullError())
                _G_or_9, lastError = self._or([_G_optional_7, _G_optional_8])
                self.considerError(lastError)
                return (_G_or_9, self.currentError)
            _G_consumedby_2, lastError = self.consumedby(_G_consumedby_1)
            self.considerError(lastError)
            return (_G_consumedby_2, self.currentError)
        def _G_or_2():
            def _G_consumedby_1():
                _G_apply_1, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                _locals['a'] = _G_apply_1
                def _G_pred_2():
                    _G_python_1, lastError = eval('contains("4567", a)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_1, self.currentError)
                _G_pred_3, lastError = self.pred(_G_pred_2)
                self.considerError(lastError)
                def _G_optional_4():
                    _G_apply_1, lastError = self._apply(self.rule_octdigit, "octdigit", [])
                    self.considerError(lastError)
                    return (_G_apply_1, self.currentError)
                def _G_optional_5():
                    return (None, self.input.nullError())
                _G_or_6, lastError = self._or([_G_optional_4, _G_optional_5])
                self.considerError(lastError)
                return (_G_or_6, self.currentError)
            _G_consumedby_2, lastError = self.consumedby(_G_consumedby_1)
            self.considerError(lastError)
            return (_G_consumedby_2, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        _locals['os'] = _G_or_3
        _G_python_4, lastError = eval('int(os, 8)', self.globals, _locals), None
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
            _G_python_2, lastError = eval("'\\n'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_3():
            _G_exactly_1, lastError = self.exactly('r')
            self.considerError(lastError)
            _G_python_2, lastError = eval("'\\r'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_4():
            _G_exactly_1, lastError = self.exactly('t')
            self.considerError(lastError)
            _G_python_2, lastError = eval("'\\t'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_5():
            _G_exactly_1, lastError = self.exactly('b')
            self.considerError(lastError)
            _G_python_2, lastError = eval("'\\b'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_6():
            _G_exactly_1, lastError = self.exactly('f')
            self.considerError(lastError)
            _G_python_2, lastError = eval("'\\f'", self.globals, _locals), None
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
            _G_python_2, lastError = eval("'\\''", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_9():
            _G_exactly_1, lastError = self.exactly('?')
            self.considerError(lastError)
            _G_python_2, lastError = eval("'?'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_10():
            _G_exactly_1, lastError = self.exactly('\\')
            self.considerError(lastError)
            _G_python_2, lastError = eval("'\\\\'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_11():
            _G_apply_1, lastError = self._apply(self.rule_escapedUnicode, "escapedUnicode", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_12():
            _G_apply_1, lastError = self._apply(self.rule_escapedOctal, "escapedOctal", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_13():
            _G_apply_1, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_eol, "eol", [])
            self.considerError(lastError)
            _G_python_3, lastError = eval('""', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_3, self.currentError)
        _G_or_14, lastError = self._or([_G_or_2, _G_or_3, _G_or_4, _G_or_5, _G_or_6, _G_or_7, _G_or_8, _G_or_9, _G_or_10, _G_or_11, _G_or_12, _G_or_13])
        self.considerError(lastError)
        return (_G_or_14, self.currentError)


    def rule_eol(self):
        _locals = {'self': self}
        self.locals['eol'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('\r')
            self.considerError(lastError)
            _G_exactly_2, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_2, self.currentError)
        def _G_or_3():
            _G_exactly_1, lastError = self.exactly('\r')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        def _G_or_4():
            _G_exactly_1, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        _G_or_5, lastError = self._or([_G_or_2, _G_or_3, _G_or_4])
        self.considerError(lastError)
        return (_G_or_5, self.currentError)


    def rule_uriBody(self):
        _locals = {'self': self}
        self.locals['uriBody'] = _locals
        def _G_consumedby_1():
            def _G_many1_1():
                def _G_or_1():
                    _G_apply_1, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                    self.considerError(lastError)
                    return (_G_apply_1, self.currentError)
                def _G_or_2():
                    _G_exactly_1, lastError = self.exactly(';')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_3():
                    _G_exactly_1, lastError = self.exactly('/')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_4():
                    _G_exactly_1, lastError = self.exactly('?')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_5():
                    _G_exactly_1, lastError = self.exactly(':')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_6():
                    _G_exactly_1, lastError = self.exactly('@')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_7():
                    _G_exactly_1, lastError = self.exactly('&')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_8():
                    _G_exactly_1, lastError = self.exactly('=')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_9():
                    _G_exactly_1, lastError = self.exactly('+')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_10():
                    _G_exactly_1, lastError = self.exactly('$')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_11():
                    _G_exactly_1, lastError = self.exactly(',')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_12():
                    _G_exactly_1, lastError = self.exactly('-')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_13():
                    _G_exactly_1, lastError = self.exactly('.')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_14():
                    _G_exactly_1, lastError = self.exactly('!')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_15():
                    _G_exactly_1, lastError = self.exactly('~')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_16():
                    _G_exactly_1, lastError = self.exactly('*')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_17():
                    _G_exactly_1, lastError = self.exactly("'")
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_18():
                    _G_exactly_1, lastError = self.exactly('(')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_19():
                    _G_exactly_1, lastError = self.exactly(')')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_20():
                    _G_exactly_1, lastError = self.exactly('%')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_21():
                    _G_exactly_1, lastError = self.exactly('\\')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_22():
                    _G_exactly_1, lastError = self.exactly('|')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                def _G_or_23():
                    _G_exactly_1, lastError = self.exactly('#')
                    self.considerError(lastError)
                    return (_G_exactly_1, self.currentError)
                _G_or_24, lastError = self._or([_G_or_1, _G_or_2, _G_or_3, _G_or_4, _G_or_5, _G_or_6, _G_or_7, _G_or_8, _G_or_9, _G_or_10, _G_or_11, _G_or_12, _G_or_13, _G_or_14, _G_or_15, _G_or_16, _G_or_17, _G_or_18, _G_or_19, _G_or_20, _G_or_21, _G_or_22, _G_or_23])
                self.considerError(lastError)
                return (_G_or_24, self.currentError)
            _G_many1_2, lastError = self.many(_G_many1_1, _G_many1_1())
            self.considerError(lastError)
            return (_G_many1_2, self.currentError)
        _G_consumedby_2, lastError = self.consumedby(_G_consumedby_1)
        self.considerError(lastError)
        return (_G_consumedby_2, self.currentError)