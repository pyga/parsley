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
                _G_python_16, lastError = "\r\n", None
                self.considerError(lastError, None)
                _G_apply_17, lastError = self._apply(self.rule_token, "token", [_G_python_16])
                self.considerError(lastError, None)
                return (_G_apply_17, self.currentError)
            def _G_or_18():
                _G_exactly_19, lastError = self.exactly('\r')
                self.considerError(lastError, None)
                return (_G_exactly_19, self.currentError)
            def _G_or_20():
                _G_exactly_21, lastError = self.exactly('\n')
                self.considerError(lastError, None)
                return (_G_exactly_21, self.currentError)
            _G_or_22, lastError = self._or([_G_or_15, _G_or_18, _G_or_20])
            self.considerError(lastError, 'vspace')
            return (_G_or_22, self.currentError)


        def rule_emptyline(self):
            _locals = {'self': self}
            self.locals['emptyline'] = _locals
            def _G_many_23():
                _G_apply_24, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError, None)
                return (_G_apply_24, self.currentError)
            _G_many_25, lastError = self.many(_G_many_23)
            self.considerError(lastError, 'emptyline')
            _G_apply_26, lastError = self._apply(self.rule_vspace, "vspace", [])
            self.considerError(lastError, 'emptyline')
            return (_G_apply_26, self.currentError)


        def rule_indentation(self):
            _locals = {'self': self}
            self.locals['indentation'] = _locals
            def _G_many_27():
                _G_apply_28, lastError = self._apply(self.rule_emptyline, "emptyline", [])
                self.considerError(lastError, None)
                return (_G_apply_28, self.currentError)
            _G_many_29, lastError = self.many(_G_many_27)
            self.considerError(lastError, 'indentation')
            def _G_many1_30():
                _G_apply_31, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError, None)
                return (_G_apply_31, self.currentError)
            _G_many1_32, lastError = self.many(_G_many1_30, _G_many1_30())
            self.considerError(lastError, 'indentation')
            return (_G_many1_32, self.currentError)


        def rule_noindentation(self):
            _locals = {'self': self}
            self.locals['noindentation'] = _locals
            def _G_many_33():
                _G_apply_34, lastError = self._apply(self.rule_emptyline, "emptyline", [])
                self.considerError(lastError, None)
                return (_G_apply_34, self.currentError)
            _G_many_35, lastError = self.many(_G_many_33)
            self.considerError(lastError, 'noindentation')
            def _G_lookahead_36():
                def _G_not_37():
                    _G_apply_38, lastError = self._apply(self.rule_hspace, "hspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_38, self.currentError)
                _G_not_39, lastError = self._not(_G_not_37)
                self.considerError(lastError, None)
                return (_G_not_39, self.currentError)
            _G_lookahead_40, lastError = self.lookahead(_G_lookahead_36)
            self.considerError(lastError, 'noindentation')
            return (_G_lookahead_40, self.currentError)


        def rule_number(self):
            _locals = {'self': self}
            self.locals['number'] = _locals
            _G_apply_41, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'number')
            def _G_or_42():
                _G_exactly_43, lastError = self.exactly('-')
                self.considerError(lastError, None)
                _G_apply_44, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_44
                _G_python_45, lastError = eval('t.Exactly(-x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_45, self.currentError)
            def _G_or_46():
                _G_apply_47, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_47
                _G_python_48, lastError = eval('t.Exactly(x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_48, self.currentError)
            _G_or_49, lastError = self._or([_G_or_42, _G_or_46])
            self.considerError(lastError, 'number')
            return (_G_or_49, self.currentError)


        def rule_barenumber(self):
            _locals = {'self': self}
            self.locals['barenumber'] = _locals
            def _G_or_50():
                _G_exactly_51, lastError = self.exactly('0')
                self.considerError(lastError, None)
                def _G_or_52():
                    def _G_or_53():
                        _G_exactly_54, lastError = self.exactly('x')
                        self.considerError(lastError, None)
                        return (_G_exactly_54, self.currentError)
                    def _G_or_55():
                        _G_exactly_56, lastError = self.exactly('X')
                        self.considerError(lastError, None)
                        return (_G_exactly_56, self.currentError)
                    _G_or_57, lastError = self._or([_G_or_53, _G_or_55])
                    self.considerError(lastError, None)
                    def _G_consumedby_58():
                        def _G_many1_59():
                            _G_apply_60, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                            self.considerError(lastError, None)
                            return (_G_apply_60, self.currentError)
                        _G_many1_61, lastError = self.many(_G_many1_59, _G_many1_59())
                        self.considerError(lastError, None)
                        return (_G_many1_61, self.currentError)
                    _G_consumedby_62, lastError = self.consumedby(_G_consumedby_58)
                    self.considerError(lastError, None)
                    _locals['hs'] = _G_consumedby_62
                    _G_python_63, lastError = eval('int(hs, 16)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_63, self.currentError)
                def _G_or_64():
                    def _G_consumedby_65():
                        def _G_many1_66():
                            _G_apply_67, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                            self.considerError(lastError, None)
                            return (_G_apply_67, self.currentError)
                        _G_many1_68, lastError = self.many(_G_many1_66, _G_many1_66())
                        self.considerError(lastError, None)
                        return (_G_many1_68, self.currentError)
                    _G_consumedby_69, lastError = self.consumedby(_G_consumedby_65)
                    self.considerError(lastError, None)
                    _locals['ds'] = _G_consumedby_69
                    _G_python_70, lastError = eval('int(ds, 8)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_70, self.currentError)
                _G_or_71, lastError = self._or([_G_or_52, _G_or_64])
                self.considerError(lastError, None)
                return (_G_or_71, self.currentError)
            def _G_or_72():
                def _G_consumedby_73():
                    def _G_many1_74():
                        _G_apply_75, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_75, self.currentError)
                    _G_many1_76, lastError = self.many(_G_many1_74, _G_many1_74())
                    self.considerError(lastError, None)
                    return (_G_many1_76, self.currentError)
                _G_consumedby_77, lastError = self.consumedby(_G_consumedby_73)
                self.considerError(lastError, None)
                _locals['ds'] = _G_consumedby_77
                _G_python_78, lastError = eval('int(ds)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_78, self.currentError)
            _G_or_79, lastError = self._or([_G_or_50, _G_or_72])
            self.considerError(lastError, 'barenumber')
            return (_G_or_79, self.currentError)


        def rule_octaldigit(self):
            _locals = {'self': self}
            self.locals['octaldigit'] = _locals
            _G_apply_80, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'octaldigit')
            _locals['x'] = _G_apply_80
            def _G_pred_81():
                _G_python_82, lastError = eval("x in '01234567'", self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_82, self.currentError)
            _G_pred_83, lastError = self.pred(_G_pred_81)
            self.considerError(lastError, 'octaldigit')
            _G_python_84, lastError = eval('x', self.globals, _locals), None
            self.considerError(lastError, 'octaldigit')
            return (_G_python_84, self.currentError)


        def rule_hexdigit(self):
            _locals = {'self': self}
            self.locals['hexdigit'] = _locals
            _G_apply_85, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'hexdigit')
            _locals['x'] = _G_apply_85
            def _G_pred_86():
                _G_python_87, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_87, self.currentError)
            _G_pred_88, lastError = self.pred(_G_pred_86)
            self.considerError(lastError, 'hexdigit')
            _G_python_89, lastError = eval('x', self.globals, _locals), None
            self.considerError(lastError, 'hexdigit')
            return (_G_python_89, self.currentError)


        def rule_escapedChar(self):
            _locals = {'self': self}
            self.locals['escapedChar'] = _locals
            _G_exactly_90, lastError = self.exactly('\\')
            self.considerError(lastError, 'escapedChar')
            def _G_or_91():
                _G_exactly_92, lastError = self.exactly('n')
                self.considerError(lastError, None)
                _G_python_93, lastError = "\n", None
                self.considerError(lastError, None)
                return (_G_python_93, self.currentError)
            def _G_or_94():
                _G_exactly_95, lastError = self.exactly('r')
                self.considerError(lastError, None)
                _G_python_96, lastError = "\r", None
                self.considerError(lastError, None)
                return (_G_python_96, self.currentError)
            def _G_or_97():
                _G_exactly_98, lastError = self.exactly('t')
                self.considerError(lastError, None)
                _G_python_99, lastError = "\t", None
                self.considerError(lastError, None)
                return (_G_python_99, self.currentError)
            def _G_or_100():
                _G_exactly_101, lastError = self.exactly('b')
                self.considerError(lastError, None)
                _G_python_102, lastError = "\b", None
                self.considerError(lastError, None)
                return (_G_python_102, self.currentError)
            def _G_or_103():
                _G_exactly_104, lastError = self.exactly('f')
                self.considerError(lastError, None)
                _G_python_105, lastError = "\f", None
                self.considerError(lastError, None)
                return (_G_python_105, self.currentError)
            def _G_or_106():
                _G_exactly_107, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_108, lastError = '"', None
                self.considerError(lastError, None)
                return (_G_python_108, self.currentError)
            def _G_or_109():
                _G_exactly_110, lastError = self.exactly("'")
                self.considerError(lastError, None)
                _G_python_111, lastError = "'", None
                self.considerError(lastError, None)
                return (_G_python_111, self.currentError)
            def _G_or_112():
                _G_exactly_113, lastError = self.exactly('x')
                self.considerError(lastError, None)
                def _G_consumedby_114():
                    _G_apply_115, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                    self.considerError(lastError, None)
                    _G_apply_116, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_116, self.currentError)
                _G_consumedby_117, lastError = self.consumedby(_G_consumedby_114)
                self.considerError(lastError, None)
                _locals['d'] = _G_consumedby_117
                _G_python_118, lastError = eval('chr(int(d, 16))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_118, self.currentError)
            def _G_or_119():
                _G_exactly_120, lastError = self.exactly('\\')
                self.considerError(lastError, None)
                _G_python_121, lastError = "\\", None
                self.considerError(lastError, None)
                return (_G_python_121, self.currentError)
            _G_or_122, lastError = self._or([_G_or_91, _G_or_94, _G_or_97, _G_or_100, _G_or_103, _G_or_106, _G_or_109, _G_or_112, _G_or_119])
            self.considerError(lastError, 'escapedChar')
            return (_G_or_122, self.currentError)


        def rule_character(self):
            _locals = {'self': self}
            self.locals['character'] = _locals
            _G_python_123, lastError = "'", None
            self.considerError(lastError, 'character')
            _G_apply_124, lastError = self._apply(self.rule_token, "token", [_G_python_123])
            self.considerError(lastError, 'character')
            def _G_many1_125():
                def _G_not_126():
                    _G_exactly_127, lastError = self.exactly("'")
                    self.considerError(lastError, None)
                    return (_G_exactly_127, self.currentError)
                _G_not_128, lastError = self._not(_G_not_126)
                self.considerError(lastError, None)
                def _G_or_129():
                    _G_apply_130, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                    self.considerError(lastError, None)
                    return (_G_apply_130, self.currentError)
                def _G_or_131():
                    _G_apply_132, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_132, self.currentError)
                _G_or_133, lastError = self._or([_G_or_129, _G_or_131])
                self.considerError(lastError, None)
                return (_G_or_133, self.currentError)
            _G_many1_134, lastError = self.many(_G_many1_125, _G_many1_125())
            self.considerError(lastError, 'character')
            _locals['c'] = _G_many1_134
            _G_python_135, lastError = "'", None
            self.considerError(lastError, 'character')
            _G_apply_136, lastError = self._apply(self.rule_token, "token", [_G_python_135])
            self.considerError(lastError, 'character')
            _G_python_137, lastError = eval("t.Exactly(''.join(c))", self.globals, _locals), None
            self.considerError(lastError, 'character')
            return (_G_python_137, self.currentError)


        def rule_string(self):
            _locals = {'self': self}
            self.locals['string'] = _locals
            _G_python_138, lastError = '"', None
            self.considerError(lastError, 'string')
            _G_apply_139, lastError = self._apply(self.rule_token, "token", [_G_python_138])
            self.considerError(lastError, 'string')
            def _G_many_140():
                def _G_or_141():
                    _G_apply_142, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                    self.considerError(lastError, None)
                    return (_G_apply_142, self.currentError)
                def _G_or_143():
                    def _G_not_144():
                        _G_exactly_145, lastError = self.exactly('"')
                        self.considerError(lastError, None)
                        return (_G_exactly_145, self.currentError)
                    _G_not_146, lastError = self._not(_G_not_144)
                    self.considerError(lastError, None)
                    _G_apply_147, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_147, self.currentError)
                _G_or_148, lastError = self._or([_G_or_141, _G_or_143])
                self.considerError(lastError, None)
                return (_G_or_148, self.currentError)
            _G_many_149, lastError = self.many(_G_many_140)
            self.considerError(lastError, 'string')
            _locals['c'] = _G_many_149
            _G_python_150, lastError = '"', None
            self.considerError(lastError, 'string')
            _G_apply_151, lastError = self._apply(self.rule_token, "token", [_G_python_150])
            self.considerError(lastError, 'string')
            _G_python_152, lastError = eval("t.Token(''.join(c))", self.globals, _locals), None
            self.considerError(lastError, 'string')
            return (_G_python_152, self.currentError)


        def rule_name(self):
            _locals = {'self': self}
            self.locals['name'] = _locals
            def _G_consumedby_153():
                _G_apply_154, lastError = self._apply(self.rule_letter, "letter", [])
                self.considerError(lastError, None)
                def _G_many_155():
                    _G_apply_156, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_156, self.currentError)
                _G_many_157, lastError = self.many(_G_many_155)
                self.considerError(lastError, None)
                return (_G_many_157, self.currentError)
            _G_consumedby_158, lastError = self.consumedby(_G_consumedby_153)
            self.considerError(lastError, 'name')
            return (_G_consumedby_158, self.currentError)


        def rule_args(self):
            _locals = {'self': self}
            self.locals['args'] = _locals
            def _G_or_159():
                _G_exactly_160, lastError = self.exactly('(')
                self.considerError(lastError, None)
                _G_python_161, lastError = eval("self.applicationArgs(finalChar=')')", self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['args'] = _G_python_161
                _G_exactly_162, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_163, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_163, self.currentError)
            def _G_or_164():
                _G_python_165, lastError = [], None
                self.considerError(lastError, None)
                return (_G_python_165, self.currentError)
            _G_or_166, lastError = self._or([_G_or_159, _G_or_164])
            self.considerError(lastError, 'args')
            return (_G_or_166, self.currentError)


        def rule_application(self):
            _locals = {'self': self}
            self.locals['application'] = _locals
            def _G_optional_167():
                _G_apply_168, lastError = self._apply(self.rule_indentation, "indentation", [])
                self.considerError(lastError, None)
                return (_G_apply_168, self.currentError)
            def _G_optional_169():
                return (None, self.input.nullError())
            _G_or_170, lastError = self._or([_G_optional_167, _G_optional_169])
            self.considerError(lastError, 'application')
            _G_apply_171, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'application')
            _locals['name'] = _G_apply_171
            _G_apply_172, lastError = self._apply(self.rule_args, "args", [])
            self.considerError(lastError, 'application')
            _locals['args'] = _G_apply_172
            _G_python_173, lastError = eval('t.Apply(name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError, 'application')
            return (_G_python_173, self.currentError)


        def rule_foreignApply(self):
            _locals = {'self': self}
            self.locals['foreignApply'] = _locals
            def _G_optional_174():
                _G_apply_175, lastError = self._apply(self.rule_indentation, "indentation", [])
                self.considerError(lastError, None)
                return (_G_apply_175, self.currentError)
            def _G_optional_176():
                return (None, self.input.nullError())
            _G_or_177, lastError = self._or([_G_optional_174, _G_optional_176])
            self.considerError(lastError, 'foreignApply')
            _G_apply_178, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'foreignApply')
            _locals['grammar_name'] = _G_apply_178
            _G_exactly_179, lastError = self.exactly('.')
            self.considerError(lastError, 'foreignApply')
            _G_apply_180, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'foreignApply')
            _locals['rule_name'] = _G_apply_180
            _G_apply_181, lastError = self._apply(self.rule_args, "args", [])
            self.considerError(lastError, 'foreignApply')
            _locals['args'] = _G_apply_181
            _G_python_182, lastError = eval('t.ForeignApply(grammar_name, rule_name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError, 'foreignApply')
            return (_G_python_182, self.currentError)


        def rule_expr1(self):
            _locals = {'self': self}
            self.locals['expr1'] = _locals
            def _G_or_183():
                _G_apply_184, lastError = self._apply(self.rule_foreignApply, "foreignApply", [])
                self.considerError(lastError, None)
                return (_G_apply_184, self.currentError)
            def _G_or_185():
                _G_apply_186, lastError = self._apply(self.rule_application, "application", [])
                self.considerError(lastError, None)
                return (_G_apply_186, self.currentError)
            def _G_or_187():
                _G_apply_188, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
                self.considerError(lastError, None)
                return (_G_apply_188, self.currentError)
            def _G_or_189():
                _G_apply_190, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
                self.considerError(lastError, None)
                return (_G_apply_190, self.currentError)
            def _G_or_191():
                _G_apply_192, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
                self.considerError(lastError, None)
                return (_G_apply_192, self.currentError)
            def _G_or_193():
                _G_apply_194, lastError = self._apply(self.rule_number, "number", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_194
                _G_python_195, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_196, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_196, self.currentError)
            def _G_or_197():
                _G_apply_198, lastError = self._apply(self.rule_character, "character", [])
                self.considerError(lastError, None)
                return (_G_apply_198, self.currentError)
            def _G_or_199():
                _G_apply_200, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                return (_G_apply_200, self.currentError)
            def _G_or_201():
                _G_python_202, lastError = '(', None
                self.considerError(lastError, None)
                _G_apply_203, lastError = self._apply(self.rule_token, "token", [_G_python_202])
                self.considerError(lastError, None)
                _G_apply_204, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_204
                _G_python_205, lastError = ')', None
                self.considerError(lastError, None)
                _G_apply_206, lastError = self._apply(self.rule_token, "token", [_G_python_205])
                self.considerError(lastError, None)
                _G_python_207, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_207, self.currentError)
            def _G_or_208():
                _G_python_209, lastError = '<', None
                self.considerError(lastError, None)
                _G_apply_210, lastError = self._apply(self.rule_token, "token", [_G_python_209])
                self.considerError(lastError, None)
                _G_apply_211, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_211
                _G_python_212, lastError = '>', None
                self.considerError(lastError, None)
                _G_apply_213, lastError = self._apply(self.rule_token, "token", [_G_python_212])
                self.considerError(lastError, None)
                _G_python_214, lastError = eval('t.ConsumedBy(e)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_214, self.currentError)
            def _G_or_215():
                _G_python_216, lastError = '[', None
                self.considerError(lastError, None)
                _G_apply_217, lastError = self._apply(self.rule_token, "token", [_G_python_216])
                self.considerError(lastError, None)
                _G_apply_218, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_218
                _G_python_219, lastError = ']', None
                self.considerError(lastError, None)
                _G_apply_220, lastError = self._apply(self.rule_token, "token", [_G_python_219])
                self.considerError(lastError, None)
                _G_python_221, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_222, lastError = eval('t.List(e)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_222, self.currentError)
            _G_or_223, lastError = self._or([_G_or_183, _G_or_185, _G_or_187, _G_or_189, _G_or_191, _G_or_193, _G_or_197, _G_or_199, _G_or_201, _G_or_208, _G_or_215])
            self.considerError(lastError, 'expr1')
            return (_G_or_223, self.currentError)


        def rule_expr2(self):
            _locals = {'self': self}
            self.locals['expr2'] = _locals
            def _G_or_224():
                _G_python_225, lastError = '~', None
                self.considerError(lastError, None)
                _G_apply_226, lastError = self._apply(self.rule_token, "token", [_G_python_225])
                self.considerError(lastError, None)
                def _G_or_227():
                    _G_python_228, lastError = '~', None
                    self.considerError(lastError, None)
                    _G_apply_229, lastError = self._apply(self.rule_token, "token", [_G_python_228])
                    self.considerError(lastError, None)
                    _G_apply_230, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_230
                    _G_python_231, lastError = eval('t.Lookahead(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_231, self.currentError)
                def _G_or_232():
                    _G_apply_233, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_233
                    _G_python_234, lastError = eval('t.Not(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_234, self.currentError)
                _G_or_235, lastError = self._or([_G_or_227, _G_or_232])
                self.considerError(lastError, None)
                return (_G_or_235, self.currentError)
            def _G_or_236():
                _G_apply_237, lastError = self._apply(self.rule_expr1, "expr1", [])
                self.considerError(lastError, None)
                return (_G_apply_237, self.currentError)
            _G_or_238, lastError = self._or([_G_or_224, _G_or_236])
            self.considerError(lastError, 'expr2')
            return (_G_or_238, self.currentError)


        def rule_repeatTimes(self):
            _locals = {'self': self}
            self.locals['repeatTimes'] = _locals
            def _G_or_239():
                _G_apply_240, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_240
                _G_python_241, lastError = eval('int(x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_241, self.currentError)
            def _G_or_242():
                _G_apply_243, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                return (_G_apply_243, self.currentError)
            _G_or_244, lastError = self._or([_G_or_239, _G_or_242])
            self.considerError(lastError, 'repeatTimes')
            return (_G_or_244, self.currentError)


        def rule_expr3(self):
            _locals = {'self': self}
            self.locals['expr3'] = _locals
            def _G_or_245():
                _G_apply_246, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_246
                def _G_or_247():
                    _G_exactly_248, lastError = self.exactly('*')
                    self.considerError(lastError, None)
                    _G_python_249, lastError = eval('t.Many(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_249, self.currentError)
                def _G_or_250():
                    _G_exactly_251, lastError = self.exactly('+')
                    self.considerError(lastError, None)
                    _G_python_252, lastError = eval('t.Many1(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_252, self.currentError)
                def _G_or_253():
                    _G_exactly_254, lastError = self.exactly('?')
                    self.considerError(lastError, None)
                    _G_python_255, lastError = eval('t.Optional(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_255, self.currentError)
                def _G_or_256():
                    _G_exactly_257, lastError = self.exactly('{')
                    self.considerError(lastError, None)
                    _G_apply_258, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError, None)
                    _G_apply_259, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                    self.considerError(lastError, None)
                    _locals['start'] = _G_apply_259
                    _G_apply_260, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError, None)
                    def _G_or_261():
                        _G_exactly_262, lastError = self.exactly(',')
                        self.considerError(lastError, None)
                        _G_apply_263, lastError = self._apply(self.rule_spaces, "spaces", [])
                        self.considerError(lastError, None)
                        _G_apply_264, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                        self.considerError(lastError, None)
                        _locals['end'] = _G_apply_264
                        _G_apply_265, lastError = self._apply(self.rule_spaces, "spaces", [])
                        self.considerError(lastError, None)
                        _G_exactly_266, lastError = self.exactly('}')
                        self.considerError(lastError, None)
                        _G_python_267, lastError = eval('t.Repeat(start, end, e)', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_267, self.currentError)
                    def _G_or_268():
                        _G_apply_269, lastError = self._apply(self.rule_spaces, "spaces", [])
                        self.considerError(lastError, None)
                        _G_exactly_270, lastError = self.exactly('}')
                        self.considerError(lastError, None)
                        _G_python_271, lastError = eval('t.Repeat(start, start, e)', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_271, self.currentError)
                    _G_or_272, lastError = self._or([_G_or_261, _G_or_268])
                    self.considerError(lastError, None)
                    return (_G_or_272, self.currentError)
                def _G_or_273():
                    _G_python_274, lastError = eval('e', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_274, self.currentError)
                _G_or_275, lastError = self._or([_G_or_247, _G_or_250, _G_or_253, _G_or_256, _G_or_273])
                self.considerError(lastError, None)
                _locals['r'] = _G_or_275
                def _G_or_276():
                    _G_exactly_277, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    _G_apply_278, lastError = self._apply(self.rule_name, "name", [])
                    self.considerError(lastError, None)
                    _locals['n'] = _G_apply_278
                    _G_python_279, lastError = eval('t.Bind(n, r)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_279, self.currentError)
                def _G_or_280():
                    _G_python_281, lastError = eval('r', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_281, self.currentError)
                _G_or_282, lastError = self._or([_G_or_276, _G_or_280])
                self.considerError(lastError, None)
                return (_G_or_282, self.currentError)
            def _G_or_283():
                _G_python_284, lastError = ':', None
                self.considerError(lastError, None)
                _G_apply_285, lastError = self._apply(self.rule_token, "token", [_G_python_284])
                self.considerError(lastError, None)
                _G_apply_286, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_286
                _G_python_287, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_287, self.currentError)
            _G_or_288, lastError = self._or([_G_or_245, _G_or_283])
            self.considerError(lastError, 'expr3')
            return (_G_or_288, self.currentError)


        def rule_expr4(self):
            _locals = {'self': self}
            self.locals['expr4'] = _locals
            def _G_many_289():
                _G_apply_290, lastError = self._apply(self.rule_expr3, "expr3", [])
                self.considerError(lastError, None)
                return (_G_apply_290, self.currentError)
            _G_many_291, lastError = self.many(_G_many_289)
            self.considerError(lastError, 'expr4')
            _locals['es'] = _G_many_291
            _G_python_292, lastError = eval('t.And(es)', self.globals, _locals), None
            self.considerError(lastError, 'expr4')
            return (_G_python_292, self.currentError)


        def rule_expr(self):
            _locals = {'self': self}
            self.locals['expr'] = _locals
            _G_apply_293, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError, 'expr')
            _locals['e'] = _G_apply_293
            def _G_many_294():
                _G_python_295, lastError = '|', None
                self.considerError(lastError, None)
                _G_apply_296, lastError = self._apply(self.rule_token, "token", [_G_python_295])
                self.considerError(lastError, None)
                _G_apply_297, lastError = self._apply(self.rule_expr4, "expr4", [])
                self.considerError(lastError, None)
                return (_G_apply_297, self.currentError)
            _G_many_298, lastError = self.many(_G_many_294)
            self.considerError(lastError, 'expr')
            _locals['es'] = _G_many_298
            _G_python_299, lastError = eval('t.Or([e] + es)', self.globals, _locals), None
            self.considerError(lastError, 'expr')
            return (_G_python_299, self.currentError)


        def rule_ruleValue(self):
            _locals = {'self': self}
            self.locals['ruleValue'] = _locals
            _G_python_300, lastError = "->", None
            self.considerError(lastError, 'ruleValue')
            _G_apply_301, lastError = self._apply(self.rule_token, "token", [_G_python_300])
            self.considerError(lastError, 'ruleValue')
            _G_python_302, lastError = eval('self.ruleValueExpr(True)', self.globals, _locals), None
            self.considerError(lastError, 'ruleValue')
            return (_G_python_302, self.currentError)


        def rule_semanticPredicate(self):
            _locals = {'self': self}
            self.locals['semanticPredicate'] = _locals
            _G_python_303, lastError = "?(", None
            self.considerError(lastError, 'semanticPredicate')
            _G_apply_304, lastError = self._apply(self.rule_token, "token", [_G_python_303])
            self.considerError(lastError, 'semanticPredicate')
            _G_python_305, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticPredicate')
            return (_G_python_305, self.currentError)


        def rule_semanticAction(self):
            _locals = {'self': self}
            self.locals['semanticAction'] = _locals
            _G_python_306, lastError = "!(", None
            self.considerError(lastError, 'semanticAction')
            _G_apply_307, lastError = self._apply(self.rule_token, "token", [_G_python_306])
            self.considerError(lastError, 'semanticAction')
            _G_python_308, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticAction')
            return (_G_python_308, self.currentError)


        def rule_ruleEnd(self):
            _locals = {'self': self}
            self.locals['ruleEnd'] = _locals
            def _G_or_309():
                def _G_many_310():
                    _G_apply_311, lastError = self._apply(self.rule_hspace, "hspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_311, self.currentError)
                _G_many_312, lastError = self.many(_G_many_310)
                self.considerError(lastError, None)
                def _G_many1_313():
                    _G_apply_314, lastError = self._apply(self.rule_vspace, "vspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_314, self.currentError)
                _G_many1_315, lastError = self.many(_G_many1_313, _G_many1_313())
                self.considerError(lastError, None)
                return (_G_many1_315, self.currentError)
            def _G_or_316():
                _G_apply_317, lastError = self._apply(self.rule_end, "end", [])
                self.considerError(lastError, None)
                return (_G_apply_317, self.currentError)
            _G_or_318, lastError = self._or([_G_or_309, _G_or_316])
            self.considerError(lastError, 'ruleEnd')
            return (_G_or_318, self.currentError)


        def rule_rulePart(self):
            _locals = {'self': self}
            self.locals['rulePart'] = _locals
            _G_apply_319, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'rulePart')
            _locals['requiredName'] = _G_apply_319
            _G_apply_320, lastError = self._apply(self.rule_noindentation, "noindentation", [])
            self.considerError(lastError, 'rulePart')
            _G_apply_321, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'rulePart')
            _locals['n'] = _G_apply_321
            def _G_pred_322():
                _G_python_323, lastError = eval('n == requiredName', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_323, self.currentError)
            _G_pred_324, lastError = self.pred(_G_pred_322)
            self.considerError(lastError, 'rulePart')
            _G_python_325, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
            self.considerError(lastError, 'rulePart')
            _G_apply_326, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError, 'rulePart')
            _locals['args'] = _G_apply_326
            def _G_or_327():
                _G_python_328, lastError = "=", None
                self.considerError(lastError, None)
                _G_apply_329, lastError = self._apply(self.rule_token, "token", [_G_python_328])
                self.considerError(lastError, None)
                _G_apply_330, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_330
                _G_apply_331, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_332, lastError = eval('t.And([args, e])', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_332, self.currentError)
            def _G_or_333():
                _G_apply_334, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_335, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_335, self.currentError)
            _G_or_336, lastError = self._or([_G_or_327, _G_or_333])
            self.considerError(lastError, 'rulePart')
            return (_G_or_336, self.currentError)


        def rule_rule(self):
            _locals = {'self': self}
            self.locals['rule'] = _locals
            _G_apply_337, lastError = self._apply(self.rule_noindentation, "noindentation", [])
            self.considerError(lastError, 'rule')
            def _G_lookahead_338():
                _G_apply_339, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_339
                return (_locals['n'], self.currentError)
            _G_lookahead_340, lastError = self.lookahead(_G_lookahead_338)
            self.considerError(lastError, 'rule')
            def _G_many1_341():
                _G_python_342, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_apply_343, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_342])
                self.considerError(lastError, None)
                return (_G_apply_343, self.currentError)
            _G_many1_344, lastError = self.many(_G_many1_341, _G_many1_341())
            self.considerError(lastError, 'rule')
            _locals['rs'] = _G_many1_344
            _G_python_345, lastError = eval('t.Rule(n, t.Or(rs))', self.globals, _locals), None
            self.considerError(lastError, 'rule')
            return (_G_python_345, self.currentError)


        def rule_grammar(self):
            _locals = {'self': self}
            self.locals['grammar'] = _locals
            def _G_many_346():
                _G_apply_347, lastError = self._apply(self.rule_rule, "rule", [])
                self.considerError(lastError, None)
                return (_G_apply_347, self.currentError)
            _G_many_348, lastError = self.many(_G_many_346)
            self.considerError(lastError, 'grammar')
            _locals['rs'] = _G_many_348
            _G_apply_349, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'grammar')
            _G_python_350, lastError = eval('t.Grammar(self.name, self.tree, rs)', self.globals, _locals), None
            self.considerError(lastError, 'grammar')
            return (_G_python_350, self.currentError)


    if parsley.globals is not None:
        parsley.globals = parsley.globals.copy()
        parsley.globals.update(ruleGlobals)
    else:
        parsley.globals = ruleGlobals
    return parsley