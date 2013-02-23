def createParserClass(GrammarBase, ruleGlobals):
    if ruleGlobals is None:
        ruleGlobals = {}
    class pymeta_v1(GrammarBase):
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


        def rule_number(self):
            _locals = {'self': self}
            self.locals['number'] = _locals
            _G_apply_23, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'number')
            def _G_or_24():
                _G_exactly_25, lastError = self.exactly('-')
                self.considerError(lastError, None)
                _G_apply_26, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_26
                _G_python_27, lastError = eval('t.Exactly(-x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_27, self.currentError)
            def _G_or_28():
                _G_apply_29, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_29
                _G_python_30, lastError = eval('t.Exactly(x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_30, self.currentError)
            _G_or_31, lastError = self._or([_G_or_24, _G_or_28])
            self.considerError(lastError, 'number')
            return (_G_or_31, self.currentError)


        def rule_barenumber(self):
            _locals = {'self': self}
            self.locals['barenumber'] = _locals
            def _G_or_32():
                _G_exactly_33, lastError = self.exactly('0')
                self.considerError(lastError, None)
                def _G_or_34():
                    def _G_or_35():
                        _G_exactly_36, lastError = self.exactly('x')
                        self.considerError(lastError, None)
                        return (_G_exactly_36, self.currentError)
                    def _G_or_37():
                        _G_exactly_38, lastError = self.exactly('X')
                        self.considerError(lastError, None)
                        return (_G_exactly_38, self.currentError)
                    _G_or_39, lastError = self._or([_G_or_35, _G_or_37])
                    self.considerError(lastError, None)
                    def _G_consumedby_40():
                        def _G_many1_41():
                            _G_apply_42, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                            self.considerError(lastError, None)
                            return (_G_apply_42, self.currentError)
                        _G_many1_43, lastError = self.many(_G_many1_41, _G_many1_41())
                        self.considerError(lastError, None)
                        return (_G_many1_43, self.currentError)
                    _G_consumedby_44, lastError = self.consumedby(_G_consumedby_40)
                    self.considerError(lastError, None)
                    _locals['hs'] = _G_consumedby_44
                    _G_python_45, lastError = eval('int(hs, 16)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_45, self.currentError)
                def _G_or_46():
                    def _G_consumedby_47():
                        def _G_many1_48():
                            _G_apply_49, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                            self.considerError(lastError, None)
                            return (_G_apply_49, self.currentError)
                        _G_many1_50, lastError = self.many(_G_many1_48, _G_many1_48())
                        self.considerError(lastError, None)
                        return (_G_many1_50, self.currentError)
                    _G_consumedby_51, lastError = self.consumedby(_G_consumedby_47)
                    self.considerError(lastError, None)
                    _locals['ds'] = _G_consumedby_51
                    _G_python_52, lastError = eval('int(ds, 8)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_52, self.currentError)
                _G_or_53, lastError = self._or([_G_or_34, _G_or_46])
                self.considerError(lastError, None)
                return (_G_or_53, self.currentError)
            def _G_or_54():
                def _G_consumedby_55():
                    def _G_many1_56():
                        _G_apply_57, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_57, self.currentError)
                    _G_many1_58, lastError = self.many(_G_many1_56, _G_many1_56())
                    self.considerError(lastError, None)
                    return (_G_many1_58, self.currentError)
                _G_consumedby_59, lastError = self.consumedby(_G_consumedby_55)
                self.considerError(lastError, None)
                _locals['ds'] = _G_consumedby_59
                _G_python_60, lastError = eval('int(ds)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_60, self.currentError)
            _G_or_61, lastError = self._or([_G_or_32, _G_or_54])
            self.considerError(lastError, 'barenumber')
            return (_G_or_61, self.currentError)


        def rule_octaldigit(self):
            _locals = {'self': self}
            self.locals['octaldigit'] = _locals
            _G_apply_62, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'octaldigit')
            _locals['x'] = _G_apply_62
            def _G_pred_63():
                _G_python_64, lastError = eval("x in '01234567'", self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_64, self.currentError)
            _G_pred_65, lastError = self.pred(_G_pred_63)
            self.considerError(lastError, 'octaldigit')
            _G_python_66, lastError = eval('x', self.globals, _locals), None
            self.considerError(lastError, 'octaldigit')
            return (_G_python_66, self.currentError)


        def rule_hexdigit(self):
            _locals = {'self': self}
            self.locals['hexdigit'] = _locals
            _G_apply_67, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'hexdigit')
            _locals['x'] = _G_apply_67
            def _G_pred_68():
                _G_python_69, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_69, self.currentError)
            _G_pred_70, lastError = self.pred(_G_pred_68)
            self.considerError(lastError, 'hexdigit')
            _G_python_71, lastError = eval('x', self.globals, _locals), None
            self.considerError(lastError, 'hexdigit')
            return (_G_python_71, self.currentError)


        def rule_escapedChar(self):
            _locals = {'self': self}
            self.locals['escapedChar'] = _locals
            _G_exactly_72, lastError = self.exactly('\\')
            self.considerError(lastError, 'escapedChar')
            def _G_or_73():
                _G_exactly_74, lastError = self.exactly('n')
                self.considerError(lastError, None)
                _G_python_75, lastError = "\n", None
                self.considerError(lastError, None)
                return (_G_python_75, self.currentError)
            def _G_or_76():
                _G_exactly_77, lastError = self.exactly('r')
                self.considerError(lastError, None)
                _G_python_78, lastError = "\r", None
                self.considerError(lastError, None)
                return (_G_python_78, self.currentError)
            def _G_or_79():
                _G_exactly_80, lastError = self.exactly('t')
                self.considerError(lastError, None)
                _G_python_81, lastError = "\t", None
                self.considerError(lastError, None)
                return (_G_python_81, self.currentError)
            def _G_or_82():
                _G_exactly_83, lastError = self.exactly('b')
                self.considerError(lastError, None)
                _G_python_84, lastError = "\b", None
                self.considerError(lastError, None)
                return (_G_python_84, self.currentError)
            def _G_or_85():
                _G_exactly_86, lastError = self.exactly('f')
                self.considerError(lastError, None)
                _G_python_87, lastError = "\f", None
                self.considerError(lastError, None)
                return (_G_python_87, self.currentError)
            def _G_or_88():
                _G_exactly_89, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_90, lastError = '"', None
                self.considerError(lastError, None)
                return (_G_python_90, self.currentError)
            def _G_or_91():
                _G_exactly_92, lastError = self.exactly("'")
                self.considerError(lastError, None)
                _G_python_93, lastError = "'", None
                self.considerError(lastError, None)
                return (_G_python_93, self.currentError)
            def _G_or_94():
                _G_exactly_95, lastError = self.exactly('\\')
                self.considerError(lastError, None)
                _G_python_96, lastError = "\\", None
                self.considerError(lastError, None)
                return (_G_python_96, self.currentError)
            _G_or_97, lastError = self._or([_G_or_73, _G_or_76, _G_or_79, _G_or_82, _G_or_85, _G_or_88, _G_or_91, _G_or_94])
            self.considerError(lastError, 'escapedChar')
            return (_G_or_97, self.currentError)


        def rule_character(self):
            _locals = {'self': self}
            self.locals['character'] = _locals
            _G_python_98, lastError = "'", None
            self.considerError(lastError, 'character')
            _G_apply_99, lastError = self._apply(self.rule_token, "token", [_G_python_98])
            self.considerError(lastError, 'character')
            def _G_or_100():
                _G_apply_101, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                self.considerError(lastError, None)
                return (_G_apply_101, self.currentError)
            def _G_or_102():
                _G_apply_103, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                return (_G_apply_103, self.currentError)
            _G_or_104, lastError = self._or([_G_or_100, _G_or_102])
            self.considerError(lastError, 'character')
            _locals['c'] = _G_or_104
            _G_python_105, lastError = "'", None
            self.considerError(lastError, 'character')
            _G_apply_106, lastError = self._apply(self.rule_token, "token", [_G_python_105])
            self.considerError(lastError, 'character')
            _G_python_107, lastError = eval('t.Exactly(c)', self.globals, _locals), None
            self.considerError(lastError, 'character')
            return (_G_python_107, self.currentError)


        def rule_string(self):
            _locals = {'self': self}
            self.locals['string'] = _locals
            _G_python_108, lastError = '"', None
            self.considerError(lastError, 'string')
            _G_apply_109, lastError = self._apply(self.rule_token, "token", [_G_python_108])
            self.considerError(lastError, 'string')
            def _G_many_110():
                def _G_or_111():
                    _G_apply_112, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                    self.considerError(lastError, None)
                    return (_G_apply_112, self.currentError)
                def _G_or_113():
                    def _G_not_114():
                        _G_exactly_115, lastError = self.exactly('"')
                        self.considerError(lastError, None)
                        return (_G_exactly_115, self.currentError)
                    _G_not_116, lastError = self._not(_G_not_114)
                    self.considerError(lastError, None)
                    _G_apply_117, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_117, self.currentError)
                _G_or_118, lastError = self._or([_G_or_111, _G_or_113])
                self.considerError(lastError, None)
                return (_G_or_118, self.currentError)
            _G_many_119, lastError = self.many(_G_many_110)
            self.considerError(lastError, 'string')
            _locals['c'] = _G_many_119
            _G_python_120, lastError = '"', None
            self.considerError(lastError, 'string')
            _G_apply_121, lastError = self._apply(self.rule_token, "token", [_G_python_120])
            self.considerError(lastError, 'string')
            _G_python_122, lastError = eval("t.Exactly(''.join(c))", self.globals, _locals), None
            self.considerError(lastError, 'string')
            return (_G_python_122, self.currentError)


        def rule_name(self):
            _locals = {'self': self}
            self.locals['name'] = _locals
            def _G_consumedby_123():
                _G_apply_124, lastError = self._apply(self.rule_letter, "letter", [])
                self.considerError(lastError, None)
                def _G_many_125():
                    _G_apply_126, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_126, self.currentError)
                _G_many_127, lastError = self.many(_G_many_125)
                self.considerError(lastError, None)
                return (_G_many_127, self.currentError)
            _G_consumedby_128, lastError = self.consumedby(_G_consumedby_123)
            self.considerError(lastError, 'name')
            return (_G_consumedby_128, self.currentError)


        def rule_application(self):
            _locals = {'self': self}
            self.locals['application'] = _locals
            _G_python_129, lastError = '<', None
            self.considerError(lastError, 'application')
            _G_apply_130, lastError = self._apply(self.rule_token, "token", [_G_python_129])
            self.considerError(lastError, 'application')
            _G_apply_131, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'application')
            _G_apply_132, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'application')
            _locals['name'] = _G_apply_132
            def _G_or_133():
                _G_exactly_134, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                _G_python_135, lastError = eval("self.applicationArgs(finalChar='>')", self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['args'] = _G_python_135
                _G_exactly_136, lastError = self.exactly('>')
                self.considerError(lastError, None)
                _G_python_137, lastError = eval('t.Apply(name, self.rulename, args)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_137, self.currentError)
            def _G_or_138():
                _G_python_139, lastError = '>', None
                self.considerError(lastError, None)
                _G_apply_140, lastError = self._apply(self.rule_token, "token", [_G_python_139])
                self.considerError(lastError, None)
                _G_python_141, lastError = eval('t.Apply(name, self.rulename, [])', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_141, self.currentError)
            _G_or_142, lastError = self._or([_G_or_133, _G_or_138])
            self.considerError(lastError, 'application')
            return (_G_or_142, self.currentError)


        def rule_expr1(self):
            _locals = {'self': self}
            self.locals['expr1'] = _locals
            def _G_or_143():
                _G_apply_144, lastError = self._apply(self.rule_application, "application", [])
                self.considerError(lastError, None)
                return (_G_apply_144, self.currentError)
            def _G_or_145():
                _G_apply_146, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
                self.considerError(lastError, None)
                return (_G_apply_146, self.currentError)
            def _G_or_147():
                _G_apply_148, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
                self.considerError(lastError, None)
                return (_G_apply_148, self.currentError)
            def _G_or_149():
                _G_apply_150, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
                self.considerError(lastError, None)
                return (_G_apply_150, self.currentError)
            def _G_or_151():
                _G_apply_152, lastError = self._apply(self.rule_number, "number", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_152
                _G_python_153, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_154, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_154, self.currentError)
            def _G_or_155():
                _G_apply_156, lastError = self._apply(self.rule_character, "character", [])
                self.considerError(lastError, None)
                return (_G_apply_156, self.currentError)
            def _G_or_157():
                _G_apply_158, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                return (_G_apply_158, self.currentError)
            def _G_or_159():
                _G_python_160, lastError = '(', None
                self.considerError(lastError, None)
                _G_apply_161, lastError = self._apply(self.rule_token, "token", [_G_python_160])
                self.considerError(lastError, None)
                _G_apply_162, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_162
                _G_python_163, lastError = ')', None
                self.considerError(lastError, None)
                _G_apply_164, lastError = self._apply(self.rule_token, "token", [_G_python_163])
                self.considerError(lastError, None)
                _G_python_165, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_165, self.currentError)
            def _G_or_166():
                _G_python_167, lastError = '[', None
                self.considerError(lastError, None)
                _G_apply_168, lastError = self._apply(self.rule_token, "token", [_G_python_167])
                self.considerError(lastError, None)
                _G_apply_169, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_169
                _G_python_170, lastError = ']', None
                self.considerError(lastError, None)
                _G_apply_171, lastError = self._apply(self.rule_token, "token", [_G_python_170])
                self.considerError(lastError, None)
                _G_python_172, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_173, lastError = eval('t.List(e)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_173, self.currentError)
            _G_or_174, lastError = self._or([_G_or_143, _G_or_145, _G_or_147, _G_or_149, _G_or_151, _G_or_155, _G_or_157, _G_or_159, _G_or_166])
            self.considerError(lastError, 'expr1')
            return (_G_or_174, self.currentError)


        def rule_expr2(self):
            _locals = {'self': self}
            self.locals['expr2'] = _locals
            def _G_or_175():
                _G_python_176, lastError = '~', None
                self.considerError(lastError, None)
                _G_apply_177, lastError = self._apply(self.rule_token, "token", [_G_python_176])
                self.considerError(lastError, None)
                def _G_or_178():
                    _G_python_179, lastError = '~', None
                    self.considerError(lastError, None)
                    _G_apply_180, lastError = self._apply(self.rule_token, "token", [_G_python_179])
                    self.considerError(lastError, None)
                    _G_apply_181, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_181
                    _G_python_182, lastError = eval('t.Lookahead(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_182, self.currentError)
                def _G_or_183():
                    _G_apply_184, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_184
                    _G_python_185, lastError = eval('t.Not(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_185, self.currentError)
                _G_or_186, lastError = self._or([_G_or_178, _G_or_183])
                self.considerError(lastError, None)
                return (_G_or_186, self.currentError)
            def _G_or_187():
                _G_apply_188, lastError = self._apply(self.rule_expr1, "expr1", [])
                self.considerError(lastError, None)
                return (_G_apply_188, self.currentError)
            _G_or_189, lastError = self._or([_G_or_175, _G_or_187])
            self.considerError(lastError, 'expr2')
            return (_G_or_189, self.currentError)


        def rule_expr3(self):
            _locals = {'self': self}
            self.locals['expr3'] = _locals
            def _G_or_190():
                _G_apply_191, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_191
                def _G_or_192():
                    _G_exactly_193, lastError = self.exactly('*')
                    self.considerError(lastError, None)
                    _G_python_194, lastError = eval('t.Many(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_194, self.currentError)
                def _G_or_195():
                    _G_exactly_196, lastError = self.exactly('+')
                    self.considerError(lastError, None)
                    _G_python_197, lastError = eval('t.Many1(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_197, self.currentError)
                def _G_or_198():
                    _G_exactly_199, lastError = self.exactly('?')
                    self.considerError(lastError, None)
                    _G_python_200, lastError = eval('t.Optional(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_200, self.currentError)
                def _G_or_201():
                    _G_python_202, lastError = eval('e', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_202, self.currentError)
                _G_or_203, lastError = self._or([_G_or_192, _G_or_195, _G_or_198, _G_or_201])
                self.considerError(lastError, None)
                _locals['r'] = _G_or_203
                def _G_or_204():
                    _G_exactly_205, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    _G_apply_206, lastError = self._apply(self.rule_name, "name", [])
                    self.considerError(lastError, None)
                    _locals['n'] = _G_apply_206
                    _G_python_207, lastError = eval('t.Bind(n, r)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_207, self.currentError)
                def _G_or_208():
                    _G_python_209, lastError = eval('r', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_209, self.currentError)
                _G_or_210, lastError = self._or([_G_or_204, _G_or_208])
                self.considerError(lastError, None)
                return (_G_or_210, self.currentError)
            def _G_or_211():
                _G_python_212, lastError = ':', None
                self.considerError(lastError, None)
                _G_apply_213, lastError = self._apply(self.rule_token, "token", [_G_python_212])
                self.considerError(lastError, None)
                _G_apply_214, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_214
                _G_python_215, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_215, self.currentError)
            _G_or_216, lastError = self._or([_G_or_190, _G_or_211])
            self.considerError(lastError, 'expr3')
            return (_G_or_216, self.currentError)


        def rule_expr4(self):
            _locals = {'self': self}
            self.locals['expr4'] = _locals
            def _G_many_217():
                _G_apply_218, lastError = self._apply(self.rule_expr3, "expr3", [])
                self.considerError(lastError, None)
                return (_G_apply_218, self.currentError)
            _G_many_219, lastError = self.many(_G_many_217)
            self.considerError(lastError, 'expr4')
            _locals['es'] = _G_many_219
            _G_python_220, lastError = eval('t.And(es)', self.globals, _locals), None
            self.considerError(lastError, 'expr4')
            return (_G_python_220, self.currentError)


        def rule_expr(self):
            _locals = {'self': self}
            self.locals['expr'] = _locals
            _G_apply_221, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError, 'expr')
            _locals['e'] = _G_apply_221
            def _G_many_222():
                _G_python_223, lastError = '|', None
                self.considerError(lastError, None)
                _G_apply_224, lastError = self._apply(self.rule_token, "token", [_G_python_223])
                self.considerError(lastError, None)
                _G_apply_225, lastError = self._apply(self.rule_expr4, "expr4", [])
                self.considerError(lastError, None)
                return (_G_apply_225, self.currentError)
            _G_many_226, lastError = self.many(_G_many_222)
            self.considerError(lastError, 'expr')
            _locals['es'] = _G_many_226
            _G_python_227, lastError = eval('t.Or([e] + es)', self.globals, _locals), None
            self.considerError(lastError, 'expr')
            return (_G_python_227, self.currentError)


        def rule_ruleValue(self):
            _locals = {'self': self}
            self.locals['ruleValue'] = _locals
            _G_python_228, lastError = "=>", None
            self.considerError(lastError, 'ruleValue')
            _G_apply_229, lastError = self._apply(self.rule_token, "token", [_G_python_228])
            self.considerError(lastError, 'ruleValue')
            _G_python_230, lastError = eval('self.ruleValueExpr(False)', self.globals, _locals), None
            self.considerError(lastError, 'ruleValue')
            return (_G_python_230, self.currentError)


        def rule_semanticPredicate(self):
            _locals = {'self': self}
            self.locals['semanticPredicate'] = _locals
            _G_python_231, lastError = "?(", None
            self.considerError(lastError, 'semanticPredicate')
            _G_apply_232, lastError = self._apply(self.rule_token, "token", [_G_python_231])
            self.considerError(lastError, 'semanticPredicate')
            _G_python_233, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticPredicate')
            return (_G_python_233, self.currentError)


        def rule_semanticAction(self):
            _locals = {'self': self}
            self.locals['semanticAction'] = _locals
            _G_python_234, lastError = "!(", None
            self.considerError(lastError, 'semanticAction')
            _G_apply_235, lastError = self._apply(self.rule_token, "token", [_G_python_234])
            self.considerError(lastError, 'semanticAction')
            _G_python_236, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticAction')
            return (_G_python_236, self.currentError)


        def rule_ruleEnd(self):
            _locals = {'self': self}
            self.locals['ruleEnd'] = _locals
            def _G_or_237():
                def _G_many_238():
                    _G_apply_239, lastError = self._apply(self.rule_hspace, "hspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_239, self.currentError)
                _G_many_240, lastError = self.many(_G_many_238)
                self.considerError(lastError, None)
                def _G_many1_241():
                    _G_apply_242, lastError = self._apply(self.rule_vspace, "vspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_242, self.currentError)
                _G_many1_243, lastError = self.many(_G_many1_241, _G_many1_241())
                self.considerError(lastError, None)
                return (_G_many1_243, self.currentError)
            def _G_or_244():
                _G_apply_245, lastError = self._apply(self.rule_end, "end", [])
                self.considerError(lastError, None)
                return (_G_apply_245, self.currentError)
            _G_or_246, lastError = self._or([_G_or_237, _G_or_244])
            self.considerError(lastError, 'ruleEnd')
            return (_G_or_246, self.currentError)


        def rule_rulePart(self):
            _locals = {'self': self}
            self.locals['rulePart'] = _locals
            _G_apply_247, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'rulePart')
            _locals['requiredName'] = _G_apply_247
            _G_apply_248, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'rulePart')
            _G_apply_249, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'rulePart')
            _locals['n'] = _G_apply_249
            def _G_pred_250():
                _G_python_251, lastError = eval('n == requiredName', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_251, self.currentError)
            _G_pred_252, lastError = self.pred(_G_pred_250)
            self.considerError(lastError, 'rulePart')
            _G_python_253, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
            self.considerError(lastError, 'rulePart')
            _G_apply_254, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError, 'rulePart')
            _locals['args'] = _G_apply_254
            def _G_or_255():
                _G_python_256, lastError = "::=", None
                self.considerError(lastError, None)
                _G_apply_257, lastError = self._apply(self.rule_token, "token", [_G_python_256])
                self.considerError(lastError, None)
                _G_apply_258, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_258
                _G_apply_259, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_260, lastError = eval('t.And([args, e])', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_260, self.currentError)
            def _G_or_261():
                _G_apply_262, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_263, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_263, self.currentError)
            _G_or_264, lastError = self._or([_G_or_255, _G_or_261])
            self.considerError(lastError, 'rulePart')
            return (_G_or_264, self.currentError)


        def rule_rule(self):
            _locals = {'self': self}
            self.locals['rule'] = _locals
            _G_apply_265, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'rule')
            def _G_lookahead_266():
                _G_apply_267, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_267
                return (_locals['n'], self.currentError)
            _G_lookahead_268, lastError = self.lookahead(_G_lookahead_266)
            self.considerError(lastError, 'rule')
            _G_python_269, lastError = eval('n', self.globals, _locals), None
            self.considerError(lastError, 'rule')
            _G_apply_270, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_269])
            self.considerError(lastError, 'rule')
            _locals['r'] = _G_apply_270
            def _G_or_271():
                def _G_many1_272():
                    _G_python_273, lastError = eval('n', self.globals, _locals), None
                    self.considerError(lastError, None)
                    _G_apply_274, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_273])
                    self.considerError(lastError, None)
                    return (_G_apply_274, self.currentError)
                _G_many1_275, lastError = self.many(_G_many1_272, _G_many1_272())
                self.considerError(lastError, None)
                _locals['rs'] = _G_many1_275
                _G_python_276, lastError = eval('t.Rule(n, t.Or([r] + rs))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_276, self.currentError)
            def _G_or_277():
                _G_python_278, lastError = eval('t.Rule(n, r)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_278, self.currentError)
            _G_or_279, lastError = self._or([_G_or_271, _G_or_277])
            self.considerError(lastError, 'rule')
            return (_G_or_279, self.currentError)


        def rule_grammar(self):
            _locals = {'self': self}
            self.locals['grammar'] = _locals
            def _G_many_280():
                _G_apply_281, lastError = self._apply(self.rule_rule, "rule", [])
                self.considerError(lastError, None)
                return (_G_apply_281, self.currentError)
            _G_many_282, lastError = self.many(_G_many_280)
            self.considerError(lastError, 'grammar')
            _locals['rs'] = _G_many_282
            _G_apply_283, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'grammar')
            _G_python_284, lastError = eval('t.Grammar(self.name, self.tree, rs)', self.globals, _locals), None
            self.considerError(lastError, 'grammar')
            return (_G_python_284, self.currentError)


    if pymeta_v1.globals is not None:
        pymeta_v1.globals = pymeta_v1.globals.copy()
        pymeta_v1.globals.update(ruleGlobals)
    else:
        pymeta_v1.globals = ruleGlobals
    return pymeta_v1