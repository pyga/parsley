from ometa.runtime import OMetaBase as GrammarBase
class Parser(GrammarBase):
    def rule_spaces(self):
        _locals = {'self': self}
        self.locals['spaces'] = _locals
        def _G_many_1():
            def _G_or_2():
                _G_exactly_3, lastError = self.exactly('\r')
                self.considerError(lastError)
                _G_exactly_4, lastError = self.exactly('\n')
                self.considerError(lastError)
                return (_G_exactly_4, self.currentError)
            def _G_or_5():
                _G_exactly_6, lastError = self.exactly('\r')
                self.considerError(lastError)
                return (_G_exactly_6, self.currentError)
            def _G_or_7():
                _G_exactly_8, lastError = self.exactly('\n')
                self.considerError(lastError)
                return (_G_exactly_8, self.currentError)
            def _G_or_9():
                _G_apply_10, lastError = self._apply(self.rule_horizontal_space, "horizontal_space", [])
                self.considerError(lastError)
                return (_G_apply_10, self.currentError)
            _G_or_11, lastError = self._or([_G_or_2, _G_or_5, _G_or_7, _G_or_9])
            self.considerError(lastError)
            return (_G_or_11, self.currentError)
        _G_many_12, lastError = self.many(_G_many_1)
        self.considerError(lastError)
        return (_G_many_12, self.currentError)


    def rule_literal(self):
        _locals = {'self': self}
        self.locals['literal'] = _locals
        _G_python_13, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_13
        def _G_or_14():
            _G_apply_15, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_15
            _G_python_16, lastError = eval('leafInternal(Tag(".String."), x, self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_16, self.currentError)
        def _G_or_17():
            _G_apply_18, lastError = self._apply(self.rule_character, "character", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_18
            _G_python_19, lastError = eval('leafInternal(Tag(".char."), x.args[0].data, self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_19, self.currentError)
        def _G_or_20():
            _G_apply_21, lastError = self._apply(self.rule_number, "number", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_21
            _G_python_22, lastError = eval('leafInternal(Tag(numberType(x)), x, self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_22, self.currentError)
        _G_or_23, lastError = self._or([_G_or_14, _G_or_17, _G_or_20])
        self.considerError(lastError)
        return (_G_or_23, self.currentError)


    def rule_tag(self):
        _locals = {'self': self}
        self.locals['tag'] = _locals
        def _G_or_24():
            _G_apply_25, lastError = self._apply(self.rule_segment, "segment", [])
            self.considerError(lastError)
            _locals['seg1'] = _G_apply_25
            def _G_many_26():
                _G_exactly_27, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_exactly_28, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_29, lastError = self._apply(self.rule_sos, "sos", [])
                self.considerError(lastError)
                return (_G_apply_29, self.currentError)
            _G_many_30, lastError = self.many(_G_many_26)
            self.considerError(lastError)
            _locals['segs'] = _G_many_30
            _G_python_31, lastError = eval('makeTag(cons(seg1, segs))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_31, self.currentError)
        def _G_or_32():
            def _G_many1_33():
                _G_exactly_34, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_exactly_35, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_36, lastError = self._apply(self.rule_sos, "sos", [])
                self.considerError(lastError)
                return (_G_apply_36, self.currentError)
            _G_many1_37, lastError = self.many(_G_many1_33, _G_many1_33())
            self.considerError(lastError)
            _locals['segs'] = _G_many1_37
            _G_python_38, lastError = eval('prefixedTag(segs)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_38, self.currentError)
        _G_or_39, lastError = self._or([_G_or_24, _G_or_32])
        self.considerError(lastError)
        return (_G_or_39, self.currentError)


    def rule_sos(self):
        _locals = {'self': self}
        self.locals['sos'] = _locals
        def _G_or_40():
            _G_apply_41, lastError = self._apply(self.rule_segment, "segment", [])
            self.considerError(lastError)
            return (_G_apply_41, self.currentError)
        def _G_or_42():
            _G_apply_43, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            _locals['s'] = _G_apply_43
            _G_python_44, lastError = eval('tagString(s)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_44, self.currentError)
        _G_or_45, lastError = self._or([_G_or_40, _G_or_42])
        self.considerError(lastError)
        return (_G_or_45, self.currentError)


    def rule_segment(self):
        _locals = {'self': self}
        self.locals['segment'] = _locals
        def _G_or_46():
            _G_apply_47, lastError = self._apply(self.rule_ident, "ident", [])
            self.considerError(lastError)
            return (_G_apply_47, self.currentError)
        def _G_or_48():
            _G_apply_49, lastError = self._apply(self.rule_special, "special", [])
            self.considerError(lastError)
            return (_G_apply_49, self.currentError)
        def _G_or_50():
            _G_apply_51, lastError = self._apply(self.rule_uri, "uri", [])
            self.considerError(lastError)
            return (_G_apply_51, self.currentError)
        _G_or_52, lastError = self._or([_G_or_46, _G_or_48, _G_or_50])
        self.considerError(lastError)
        return (_G_or_52, self.currentError)


    def rule_ident(self):
        _locals = {'self': self}
        self.locals['ident'] = _locals
        _G_apply_53, lastError = self._apply(self.rule_segStart, "segStart", [])
        self.considerError(lastError)
        _locals['i1'] = _G_apply_53
        def _G_many_54():
            _G_apply_55, lastError = self._apply(self.rule_segPart, "segPart", [])
            self.considerError(lastError)
            return (_G_apply_55, self.currentError)
        _G_many_56, lastError = self.many(_G_many_54)
        self.considerError(lastError)
        _locals['ibits'] = _G_many_56
        _G_python_57, lastError = eval('join(cons(i1, ibits))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_57, self.currentError)


    def rule_segStart(self):
        _locals = {'self': self}
        self.locals['segStart'] = _locals
        def _G_or_58():
            _G_apply_59, lastError = self._apply(self.rule_letter, "letter", [])
            self.considerError(lastError)
            return (_G_apply_59, self.currentError)
        def _G_or_60():
            _G_exactly_61, lastError = self.exactly('_')
            self.considerError(lastError)
            return (_G_exactly_61, self.currentError)
        def _G_or_62():
            _G_exactly_63, lastError = self.exactly('$')
            self.considerError(lastError)
            return (_G_exactly_63, self.currentError)
        _G_or_64, lastError = self._or([_G_or_58, _G_or_60, _G_or_62])
        self.considerError(lastError)
        return (_G_or_64, self.currentError)


    def rule_segPart(self):
        _locals = {'self': self}
        self.locals['segPart'] = _locals
        def _G_or_65():
            _G_apply_66, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
            self.considerError(lastError)
            return (_G_apply_66, self.currentError)
        def _G_or_67():
            _G_exactly_68, lastError = self.exactly('_')
            self.considerError(lastError)
            return (_G_exactly_68, self.currentError)
        def _G_or_69():
            _G_exactly_70, lastError = self.exactly('.')
            self.considerError(lastError)
            return (_G_exactly_70, self.currentError)
        def _G_or_71():
            _G_exactly_72, lastError = self.exactly('-')
            self.considerError(lastError)
            return (_G_exactly_72, self.currentError)
        def _G_or_73():
            _G_exactly_74, lastError = self.exactly('$')
            self.considerError(lastError)
            return (_G_exactly_74, self.currentError)
        _G_or_75, lastError = self._or([_G_or_65, _G_or_67, _G_or_69, _G_or_71, _G_or_73])
        self.considerError(lastError)
        return (_G_or_75, self.currentError)


    def rule_special(self):
        _locals = {'self': self}
        self.locals['special'] = _locals
        _G_exactly_76, lastError = self.exactly('.')
        self.considerError(lastError)
        _locals['a'] = _G_exactly_76
        _G_apply_77, lastError = self._apply(self.rule_ident, "ident", [])
        self.considerError(lastError)
        _locals['b'] = _G_apply_77
        _G_python_78, lastError = eval('concat(a, b)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_78, self.currentError)


    def rule_uri(self):
        _locals = {'self': self}
        self.locals['uri'] = _locals
        _G_exactly_79, lastError = self.exactly('<')
        self.considerError(lastError)
        def _G_many_80():
            _G_apply_81, lastError = self._apply(self.rule_uriBody, "uriBody", [])
            self.considerError(lastError)
            return (_G_apply_81, self.currentError)
        _G_many_82, lastError = self.many(_G_many_80)
        self.considerError(lastError)
        _locals['uriChars'] = _G_many_82
        _G_exactly_83, lastError = self.exactly('>')
        self.considerError(lastError)
        _G_python_84, lastError = eval('concat(b, uriChars, e)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_84, self.currentError)


    def rule_functor(self):
        _locals = {'self': self}
        self.locals['functor'] = _locals
        _G_apply_85, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_or_86():
            _G_apply_87, lastError = self._apply(self.rule_literal, "literal", [])
            self.considerError(lastError)
            return (_G_apply_87, self.currentError)
        def _G_or_88():
            _G_apply_89, lastError = self._apply(self.rule_tag, "tag", [])
            self.considerError(lastError)
            _locals['t'] = _G_apply_89
            _G_python_90, lastError = eval('leafInternal(t, None, None)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_90, self.currentError)
        _G_or_91, lastError = self._or([_G_or_86, _G_or_88])
        self.considerError(lastError)
        return (_G_or_91, self.currentError)


    def rule_baseTerm(self):
        _locals = {'self': self}
        self.locals['baseTerm'] = _locals
        _G_python_92, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_92
        _G_apply_93, lastError = self._apply(self.rule_functor, "functor", [])
        self.considerError(lastError)
        _locals['f'] = _G_apply_93
        def _G_or_94():
            _G_exactly_95, lastError = self.exactly('(')
            self.considerError(lastError)
            _G_apply_96, lastError = self._apply(self.rule_argList, "argList", [])
            self.considerError(lastError)
            _locals['a'] = _G_apply_96
            _G_apply_97, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError)
            _G_exactly_98, lastError = self.exactly(')')
            self.considerError(lastError)
            _G_python_99, lastError = eval('makeTerm(f, a, self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_99, self.currentError)
        def _G_or_100():
            _G_python_101, lastError = eval('makeTerm(f, None, self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_101, self.currentError)
        _G_or_102, lastError = self._or([_G_or_94, _G_or_100])
        self.considerError(lastError)
        return (_G_or_102, self.currentError)


    def rule_arg(self):
        _locals = {'self': self}
        self.locals['arg'] = _locals
        _G_apply_103, lastError = self._apply(self.rule_term, "term", [])
        self.considerError(lastError)
        return (_G_apply_103, self.currentError)


    def rule_argList(self):
        _locals = {'self': self}
        self.locals['argList'] = _locals
        def _G_or_104():
            _G_apply_105, lastError = self._apply(self.rule_arg, "arg", [])
            self.considerError(lastError)
            _locals['t'] = _G_apply_105
            def _G_many_106():
                _G_python_107, lastError = eval("','", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_108, lastError = self._apply(self.rule_token, "token", [_G_python_107])
                self.considerError(lastError)
                _G_apply_109, lastError = self._apply(self.rule_arg, "arg", [])
                self.considerError(lastError)
                return (_G_apply_109, self.currentError)
            _G_many_110, lastError = self.many(_G_many_106)
            self.considerError(lastError)
            _locals['ts'] = _G_many_110
            def _G_optional_111():
                _G_python_112, lastError = eval("','", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_113, lastError = self._apply(self.rule_token, "token", [_G_python_112])
                self.considerError(lastError)
                return (_G_apply_113, self.currentError)
            def _G_optional_114():
                return (None, self.input.nullError())
            _G_or_115, lastError = self._or([_G_optional_111, _G_optional_114])
            self.considerError(lastError)
            _G_python_116, lastError = eval('cons(t, ts)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_116, self.currentError)
        def _G_or_117():
            _G_python_118, lastError = eval('[]', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_118, self.currentError)
        _G_or_119, lastError = self._or([_G_or_104, _G_or_117])
        self.considerError(lastError)
        return (_G_or_119, self.currentError)


    def rule_tupleTerm(self):
        _locals = {'self': self}
        self.locals['tupleTerm'] = _locals
        _G_python_120, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_120
        _G_python_121, lastError = eval("'['", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_122, lastError = self._apply(self.rule_token, "token", [_G_python_121])
        self.considerError(lastError)
        _G_apply_123, lastError = self._apply(self.rule_argList, "argList", [])
        self.considerError(lastError)
        _locals['a'] = _G_apply_123
        _G_python_124, lastError = eval("']'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_125, lastError = self._apply(self.rule_token, "token", [_G_python_124])
        self.considerError(lastError)
        _G_python_126, lastError = eval('Tuple(a, self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_126, self.currentError)


    def rule_bagTerm(self):
        _locals = {'self': self}
        self.locals['bagTerm'] = _locals
        _G_python_127, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_127
        _G_python_128, lastError = eval("'{'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_129, lastError = self._apply(self.rule_token, "token", [_G_python_128])
        self.considerError(lastError)
        _G_apply_130, lastError = self._apply(self.rule_argList, "argList", [])
        self.considerError(lastError)
        _locals['a'] = _G_apply_130
        _G_python_131, lastError = eval("'}'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_132, lastError = self._apply(self.rule_token, "token", [_G_python_131])
        self.considerError(lastError)
        _G_python_133, lastError = eval('Bag(a, self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_133, self.currentError)


    def rule_labelledBagTerm(self):
        _locals = {'self': self}
        self.locals['labelledBagTerm'] = _locals
        _G_python_134, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_134
        _G_apply_135, lastError = self._apply(self.rule_functor, "functor", [])
        self.considerError(lastError)
        _locals['f'] = _G_apply_135
        _G_apply_136, lastError = self._apply(self.rule_bagTerm, "bagTerm", [])
        self.considerError(lastError)
        _locals['b'] = _G_apply_136
        _G_python_137, lastError = eval('LabelledBag(f, b, self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_137, self.currentError)


    def rule_extraTerm(self):
        _locals = {'self': self}
        self.locals['extraTerm'] = _locals
        def _G_or_138():
            _G_apply_139, lastError = self._apply(self.rule_tupleTerm, "tupleTerm", [])
            self.considerError(lastError)
            return (_G_apply_139, self.currentError)
        def _G_or_140():
            _G_apply_141, lastError = self._apply(self.rule_labelledBagTerm, "labelledBagTerm", [])
            self.considerError(lastError)
            return (_G_apply_141, self.currentError)
        def _G_or_142():
            _G_apply_143, lastError = self._apply(self.rule_bagTerm, "bagTerm", [])
            self.considerError(lastError)
            return (_G_apply_143, self.currentError)
        def _G_or_144():
            _G_apply_145, lastError = self._apply(self.rule_baseTerm, "baseTerm", [])
            self.considerError(lastError)
            return (_G_apply_145, self.currentError)
        _G_or_146, lastError = self._or([_G_or_138, _G_or_140, _G_or_142, _G_or_144])
        self.considerError(lastError)
        return (_G_or_146, self.currentError)


    def rule_attrTerm(self):
        _locals = {'self': self}
        self.locals['attrTerm'] = _locals
        _G_python_147, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_147
        _G_apply_148, lastError = self._apply(self.rule_extraTerm, "extraTerm", [])
        self.considerError(lastError)
        _locals['k'] = _G_apply_148
        _G_python_149, lastError = eval("':'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_150, lastError = self._apply(self.rule_token, "token", [_G_python_149])
        self.considerError(lastError)
        _G_apply_151, lastError = self._apply(self.rule_extraTerm, "extraTerm", [])
        self.considerError(lastError)
        _locals['v'] = _G_apply_151
        _G_python_152, lastError = eval('Attr(k, v, self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_152, self.currentError)


    def rule_term(self):
        _locals = {'self': self}
        self.locals['term'] = _locals
        _G_apply_153, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_or_154():
            _G_apply_155, lastError = self._apply(self.rule_attrTerm, "attrTerm", [])
            self.considerError(lastError)
            return (_G_apply_155, self.currentError)
        def _G_or_156():
            _G_apply_157, lastError = self._apply(self.rule_extraTerm, "extraTerm", [])
            self.considerError(lastError)
            return (_G_apply_157, self.currentError)
        _G_or_158, lastError = self._or([_G_or_154, _G_or_156])
        self.considerError(lastError)
        return (_G_or_158, self.currentError)
