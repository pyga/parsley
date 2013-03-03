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


        def rule_number(self):
            _locals = {'self': self}
            self.locals['number'] = _locals
            _G_apply_31, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'number')
            def _G_or_32():
                _G_exactly_33, lastError = self.exactly('-')
                self.considerError(lastError, None)
                _G_apply_34, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_34
                _G_python_35, lastError = eval('t.Exactly(-x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_35, self.currentError)
            def _G_or_36():
                _G_apply_37, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_37
                _G_python_38, lastError = eval('t.Exactly(x)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_38, self.currentError)
            _G_or_39, lastError = self._or([_G_or_32, _G_or_36])
            self.considerError(lastError, 'number')
            return (_G_or_39, self.currentError)


        def rule_barenumber(self):
            _locals = {'self': self}
            self.locals['barenumber'] = _locals
            def _G_or_40():
                _G_exactly_41, lastError = self.exactly('0')
                self.considerError(lastError, None)
                def _G_or_42():
                    def _G_or_43():
                        _G_exactly_44, lastError = self.exactly('x')
                        self.considerError(lastError, None)
                        return (_G_exactly_44, self.currentError)
                    def _G_or_45():
                        _G_exactly_46, lastError = self.exactly('X')
                        self.considerError(lastError, None)
                        return (_G_exactly_46, self.currentError)
                    _G_or_47, lastError = self._or([_G_or_43, _G_or_45])
                    self.considerError(lastError, None)
                    def _G_consumedby_48():
                        def _G_many1_49():
                            _G_apply_50, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                            self.considerError(lastError, None)
                            return (_G_apply_50, self.currentError)
                        _G_many1_51, lastError = self.many(_G_many1_49, _G_many1_49())
                        self.considerError(lastError, None)
                        return (_G_many1_51, self.currentError)
                    _G_consumedby_52, lastError = self.consumedby(_G_consumedby_48)
                    self.considerError(lastError, None)
                    _locals['hs'] = _G_consumedby_52
                    _G_python_53, lastError = eval('int(hs, 16)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_53, self.currentError)
                def _G_or_54():
                    def _G_consumedby_55():
                        def _G_many1_56():
                            _G_apply_57, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                            self.considerError(lastError, None)
                            return (_G_apply_57, self.currentError)
                        _G_many1_58, lastError = self.many(_G_many1_56, _G_many1_56())
                        self.considerError(lastError, None)
                        return (_G_many1_58, self.currentError)
                    _G_consumedby_59, lastError = self.consumedby(_G_consumedby_55)
                    self.considerError(lastError, None)
                    _locals['ds'] = _G_consumedby_59
                    _G_python_60, lastError = eval('int(ds, 8)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_60, self.currentError)
                _G_or_61, lastError = self._or([_G_or_42, _G_or_54])
                self.considerError(lastError, None)
                return (_G_or_61, self.currentError)
            def _G_or_62():
                def _G_consumedby_63():
                    def _G_many1_64():
                        _G_apply_65, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_65, self.currentError)
                    _G_many1_66, lastError = self.many(_G_many1_64, _G_many1_64())
                    self.considerError(lastError, None)
                    return (_G_many1_66, self.currentError)
                _G_consumedby_67, lastError = self.consumedby(_G_consumedby_63)
                self.considerError(lastError, None)
                _locals['ds'] = _G_consumedby_67
                _G_python_68, lastError = eval('int(ds)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_68, self.currentError)
            _G_or_69, lastError = self._or([_G_or_40, _G_or_62])
            self.considerError(lastError, 'barenumber')
            return (_G_or_69, self.currentError)


        def rule_octaldigit(self):
            _locals = {'self': self}
            self.locals['octaldigit'] = _locals
            _G_apply_70, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'octaldigit')
            _locals['x'] = _G_apply_70
            def _G_pred_71():
                _G_python_72, lastError = eval("x in '01234567'", self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_72, self.currentError)
            _G_pred_73, lastError = self.pred(_G_pred_71)
            self.considerError(lastError, 'octaldigit')
            _G_python_74, lastError = eval('x', self.globals, _locals), None
            self.considerError(lastError, 'octaldigit')
            return (_G_python_74, self.currentError)


        def rule_hexdigit(self):
            _locals = {'self': self}
            self.locals['hexdigit'] = _locals
            _G_apply_75, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'hexdigit')
            _locals['x'] = _G_apply_75
            def _G_pred_76():
                _G_python_77, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_77, self.currentError)
            _G_pred_78, lastError = self.pred(_G_pred_76)
            self.considerError(lastError, 'hexdigit')
            _G_python_79, lastError = eval('x', self.globals, _locals), None
            self.considerError(lastError, 'hexdigit')
            return (_G_python_79, self.currentError)


        def rule_escapedChar(self):
            _locals = {'self': self}
            self.locals['escapedChar'] = _locals
            _G_exactly_80, lastError = self.exactly('\\')
            self.considerError(lastError, 'escapedChar')
            def _G_or_81():
                _G_exactly_82, lastError = self.exactly('n')
                self.considerError(lastError, None)
                _G_python_83, lastError = "\n", None
                self.considerError(lastError, None)
                return (_G_python_83, self.currentError)
            def _G_or_84():
                _G_exactly_85, lastError = self.exactly('r')
                self.considerError(lastError, None)
                _G_python_86, lastError = "\r", None
                self.considerError(lastError, None)
                return (_G_python_86, self.currentError)
            def _G_or_87():
                _G_exactly_88, lastError = self.exactly('t')
                self.considerError(lastError, None)
                _G_python_89, lastError = "\t", None
                self.considerError(lastError, None)
                return (_G_python_89, self.currentError)
            def _G_or_90():
                _G_exactly_91, lastError = self.exactly('b')
                self.considerError(lastError, None)
                _G_python_92, lastError = "\b", None
                self.considerError(lastError, None)
                return (_G_python_92, self.currentError)
            def _G_or_93():
                _G_exactly_94, lastError = self.exactly('f')
                self.considerError(lastError, None)
                _G_python_95, lastError = "\f", None
                self.considerError(lastError, None)
                return (_G_python_95, self.currentError)
            def _G_or_96():
                _G_exactly_97, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_98, lastError = '"', None
                self.considerError(lastError, None)
                return (_G_python_98, self.currentError)
            def _G_or_99():
                _G_exactly_100, lastError = self.exactly("'")
                self.considerError(lastError, None)
                _G_python_101, lastError = "'", None
                self.considerError(lastError, None)
                return (_G_python_101, self.currentError)
            def _G_or_102():
                _G_exactly_103, lastError = self.exactly('\\')
                self.considerError(lastError, None)
                _G_python_104, lastError = "\\", None
                self.considerError(lastError, None)
                return (_G_python_104, self.currentError)
            _G_or_105, lastError = self._or([_G_or_81, _G_or_84, _G_or_87, _G_or_90, _G_or_93, _G_or_96, _G_or_99, _G_or_102])
            self.considerError(lastError, 'escapedChar')
            return (_G_or_105, self.currentError)


        def rule_character(self):
            _locals = {'self': self}
            self.locals['character'] = _locals
            _G_apply_106, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'character')
            _G_exactly_107, lastError = self.exactly("'")
            self.considerError(lastError, 'character')
            def _G_or_108():
                _G_apply_109, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                self.considerError(lastError, None)
                return (_G_apply_109, self.currentError)
            def _G_or_110():
                _G_apply_111, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                return (_G_apply_111, self.currentError)
            _G_or_112, lastError = self._or([_G_or_108, _G_or_110])
            self.considerError(lastError, 'character')
            _locals['c'] = _G_or_112
            _G_apply_113, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'character')
            _G_exactly_114, lastError = self.exactly("'")
            self.considerError(lastError, 'character')
            _G_python_115, lastError = eval('t.Exactly(c)', self.globals, _locals), None
            self.considerError(lastError, 'character')
            return (_G_python_115, self.currentError)


        def rule_string(self):
            _locals = {'self': self}
            self.locals['string'] = _locals
            _G_apply_116, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'string')
            _G_exactly_117, lastError = self.exactly('"')
            self.considerError(lastError, 'string')
            def _G_many_118():
                def _G_or_119():
                    _G_apply_120, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                    self.considerError(lastError, None)
                    return (_G_apply_120, self.currentError)
                def _G_or_121():
                    def _G_not_122():
                        _G_exactly_123, lastError = self.exactly('"')
                        self.considerError(lastError, None)
                        return (_G_exactly_123, self.currentError)
                    _G_not_124, lastError = self._not(_G_not_122)
                    self.considerError(lastError, None)
                    _G_apply_125, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_125, self.currentError)
                _G_or_126, lastError = self._or([_G_or_119, _G_or_121])
                self.considerError(lastError, None)
                return (_G_or_126, self.currentError)
            _G_many_127, lastError = self.many(_G_many_118)
            self.considerError(lastError, 'string')
            _locals['c'] = _G_many_127
            _G_exactly_128, lastError = self.exactly('"')
            self.considerError(lastError, 'string')
            _G_python_129, lastError = eval("t.Exactly(''.join(c))", self.globals, _locals), None
            self.considerError(lastError, 'string')
            return (_G_python_129, self.currentError)


        def rule_name(self):
            _locals = {'self': self}
            self.locals['name'] = _locals
            def _G_consumedby_130():
                _G_apply_131, lastError = self._apply(self.rule_letter, "letter", [])
                self.considerError(lastError, None)
                def _G_many_132():
                    _G_apply_133, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_133, self.currentError)
                _G_many_134, lastError = self.many(_G_many_132)
                self.considerError(lastError, None)
                return (_G_many_134, self.currentError)
            _G_consumedby_135, lastError = self.consumedby(_G_consumedby_130)
            self.considerError(lastError, 'name')
            return (_G_consumedby_135, self.currentError)


        def rule_application(self):
            _locals = {'self': self}
            self.locals['application'] = _locals
            _G_apply_136, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'application')
            _G_exactly_137, lastError = self.exactly('<')
            self.considerError(lastError, 'application')
            _G_apply_138, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'application')
            _G_apply_139, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'application')
            _locals['name'] = _G_apply_139
            def _G_or_140():
                _G_exactly_141, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                _G_python_142, lastError = eval("self.applicationArgs(finalChar='>')", self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['args'] = _G_python_142
                _G_exactly_143, lastError = self.exactly('>')
                self.considerError(lastError, None)
                _G_python_144, lastError = eval('t.Apply(name, self.rulename, args)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_144, self.currentError)
            def _G_or_145():
                _G_apply_146, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_147, lastError = self.exactly('>')
                self.considerError(lastError, None)
                _G_python_148, lastError = eval('t.Apply(name, self.rulename, [])', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_148, self.currentError)
            _G_or_149, lastError = self._or([_G_or_140, _G_or_145])
            self.considerError(lastError, 'application')
            return (_G_or_149, self.currentError)


        def rule_expr1(self):
            _locals = {'self': self}
            self.locals['expr1'] = _locals
            def _G_or_150():
                _G_apply_151, lastError = self._apply(self.rule_application, "application", [])
                self.considerError(lastError, None)
                return (_G_apply_151, self.currentError)
            def _G_or_152():
                _G_apply_153, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
                self.considerError(lastError, None)
                return (_G_apply_153, self.currentError)
            def _G_or_154():
                _G_apply_155, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
                self.considerError(lastError, None)
                return (_G_apply_155, self.currentError)
            def _G_or_156():
                _G_apply_157, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
                self.considerError(lastError, None)
                return (_G_apply_157, self.currentError)
            def _G_or_158():
                _G_apply_159, lastError = self._apply(self.rule_number, "number", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_159
                _G_python_160, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_161, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_161, self.currentError)
            def _G_or_162():
                _G_apply_163, lastError = self._apply(self.rule_character, "character", [])
                self.considerError(lastError, None)
                return (_G_apply_163, self.currentError)
            def _G_or_164():
                _G_apply_165, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                return (_G_apply_165, self.currentError)
            def _G_or_166():
                _G_apply_167, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_168, lastError = self.exactly('(')
                self.considerError(lastError, None)
                _G_apply_169, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_169
                _G_apply_170, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_171, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_172, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_172, self.currentError)
            def _G_or_173():
                _G_apply_174, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_175, lastError = self.exactly('[')
                self.considerError(lastError, None)
                _G_apply_176, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_176
                _G_apply_177, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_178, lastError = self.exactly(']')
                self.considerError(lastError, None)
                _G_python_179, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_180, lastError = eval('t.List(e)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_180, self.currentError)
            _G_or_181, lastError = self._or([_G_or_150, _G_or_152, _G_or_154, _G_or_156, _G_or_158, _G_or_162, _G_or_164, _G_or_166, _G_or_173])
            self.considerError(lastError, 'expr1')
            return (_G_or_181, self.currentError)


        def rule_expr2(self):
            _locals = {'self': self}
            self.locals['expr2'] = _locals
            def _G_or_182():
                _G_apply_183, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_184, lastError = self.exactly('~')
                self.considerError(lastError, None)
                def _G_or_185():
                    _G_exactly_186, lastError = self.exactly('~')
                    self.considerError(lastError, None)
                    _G_apply_187, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_187
                    _G_python_188, lastError = eval('t.Lookahead(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_188, self.currentError)
                def _G_or_189():
                    _G_apply_190, lastError = self._apply(self.rule_expr2, "expr2", [])
                    self.considerError(lastError, None)
                    _locals['e'] = _G_apply_190
                    _G_python_191, lastError = eval('t.Not(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_191, self.currentError)
                _G_or_192, lastError = self._or([_G_or_185, _G_or_189])
                self.considerError(lastError, None)
                return (_G_or_192, self.currentError)
            def _G_or_193():
                _G_apply_194, lastError = self._apply(self.rule_expr1, "expr1", [])
                self.considerError(lastError, None)
                return (_G_apply_194, self.currentError)
            _G_or_195, lastError = self._or([_G_or_182, _G_or_193])
            self.considerError(lastError, 'expr2')
            return (_G_or_195, self.currentError)


        def rule_expr3(self):
            _locals = {'self': self}
            self.locals['expr3'] = _locals
            def _G_or_196():
                _G_apply_197, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_197
                def _G_or_198():
                    _G_exactly_199, lastError = self.exactly('*')
                    self.considerError(lastError, None)
                    _G_python_200, lastError = eval('t.Many(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_200, self.currentError)
                def _G_or_201():
                    _G_exactly_202, lastError = self.exactly('+')
                    self.considerError(lastError, None)
                    _G_python_203, lastError = eval('t.Many1(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_203, self.currentError)
                def _G_or_204():
                    _G_exactly_205, lastError = self.exactly('?')
                    self.considerError(lastError, None)
                    _G_python_206, lastError = eval('t.Optional(e)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_206, self.currentError)
                def _G_or_207():
                    _G_python_208, lastError = eval('e', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_208, self.currentError)
                _G_or_209, lastError = self._or([_G_or_198, _G_or_201, _G_or_204, _G_or_207])
                self.considerError(lastError, None)
                _locals['r'] = _G_or_209
                def _G_or_210():
                    _G_exactly_211, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    _G_apply_212, lastError = self._apply(self.rule_name, "name", [])
                    self.considerError(lastError, None)
                    _locals['n'] = _G_apply_212
                    _G_python_213, lastError = eval('t.Bind(n, r)', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_213, self.currentError)
                def _G_or_214():
                    _G_python_215, lastError = eval('r', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_215, self.currentError)
                _G_or_216, lastError = self._or([_G_or_210, _G_or_214])
                self.considerError(lastError, None)
                return (_G_or_216, self.currentError)
            def _G_or_217():
                _G_apply_218, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_219, lastError = self.exactly(':')
                self.considerError(lastError, None)
                _G_apply_220, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_220
                _G_python_221, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_221, self.currentError)
            _G_or_222, lastError = self._or([_G_or_196, _G_or_217])
            self.considerError(lastError, 'expr3')
            return (_G_or_222, self.currentError)


        def rule_expr4(self):
            _locals = {'self': self}
            self.locals['expr4'] = _locals
            def _G_many_223():
                _G_apply_224, lastError = self._apply(self.rule_expr3, "expr3", [])
                self.considerError(lastError, None)
                return (_G_apply_224, self.currentError)
            _G_many_225, lastError = self.many(_G_many_223)
            self.considerError(lastError, 'expr4')
            _locals['es'] = _G_many_225
            _G_python_226, lastError = eval('t.And(es)', self.globals, _locals), None
            self.considerError(lastError, 'expr4')
            return (_G_python_226, self.currentError)


        def rule_expr(self):
            _locals = {'self': self}
            self.locals['expr'] = _locals
            _G_apply_227, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError, 'expr')
            _locals['e'] = _G_apply_227
            def _G_many_228():
                _G_apply_229, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_230, lastError = self.exactly('|')
                self.considerError(lastError, None)
                _G_apply_231, lastError = self._apply(self.rule_expr4, "expr4", [])
                self.considerError(lastError, None)
                return (_G_apply_231, self.currentError)
            _G_many_232, lastError = self.many(_G_many_228)
            self.considerError(lastError, 'expr')
            _locals['es'] = _G_many_232
            _G_python_233, lastError = eval('t.Or([e] + es)', self.globals, _locals), None
            self.considerError(lastError, 'expr')
            return (_G_python_233, self.currentError)


        def rule_ruleValue(self):
            _locals = {'self': self}
            self.locals['ruleValue'] = _locals
            _G_apply_234, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'ruleValue')
            _G_exactly_235, lastError = self.exactly('=>')
            self.considerError(lastError, 'ruleValue')
            _G_python_236, lastError = eval('self.ruleValueExpr(False)', self.globals, _locals), None
            self.considerError(lastError, 'ruleValue')
            return (_G_python_236, self.currentError)


        def rule_semanticPredicate(self):
            _locals = {'self': self}
            self.locals['semanticPredicate'] = _locals
            _G_apply_237, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'semanticPredicate')
            _G_exactly_238, lastError = self.exactly('?(')
            self.considerError(lastError, 'semanticPredicate')
            _G_python_239, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticPredicate')
            return (_G_python_239, self.currentError)


        def rule_semanticAction(self):
            _locals = {'self': self}
            self.locals['semanticAction'] = _locals
            _G_apply_240, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'semanticAction')
            _G_exactly_241, lastError = self.exactly('!(')
            self.considerError(lastError, 'semanticAction')
            _G_python_242, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
            self.considerError(lastError, 'semanticAction')
            return (_G_python_242, self.currentError)


        def rule_ruleEnd(self):
            _locals = {'self': self}
            self.locals['ruleEnd'] = _locals
            def _G_or_243():
                def _G_many_244():
                    _G_apply_245, lastError = self._apply(self.rule_hspace, "hspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_245, self.currentError)
                _G_many_246, lastError = self.many(_G_many_244)
                self.considerError(lastError, None)
                def _G_many1_247():
                    _G_apply_248, lastError = self._apply(self.rule_vspace, "vspace", [])
                    self.considerError(lastError, None)
                    return (_G_apply_248, self.currentError)
                _G_many1_249, lastError = self.many(_G_many1_247, _G_many1_247())
                self.considerError(lastError, None)
                return (_G_many1_249, self.currentError)
            def _G_or_250():
                _G_apply_251, lastError = self._apply(self.rule_end, "end", [])
                self.considerError(lastError, None)
                return (_G_apply_251, self.currentError)
            _G_or_252, lastError = self._or([_G_or_243, _G_or_250])
            self.considerError(lastError, 'ruleEnd')
            return (_G_or_252, self.currentError)


        def rule_rulePart(self):
            _locals = {'self': self}
            self.locals['rulePart'] = _locals
            _G_apply_253, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'rulePart')
            _locals['requiredName'] = _G_apply_253
            _G_apply_254, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'rulePart')
            _G_apply_255, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'rulePart')
            _locals['n'] = _G_apply_255
            def _G_pred_256():
                _G_python_257, lastError = eval('n == requiredName', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_257, self.currentError)
            _G_pred_258, lastError = self.pred(_G_pred_256)
            self.considerError(lastError, 'rulePart')
            _G_python_259, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
            self.considerError(lastError, 'rulePart')
            _G_apply_260, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError, 'rulePart')
            _locals['args'] = _G_apply_260
            def _G_or_261():
                _G_apply_262, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_263, lastError = self.exactly('::=')
                self.considerError(lastError, None)
                _G_apply_264, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_264
                _G_apply_265, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_266, lastError = eval('t.And([args, e])', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_266, self.currentError)
            def _G_or_267():
                _G_apply_268, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
                self.considerError(lastError, None)
                _G_python_269, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_269, self.currentError)
            _G_or_270, lastError = self._or([_G_or_261, _G_or_267])
            self.considerError(lastError, 'rulePart')
            return (_G_or_270, self.currentError)


        def rule_rule(self):
            _locals = {'self': self}
            self.locals['rule'] = _locals
            _G_apply_271, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'rule')
            def _G_lookahead_272():
                _G_apply_273, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_273
                return (_locals['n'], self.currentError)
            _G_lookahead_274, lastError = self.lookahead(_G_lookahead_272)
            self.considerError(lastError, 'rule')
            _G_python_275, lastError = eval('n', self.globals, _locals), None
            self.considerError(lastError, 'rule')
            _G_apply_276, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_275])
            self.considerError(lastError, 'rule')
            _locals['r'] = _G_apply_276
            def _G_or_277():
                def _G_many1_278():
                    _G_python_279, lastError = eval('n', self.globals, _locals), None
                    self.considerError(lastError, None)
                    _G_apply_280, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_279])
                    self.considerError(lastError, None)
                    return (_G_apply_280, self.currentError)
                _G_many1_281, lastError = self.many(_G_many1_278, _G_many1_278())
                self.considerError(lastError, None)
                _locals['rs'] = _G_many1_281
                _G_python_282, lastError = eval('t.Rule(n, t.Or([r] + rs))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_282, self.currentError)
            def _G_or_283():
                _G_python_284, lastError = eval('t.Rule(n, r)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_284, self.currentError)
            _G_or_285, lastError = self._or([_G_or_277, _G_or_283])
            self.considerError(lastError, 'rule')
            return (_G_or_285, self.currentError)


        def rule_grammar(self):
            _locals = {'self': self}
            self.locals['grammar'] = _locals
            def _G_many_286():
                _G_apply_287, lastError = self._apply(self.rule_rule, "rule", [])
                self.considerError(lastError, None)
                return (_G_apply_287, self.currentError)
            _G_many_288, lastError = self.many(_G_many_286)
            self.considerError(lastError, 'grammar')
            _locals['rs'] = _G_many_288
            _G_apply_289, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'grammar')
            _G_python_290, lastError = eval('t.Grammar(self.name, self.tree_target, rs)', self.globals, _locals), None
            self.considerError(lastError, 'grammar')
            return (_G_python_290, self.currentError)


    if pymeta_v1.globals is not None:
        pymeta_v1.globals = pymeta_v1.globals.copy()
        pymeta_v1.globals.update(ruleGlobals)
    else:
        pymeta_v1.globals = ruleGlobals
    return pymeta_v1