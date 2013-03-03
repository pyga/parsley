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
                    _G_apply_164, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_164, self.currentError)
                _G_many_165, lastError = self.many(_G_many_163)
                self.considerError(lastError, None)
                return (_G_many_165, self.currentError)
            _G_consumedby_166, lastError = self.consumedby(_G_consumedby_161)
            self.considerError(lastError, 'name')
            return (_G_consumedby_166, self.currentError)


        def rule_args(self):
            _locals = {'self': self}
            self.locals['args'] = _locals
            def _G_or_167():
                _G_exactly_168, lastError = self.exactly('(')
                self.considerError(lastError, None)
                _G_python_169, lastError = eval("self.applicationArgs(finalChar=')')", self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['args'] = _G_python_169
                _G_exactly_170, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_171, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_171, self.currentError)
            def _G_or_172():
                _G_python_173, lastError = [], None
                self.considerError(lastError, None)
                return (_G_python_173, self.currentError)
            _G_or_174, lastError = self._or([_G_or_167, _G_or_172])
            self.considerError(lastError, 'args')
            return (_G_or_174, self.currentError)


        def rule_application(self):
            _locals = {'self': self}
            self.locals['application'] = _locals
            def _G_optional_175():
                _G_apply_176, lastError = self._apply(self.rule_indentation, "indentation", [])
                self.considerError(lastError, None)
                return (_G_apply_176, self.currentError)
            def _G_optional_177():
                return (None, self.input.nullError())
            _G_or_178, lastError = self._or([_G_optional_175, _G_optional_177])
            self.considerError(lastError, 'application')
            _G_apply_179, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'application')
            _locals['name'] = _G_apply_179
            _G_apply_180, lastError = self._apply(self.rule_args, "args", [])
            self.considerError(lastError, 'application')
            _locals['args'] = _G_apply_180
            _G_python_181, lastError = eval('t.Apply(name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError, 'application')
            return (_G_python_181, self.currentError)


        def rule_foreignApply(self):
            _locals = {'self': self}
            self.locals['foreignApply'] = _locals
            def _G_optional_182():
                _G_apply_183, lastError = self._apply(self.rule_indentation, "indentation", [])
                self.considerError(lastError, None)
                return (_G_apply_183, self.currentError)
            def _G_optional_184():
                return (None, self.input.nullError())
            _G_or_185, lastError = self._or([_G_optional_182, _G_optional_184])
            self.considerError(lastError, 'foreignApply')
            _G_apply_186, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'foreignApply')
            _locals['grammar_name'] = _G_apply_186
            _G_exactly_187, lastError = self.exactly('.')
            self.considerError(lastError, 'foreignApply')
            _G_apply_188, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'foreignApply')
            _locals['rule_name'] = _G_apply_188
            _G_apply_189, lastError = self._apply(self.rule_args, "args", [])
            self.considerError(lastError, 'foreignApply')
            _locals['args'] = _G_apply_189
            _G_python_190, lastError = eval('t.ForeignApply(grammar_name, rule_name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError, 'foreignApply')
            return (_G_python_190, self.currentError)


        def rule_expr1(self):
            _locals = {'self': self}
            self.locals['expr1'] = _locals
            def _G_or_191():
                _G_apply_192, lastError = self._apply(self.rule_foreignApply, "foreignApply", [])
                self.considerError(lastError, None)
                return (_G_apply_192, self.currentError)
            def _G_or_193():
                _G_apply_194, lastError = self._apply(self.rule_application, "application", [])
                self.considerError(lastError, None)
                return (_G_apply_194, self.currentError)
            def _G_or_195():
                _G_apply_196, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
                self.considerError(lastError, None)
                return (_G_apply_196, self.currentError)
            def _G_or_197():
                _G_apply_198, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
                self.considerError(lastError, None)
                return (_G_apply_198, self.currentError)
            def _G_or_199():
                _G_apply_200, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
                self.considerError(lastError, None)
                return (_G_apply_200, self.currentError)
            def _G_or_201():
                _G_apply_202, lastError = self._apply(self.rule_number, "number", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_202
                _G_python_203, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_204, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_204, self.currentError)
            def _G_or_205():
                _G_apply_206, lastError = self._apply(self.rule_character, "character", [])
                self.considerError(lastError, None)
                return (_G_apply_206, self.currentError)
            def _G_or_207():
                _G_apply_208, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                return (_G_apply_208, self.currentError)
            def _G_or_209():
                _G_apply_210, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_211, lastError = self.exactly('(')
                self.considerError(lastError, None)
                _G_apply_212, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_212
                _G_apply_213, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_214, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_215, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_215, self.currentError)
            def _G_or_216():
                _G_apply_217, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_218, lastError = self.exactly('<')
                self.considerError(lastError, None)
                _G_apply_219, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_219
                _G_apply_220, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_221, lastError = self.exactly('>')
                self.considerError(lastError, None)
                _G_python_222, lastError = eval('t.ConsumedBy(e)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_222, self.currentError)
            def _G_or_223():
                _G_apply_224, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_225, lastError = self.exactly('[')
                self.considerError(lastError, None)
                def _G_optional_226():
                    _G_apply_227, lastError = self._apply(self.rule_expr, "expr", [])
                    self.considerError(lastError, None)
                    return (_G_apply_227, self.currentError)
                def _G_optional_228():
                    return (None, self.input.nullError())
                _G_or_229, lastError = self._or([_G_optional_226, _G_optional_228])
                self.considerError(lastError, None)
                _locals['e'] = _G_or_229
                _G_apply_230, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_231, lastError = self.exactly(']')
                self.considerError(lastError, None)
                _G_python_232, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_233, lastError = eval('t.List(e) if e else t.List()', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_233, self.currentError)
            _G_or_234, lastError = self._or([_G_or_191, _G_or_193, _G_or_195, _G_or_197, _G_or_199, _G_or_201, _G_or_205, _G_or_207, _G_or_209, _G_or_216, _G_or_223])
            self.considerError(lastError, 'expr1')
            return (_G_or_234, self.currentError)


        def rule_expr2(self):
            _locals = {'self': self}
            self.locals['expr2'] = _locals
            def _G_or_235():
                _G_apply_236, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_237, lastError = self.exactly('~')
                self.considerError(lastError, None)
                def _G_or_238():
                    _G_exactly_239, lastError = self.exactly('~')
                    self.considerError(lastError, None)
                    _G_apply_240, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_240
                    _G_python_241, lastError = eval('t.Lookahead(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_241, self.currentError)
                def _G_or_242():
                    _G_apply_243, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_243
                    _G_python_244, lastError = eval('t.Not(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_244, self.currentError)
                _G_or_245, lastError = self._or([_G_or_238, _G_or_242])
                self.considerError(lastError, None)
                return (_G_or_245, self.currentError)
            def _G_or_246():
                _G_apply_247, lastError = self._apply(self.rule_expr1, "expr1", [])
                self.considerError(lastError, None)
                return (_G_apply_247, self.currentError)
            _G_or_248, lastError = self._or([_G_or_235, _G_or_246])
            self.considerError(lastError, 'expr2')
            return (_G_or_248, self.currentError)


        def rule_repeatTimes(self):
            _locals = {'self': self}
            self.locals['repeatTimes'] = _locals
            def _G_or_249():
                _G_apply_250, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_250
                _G_python_251, lastError = eval('int(x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_251, self.currentError)
            def _G_or_252():
                _G_apply_253, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                return (_G_apply_253, self.currentError)
            _G_or_254, lastError = self._or([_G_or_249, _G_or_252])
            self.considerError(lastError, 'repeatTimes')
            return (_G_or_254, self.currentError)


        def rule_expr3(self):
            _locals = {'self': self}
            self.locals['expr3'] = _locals
            def _G_or_255():
                _G_apply_256, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_256
                def _G_or_257():
                    _G_exactly_258, lastError = self.exactly('*')
                    self.considerError(lastError, None)
                    _G_python_259, lastError = eval('t.Many(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_259, self.currentError)
                def _G_or_260():
                    _G_exactly_261, lastError = self.exactly('+')
                    self.considerError(lastError, None)
                    _G_python_262, lastError = eval('t.Many1(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_262, self.currentError)
                def _G_or_263():
                    _G_exactly_264, lastError = self.exactly('?')
                    self.considerError(lastError, None)
                    _G_python_265, lastError = eval('t.Optional(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_265, self.currentError)
                def _G_or_266():
                    _G_exactly_267, lastError = self.exactly('{')
                    self.considerError(lastError, None)
                    _G_apply_268, lastError = self._apply(self.rule_ws, "ws", [])
                    self.considerError(lastError, None)
                    _G_apply_269, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                    self.considerError(lastError, None)
                    _locals['start'] = _G_apply_269
                    _G_apply_270, lastError = self._apply(self.rule_ws, "ws", [])
                    self.considerError(lastError, None)
                    def _G_or_271():
                        _G_exactly_272, lastError = self.exactly(',')
                        self.considerError(lastError, None)
                        _G_apply_273, lastError = self._apply(self.rule_ws, "ws", [])
                        self.considerError(lastError, None)
                        _G_apply_274, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                        self.considerError(lastError, None)
                        _locals['end'] = _G_apply_274
                        _G_apply_275, lastError = self._apply(self.rule_ws, "ws", [])
                        self.considerError(lastError, None)
                        _G_exactly_276, lastError = self.exactly('}')
                        self.considerError(lastError, None)
                        _G_python_277, lastError = eval('t.Repeat(start, end, e)', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_277, self.currentError)
                    def _G_or_278():
                        _G_apply_279, lastError = self._apply(self.rule_ws, "ws", [])
                        self.considerError(lastError, None)
                        _G_exactly_280, lastError = self.exactly('}')
                        self.considerError(lastError, None)
                        _G_python_281, lastError = eval('t.Repeat(start, start, e)', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_281, self.currentError)
                    _G_or_282, lastError = self._or([_G_or_271, _G_or_278])
                    self.considerError(lastError, None)
                    return (_G_or_282, self.currentError)
                def _G_or_283():
                    _G_python_284, lastError = eval('e', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_284, self.currentError)
                _G_or_285, lastError = self._or([_G_or_257, _G_or_260, _G_or_263, _G_or_266, _G_or_283])
                self.considerError(lastError, None)
                _locals['r'] = _G_or_285
                def _G_or_286():
                    _G_exactly_287, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    _G_apply_288, lastError = self._apply(self.rule_name, "name", [])
                    self.considerError(lastError, None)
                    _locals['n'] = _G_apply_288
                    _G_python_289, lastError = eval('t.Bind(n, r)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_289, self.currentError)
                def _G_or_290():
                    _G_python_291, lastError = eval('r', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_291, self.currentError)
                _G_or_292, lastError = self._or([_G_or_286, _G_or_290])
                self.considerError(lastError, None)
                return (_G_or_292, self.currentError)
            def _G_or_293():
                _G_apply_294, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_295, lastError = self.exactly(':')
                self.considerError(lastError, None)
                _G_apply_296, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_296
                _G_python_297, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_297, self.currentError)
            _G_or_298, lastError = self._or([_G_or_255, _G_or_293])
            self.considerError(lastError, 'expr3')
            return (_G_or_298, self.currentError)


        def rule_expr4(self):
            _locals = {'self': self}
            self.locals['expr4'] = _locals
            def _G_many1_299():
                _G_apply_300, lastError = self._apply(self.rule_expr3, "expr3", [])
                self.considerError(lastError, None)
                return (_G_apply_300, self.currentError)
            _G_many1_301, lastError = self.many(_G_many1_299, _G_many1_299())
            self.considerError(lastError, 'expr4')
            _locals['es'] = _G_many1_301
            _G_python_302, lastError = eval('es[0] if len(es) == 1 else t.And(es)', self.globals, _locals), None
            self.considerError(lastError, 'expr4')
            return (_G_python_302, self.currentError)


        def rule_expr(self):
            _locals = {'self': self}
            self.locals['expr'] = _locals
            _G_apply_303, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError, 'expr')
            _locals['e'] = _G_apply_303
            def _G_many_304():
                _G_apply_305, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_306, lastError = self.exactly('|')
                self.considerError(lastError, None)
                _G_apply_307, lastError = self._apply(self.rule_expr4, "expr4", [])
                self.considerError(lastError, None)
                return (_G_apply_307, self.currentError)
            _G_many_308, lastError = self.many(_G_many_304)
            self.considerError(lastError, 'expr')
            _locals['es'] = _G_many_308
            _G_python_309, lastError = eval('t.Or([e] + es) if es else e', self.globals, _locals), None
            self.considerError(lastError, 'expr')
            return (_G_python_309, self.currentError)


        def rule_ruleValue(self):
            _locals = {'self': self}
            self.locals['ruleValue'] = _locals
            _G_apply_310, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'ruleValue')
            _G_exactly_311, lastError = self.exactly('->')
            self.considerError(lastError, 'ruleValue')
            _G_python_312, lastError = eval('self.ruleValueExpr(True)', self.globals, _locals), None
            self.considerError(lastError, 'ruleValue')
            return (_G_python_312, self.currentError)


        def rule_semanticPredicate(self):
            _locals = {'self': self}
            self.locals['semanticPredicate'] = _locals
            _G_apply_313, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'semanticPredicate')
            _G_exactly_314, lastError = self.exactly('?(')
            self.considerError(lastError, 'semanticPredicate')
            _G_python_315, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticPredicate')
            return (_G_python_315, self.currentError)


        def rule_semanticAction(self):
            _locals = {'self': self}
            self.locals['semanticAction'] = _locals
            _G_apply_316, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'semanticAction')
            _G_exactly_317, lastError = self.exactly('!(')
            self.considerError(lastError, 'semanticAction')
            _G_python_318, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticAction')
            return (_G_python_318, self.currentError)


        def rule_ruleEnd(self):
            _locals = {'self': self}
            self.locals['ruleEnd'] = _locals
            def _G_or_319():
                def _G_many_320():
                    _G_apply_321, lastError = self._apply(self.rule_hspace, "hspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_321, self.currentError)
                _G_many_322, lastError = self.many(_G_many_320)
                self.considerError(lastError, None)
                def _G_many1_323():
                    _G_apply_324, lastError = self._apply(self.rule_vspace, "vspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_324, self.currentError)
                _G_many1_325, lastError = self.many(_G_many1_323, _G_many1_323())
                self.considerError(lastError, None)
                return (_G_many1_325, self.currentError)
            def _G_or_326():
                _G_apply_327, lastError = self._apply(self.rule_end, "end", [])
                self.considerError(lastError, None)
                return (_G_apply_327, self.currentError)
            _G_or_328, lastError = self._or([_G_or_319, _G_or_326])
            self.considerError(lastError, 'ruleEnd')
            return (_G_or_328, self.currentError)


        def rule_rulePart(self):
            _locals = {'self': self}
            self.locals['rulePart'] = _locals
            _G_apply_329, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'rulePart')
            _locals['requiredName'] = _G_apply_329
            _G_apply_330, lastError = self._apply(self.rule_noindentation, "noindentation", [])
            self.considerError(lastError, 'rulePart')
            _G_apply_331, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'rulePart')
            _locals['n'] = _G_apply_331
            def _G_pred_332():
                _G_python_333, lastError = eval('n == requiredName', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_333, self.currentError)
            _G_pred_334, lastError = self.pred(_G_pred_332)
            self.considerError(lastError, 'rulePart')
            _G_python_335, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
            self.considerError(lastError, 'rulePart')
            def _G_optional_336():
                _G_apply_337, lastError = self._apply(self.rule_expr4, "expr4", [])
                self.considerError(lastError, None)
                return (_G_apply_337, self.currentError)
            def _G_optional_338():
                return (None, self.input.nullError())
            _G_or_339, lastError = self._or([_G_optional_336, _G_optional_338])
            self.considerError(lastError, 'rulePart')
            _locals['args'] = _G_or_339
            def _G_or_340():
                _G_apply_341, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_342, lastError = self.exactly('=')
                self.considerError(lastError, None)
                _G_apply_343, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_343
                _G_apply_344, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_345, lastError = eval('t.And([args, e]) if args else e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_345, self.currentError)
            def _G_or_346():
                _G_apply_347, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_348, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_348, self.currentError)
            _G_or_349, lastError = self._or([_G_or_340, _G_or_346])
            self.considerError(lastError, 'rulePart')
            return (_G_or_349, self.currentError)


        def rule_rule(self):
            _locals = {'self': self}
            self.locals['rule'] = _locals
            _G_apply_350, lastError = self._apply(self.rule_noindentation, "noindentation", [])
            self.considerError(lastError, 'rule')
            def _G_lookahead_351():
                _G_apply_352, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_352
                return (_locals['n'], self.currentError)
            _G_lookahead_353, lastError = self.lookahead(_G_lookahead_351)
            self.considerError(lastError, 'rule')
            def _G_many1_354():
                _G_python_355, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_apply_356, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_355])
                self.considerError(lastError, None)
                return (_G_apply_356, self.currentError)
            _G_many1_357, lastError = self.many(_G_many1_354, _G_many1_354())
            self.considerError(lastError, 'rule')
            _locals['rs'] = _G_many1_357
            _G_python_358, lastError = eval('t.Rule(n, t.Or(rs))', self.globals, _locals), None
            self.considerError(lastError, 'rule')
            return (_G_python_358, self.currentError)


        def rule_grammar(self):
            _locals = {'self': self}
            self.locals['grammar'] = _locals
            def _G_many_359():
                _G_apply_360, lastError = self._apply(self.rule_rule, "rule", [])
                self.considerError(lastError, None)
                return (_G_apply_360, self.currentError)
            _G_many_361, lastError = self.many(_G_many_359)
            self.considerError(lastError, 'grammar')
            _locals['rs'] = _G_many_361
            _G_apply_362, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'grammar')
            _G_python_363, lastError = eval('t.Grammar(self.name, self.tree_target, rs)', self.globals, _locals), None
            self.considerError(lastError, 'grammar')
            return (_G_python_363, self.currentError)


    if parsley.globals is not None:
        parsley.globals = parsley.globals.copy()
        parsley.globals.update(ruleGlobals)
    else:
        parsley.globals = ruleGlobals
    return parsley