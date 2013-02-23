def createParserClass(GrammarBase, ruleGlobals):
    if ruleGlobals is None:
        ruleGlobals = {}
    class quasiterm(GrammarBase):
        def rule_schema(self):
            _locals = {'self': self}
            self.locals['schema'] = _locals
            def _G_many1_1():
                _G_apply_2, lastError = self._apply(self.rule_production, "production", [])
                self.considerError(lastError, None)
                return (_G_apply_2, self.currentError)
            _G_many1_3, lastError = self.many(_G_many1_1, _G_many1_1())
            self.considerError(lastError, 'schema')
            _locals['ps'] = _G_many1_3
            _G_python_4, lastError = eval('schema(ps)', self.globals, _locals), None
            self.considerError(lastError, 'schema')
            return (_G_python_4, self.currentError)


        def rule_production(self):
            _locals = {'self': self}
            self.locals['production'] = _locals
            _G_apply_5, lastError = self._apply(self.rule_tag, "tag", [])
            self.considerError(lastError, 'production')
            _locals['t'] = _G_apply_5
            _G_python_6, lastError = '::=', None
            self.considerError(lastError, 'production')
            _G_apply_7, lastError = self._apply(self.rule_token, "token", [_G_python_6])
            self.considerError(lastError, 'production')
            _G_apply_8, lastError = self._apply(self.rule_argList, "argList", [])
            self.considerError(lastError, 'production')
            _locals['a'] = _G_apply_8
            _G_python_9, lastError = ';', None
            self.considerError(lastError, 'production')
            _G_apply_10, lastError = self._apply(self.rule_token, "token", [_G_python_9])
            self.considerError(lastError, 'production')
            _G_python_11, lastError = eval('production(t, a)', self.globals, _locals), None
            self.considerError(lastError, 'production')
            return (_G_python_11, self.currentError)


        def rule_functor(self):
            _locals = {'self': self}
            self.locals['functor'] = _locals
            def _G_or_12():
                _G_apply_13, lastError = self._apply(self.rule_spaces, "spaces", [])
                self.considerError(lastError, None)
                def _G_or_14():
                    _G_apply_15, lastError = self._apply(self.rule_functorHole, "functorHole", [])
                    self.considerError(lastError, None)
                    _G_apply_16, lastError = self._apply(self.rule_functorHole, "functorHole", [])
                    self.considerError(lastError, None)
                    _G_python_17, lastError = eval('reserved("hole-tagged-hole")', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_17, self.currentError)
                def _G_or_18():
                    def _G_optional_19():
                        _G_exactly_20, lastError = self.exactly('.')
                        self.considerError(lastError, None)
                        return (_G_exactly_20, self.currentError)
                    def _G_optional_21():
                        return (None, self.input.nullError())
                    _G_or_22, lastError = self._or([_G_optional_19, _G_optional_21])
                    self.considerError(lastError, None)
                    _G_apply_23, lastError = self._apply(self.rule_functorHole, "functorHole", [])
                    self.considerError(lastError, None)
                    return (_G_apply_23, self.currentError)
                def _G_or_24():
                    _G_apply_25, lastError = self._apply(self.rule_tag, "tag", [])
                    self.considerError(lastError, None)
                    _locals['t'] = _G_apply_25
                    _G_apply_26, lastError = self._apply(self.rule_functorHole, "functorHole", [])
                    self.considerError(lastError, None)
                    _locals['h'] = _G_apply_26
                    _G_python_27, lastError = eval('taggedHole(t, h)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_27, self.currentError)
                _G_or_28, lastError = self._or([_G_or_14, _G_or_18, _G_or_24])
                self.considerError(lastError, None)
                return (_G_or_28, self.currentError)
            def _G_or_29():
                _G_apply_30, lastError = self.superApply("functor", )
                self.considerError(lastError, None)
                return (_G_apply_30, self.currentError)
            _G_or_31, lastError = self._or([_G_or_12, _G_or_29])
            self.considerError(lastError, 'functor')
            return (_G_or_31, self.currentError)


        def rule_arg(self):
            _locals = {'self': self}
            self.locals['arg'] = _locals
            _G_apply_32, lastError = self._apply(self.rule_interleave, "interleave", [])
            self.considerError(lastError, 'arg')
            _locals['l'] = _G_apply_32
            def _G_many_33():
                _G_python_34, lastError = '|', None
                self.considerError(lastError, None)
                _G_apply_35, lastError = self._apply(self.rule_token, "token", [_G_python_34])
                self.considerError(lastError, None)
                _G_apply_36, lastError = self._apply(self.rule_interleave, "interleave", [])
                self.considerError(lastError, None)
                return (_G_apply_36, self.currentError)
            _G_many_37, lastError = self.many(_G_many_33)
            self.considerError(lastError, 'arg')
            _locals['r'] = _G_many_37
            _G_python_38, lastError = eval('_or(l, *r)', self.globals, _locals), None
            self.considerError(lastError, 'arg')
            return (_G_python_38, self.currentError)


        def rule_interleave(self):
            _locals = {'self': self}
            self.locals['interleave'] = _locals
            _G_apply_39, lastError = self._apply(self.rule_action, "action", [])
            self.considerError(lastError, 'interleave')
            _locals['l'] = _G_apply_39
            def _G_many_40():
                _G_python_41, lastError = '&', None
                self.considerError(lastError, None)
                _G_apply_42, lastError = self._apply(self.rule_token, "token", [_G_python_41])
                self.considerError(lastError, None)
                _G_apply_43, lastError = self._apply(self.rule_action, "action", [])
                self.considerError(lastError, None)
                return (_G_apply_43, self.currentError)
            _G_many_44, lastError = self.many(_G_many_40)
            self.considerError(lastError, 'interleave')
            _locals['r'] = _G_many_44
            _G_python_45, lastError = eval('interleave(l, *r)', self.globals, _locals), None
            self.considerError(lastError, 'interleave')
            return (_G_python_45, self.currentError)


        def rule_action(self):
            _locals = {'self': self}
            self.locals['action'] = _locals
            _G_apply_46, lastError = self._apply(self.rule_pred, "pred", [])
            self.considerError(lastError, 'action')
            _locals['l'] = _G_apply_46
            def _G_or_47():
                _G_python_48, lastError = '->', None
                self.considerError(lastError, None)
                _G_apply_49, lastError = self._apply(self.rule_token, "token", [_G_python_48])
                self.considerError(lastError, None)
                _G_apply_50, lastError = self._apply(self.rule_pred, "pred", [])
                self.considerError(lastError, None)
                _locals['r'] = _G_apply_50
                _G_python_51, lastError = eval('action(l, *r)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_51, self.currentError)
            def _G_or_52():
                _G_python_53, lastError = eval('l', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_53, self.currentError)
            _G_or_54, lastError = self._or([_G_or_47, _G_or_52])
            self.considerError(lastError, 'action')
            return (_G_or_54, self.currentError)


        def rule_pred(self):
            _locals = {'self': self}
            self.locals['pred'] = _locals
            def _G_or_55():
                _G_apply_56, lastError = self._apply(self.rule_some, "some", [])
                self.considerError(lastError, None)
                return (_G_apply_56, self.currentError)
            def _G_or_57():
                _G_python_58, lastError = '!', None
                self.considerError(lastError, None)
                _G_apply_59, lastError = self._apply(self.rule_token, "token", [_G_python_58])
                self.considerError(lastError, None)
                _G_apply_60, lastError = self._apply(self.rule_some, "some", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_60
                _G_python_61, lastError = eval('not(x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_61, self.currentError)
            _G_or_62, lastError = self._or([_G_or_55, _G_or_57])
            self.considerError(lastError, 'pred')
            return (_G_or_62, self.currentError)


        def rule_some(self):
            _locals = {'self': self}
            self.locals['some'] = _locals
            def _G_or_63():
                _G_apply_64, lastError = self._apply(self.rule_quant, "quant", [])
                self.considerError(lastError, None)
                _locals['q'] = _G_apply_64
                _G_python_65, lastError = eval('some(None, q)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_65, self.currentError)
            def _G_or_66():
                _G_apply_67, lastError = self._apply(self.rule_prim, "prim", [])
                self.considerError(lastError, None)
                _locals['l'] = _G_apply_67
                def _G_optional_68():
                    def _G_or_69():
                        _G_python_70, lastError = '**', None
                        self.considerError(lastError, None)
                        _G_apply_71, lastError = self._apply(self.rule_token, "token", [_G_python_70])
                        self.considerError(lastError, None)
                        _G_apply_72, lastError = self._apply(self.rule_prim, "prim", [])
                        self.considerError(lastError, None)
                        _locals['r'] = _G_apply_72
                        _G_python_73, lastError = eval('matchSeparatedSequence(l, r)', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_73, self.currentError)
                    def _G_or_74():
                        _G_python_75, lastError = '++', None
                        self.considerError(lastError, None)
                        _G_apply_76, lastError = self._apply(self.rule_token, "token", [_G_python_75])
                        self.considerError(lastError, None)
                        _G_apply_77, lastError = self._apply(self.rule_prim, "prim", [])
                        self.considerError(lastError, None)
                        _locals['r'] = _G_apply_77
                        _G_python_78, lastError = eval('matchSeparatedSequence1(l, r)', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_78, self.currentError)
                    _G_or_79, lastError = self._or([_G_or_69, _G_or_74])
                    self.considerError(lastError, None)
                    return (_G_or_79, self.currentError)
                def _G_optional_80():
                    return (None, self.input.nullError())
                _G_or_81, lastError = self._or([_G_optional_68, _G_optional_80])
                self.considerError(lastError, None)
                _locals['seq'] = _G_or_81
                def _G_optional_82():
                    _G_apply_83, lastError = self._apply(self.rule_quant, "quant", [])
                    self.considerError(lastError, None)
                    return (_G_apply_83, self.currentError)
                def _G_optional_84():
                    return (None, self.input.nullError())
                _G_or_85, lastError = self._or([_G_optional_82, _G_optional_84])
                self.considerError(lastError, None)
                _locals['q'] = _G_or_85
                _G_python_86, lastError = eval('some(seq or l, q)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_86, self.currentError)
            _G_or_87, lastError = self._or([_G_or_63, _G_or_66])
            self.considerError(lastError, 'some')
            return (_G_or_87, self.currentError)


        def rule_quant(self):
            _locals = {'self': self}
            self.locals['quant'] = _locals
            def _G_or_88():
                _G_python_89, lastError = '?', None
                self.considerError(lastError, None)
                _G_apply_90, lastError = self._apply(self.rule_token, "token", [_G_python_89])
                self.considerError(lastError, None)
                return (_G_apply_90, self.currentError)
            def _G_or_91():
                _G_python_92, lastError = '+', None
                self.considerError(lastError, None)
                _G_apply_93, lastError = self._apply(self.rule_token, "token", [_G_python_92])
                self.considerError(lastError, None)
                return (_G_apply_93, self.currentError)
            def _G_or_94():
                _G_python_95, lastError = '*', None
                self.considerError(lastError, None)
                _G_apply_96, lastError = self._apply(self.rule_token, "token", [_G_python_95])
                self.considerError(lastError, None)
                return (_G_apply_96, self.currentError)
            _G_or_97, lastError = self._or([_G_or_88, _G_or_91, _G_or_94])
            self.considerError(lastError, 'quant')
            return (_G_or_97, self.currentError)


        def rule_prim(self):
            _locals = {'self': self}
            self.locals['prim'] = _locals
            def _G_or_98():
                _G_apply_99, lastError = self._apply(self.rule_term, "term", [])
                self.considerError(lastError, None)
                return (_G_apply_99, self.currentError)
            def _G_or_100():
                _G_exactly_101, lastError = self.exactly('.')
                self.considerError(lastError, None)
                _G_python_102, lastError = eval('any()', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_102, self.currentError)
            def _G_or_103():
                _G_apply_104, lastError = self._apply(self.rule_literal, "literal", [])
                self.considerError(lastError, None)
                _locals['l'] = _G_apply_104
                _G_python_105, lastError = '..', None
                self.considerError(lastError, None)
                _G_apply_106, lastError = self._apply(self.rule_token, "token", [_G_python_105])
                self.considerError(lastError, None)
                _G_apply_107, lastError = self._apply(self.rule_literal, "literal", [])
                self.considerError(lastError, None)
                _locals['r'] = _G_apply_107
                _G_python_108, lastError = eval('range(l, r)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_108, self.currentError)
            def _G_or_109():
                _G_python_110, lastError = '^', None
                self.considerError(lastError, None)
                _G_apply_111, lastError = self._apply(self.rule_token, "token", [_G_python_110])
                self.considerError(lastError, None)
                _G_apply_112, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_112
                _G_python_113, lastError = eval('anyOf(s)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_113, self.currentError)
            def _G_or_114():
                _G_python_115, lastError = '(', None
                self.considerError(lastError, None)
                _G_apply_116, lastError = self._apply(self.rule_token, "token", [_G_python_115])
                self.considerError(lastError, None)
                _G_apply_117, lastError = self._apply(self.rule_argList, "argList", [])
                self.considerError(lastError, None)
                _locals['l'] = _G_apply_117
                _G_python_118, lastError = ')', None
                self.considerError(lastError, None)
                _G_apply_119, lastError = self._apply(self.rule_token, "token", [_G_python_118])
                self.considerError(lastError, None)
                _G_python_120, lastError = eval('l', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_120, self.currentError)
            _G_or_121, lastError = self._or([_G_or_98, _G_or_100, _G_or_103, _G_or_109, _G_or_114])
            self.considerError(lastError, 'prim')
            return (_G_or_121, self.currentError)


        def rule_simpleint(self):
            _locals = {'self': self}
            self.locals['simpleint'] = _locals
            _G_apply_122, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError, 'simpleint')
            _locals['ds'] = _G_apply_122
            _G_python_123, lastError = eval('int(ds)', self.globals, _locals), None
            self.considerError(lastError, 'simpleint')
            return (_G_python_123, self.currentError)


        def rule_functorHole(self):
            _locals = {'self': self}
            self.locals['functorHole'] = _locals
            def _G_or_124():
                _G_exactly_125, lastError = self.exactly('$')
                self.considerError(lastError, None)
                def _G_or_126():
                    _G_apply_127, lastError = self._apply(self.rule_simpleint, "simpleint", [])
                    self.considerError(lastError, None)
                    _locals['i'] = _G_apply_127
                    return (_locals['i'], self.currentError)
                def _G_or_128():
                    _G_exactly_129, lastError = self.exactly('{')
                    self.considerError(lastError, None)
                    _G_apply_130, lastError = self._apply(self.rule_simpleint, "simpleint", [])
                    self.considerError(lastError, None)
                    _locals['i'] = _G_apply_130
                    _G_exactly_131, lastError = self.exactly('}')
                    self.considerError(lastError, None)
                    return (_G_exactly_131, self.currentError)
                def _G_or_132():
                    _G_apply_133, lastError = self._apply(self.rule_tag, "tag", [])
                    self.considerError(lastError, None)
                    _locals['t'] = _G_apply_133
                    _G_python_134, lastError = eval('t.name', self.globals, _locals), None
                    self.considerError(lastError, None)
                    _locals['i'] = _G_python_134
                    return (_locals['i'], self.currentError)
                _G_or_135, lastError = self._or([_G_or_126, _G_or_128, _G_or_132])
                self.considerError(lastError, None)
                _G_python_136, lastError = eval('dollarHole(i)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_136, self.currentError)
            def _G_or_137():
                def _G_or_138():
                    _G_exactly_139, lastError = self.exactly('@')
                    self.considerError(lastError, None)
                    return (_G_exactly_139, self.currentError)
                def _G_or_140():
                    _G_exactly_141, lastError = self.exactly('=')
                    self.considerError(lastError, None)
                    return (_G_exactly_141, self.currentError)
                _G_or_142, lastError = self._or([_G_or_138, _G_or_140])
                self.considerError(lastError, None)
                def _G_or_143():
                    _G_apply_144, lastError = self._apply(self.rule_simpleint, "simpleint", [])
                    self.considerError(lastError, None)
                    _locals['i'] = _G_apply_144
                    return (_locals['i'], self.currentError)
                def _G_or_145():
                    _G_exactly_146, lastError = self.exactly('{')
                    self.considerError(lastError, None)
                    _G_apply_147, lastError = self._apply(self.rule_simpleint, "simpleint", [])
                    self.considerError(lastError, None)
                    _locals['i'] = _G_apply_147
                    _G_exactly_148, lastError = self.exactly('}')
                    self.considerError(lastError, None)
                    return (_G_exactly_148, self.currentError)
                def _G_or_149():
                    _G_apply_150, lastError = self._apply(self.rule_tag, "tag", [])
                    self.considerError(lastError, None)
                    _locals['t'] = _G_apply_150
                    _G_python_151, lastError = eval('t.name', self.globals, _locals), None
                    self.considerError(lastError, None)
                    _locals['i'] = _G_python_151
                    return (_locals['i'], self.currentError)
                _G_or_152, lastError = self._or([_G_or_143, _G_or_145, _G_or_149])
                self.considerError(lastError, None)
                _G_python_153, lastError = eval('patternHole(i)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_153, self.currentError)
            _G_or_154, lastError = self._or([_G_or_124, _G_or_137])
            self.considerError(lastError, 'functorHole')
            return (_G_or_154, self.currentError)


    if quasiterm.globals is not None:
        quasiterm.globals = quasiterm.globals.copy()
        quasiterm.globals.update(ruleGlobals)
    else:
        quasiterm.globals = ruleGlobals
    return quasiterm