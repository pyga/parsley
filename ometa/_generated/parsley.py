def createParserClass(GrammarBase, ruleGlobals):
    if ruleGlobals is None:
        ruleGlobals = {}
    class parsley(GrammarBase):
        def rule_comment(self):
            _locals = {'self': self}
            self.locals['comment'] = _locals
            _G_exactly_1, lastError = self.exactly('#')
            self.considerError(lastError, 'comment')
            def _G_many_2():
                def _G_not_3():
                    _G_exactly_4, lastError = self.exactly('\n')
                    self.considerError(lastError, None)
                    return (_G_exactly_4, self.currentError)
                _G_not_5, lastError = self._not(_G_not_3)
                self.considerError(lastError, None)
                _G_apply_6, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                return (_G_apply_6, self.currentError)
            _G_many_7, lastError = self.many(_G_many_2)
            self.considerError(lastError, 'comment')
            return (_G_many_7, self.currentError)


        def rule_hspace(self):
            _locals = {'self': self}
            self.locals['hspace'] = _locals
            def _G_or_8():
                _G_exactly_9, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                return (_G_exactly_9, self.currentError)
            def _G_or_10():
                _G_exactly_11, lastError = self.exactly('\t')
                self.considerError(lastError, None)
                return (_G_exactly_11, self.currentError)
            def _G_or_12():
                _G_apply_13, lastError = self._apply(self.rule_comment, "comment", [])
                self.considerError(lastError, None)
                return (_G_apply_13, self.currentError)
            _G_or_14, lastError = self._or([_G_or_8, _G_or_10, _G_or_12])
            self.considerError(lastError, 'hspace')
            return (_G_or_14, self.currentError)


        def rule_vspace(self):
            _locals = {'self': self}
            self.locals['vspace'] = _locals
            def _G_or_15():
                _G_exactly_16, lastError = self.exactly('\r\n')
                self.considerError(lastError, None)
                return (_G_exactly_16, self.currentError)
            def _G_or_17():
                _G_exactly_18, lastError = self.exactly('\r')
                self.considerError(lastError, None)
                return (_G_exactly_18, self.currentError)
            def _G_or_19():
                _G_exactly_20, lastError = self.exactly('\n')
                self.considerError(lastError, None)
                return (_G_exactly_20, self.currentError)
            _G_or_21, lastError = self._or([_G_or_15, _G_or_17, _G_or_19])
            self.considerError(lastError, 'vspace')
            return (_G_or_21, self.currentError)


        def rule_ws(self):
            _locals = {'self': self}
            self.locals['ws'] = _locals
            def _G_many_22():
                def _G_or_23():
                    _G_apply_24, lastError = self._apply(self.rule_hspace, "hspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_24, self.currentError)
                def _G_or_25():
                    _G_apply_26, lastError = self._apply(self.rule_vspace, "vspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_26, self.currentError)
                def _G_or_27():
                    _G_apply_28, lastError = self._apply(self.rule_comment, "comment", [])
                    self.considerError(lastError, None)
                    return (_G_apply_28, self.currentError)
                _G_or_29, lastError = self._or([_G_or_23, _G_or_25, _G_or_27])
                self.considerError(lastError, None)
                return (_G_or_29, self.currentError)
            _G_many_30, lastError = self.many(_G_many_22)
            self.considerError(lastError, 'ws')
            return (_G_many_30, self.currentError)


        def rule_emptyline(self):
            _locals = {'self': self}
            self.locals['emptyline'] = _locals
            def _G_many_31():
                _G_apply_32, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError, None)
                return (_G_apply_32, self.currentError)
            _G_many_33, lastError = self.many(_G_many_31)
            self.considerError(lastError, 'emptyline')
            _G_apply_34, lastError = self._apply(self.rule_vspace, "vspace", [])
            self.considerError(lastError, 'emptyline')
            return (_G_apply_34, self.currentError)


        def rule_indentation(self):
            _locals = {'self': self}
            self.locals['indentation'] = _locals
            def _G_many_35():
                _G_apply_36, lastError = self._apply(self.rule_emptyline, "emptyline", [])
                self.considerError(lastError, None)
                return (_G_apply_36, self.currentError)
            _G_many_37, lastError = self.many(_G_many_35)
            self.considerError(lastError, 'indentation')
            def _G_many1_38():
                _G_apply_39, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError, None)
                return (_G_apply_39, self.currentError)
            _G_many1_40, lastError = self.many(_G_many1_38, _G_many1_38())
            self.considerError(lastError, 'indentation')
            return (_G_many1_40, self.currentError)


        def rule_noindentation(self):
            _locals = {'self': self}
            self.locals['noindentation'] = _locals
            def _G_many_41():
                _G_apply_42, lastError = self._apply(self.rule_emptyline, "emptyline", [])
                self.considerError(lastError, None)
                return (_G_apply_42, self.currentError)
            _G_many_43, lastError = self.many(_G_many_41)
            self.considerError(lastError, 'noindentation')
            def _G_lookahead_44():
                def _G_not_45():
                    _G_apply_46, lastError = self._apply(self.rule_hspace, "hspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_46, self.currentError)
                _G_not_47, lastError = self._not(_G_not_45)
                self.considerError(lastError, None)
                return (_G_not_47, self.currentError)
            _G_lookahead_48, lastError = self.lookahead(_G_lookahead_44)
            self.considerError(lastError, 'noindentation')
            return (_G_lookahead_48, self.currentError)


        def rule_number(self):
            _locals = {'self': self}
            self.locals['number'] = _locals
            _G_apply_49, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'number')
            def _G_or_50():
                _G_exactly_51, lastError = self.exactly('-')
                self.considerError(lastError, None)
                _G_apply_52, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_52
                _G_python_53, lastError = eval('t.Exactly(-x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_53, self.currentError)
            def _G_or_54():
                _G_apply_55, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_55
                _G_python_56, lastError = eval('t.Exactly(x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_56, self.currentError)
            _G_or_57, lastError = self._or([_G_or_50, _G_or_54])
            self.considerError(lastError, 'number')
            return (_G_or_57, self.currentError)


        def rule_barenumber(self):
            _locals = {'self': self}
            self.locals['barenumber'] = _locals
            def _G_or_58():
                _G_exactly_59, lastError = self.exactly('0')
                self.considerError(lastError, None)
                def _G_or_60():
                    def _G_or_61():
                        _G_exactly_62, lastError = self.exactly('x')
                        self.considerError(lastError, None)
                        return (_G_exactly_62, self.currentError)
                    def _G_or_63():
                        _G_exactly_64, lastError = self.exactly('X')
                        self.considerError(lastError, None)
                        return (_G_exactly_64, self.currentError)
                    _G_or_65, lastError = self._or([_G_or_61, _G_or_63])
                    self.considerError(lastError, None)
                    def _G_consumedby_66():
                        def _G_many1_67():
                            _G_apply_68, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                            self.considerError(lastError, None)
                            return (_G_apply_68, self.currentError)
                        _G_many1_69, lastError = self.many(_G_many1_67, _G_many1_67())
                        self.considerError(lastError, None)
                        return (_G_many1_69, self.currentError)
                    _G_consumedby_70, lastError = self.consumedby(_G_consumedby_66)
                    self.considerError(lastError, None)
                    _locals['hs'] = _G_consumedby_70
                    _G_python_71, lastError = eval('int(hs, 16)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_71, self.currentError)
                def _G_or_72():
                    def _G_consumedby_73():
                        def _G_many1_74():
                            _G_apply_75, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                            self.considerError(lastError, None)
                            return (_G_apply_75, self.currentError)
                        _G_many1_76, lastError = self.many(_G_many1_74, _G_many1_74())
                        self.considerError(lastError, None)
                        return (_G_many1_76, self.currentError)
                    _G_consumedby_77, lastError = self.consumedby(_G_consumedby_73)
                    self.considerError(lastError, None)
                    _locals['ds'] = _G_consumedby_77
                    _G_python_78, lastError = eval('int(ds, 8)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_78, self.currentError)
                _G_or_79, lastError = self._or([_G_or_60, _G_or_72])
                self.considerError(lastError, None)
                return (_G_or_79, self.currentError)
            def _G_or_80():
                def _G_consumedby_81():
                    def _G_many1_82():
                        _G_apply_83, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_83, self.currentError)
                    _G_many1_84, lastError = self.many(_G_many1_82, _G_many1_82())
                    self.considerError(lastError, None)
                    return (_G_many1_84, self.currentError)
                _G_consumedby_85, lastError = self.consumedby(_G_consumedby_81)
                self.considerError(lastError, None)
                _locals['ds'] = _G_consumedby_85
                _G_python_86, lastError = eval('int(ds)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_86, self.currentError)
            _G_or_87, lastError = self._or([_G_or_58, _G_or_80])
            self.considerError(lastError, 'barenumber')
            return (_G_or_87, self.currentError)


        def rule_octaldigit(self):
            _locals = {'self': self}
            self.locals['octaldigit'] = _locals
            _G_apply_88, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'octaldigit')
            _locals['x'] = _G_apply_88
            def _G_pred_89():
                _G_python_90, lastError = eval("x in '01234567'", self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_90, self.currentError)
            _G_pred_91, lastError = self.pred(_G_pred_89)
            self.considerError(lastError, 'octaldigit')
            _G_python_92, lastError = eval('x', self.globals, _locals), None
            self.considerError(lastError, 'octaldigit')
            return (_G_python_92, self.currentError)


        def rule_hexdigit(self):
            _locals = {'self': self}
            self.locals['hexdigit'] = _locals
            _G_apply_93, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'hexdigit')
            _locals['x'] = _G_apply_93
            def _G_pred_94():
                _G_python_95, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_95, self.currentError)
            _G_pred_96, lastError = self.pred(_G_pred_94)
            self.considerError(lastError, 'hexdigit')
            _G_python_97, lastError = eval('x', self.globals, _locals), None
            self.considerError(lastError, 'hexdigit')
            return (_G_python_97, self.currentError)


        def rule_escapedChar(self):
            _locals = {'self': self}
            self.locals['escapedChar'] = _locals
            _G_exactly_98, lastError = self.exactly('\\')
            self.considerError(lastError, 'escapedChar')
            def _G_or_99():
                _G_exactly_100, lastError = self.exactly('n')
                self.considerError(lastError, None)
                _G_python_101, lastError = "\n", None
                self.considerError(lastError, None)
                return (_G_python_101, self.currentError)
            def _G_or_102():
                _G_exactly_103, lastError = self.exactly('r')
                self.considerError(lastError, None)
                _G_python_104, lastError = "\r", None
                self.considerError(lastError, None)
                return (_G_python_104, self.currentError)
            def _G_or_105():
                _G_exactly_106, lastError = self.exactly('t')
                self.considerError(lastError, None)
                _G_python_107, lastError = "\t", None
                self.considerError(lastError, None)
                return (_G_python_107, self.currentError)
            def _G_or_108():
                _G_exactly_109, lastError = self.exactly('b')
                self.considerError(lastError, None)
                _G_python_110, lastError = "\b", None
                self.considerError(lastError, None)
                return (_G_python_110, self.currentError)
            def _G_or_111():
                _G_exactly_112, lastError = self.exactly('f')
                self.considerError(lastError, None)
                _G_python_113, lastError = "\f", None
                self.considerError(lastError, None)
                return (_G_python_113, self.currentError)
            def _G_or_114():
                _G_exactly_115, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_116, lastError = '"', None
                self.considerError(lastError, None)
                return (_G_python_116, self.currentError)
            def _G_or_117():
                _G_exactly_118, lastError = self.exactly("'")
                self.considerError(lastError, None)
                _G_python_119, lastError = "'", None
                self.considerError(lastError, None)
                return (_G_python_119, self.currentError)
            def _G_or_120():
                _G_exactly_121, lastError = self.exactly('x')
                self.considerError(lastError, None)
                def _G_consumedby_122():
                    _G_apply_123, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                    self.considerError(lastError, None)
                    _G_apply_124, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_124, self.currentError)
                _G_consumedby_125, lastError = self.consumedby(_G_consumedby_122)
                self.considerError(lastError, None)
                _locals['d'] = _G_consumedby_125
                _G_python_126, lastError = eval('chr(int(d, 16))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_126, self.currentError)
            def _G_or_127():
                _G_exactly_128, lastError = self.exactly('\\')
                self.considerError(lastError, None)
                _G_python_129, lastError = "\\", None
                self.considerError(lastError, None)
                return (_G_python_129, self.currentError)
            _G_or_130, lastError = self._or([_G_or_99, _G_or_102, _G_or_105, _G_or_108, _G_or_111, _G_or_114, _G_or_117, _G_or_120, _G_or_127])
            self.considerError(lastError, 'escapedChar')
            return (_G_or_130, self.currentError)


        def rule_character(self):
            _locals = {'self': self}
            self.locals['character'] = _locals
            _G_apply_131, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'character')
            _G_exactly_132, lastError = self.exactly("'")
            self.considerError(lastError, 'character')
            def _G_many1_133():
                def _G_not_134():
                    _G_exactly_135, lastError = self.exactly("'")
                    self.considerError(lastError, None)
                    return (_G_exactly_135, self.currentError)
                _G_not_136, lastError = self._not(_G_not_134)
                self.considerError(lastError, None)
                def _G_or_137():
                    _G_apply_138, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                    self.considerError(lastError, None)
                    return (_G_apply_138, self.currentError)
                def _G_or_139():
                    _G_apply_140, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_140, self.currentError)
                _G_or_141, lastError = self._or([_G_or_137, _G_or_139])
                self.considerError(lastError, None)
                return (_G_or_141, self.currentError)
            _G_many1_142, lastError = self.many(_G_many1_133, _G_many1_133())
            self.considerError(lastError, 'character')
            _locals['c'] = _G_many1_142
            _G_apply_143, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'character')
            _G_exactly_144, lastError = self.exactly("'")
            self.considerError(lastError, 'character')
            _G_python_145, lastError = eval("t.Exactly(''.join(c))", self.globals, _locals), None
            self.considerError(lastError, 'character')
            return (_G_python_145, self.currentError)


        def rule_string(self):
            _locals = {'self': self}
            self.locals['string'] = _locals
            _G_apply_146, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'string')
            _G_exactly_147, lastError = self.exactly('"')
            self.considerError(lastError, 'string')
            def _G_many_148():
                def _G_or_149():
                    _G_apply_150, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                    self.considerError(lastError, None)
                    return (_G_apply_150, self.currentError)
                def _G_or_151():
                    def _G_not_152():
                        _G_exactly_153, lastError = self.exactly('"')
                        self.considerError(lastError, None)
                        return (_G_exactly_153, self.currentError)
                    _G_not_154, lastError = self._not(_G_not_152)
                    self.considerError(lastError, None)
                    _G_apply_155, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_155, self.currentError)
                _G_or_156, lastError = self._or([_G_or_149, _G_or_151])
                self.considerError(lastError, None)
                return (_G_or_156, self.currentError)
            _G_many_157, lastError = self.many(_G_many_148)
            self.considerError(lastError, 'string')
            _locals['c'] = _G_many_157
            _G_apply_158, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'string')
            _G_exactly_159, lastError = self.exactly('"')
            self.considerError(lastError, 'string')
            _G_python_160, lastError = eval("t.Token(''.join(c))", self.globals, _locals), None
            self.considerError(lastError, 'string')
            return (_G_python_160, self.currentError)


        def rule_name(self):
            _locals = {'self': self}
            self.locals['name'] = _locals
            def _G_consumedby_161():
                _G_apply_162, lastError = self._apply(self.rule_letter, "letter", [])
                self.considerError(lastError, None)
                def _G_many_163():
                    def _G_or_164():
                        _G_exactly_165, lastError = self.exactly('_')
                        self.considerError(lastError, None)
                        return (_G_exactly_165, self.currentError)
                    def _G_or_166():
                        _G_apply_167, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_167, self.currentError)
                    _G_or_168, lastError = self._or([_G_or_164, _G_or_166])
                    self.considerError(lastError, None)
                    return (_G_or_168, self.currentError)
                _G_many_169, lastError = self.many(_G_many_163)
                self.considerError(lastError, None)
                return (_G_many_169, self.currentError)
            _G_consumedby_170, lastError = self.consumedby(_G_consumedby_161)
            self.considerError(lastError, 'name')
            return (_G_consumedby_170, self.currentError)


        def rule_args(self):
            _locals = {'self': self}
            self.locals['args'] = _locals
            def _G_or_171():
                _G_exactly_172, lastError = self.exactly('(')
                self.considerError(lastError, None)
                _G_python_173, lastError = eval("self.applicationArgs(finalChar=')')", self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['args'] = _G_python_173
                _G_exactly_174, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_175, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_175, self.currentError)
            def _G_or_176():
                _G_python_177, lastError = [], None
                self.considerError(lastError, None)
                return (_G_python_177, self.currentError)
            _G_or_178, lastError = self._or([_G_or_171, _G_or_176])
            self.considerError(lastError, 'args')
            return (_G_or_178, self.currentError)


        def rule_application(self):
            _locals = {'self': self}
            self.locals['application'] = _locals
            def _G_optional_179():
                _G_apply_180, lastError = self._apply(self.rule_indentation, "indentation", [])
                self.considerError(lastError, None)
                return (_G_apply_180, self.currentError)
            def _G_optional_181():
                return (None, self.input.nullError())
            _G_or_182, lastError = self._or([_G_optional_179, _G_optional_181])
            self.considerError(lastError, 'application')
            _G_apply_183, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'application')
            _locals['name'] = _G_apply_183
            _G_apply_184, lastError = self._apply(self.rule_args, "args", [])
            self.considerError(lastError, 'application')
            _locals['args'] = _G_apply_184
            _G_python_185, lastError = eval('t.Apply(name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError, 'application')
            return (_G_python_185, self.currentError)


        def rule_foreignApply(self):
            _locals = {'self': self}
            self.locals['foreignApply'] = _locals
            def _G_optional_186():
                _G_apply_187, lastError = self._apply(self.rule_indentation, "indentation", [])
                self.considerError(lastError, None)
                return (_G_apply_187, self.currentError)
            def _G_optional_188():
                return (None, self.input.nullError())
            _G_or_189, lastError = self._or([_G_optional_186, _G_optional_188])
            self.considerError(lastError, 'foreignApply')
            _G_apply_190, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'foreignApply')
            _locals['grammar_name'] = _G_apply_190
            _G_exactly_191, lastError = self.exactly('.')
            self.considerError(lastError, 'foreignApply')
            _G_apply_192, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'foreignApply')
            _locals['rule_name'] = _G_apply_192
            _G_apply_193, lastError = self._apply(self.rule_args, "args", [])
            self.considerError(lastError, 'foreignApply')
            _locals['args'] = _G_apply_193
            _G_python_194, lastError = eval('t.ForeignApply(grammar_name, rule_name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError, 'foreignApply')
            return (_G_python_194, self.currentError)


        def rule_expr1(self):
            _locals = {'self': self}
            self.locals['expr1'] = _locals
            def _G_or_195():
                _G_apply_196, lastError = self._apply(self.rule_foreignApply, "foreignApply", [])
                self.considerError(lastError, None)
                return (_G_apply_196, self.currentError)
            def _G_or_197():
                _G_apply_198, lastError = self._apply(self.rule_application, "application", [])
                self.considerError(lastError, None)
                return (_G_apply_198, self.currentError)
            def _G_or_199():
                _G_apply_200, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
                self.considerError(lastError, None)
                return (_G_apply_200, self.currentError)
            def _G_or_201():
                _G_apply_202, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
                self.considerError(lastError, None)
                return (_G_apply_202, self.currentError)
            def _G_or_203():
                _G_apply_204, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
                self.considerError(lastError, None)
                return (_G_apply_204, self.currentError)
            def _G_or_205():
                _G_apply_206, lastError = self._apply(self.rule_number, "number", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_206
                _G_python_207, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_208, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_208, self.currentError)
            def _G_or_209():
                _G_apply_210, lastError = self._apply(self.rule_character, "character", [])
                self.considerError(lastError, None)
                return (_G_apply_210, self.currentError)
            def _G_or_211():
                _G_apply_212, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                return (_G_apply_212, self.currentError)
            def _G_or_213():
                _G_apply_214, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_215, lastError = self.exactly('(')
                self.considerError(lastError, None)
                _G_apply_216, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_216
                _G_apply_217, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_218, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_219, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_219, self.currentError)
            def _G_or_220():
                _G_apply_221, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_222, lastError = self.exactly('<')
                self.considerError(lastError, None)
                _G_apply_223, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_223
                _G_apply_224, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_225, lastError = self.exactly('>')
                self.considerError(lastError, None)
                _G_python_226, lastError = eval('t.ConsumedBy(e)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_226, self.currentError)
            def _G_or_227():
                _G_apply_228, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_229, lastError = self.exactly('[')
                self.considerError(lastError, None)
                def _G_optional_230():
                    _G_apply_231, lastError = self._apply(self.rule_expr, "expr", [])
                    self.considerError(lastError, None)
                    return (_G_apply_231, self.currentError)
                def _G_optional_232():
                    return (None, self.input.nullError())
                _G_or_233, lastError = self._or([_G_optional_230, _G_optional_232])
                self.considerError(lastError, None)
                _locals['e'] = _G_or_233
                _G_apply_234, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_235, lastError = self.exactly(']')
                self.considerError(lastError, None)
                _G_python_236, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_237, lastError = eval('t.List(e) if e else t.List()', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_237, self.currentError)
            _G_or_238, lastError = self._or([_G_or_195, _G_or_197, _G_or_199, _G_or_201, _G_or_203, _G_or_205, _G_or_209, _G_or_211, _G_or_213, _G_or_220, _G_or_227])
            self.considerError(lastError, 'expr1')
            return (_G_or_238, self.currentError)


        def rule_expr2(self):
            _locals = {'self': self}
            self.locals['expr2'] = _locals
            def _G_or_239():
                _G_apply_240, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_241, lastError = self.exactly('~')
                self.considerError(lastError, None)
                def _G_or_242():
                    _G_exactly_243, lastError = self.exactly('~')
                    self.considerError(lastError, None)
                    _G_apply_244, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_244
                    _G_python_245, lastError = eval('t.Lookahead(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_245, self.currentError)
                def _G_or_246():
                    _G_apply_247, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_247
                    _G_python_248, lastError = eval('t.Not(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_248, self.currentError)
                _G_or_249, lastError = self._or([_G_or_242, _G_or_246])
                self.considerError(lastError, None)
                return (_G_or_249, self.currentError)
            def _G_or_250():
                _G_apply_251, lastError = self._apply(self.rule_expr1, "expr1", [])
                self.considerError(lastError, None)
                return (_G_apply_251, self.currentError)
            _G_or_252, lastError = self._or([_G_or_239, _G_or_250])
            self.considerError(lastError, 'expr2')
            return (_G_or_252, self.currentError)


        def rule_repeatTimes(self):
            _locals = {'self': self}
            self.locals['repeatTimes'] = _locals
            def _G_or_253():
                _G_apply_254, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_254
                _G_python_255, lastError = eval('int(x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_255, self.currentError)
            def _G_or_256():
                _G_apply_257, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                return (_G_apply_257, self.currentError)
            _G_or_258, lastError = self._or([_G_or_253, _G_or_256])
            self.considerError(lastError, 'repeatTimes')
            return (_G_or_258, self.currentError)


        def rule_expr3(self):
            _locals = {'self': self}
            self.locals['expr3'] = _locals
            def _G_or_259():
                _G_apply_260, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_260
                def _G_or_261():
                    _G_exactly_262, lastError = self.exactly('*')
                    self.considerError(lastError, None)
                    _G_python_263, lastError = eval('t.Many(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_263, self.currentError)
                def _G_or_264():
                    _G_exactly_265, lastError = self.exactly('+')
                    self.considerError(lastError, None)
                    _G_python_266, lastError = eval('t.Many1(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_266, self.currentError)
                def _G_or_267():
                    _G_exactly_268, lastError = self.exactly('?')
                    self.considerError(lastError, None)
                    _G_python_269, lastError = eval('t.Optional(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_269, self.currentError)
                def _G_or_270():
                    _G_apply_271, lastError = self._apply(self.rule_customLabel, "customLabel", [])
                    self.considerError(lastError, None)
                    _locals['l'] = _G_apply_271
                    _G_python_272, lastError = eval('t.Label(e, l)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_272, self.currentError)
                def _G_or_273():
                    _G_exactly_274, lastError = self.exactly('{')
                    self.considerError(lastError, None)
                    _G_apply_275, lastError = self._apply(self.rule_ws, "ws", [])
                    self.considerError(lastError, None)
                    _G_apply_276, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                    self.considerError(lastError, None)
                    _locals['start'] = _G_apply_276
                    _G_apply_277, lastError = self._apply(self.rule_ws, "ws", [])
                    self.considerError(lastError, None)
                    def _G_or_278():
                        _G_exactly_279, lastError = self.exactly(',')
                        self.considerError(lastError, None)
                        _G_apply_280, lastError = self._apply(self.rule_ws, "ws", [])
                        self.considerError(lastError, None)
                        _G_apply_281, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                        self.considerError(lastError, None)
                        _locals['end'] = _G_apply_281
                        _G_apply_282, lastError = self._apply(self.rule_ws, "ws", [])
                        self.considerError(lastError, None)
                        _G_exactly_283, lastError = self.exactly('}')
                        self.considerError(lastError, None)
                        _G_python_284, lastError = eval('t.Repeat(start, end, e)', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_284, self.currentError)
                    def _G_or_285():
                        _G_apply_286, lastError = self._apply(self.rule_ws, "ws", [])
                        self.considerError(lastError, None)
                        _G_exactly_287, lastError = self.exactly('}')
                        self.considerError(lastError, None)
                        _G_python_288, lastError = eval('t.Repeat(start, start, e)', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_288, self.currentError)
                    _G_or_289, lastError = self._or([_G_or_278, _G_or_285])
                    self.considerError(lastError, None)
                    return (_G_or_289, self.currentError)
                def _G_or_290():
                    _G_python_291, lastError = eval('e', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_291, self.currentError)
                _G_or_292, lastError = self._or([_G_or_261, _G_or_264, _G_or_267, _G_or_270, _G_or_273, _G_or_290])
                self.considerError(lastError, None)
                _locals['r'] = _G_or_292
                def _G_or_293():
                    _G_exactly_294, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    _G_apply_295, lastError = self._apply(self.rule_name, "name", [])
                    self.considerError(lastError, None)
                    _locals['n'] = _G_apply_295
                    _G_python_296, lastError = eval('t.Bind(n, r)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_296, self.currentError)
                def _G_or_297():
                    _G_python_298, lastError = eval('r', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_298, self.currentError)
                _G_or_299, lastError = self._or([_G_or_293, _G_or_297])
                self.considerError(lastError, None)
                return (_G_or_299, self.currentError)
            def _G_or_300():
                _G_apply_301, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_302, lastError = self.exactly(':')
                self.considerError(lastError, None)
                _G_apply_303, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_303
                _G_python_304, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_304, self.currentError)
            _G_or_305, lastError = self._or([_G_or_259, _G_or_300])
            self.considerError(lastError, 'expr3')
            return (_G_or_305, self.currentError)


        def rule_expr4(self):
            _locals = {'self': self}
            self.locals['expr4'] = _locals
            def _G_many1_306():
                _G_apply_307, lastError = self._apply(self.rule_expr3, "expr3", [])
                self.considerError(lastError, None)
                return (_G_apply_307, self.currentError)
            _G_many1_308, lastError = self.many(_G_many1_306, _G_many1_306())
            self.considerError(lastError, 'expr4')
            _locals['es'] = _G_many1_308
            _G_python_309, lastError = eval('es[0] if len(es) == 1 else t.And(es)', self.globals, _locals), None
            self.considerError(lastError, 'expr4')
            return (_G_python_309, self.currentError)


        def rule_expr(self):
            _locals = {'self': self}
            self.locals['expr'] = _locals
            _G_apply_310, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError, 'expr')
            _locals['e'] = _G_apply_310
            def _G_many_311():
                _G_apply_312, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_313, lastError = self.exactly('|')
                self.considerError(lastError, None)
                _G_apply_314, lastError = self._apply(self.rule_expr4, "expr4", [])
                self.considerError(lastError, None)
                return (_G_apply_314, self.currentError)
            _G_many_315, lastError = self.many(_G_many_311)
            self.considerError(lastError, 'expr')
            _locals['es'] = _G_many_315
            _G_python_316, lastError = eval('t.Or([e] + es) if es else e', self.globals, _locals), None
            self.considerError(lastError, 'expr')
            return (_G_python_316, self.currentError)


        def rule_ruleValue(self):
            _locals = {'self': self}
            self.locals['ruleValue'] = _locals
            _G_apply_317, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'ruleValue')
            _G_exactly_318, lastError = self.exactly('->')
            self.considerError(lastError, 'ruleValue')
            _G_python_319, lastError = eval('self.ruleValueExpr(True)', self.globals, _locals), None
            self.considerError(lastError, 'ruleValue')
            return (_G_python_319, self.currentError)


        def rule_customLabel(self):
            _locals = {'self': self}
            self.locals['customLabel'] = _locals
            _G_apply_320, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'customLabel')
            _G_exactly_321, lastError = self.exactly('^')
            self.considerError(lastError, 'customLabel')
            _G_apply_322, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'customLabel')
            _G_exactly_323, lastError = self.exactly('(')
            self.considerError(lastError, 'customLabel')
            def _G_consumedby_324():
                def _G_many1_325():
                    def _G_not_326():
                        _G_exactly_327, lastError = self.exactly(')')
                        self.considerError(lastError, None)
                        return (_G_exactly_327, self.currentError)
                    _G_not_328, lastError = self._not(_G_not_326)
                    self.considerError(lastError, None)
                    _G_apply_329, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_329, self.currentError)
                _G_many1_330, lastError = self.many(_G_many1_325, _G_many1_325())
                self.considerError(lastError, None)
                return (_G_many1_330, self.currentError)
            _G_consumedby_331, lastError = self.consumedby(_G_consumedby_324)
            self.considerError(lastError, 'customLabel')
            _locals['e'] = _G_consumedby_331
            _G_exactly_332, lastError = self.exactly(')')
            self.considerError(lastError, 'customLabel')
            _G_python_333, lastError = eval('e', self.globals, _locals), None
            self.considerError(lastError, 'customLabel')
            return (_G_python_333, self.currentError)


        def rule_semanticPredicate(self):
            _locals = {'self': self}
            self.locals['semanticPredicate'] = _locals
            _G_apply_334, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'semanticPredicate')
            _G_exactly_335, lastError = self.exactly('?(')
            self.considerError(lastError, 'semanticPredicate')
            _G_python_336, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticPredicate')
            return (_G_python_336, self.currentError)


        def rule_semanticAction(self):
            _locals = {'self': self}
            self.locals['semanticAction'] = _locals
            _G_apply_337, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'semanticAction')
            _G_exactly_338, lastError = self.exactly('!(')
            self.considerError(lastError, 'semanticAction')
            _G_python_339, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticAction')
            return (_G_python_339, self.currentError)


        def rule_ruleEnd(self):
            _locals = {'self': self}
            self.locals['ruleEnd'] = _locals
            def _G_or_340():
                def _G_many_341():
                    _G_apply_342, lastError = self._apply(self.rule_hspace, "hspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_342, self.currentError)
                _G_many_343, lastError = self.many(_G_many_341)
                self.considerError(lastError, None)
                def _G_many1_344():
                    _G_apply_345, lastError = self._apply(self.rule_vspace, "vspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_345, self.currentError)
                _G_many1_346, lastError = self.many(_G_many1_344, _G_many1_344())
                self.considerError(lastError, None)
                return (_G_many1_346, self.currentError)
            def _G_or_347():
                _G_apply_348, lastError = self._apply(self.rule_end, "end", [])
                self.considerError(lastError, None)
                return (_G_apply_348, self.currentError)
            _G_or_349, lastError = self._or([_G_or_340, _G_or_347])
            self.considerError(lastError, 'ruleEnd')
            return (_G_or_349, self.currentError)


        def rule_rulePart(self):
            _locals = {'self': self}
            self.locals['rulePart'] = _locals
            _G_apply_350, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'rulePart')
            _locals['requiredName'] = _G_apply_350
            _G_apply_351, lastError = self._apply(self.rule_noindentation, "noindentation", [])
            self.considerError(lastError, 'rulePart')
            _G_apply_352, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'rulePart')
            _locals['n'] = _G_apply_352
            def _G_pred_353():
                _G_python_354, lastError = eval('n == requiredName', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_354, self.currentError)
            _G_pred_355, lastError = self.pred(_G_pred_353)
            self.considerError(lastError, 'rulePart')
            _G_python_356, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
            self.considerError(lastError, 'rulePart')
            def _G_optional_357():
                _G_apply_358, lastError = self._apply(self.rule_expr4, "expr4", [])
                self.considerError(lastError, None)
                return (_G_apply_358, self.currentError)
            def _G_optional_359():
                return (None, self.input.nullError())
            _G_or_360, lastError = self._or([_G_optional_357, _G_optional_359])
            self.considerError(lastError, 'rulePart')
            _locals['args'] = _G_or_360
            def _G_or_361():
                _G_apply_362, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_363, lastError = self.exactly('=')
                self.considerError(lastError, None)
                _G_apply_364, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_364
                _G_apply_365, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_366, lastError = eval('t.And([args, e]) if args else e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_366, self.currentError)
            def _G_or_367():
                _G_apply_368, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_369, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_369, self.currentError)
            _G_or_370, lastError = self._or([_G_or_361, _G_or_367])
            self.considerError(lastError, 'rulePart')
            return (_G_or_370, self.currentError)


        def rule_rule(self):
            _locals = {'self': self}
            self.locals['rule'] = _locals
            _G_apply_371, lastError = self._apply(self.rule_noindentation, "noindentation", [])
            self.considerError(lastError, 'rule')
            def _G_lookahead_372():
                _G_apply_373, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_373
                return (_locals['n'], self.currentError)
            _G_lookahead_374, lastError = self.lookahead(_G_lookahead_372)
            self.considerError(lastError, 'rule')
            def _G_many1_375():
                _G_python_376, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_apply_377, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_376])
                self.considerError(lastError, None)
                return (_G_apply_377, self.currentError)
            _G_many1_378, lastError = self.many(_G_many1_375, _G_many1_375())
            self.considerError(lastError, 'rule')
            _locals['rs'] = _G_many1_378
            _G_python_379, lastError = eval('t.Rule(n, t.Or(rs))', self.globals, _locals), None
            self.considerError(lastError, 'rule')
            return (_G_python_379, self.currentError)


        def rule_grammar(self):
            _locals = {'self': self}
            self.locals['grammar'] = _locals
            def _G_many_380():
                _G_apply_381, lastError = self._apply(self.rule_rule, "rule", [])
                self.considerError(lastError, None)
                return (_G_apply_381, self.currentError)
            _G_many_382, lastError = self.many(_G_many_380)
            self.considerError(lastError, 'grammar')
            _locals['rs'] = _G_many_382
            _G_apply_383, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'grammar')
            _G_python_384, lastError = eval('t.Grammar(self.name, self.tree_target, rs)', self.globals, _locals), None
            self.considerError(lastError, 'grammar')
            return (_G_python_384, self.currentError)


    if parsley.globals is not None:
        parsley.globals = parsley.globals.copy()
        parsley.globals.update(ruleGlobals)
    else:
        parsley.globals = ruleGlobals
    return parsley