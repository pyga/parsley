from ometa.runtime import OMetaGrammarBase as GrammarBase
class Parser(GrammarBase):
    def rule_literal(self):
        _locals = {'self': self}
        self.locals['literal'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_1
            _G_python_2, lastError = eval('Term(Tag(".String."), x, None, None)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_2():
            _G_apply_1, lastError = self._apply(self.rule_character, "character", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_1
            _G_python_2, lastError = eval('Term(Tag(".char."), x, None, None)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        def _G_or_3():
            _G_apply_1, lastError = self._apply(self.rule_number, "number", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_1
            _G_python_2, lastError = eval('Term(Tag(numberType(x)), x, None, None)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        _G_or_4, lastError = self._or([_G_or_1, _G_or_2, _G_or_3])
        self.considerError(lastError)
        return (_G_or_4, self.currentError)


    def rule_tag(self):
        _locals = {'self': self}
        self.locals['tag'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_segment, "segment", [])
            self.considerError(lastError)
            _locals['seg1'] = _G_apply_1
            def _G_many_2():
                _G_exactly_1, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_exactly_2, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_3, lastError = self._apply(self.rule_sos, "sos", [])
                self.considerError(lastError)
                return (_G_apply_3, self.currentError)
            _G_many_3, lastError = self.many(_G_many_2)
            self.considerError(lastError)
            _locals['segs'] = _G_many_3
            _G_python_4, lastError = eval('makeTag(cons(seg1, segs))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        def _G_or_2():
            def _G_many1_1():
                _G_exactly_1, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_exactly_2, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_3, lastError = self._apply(self.rule_sos, "sos", [])
                self.considerError(lastError)
                return (_G_apply_3, self.currentError)
            _G_many1_2, lastError = self.many(_G_many1_1, _G_many1_1())
            self.considerError(lastError)
            _locals['segs'] = _G_many1_2
            _G_python_3, lastError = eval('prefixedTag(segs)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_3, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)


    def rule_sos(self):
        _locals = {'self': self}
        self.locals['sos'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_segment, "segment", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_2():
            _G_apply_1, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            _locals['s'] = _G_apply_1
            _G_python_2, lastError = eval('tagString(s)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_2, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)


    def rule_segment(self):
        _locals = {'self': self}
        self.locals['segment'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_ident, "ident", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_2():
            _G_apply_1, lastError = self._apply(self.rule_special, "special", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_3():
            _G_apply_1, lastError = self._apply(self.rule_uri, "uri", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_or_4, lastError = self._or([_G_or_1, _G_or_2, _G_or_3])
        self.considerError(lastError)
        return (_G_or_4, self.currentError)


    def rule_ident(self):
        _locals = {'self': self}
        self.locals['ident'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_segStart, "segStart", [])
        self.considerError(lastError)
        _locals['i1'] = _G_apply_1
        def _G_many_2():
            _G_apply_1, lastError = self._apply(self.rule_segPart, "segPart", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_many_3, lastError = self.many(_G_many_2)
        self.considerError(lastError)
        _locals['ibits'] = _G_many_3
        _G_python_4, lastError = eval('join(cons(i1, ibits))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_4, self.currentError)


    def rule_segStart(self):
        _locals = {'self': self}
        self.locals['segStart'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_letter, "letter", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('_')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        def _G_or_3():
            _G_exactly_1, lastError = self.exactly('$')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        _G_or_4, lastError = self._or([_G_or_1, _G_or_2, _G_or_3])
        self.considerError(lastError)
        return (_G_or_4, self.currentError)


    def rule_segPart(self):
        _locals = {'self': self}
        self.locals['segPart'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('_')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        def _G_or_3():
            _G_exactly_1, lastError = self.exactly('.')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        def _G_or_4():
            _G_exactly_1, lastError = self.exactly('-')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        def _G_or_5():
            _G_exactly_1, lastError = self.exactly('$')
            self.considerError(lastError)
            return (_G_exactly_1, self.currentError)
        _G_or_6, lastError = self._or([_G_or_1, _G_or_2, _G_or_3, _G_or_4, _G_or_5])
        self.considerError(lastError)
        return (_G_or_6, self.currentError)


    def rule_special(self):
        _locals = {'self': self}
        self.locals['special'] = _locals
        _G_exactly_1, lastError = self.exactly('.')
        self.considerError(lastError)
        _locals['a'] = _G_exactly_1
        _G_apply_2, lastError = self._apply(self.rule_ident, "ident", [])
        self.considerError(lastError)
        _locals['b'] = _G_apply_2
        _G_python_3, lastError = eval('concat(a, b)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_3, self.currentError)


    def rule_uri(self):
        _locals = {'self': self}
        self.locals['uri'] = _locals
        _G_exactly_1, lastError = self.exactly('<')
        self.considerError(lastError)
        def _G_many_2():
            _G_apply_1, lastError = self._apply(self.rule_uriBody, "uriBody", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_many_3, lastError = self.many(_G_many_2)
        self.considerError(lastError)
        _locals['uriChars'] = _G_many_3
        _G_exactly_4, lastError = self.exactly('>')
        self.considerError(lastError)
        _G_python_5, lastError = eval('concat(b, uriChars, e)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_5, self.currentError)


    def rule_functor(self):
        _locals = {'self': self}
        self.locals['functor'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_or_2():
            _G_apply_1, lastError = self._apply(self.rule_literal, "literal", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_3():
            _G_apply_1, lastError = self._apply(self.rule_tag, "tag", [])
            self.considerError(lastError)
            _locals['t'] = _G_apply_1
            def _G_or_2():
                _G_apply_1, lastError = self._apply(self.rule_functorHole, "functorHole", [])
                self.considerError(lastError)
                _locals['h'] = _G_apply_1
                _G_python_2, lastError = eval('taggedHole(t, h)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_2, self.currentError)
            def _G_or_3():
                _G_python_1, lastError = eval('t', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_1, self.currentError)
            _G_or_4, lastError = self._or([_G_or_2, _G_or_3])
            self.considerError(lastError)
            return (_G_or_4, self.currentError)
        def _G_or_4():
            _G_apply_1, lastError = self._apply(self.rule_functorHole, "functorHole", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_or_5, lastError = self._or([_G_or_2, _G_or_3, _G_or_4])
        self.considerError(lastError)
        return (_G_or_5, self.currentError)


    def rule_functorHole(self):
        _locals = {'self': self}
        self.locals['functorHole'] = _locals
        def _G_or_1():
            _G_python_1, lastError = eval('"${"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_3
            _G_exactly_4, lastError = self.exactly('}')
            self.considerError(lastError)
            _G_python_5, lastError = eval('ValueHole(n)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_5, self.currentError)
        def _G_or_2():
            _G_python_1, lastError = eval('"$"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_3
            _G_python_4, lastError = eval('ValueHole(n)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        def _G_or_3():
            _G_python_1, lastError = eval('"$"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_tag, "tag", [])
            self.considerError(lastError)
            _locals['t'] = _G_apply_3
            _G_python_4, lastError = eval('NamedValueHole(t)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        def _G_or_4():
            _G_python_1, lastError = eval('"@{"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_3
            _G_exactly_4, lastError = self.exactly('}')
            self.considerError(lastError)
            _G_python_5, lastError = eval('PatternHole(n)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_5, self.currentError)
        def _G_or_5():
            _G_python_1, lastError = eval('"@"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_3
            _G_python_4, lastError = eval('PatternHole(n)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        def _G_or_6():
            _G_python_1, lastError = eval('"@"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
            self.considerError(lastError)
            _G_apply_3, lastError = self._apply(self.rule_tag, "tag", [])
            self.considerError(lastError)
            _locals['t'] = _G_apply_3
            _G_python_4, lastError = eval('NamedPatternHole(t)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        _G_or_7, lastError = self._or([_G_or_1, _G_or_2, _G_or_3, _G_or_4, _G_or_5, _G_or_6])
        self.considerError(lastError)
        return (_G_or_7, self.currentError)


    def rule_baseTerm(self):
        _locals = {'self': self}
        self.locals['baseTerm'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_functor, "functor", [])
        self.considerError(lastError)
        _locals['f'] = _G_apply_1
        def _G_or_2():
            _G_exactly_1, lastError = self.exactly('(')
            self.considerError(lastError)
            _G_apply_2, lastError = self._apply(self.rule_argList, "argList", [])
            self.considerError(lastError)
            _locals['a'] = _G_apply_2
            _G_exactly_3, lastError = self.exactly(')')
            self.considerError(lastError)
            _G_python_4, lastError = eval('makeTerm(f, a)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        def _G_or_3():
            _G_python_1, lastError = eval('makeTerm(f)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_or_4, lastError = self._or([_G_or_2, _G_or_3])
        self.considerError(lastError)
        return (_G_or_4, self.currentError)


    def rule_argList(self):
        _locals = {'self': self}
        self.locals['argList'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_term, "term", [])
            self.considerError(lastError)
            _locals['t'] = _G_apply_1
            def _G_many_2():
                _G_exactly_1, lastError = self.exactly(',')
                self.considerError(lastError)
                _G_apply_2, lastError = self._apply(self.rule_term, "term", [])
                self.considerError(lastError)
                return (_G_apply_2, self.currentError)
            _G_many_3, lastError = self.many(_G_many_2)
            self.considerError(lastError)
            _locals['ts'] = _G_many_3
            _G_python_4, lastError = eval('cons(t, ts)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_4, self.currentError)
        def _G_or_2():
            _G_python_1, lastError = eval('[]', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_1, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)


    def rule_tupleTerm(self):
        _locals = {'self': self}
        self.locals['tupleTerm'] = _locals
        _G_python_1, lastError = eval("'['", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
        self.considerError(lastError)
        _G_apply_3, lastError = self._apply(self.rule_argList, "argList", [])
        self.considerError(lastError)
        _locals['a'] = _G_apply_3
        _G_python_4, lastError = eval("']'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_5, lastError = self._apply(self.rule_token, "token", [_G_python_4])
        self.considerError(lastError)
        _G_python_6, lastError = eval('Tuple(a)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_6, self.currentError)


    def rule_bagTerm(self):
        _locals = {'self': self}
        self.locals['bagTerm'] = _locals
        _G_python_1, lastError = eval("'{'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_2, lastError = self._apply(self.rule_token, "token", [_G_python_1])
        self.considerError(lastError)
        _G_apply_3, lastError = self._apply(self.rule_argList, "argList", [])
        self.considerError(lastError)
        _locals['a'] = _G_apply_3
        _G_python_4, lastError = eval("'}'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_5, lastError = self._apply(self.rule_token, "token", [_G_python_4])
        self.considerError(lastError)
        _G_python_6, lastError = eval('Bag(a)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_6, self.currentError)


    def rule_labelledBagTerm(self):
        _locals = {'self': self}
        self.locals['labelledBagTerm'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_functor, "functor", [])
        self.considerError(lastError)
        _locals['f'] = _G_apply_1
        _G_apply_2, lastError = self._apply(self.rule_bagTerm, "bagTerm", [])
        self.considerError(lastError)
        _locals['b'] = _G_apply_2
        _G_python_3, lastError = eval('LabelledBag(f, b)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_3, self.currentError)


    def rule_extraTerm(self):
        _locals = {'self': self}
        self.locals['extraTerm'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_tupleTerm, "tupleTerm", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_2():
            _G_apply_1, lastError = self._apply(self.rule_labelledBagTerm, "labelledBagTerm", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_3():
            _G_apply_1, lastError = self._apply(self.rule_bagTerm, "bagTerm", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_4():
            _G_apply_1, lastError = self._apply(self.rule_baseTerm, "baseTerm", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_or_5, lastError = self._or([_G_or_1, _G_or_2, _G_or_3, _G_or_4])
        self.considerError(lastError)
        return (_G_or_5, self.currentError)


    def rule_attrTerm(self):
        _locals = {'self': self}
        self.locals['attrTerm'] = _locals
        _G_apply_1, lastError = self._apply(self.rule_extraTerm, "extraTerm", [])
        self.considerError(lastError)
        _locals['k'] = _G_apply_1
        _G_python_2, lastError = eval("':'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_3, lastError = self._apply(self.rule_token, "token", [_G_python_2])
        self.considerError(lastError)
        _G_apply_4, lastError = self._apply(self.rule_extraTerm, "extraTerm", [])
        self.considerError(lastError)
        _locals['v'] = _G_apply_4
        _G_python_5, lastError = eval('Attr(k, v)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_5, self.currentError)


    def rule_term(self):
        _locals = {'self': self}
        self.locals['term'] = _locals
        def _G_or_1():
            _G_apply_1, lastError = self._apply(self.rule_attrTerm, "attrTerm", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        def _G_or_2():
            _G_apply_1, lastError = self._apply(self.rule_extraTerm, "extraTerm", [])
            self.considerError(lastError)
            return (_G_apply_1, self.currentError)
        _G_or_3, lastError = self._or([_G_or_1, _G_or_2])
        self.considerError(lastError)
        return (_G_or_3, self.currentError)