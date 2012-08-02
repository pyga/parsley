from ometa.runtime import OMetaGrammarBase as GrammarBase
from terml.nodes import termMaker as t

class BootOMetaGrammar(GrammarBase):
    def __init__(self, *a, **kw):
        GrammarBase.__init__(self, *a, **kw)
        self.globals['t'] = t

    def rule_hspace(self):
        _locals = {'self': self}
        self.locals['hspace'] = _locals
        def _G_or_1():
            _G_exactly_2, lastError = self.exactly(' ')
            self.considerError(lastError)
            return (_G_exactly_2, self.currentError)
        def _G_or_3():
            _G_exactly_4, lastError = self.exactly('\t')
            self.considerError(lastError)
            return (_G_exactly_4, self.currentError)
        def _G_or_5():
            _G_exactly_6, lastError = self.exactly('#')
            self.considerError(lastError)
            def _G_many_7():
                def _G_not_8():
                    _G_apply_9, lastError = self._apply(self.rule_vspace, "vspace", [])
                    self.considerError(lastError)
                    return (_G_apply_9, self.currentError)
                _G_not_10, lastError = self._not(_G_not_8)
                self.considerError(lastError)
                _G_apply_11, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                return (_G_apply_11, self.currentError)
            _G_many_12, lastError = self.many(_G_many_7)
            self.considerError(lastError)
            return (_G_many_12, self.currentError)
        _G_or_13, lastError = self._or([_G_or_1, _G_or_3, _G_or_5])
        self.considerError(lastError)
        return (_G_or_13, self.currentError)


    def rule_vspace(self):
        _locals = {'self': self}
        self.locals['vspace'] = _locals
        def _G_or_14():
            _G_python_15, lastError = eval('"\\r\\n"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_16, lastError = self._apply(self.rule_token, "token", [_G_python_15])
            self.considerError(lastError)
            return (_G_apply_16, self.currentError)
        def _G_or_17():
            _G_exactly_18, lastError = self.exactly('\r')
            self.considerError(lastError)
            return (_G_exactly_18, self.currentError)
        def _G_or_19():
            _G_exactly_20, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_20, self.currentError)
        _G_or_21, lastError = self._or([_G_or_14, _G_or_17, _G_or_19])
        self.considerError(lastError)
        return (_G_or_21, self.currentError)


    def rule_number(self):
        _locals = {'self': self}
        self.locals['number'] = _locals
        _G_apply_22, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_or_23():
            _G_exactly_24, lastError = self.exactly('-')
            self.considerError(lastError)
            _G_apply_25, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_25
            _G_python_26, lastError = eval('t.Exactly(-x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_26, self.currentError)
        def _G_or_27():
            _G_apply_28, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_28
            _G_python_29, lastError = eval('t.Exactly(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_29, self.currentError)
        _G_or_30, lastError = self._or([_G_or_23, _G_or_27])
        self.considerError(lastError)
        return (_G_or_30, self.currentError)


    def rule_barenumber(self):
        _locals = {'self': self}
        self.locals['barenumber'] = _locals
        def _G_or_31():
            _G_exactly_32, lastError = self.exactly('0')
            self.considerError(lastError)
            def _G_or_33():
                def _G_or_34():
                    _G_exactly_35, lastError = self.exactly('x')
                    self.considerError(lastError)
                    return (_G_exactly_35, self.currentError)
                def _G_or_36():
                    _G_exactly_37, lastError = self.exactly('X')
                    self.considerError(lastError)
                    return (_G_exactly_37, self.currentError)
                _G_or_38, lastError = self._or([_G_or_34, _G_or_36])
                self.considerError(lastError)
                def _G_consumedby_39():
                    def _G_many1_40():
                        _G_apply_41, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                        self.considerError(lastError)
                        return (_G_apply_41, self.currentError)
                    _G_many1_42, lastError = self.many(_G_many1_40, _G_many1_40())
                    self.considerError(lastError)
                    return (_G_many1_42, self.currentError)
                _G_consumedby_43, lastError = self.consumedby(_G_consumedby_39)
                self.considerError(lastError)
                _locals['hs'] = _G_consumedby_43
                _G_python_44, lastError = eval('int(hs, 16)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_44, self.currentError)
            def _G_or_45():
                def _G_consumedby_46():
                    def _G_many1_47():
                        _G_apply_48, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                        self.considerError(lastError)
                        return (_G_apply_48, self.currentError)
                    _G_many1_49, lastError = self.many(_G_many1_47, _G_many1_47())
                    self.considerError(lastError)
                    return (_G_many1_49, self.currentError)
                _G_consumedby_50, lastError = self.consumedby(_G_consumedby_46)
                self.considerError(lastError)
                _locals['ds'] = _G_consumedby_50
                _G_python_51, lastError = eval('int(ds, 8)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_51, self.currentError)
            _G_or_52, lastError = self._or([_G_or_33, _G_or_45])
            self.considerError(lastError)
            return (_G_or_52, self.currentError)
        def _G_or_53():
            def _G_consumedby_54():
                def _G_many1_55():
                    _G_apply_56, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError)
                    return (_G_apply_56, self.currentError)
                _G_many1_57, lastError = self.many(_G_many1_55, _G_many1_55())
                self.considerError(lastError)
                return (_G_many1_57, self.currentError)
            _G_consumedby_58, lastError = self.consumedby(_G_consumedby_54)
            self.considerError(lastError)
            _locals['ds'] = _G_consumedby_58
            _G_python_59, lastError = eval('int(ds)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_59, self.currentError)
        _G_or_60, lastError = self._or([_G_or_31, _G_or_53])
        self.considerError(lastError)
        return (_G_or_60, self.currentError)


    def rule_octaldigit(self):
        _locals = {'self': self}
        self.locals['octaldigit'] = _locals
        _G_apply_61, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_61
        def _G_pred_62():
            _G_python_63, lastError = eval("x in '01234567'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_63, self.currentError)
        _G_pred_64, lastError = self.pred(_G_pred_62)
        self.considerError(lastError)
        _G_python_65, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_65, self.currentError)


    def rule_hexdigit(self):
        _locals = {'self': self}
        self.locals['hexdigit'] = _locals
        _G_apply_66, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_66
        def _G_pred_67():
            _G_python_68, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_68, self.currentError)
        _G_pred_69, lastError = self.pred(_G_pred_67)
        self.considerError(lastError)
        _G_python_70, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_70, self.currentError)


    def rule_escapedChar(self):
        _locals = {'self': self}
        self.locals['escapedChar'] = _locals
        _G_exactly_71, lastError = self.exactly('\\')
        self.considerError(lastError)
        def _G_or_72():
            _G_exactly_73, lastError = self.exactly('n')
            self.considerError(lastError)
            _G_python_74, lastError = eval('"\\n"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_74, self.currentError)
        def _G_or_75():
            _G_exactly_76, lastError = self.exactly('r')
            self.considerError(lastError)
            _G_python_77, lastError = eval('"\\r"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_77, self.currentError)
        def _G_or_78():
            _G_exactly_79, lastError = self.exactly('t')
            self.considerError(lastError)
            _G_python_80, lastError = eval('"\\t"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_80, self.currentError)
        def _G_or_81():
            _G_exactly_82, lastError = self.exactly('b')
            self.considerError(lastError)
            _G_python_83, lastError = eval('"\\b"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_83, self.currentError)
        def _G_or_84():
            _G_exactly_85, lastError = self.exactly('f')
            self.considerError(lastError)
            _G_python_86, lastError = eval('"\\f"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_86, self.currentError)
        def _G_or_87():
            _G_exactly_88, lastError = self.exactly('"')
            self.considerError(lastError)
            _G_python_89, lastError = eval('\'"\'', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_89, self.currentError)
        def _G_or_90():
            _G_exactly_91, lastError = self.exactly("'")
            self.considerError(lastError)
            _G_python_92, lastError = eval('"\'"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_92, self.currentError)
        def _G_or_93():
            _G_exactly_94, lastError = self.exactly('\\')
            self.considerError(lastError)
            _G_python_95, lastError = eval('"\\\\"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_95, self.currentError)
        _G_or_96, lastError = self._or([_G_or_72, _G_or_75, _G_or_78, _G_or_81, _G_or_84, _G_or_87, _G_or_90, _G_or_93])
        self.considerError(lastError)
        return (_G_or_96, self.currentError)


    def rule_character(self):
        _locals = {'self': self}
        self.locals['character'] = _locals
        _G_python_97, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_98, lastError = self._apply(self.rule_token, "token", [_G_python_97])
        self.considerError(lastError)
        def _G_or_99():
            _G_apply_100, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
            self.considerError(lastError)
            return (_G_apply_100, self.currentError)
        def _G_or_101():
            _G_apply_102, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError)
            return (_G_apply_102, self.currentError)
        _G_or_103, lastError = self._or([_G_or_99, _G_or_101])
        self.considerError(lastError)
        _locals['c'] = _G_or_103
        _G_python_104, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_105, lastError = self._apply(self.rule_token, "token", [_G_python_104])
        self.considerError(lastError)
        _G_python_106, lastError = eval('t.Exactly(c)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_106, self.currentError)


    def rule_string(self):
        _locals = {'self': self}
        self.locals['string'] = _locals
        _G_python_107, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_108, lastError = self._apply(self.rule_token, "token", [_G_python_107])
        self.considerError(lastError)
        def _G_many_109():
            def _G_or_110():
                _G_apply_111, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                self.considerError(lastError)
                return (_G_apply_111, self.currentError)
            def _G_or_112():
                def _G_not_113():
                    _G_exactly_114, lastError = self.exactly('"')
                    self.considerError(lastError)
                    return (_G_exactly_114, self.currentError)
                _G_not_115, lastError = self._not(_G_not_113)
                self.considerError(lastError)
                _G_apply_116, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                return (_G_apply_116, self.currentError)
            _G_or_117, lastError = self._or([_G_or_110, _G_or_112])
            self.considerError(lastError)
            return (_G_or_117, self.currentError)
        _G_many_118, lastError = self.many(_G_many_109)
        self.considerError(lastError)
        _locals['c'] = _G_many_118
        _G_python_119, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_120, lastError = self._apply(self.rule_token, "token", [_G_python_119])
        self.considerError(lastError)
        _G_python_121, lastError = eval("t.Exactly(''.join(c))", self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_121, self.currentError)


    def rule_name(self):
        _locals = {'self': self}
        self.locals['name'] = _locals
        def _G_consumedby_122():
            _G_apply_123, lastError = self._apply(self.rule_letter, "letter", [])
            self.considerError(lastError)
            def _G_many_124():
                _G_apply_125, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                self.considerError(lastError)
                return (_G_apply_125, self.currentError)
            _G_many_126, lastError = self.many(_G_many_124)
            self.considerError(lastError)
            return (_G_many_126, self.currentError)
        _G_consumedby_127, lastError = self.consumedby(_G_consumedby_122)
        self.considerError(lastError)
        return (_G_consumedby_127, self.currentError)


    def rule_application(self):
        _locals = {'self': self}
        self.locals['application'] = _locals
        _G_python_128, lastError = eval("'<'", self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_129, lastError = self._apply(self.rule_token, "token", [_G_python_128])
        self.considerError(lastError)
        _G_apply_130, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_apply_131, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['name'] = _G_apply_131
        def _G_or_132():
            _G_exactly_133, lastError = self.exactly(' ')
            self.considerError(lastError)
            _G_python_134, lastError = eval("self.applicationArgs(finalChar='>')", self.globals, _locals), None
            self.considerError(lastError)
            _locals['args'] = _G_python_134
            _G_exactly_135, lastError = self.exactly('>')
            self.considerError(lastError)
            _G_python_136, lastError = eval('t.Apply(name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_136, self.currentError)
        def _G_or_137():
            _G_python_138, lastError = eval("'>'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_139, lastError = self._apply(self.rule_token, "token", [_G_python_138])
            self.considerError(lastError)
            _G_python_140, lastError = eval('t.Apply(name, self.rulename, [])', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_140, self.currentError)
        _G_or_141, lastError = self._or([_G_or_132, _G_or_137])
        self.considerError(lastError)
        return (_G_or_141, self.currentError)


    def rule_expr1(self):
        _locals = {'self': self}
        self.locals['expr1'] = _locals
        def _G_or_142():
            _G_apply_143, lastError = self._apply(self.rule_application, "application", [])
            self.considerError(lastError)
            return (_G_apply_143, self.currentError)
        def _G_or_144():
            _G_apply_145, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
            self.considerError(lastError)
            return (_G_apply_145, self.currentError)
        def _G_or_146():
            _G_apply_147, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
            self.considerError(lastError)
            return (_G_apply_147, self.currentError)
        def _G_or_148():
            _G_apply_149, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
            self.considerError(lastError)
            return (_G_apply_149, self.currentError)
        def _G_or_150():
            _G_apply_151, lastError = self._apply(self.rule_number, "number", [])
            self.considerError(lastError)
            return (_G_apply_151, self.currentError)
        def _G_or_152():
            _G_apply_153, lastError = self._apply(self.rule_character, "character", [])
            self.considerError(lastError)
            return (_G_apply_153, self.currentError)
        def _G_or_154():
            _G_apply_155, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            return (_G_apply_155, self.currentError)
        def _G_or_156():
            _G_python_157, lastError = eval("'('", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_158, lastError = self._apply(self.rule_token, "token", [_G_python_157])
            self.considerError(lastError)
            _G_apply_159, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_159
            _G_python_160, lastError = eval("')'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_161, lastError = self._apply(self.rule_token, "token", [_G_python_160])
            self.considerError(lastError)
            _G_python_162, lastError = eval('e', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_162, self.currentError)
        def _G_or_163():
            _G_python_164, lastError = eval("'['", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_165, lastError = self._apply(self.rule_token, "token", [_G_python_164])
            self.considerError(lastError)
            _G_apply_166, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_166
            _G_python_167, lastError = eval("']'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_168, lastError = self._apply(self.rule_token, "token", [_G_python_167])
            self.considerError(lastError)
            _G_python_169, lastError = eval('t.List(e)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_169, self.currentError)
        _G_or_170, lastError = self._or([_G_or_142, _G_or_144, _G_or_146, _G_or_148, _G_or_150, _G_or_152, _G_or_154, _G_or_156, _G_or_163])
        self.considerError(lastError)
        return (_G_or_170, self.currentError)


    def rule_expr2(self):
        _locals = {'self': self}
        self.locals['expr2'] = _locals
        def _G_or_171():
            _G_python_172, lastError = eval("'~'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_173, lastError = self._apply(self.rule_token, "token", [_G_python_172])
            self.considerError(lastError)
            def _G_or_174():
                _G_python_175, lastError = eval("'~'", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_176, lastError = self._apply(self.rule_token, "token", [_G_python_175])
                self.considerError(lastError)
                _G_apply_177, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_177
                _G_python_178, lastError = eval('t.Lookahead(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_178, self.currentError)
            def _G_or_179():
                _G_apply_180, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_180
                _G_python_181, lastError = eval('t.Not(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_181, self.currentError)
            _G_or_182, lastError = self._or([_G_or_174, _G_or_179])
            self.considerError(lastError)
            return (_G_or_182, self.currentError)
        def _G_or_183():
            _G_apply_184, lastError = self._apply(self.rule_expr1, "expr1", [])
            self.considerError(lastError)
            return (_G_apply_184, self.currentError)
        _G_or_185, lastError = self._or([_G_or_171, _G_or_183])
        self.considerError(lastError)
        return (_G_or_185, self.currentError)


    def rule_expr3(self):
        _locals = {'self': self}
        self.locals['expr3'] = _locals
        def _G_or_186():
            _G_apply_187, lastError = self._apply(self.rule_expr2, "expr2", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_187
            def _G_or_188():
                _G_exactly_189, lastError = self.exactly('*')
                self.considerError(lastError)
                _G_python_190, lastError = eval('t.Many(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_190, self.currentError)
            def _G_or_191():
                _G_exactly_192, lastError = self.exactly('+')
                self.considerError(lastError)
                _G_python_193, lastError = eval('t.Many1(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_193, self.currentError)
            def _G_or_194():
                _G_exactly_195, lastError = self.exactly('?')
                self.considerError(lastError)
                _G_python_196, lastError = eval('t.Optional(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_196, self.currentError)
            def _G_or_197():
                _G_python_198, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_198, self.currentError)
            _G_or_199, lastError = self._or([_G_or_188, _G_or_191, _G_or_194, _G_or_197])
            self.considerError(lastError)
            _locals['r'] = _G_or_199
            def _G_or_200():
                _G_exactly_201, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_202, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError)
                _locals['n'] = _G_apply_202
                _G_python_203, lastError = eval('t.Bind(n, r)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_203, self.currentError)
            def _G_or_204():
                _G_python_205, lastError = eval('r', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_205, self.currentError)
            _G_or_206, lastError = self._or([_G_or_200, _G_or_204])
            self.considerError(lastError)
            return (_G_or_206, self.currentError)
        def _G_or_207():
            _G_python_208, lastError = eval("':'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_209, lastError = self._apply(self.rule_token, "token", [_G_python_208])
            self.considerError(lastError)
            _G_apply_210, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_210
            _G_python_211, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_211, self.currentError)
        _G_or_212, lastError = self._or([_G_or_186, _G_or_207])
        self.considerError(lastError)
        return (_G_or_212, self.currentError)


    def rule_expr4(self):
        _locals = {'self': self}
        self.locals['expr4'] = _locals
        def _G_many_213():
            _G_apply_214, lastError = self._apply(self.rule_expr3, "expr3", [])
            self.considerError(lastError)
            return (_G_apply_214, self.currentError)
        _G_many_215, lastError = self.many(_G_many_213)
        self.considerError(lastError)
        _locals['es'] = _G_many_215
        _G_python_216, lastError = eval('t.And(es)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_216, self.currentError)


    def rule_expr(self):
        _locals = {'self': self}
        self.locals['expr'] = _locals
        _G_apply_217, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['e'] = _G_apply_217
        def _G_many_218():
            _G_python_219, lastError = eval("'|'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_220, lastError = self._apply(self.rule_token, "token", [_G_python_219])
            self.considerError(lastError)
            _G_apply_221, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError)
            return (_G_apply_221, self.currentError)
        _G_many_222, lastError = self.many(_G_many_218)
        self.considerError(lastError)
        _locals['es'] = _G_many_222
        _G_python_223, lastError = eval('t.Or([e] + es)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_223, self.currentError)


    def rule_ruleValue(self):
        _locals = {'self': self}
        self.locals['ruleValue'] = _locals
        _G_python_224, lastError = eval('"=>"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_225, lastError = self._apply(self.rule_token, "token", [_G_python_224])
        self.considerError(lastError)
        _G_python_226, lastError = eval('self.ruleValueExpr(False)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_226, self.currentError)


    def rule_semanticPredicate(self):
        _locals = {'self': self}
        self.locals['semanticPredicate'] = _locals
        _G_python_227, lastError = eval('"?("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_228, lastError = self._apply(self.rule_token, "token", [_G_python_227])
        self.considerError(lastError)
        _G_python_229, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_229, self.currentError)


    def rule_semanticAction(self):
        _locals = {'self': self}
        self.locals['semanticAction'] = _locals
        _G_python_230, lastError = eval('"!("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_231, lastError = self._apply(self.rule_token, "token", [_G_python_230])
        self.considerError(lastError)
        _G_python_232, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_232, self.currentError)


    def rule_ruleEnd(self):
        _locals = {'self': self}
        self.locals['ruleEnd'] = _locals
        def _G_or_233():
            def _G_many_234():
                _G_apply_235, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError)
                return (_G_apply_235, self.currentError)
            _G_many_236, lastError = self.many(_G_many_234)
            self.considerError(lastError)
            def _G_many1_237():
                _G_apply_238, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError)
                return (_G_apply_238, self.currentError)
            _G_many1_239, lastError = self.many(_G_many1_237, _G_many1_237())
            self.considerError(lastError)
            return (_G_many1_239, self.currentError)
        def _G_or_240():
            _G_apply_241, lastError = self._apply(self.rule_end, "end", [])
            self.considerError(lastError)
            return (_G_apply_241, self.currentError)
        _G_or_242, lastError = self._or([_G_or_233, _G_or_240])
        self.considerError(lastError)
        return (_G_or_242, self.currentError)


    def rule_rulePart(self):
        _locals = {'self': self}
        self.locals['rulePart'] = _locals
        _G_apply_243, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['requiredName'] = _G_apply_243
        _G_apply_244, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_apply_245, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['n'] = _G_apply_245
        def _G_pred_246():
            _G_python_247, lastError = eval('n == requiredName', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_247, self.currentError)
        _G_pred_248, lastError = self.pred(_G_pred_246)
        self.considerError(lastError)
        _G_python_249, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_250, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['args'] = _G_apply_250
        def _G_or_251():
            _G_python_252, lastError = eval('"::="', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_253, lastError = self._apply(self.rule_token, "token", [_G_python_252])
            self.considerError(lastError)
            _G_apply_254, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_254
            _G_apply_255, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
            self.considerError(lastError)
            _G_python_256, lastError = eval('t.And([args, e])', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_256, self.currentError)
        def _G_or_257():
            _G_apply_258, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
            self.considerError(lastError)
            _G_python_259, lastError = eval('args', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_259, self.currentError)
        _G_or_260, lastError = self._or([_G_or_251, _G_or_257])
        self.considerError(lastError)
        return (_G_or_260, self.currentError)


    def rule_rule(self):
        _locals = {'self': self}
        self.locals['rule'] = _locals
        _G_apply_261, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_lookahead_262():
            _G_apply_263, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_263
            return (_locals['n'], self.currentError)
        _G_lookahead_264, lastError = self.lookahead(_G_lookahead_262)
        self.considerError(lastError)
        _G_python_265, lastError = eval('n', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_266, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_265])
        self.considerError(lastError)
        _locals['r'] = _G_apply_266
        def _G_or_267():
            def _G_many1_268():
                _G_python_269, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_270, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_269])
                self.considerError(lastError)
                return (_G_apply_270, self.currentError)
            _G_many1_271, lastError = self.many(_G_many1_268, _G_many1_268())
            self.considerError(lastError)
            _locals['rs'] = _G_many1_271
            _G_python_272, lastError = eval('t.Rule(n, t.Or([r] + rs))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_272, self.currentError)
        def _G_or_273():
            _G_python_274, lastError = eval('t.Rule(n, r)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_274, self.currentError)
        _G_or_275, lastError = self._or([_G_or_267, _G_or_273])
        self.considerError(lastError)
        return (_G_or_275, self.currentError)


    def rule_grammar(self):
        _locals = {'self': self}
        self.locals['grammar'] = _locals
        def _G_many_276():
            _G_apply_277, lastError = self._apply(self.rule_rule, "rule", [])
            self.considerError(lastError)
            return (_G_apply_277, self.currentError)
        _G_many_278, lastError = self.many(_G_many_276)
        self.considerError(lastError)
        _locals['rs'] = _G_many_278
        _G_apply_279, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_python_280, lastError = eval('t.Grammar(self.name, rs)', self.globals, _locals), None
        self.considerError(lastError)
        _G_exactly_281, lastError = self.exactly('')
        self.considerError(lastError)
        _G_exactly_282, lastError = self.exactly('\n\nv2Grammar = r')
        self.considerError(lastError)
        _G_exactly_283, lastError = self.exactly('')
        self.considerError(lastError)
        return (_G_exactly_283, self.currentError)


    def rule_hspace(self):
        _locals = {'self': self}
        self.locals['hspace'] = _locals
        def _G_or_284():
            _G_exactly_285, lastError = self.exactly(' ')
            self.considerError(lastError)
            return (_G_exactly_285, self.currentError)
        def _G_or_286():
            _G_exactly_287, lastError = self.exactly('\t')
            self.considerError(lastError)
            return (_G_exactly_287, self.currentError)
        _G_or_288, lastError = self._or([_G_or_284, _G_or_286])
        self.considerError(lastError)
        return (_G_or_288, self.currentError)


    def rule_vspace(self):
        _locals = {'self': self}
        self.locals['vspace'] = _locals
        def _G_or_289():
            _G_python_290, lastError = eval('"\\r\\n"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_291, lastError = self._apply(self.rule_token, "token", [_G_python_290])
            self.considerError(lastError)
            return (_G_apply_291, self.currentError)
        def _G_or_292():
            _G_exactly_293, lastError = self.exactly('\r')
            self.considerError(lastError)
            return (_G_exactly_293, self.currentError)
        def _G_or_294():
            _G_exactly_295, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_295, self.currentError)
        _G_or_296, lastError = self._or([_G_or_289, _G_or_292, _G_or_294])
        self.considerError(lastError)
        return (_G_or_296, self.currentError)


    def rule_emptyline(self):
        _locals = {'self': self}
        self.locals['emptyline'] = _locals
        def _G_many_297():
            _G_apply_298, lastError = self._apply(self.rule_hspace, "hspace", [])
            self.considerError(lastError)
            return (_G_apply_298, self.currentError)
        _G_many_299, lastError = self.many(_G_many_297)
        self.considerError(lastError)
        _G_apply_300, lastError = self._apply(self.rule_vspace, "vspace", [])
        self.considerError(lastError)
        return (_G_apply_300, self.currentError)


    def rule_indentation(self):
        _locals = {'self': self}
        self.locals['indentation'] = _locals
        def _G_many_301():
            _G_apply_302, lastError = self._apply(self.rule_emptyline, "emptyline", [])
            self.considerError(lastError)
            return (_G_apply_302, self.currentError)
        _G_many_303, lastError = self.many(_G_many_301)
        self.considerError(lastError)
        def _G_many1_304():
            _G_apply_305, lastError = self._apply(self.rule_hspace, "hspace", [])
            self.considerError(lastError)
            return (_G_apply_305, self.currentError)
        _G_many1_306, lastError = self.many(_G_many1_304, _G_many1_304())
        self.considerError(lastError)
        return (_G_many1_306, self.currentError)


    def rule_noindentation(self):
        _locals = {'self': self}
        self.locals['noindentation'] = _locals
        def _G_many_307():
            _G_apply_308, lastError = self._apply(self.rule_emptyline, "emptyline", [])
            self.considerError(lastError)
            return (_G_apply_308, self.currentError)
        _G_many_309, lastError = self.many(_G_many_307)
        self.considerError(lastError)
        def _G_lookahead_310():
            def _G_not_311():
                _G_apply_312, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError)
                return (_G_apply_312, self.currentError)
            _G_not_313, lastError = self._not(_G_not_311)
            self.considerError(lastError)
            return (_G_not_313, self.currentError)
        _G_lookahead_314, lastError = self.lookahead(_G_lookahead_310)
        self.considerError(lastError)
        return (_G_lookahead_314, self.currentError)


    def rule_number(self):
        _locals = {'self': self}
        self.locals['number'] = _locals
        _G_apply_315, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_or_316():
            _G_exactly_317, lastError = self.exactly('-')
            self.considerError(lastError)
            _G_apply_318, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_318
            _G_python_319, lastError = eval('t.Exactly(-x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_319, self.currentError)
        def _G_or_320():
            _G_apply_321, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_321
            _G_python_322, lastError = eval('t.Exactly(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_322, self.currentError)
        _G_or_323, lastError = self._or([_G_or_316, _G_or_320])
        self.considerError(lastError)
        return (_G_or_323, self.currentError)


    def rule_barenumber(self):
        _locals = {'self': self}
        self.locals['barenumber'] = _locals
        def _G_or_324():
            _G_exactly_325, lastError = self.exactly('0')
            self.considerError(lastError)
            def _G_or_326():
                def _G_or_327():
                    _G_exactly_328, lastError = self.exactly('x')
                    self.considerError(lastError)
                    return (_G_exactly_328, self.currentError)
                def _G_or_329():
                    _G_exactly_330, lastError = self.exactly('X')
                    self.considerError(lastError)
                    return (_G_exactly_330, self.currentError)
                _G_or_331, lastError = self._or([_G_or_327, _G_or_329])
                self.considerError(lastError)
                def _G_consumedby_332():
                    def _G_many1_333():
                        _G_apply_334, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                        self.considerError(lastError)
                        return (_G_apply_334, self.currentError)
                    _G_many1_335, lastError = self.many(_G_many1_333, _G_many1_333())
                    self.considerError(lastError)
                    return (_G_many1_335, self.currentError)
                _G_consumedby_336, lastError = self.consumedby(_G_consumedby_332)
                self.considerError(lastError)
                _locals['hs'] = _G_consumedby_336
                _G_python_337, lastError = eval('int(hs, 16)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_337, self.currentError)
            def _G_or_338():
                def _G_consumedby_339():
                    def _G_many1_340():
                        _G_apply_341, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                        self.considerError(lastError)
                        return (_G_apply_341, self.currentError)
                    _G_many1_342, lastError = self.many(_G_many1_340, _G_many1_340())
                    self.considerError(lastError)
                    return (_G_many1_342, self.currentError)
                _G_consumedby_343, lastError = self.consumedby(_G_consumedby_339)
                self.considerError(lastError)
                _locals['ds'] = _G_consumedby_343
                _G_python_344, lastError = eval('int(ds, 8)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_344, self.currentError)
            _G_or_345, lastError = self._or([_G_or_326, _G_or_338])
            self.considerError(lastError)
            return (_G_or_345, self.currentError)
        def _G_or_346():
            def _G_consumedby_347():
                def _G_many1_348():
                    _G_apply_349, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError)
                    return (_G_apply_349, self.currentError)
                _G_many1_350, lastError = self.many(_G_many1_348, _G_many1_348())
                self.considerError(lastError)
                return (_G_many1_350, self.currentError)
            _G_consumedby_351, lastError = self.consumedby(_G_consumedby_347)
            self.considerError(lastError)
            _locals['ds'] = _G_consumedby_351
            _G_python_352, lastError = eval('int(ds)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_352, self.currentError)
        _G_or_353, lastError = self._or([_G_or_324, _G_or_346])
        self.considerError(lastError)
        return (_G_or_353, self.currentError)


    def rule_octaldigit(self):
        _locals = {'self': self}
        self.locals['octaldigit'] = _locals
        _G_apply_354, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_354
        def _G_pred_355():
            _G_python_356, lastError = eval("x in '01234567'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_356, self.currentError)
        _G_pred_357, lastError = self.pred(_G_pred_355)
        self.considerError(lastError)
        _G_python_358, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_358, self.currentError)


    def rule_hexdigit(self):
        _locals = {'self': self}
        self.locals['hexdigit'] = _locals
        _G_apply_359, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_359
        def _G_pred_360():
            _G_python_361, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_361, self.currentError)
        _G_pred_362, lastError = self.pred(_G_pred_360)
        self.considerError(lastError)
        _G_python_363, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_363, self.currentError)


    def rule_escapedChar(self):
        _locals = {'self': self}
        self.locals['escapedChar'] = _locals
        _G_exactly_364, lastError = self.exactly('\\')
        self.considerError(lastError)
        def _G_or_365():
            _G_exactly_366, lastError = self.exactly('n')
            self.considerError(lastError)
            _G_python_367, lastError = eval('"\\n"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_367, self.currentError)
        def _G_or_368():
            _G_exactly_369, lastError = self.exactly('r')
            self.considerError(lastError)
            _G_python_370, lastError = eval('"\\r"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_370, self.currentError)
        def _G_or_371():
            _G_exactly_372, lastError = self.exactly('t')
            self.considerError(lastError)
            _G_python_373, lastError = eval('"\\t"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_373, self.currentError)
        def _G_or_374():
            _G_exactly_375, lastError = self.exactly('b')
            self.considerError(lastError)
            _G_python_376, lastError = eval('"\\b"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_376, self.currentError)
        def _G_or_377():
            _G_exactly_378, lastError = self.exactly('f')
            self.considerError(lastError)
            _G_python_379, lastError = eval('"\\f"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_379, self.currentError)
        def _G_or_380():
            _G_exactly_381, lastError = self.exactly('"')
            self.considerError(lastError)
            _G_python_382, lastError = eval('\'"\'', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_382, self.currentError)
        def _G_or_383():
            _G_exactly_384, lastError = self.exactly("'")
            self.considerError(lastError)
            _G_python_385, lastError = eval('"\'"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_385, self.currentError)
        def _G_or_386():
            _G_exactly_387, lastError = self.exactly('\\')
            self.considerError(lastError)
            _G_python_388, lastError = eval('"\\\\"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_388, self.currentError)
        _G_or_389, lastError = self._or([_G_or_365, _G_or_368, _G_or_371, _G_or_374, _G_or_377, _G_or_380, _G_or_383, _G_or_386])
        self.considerError(lastError)
        return (_G_or_389, self.currentError)


    def rule_character(self):
        _locals = {'self': self}
        self.locals['character'] = _locals
        _G_python_390, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_391, lastError = self._apply(self.rule_token, "token", [_G_python_390])
        self.considerError(lastError)
        def _G_or_392():
            _G_apply_393, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
            self.considerError(lastError)
            return (_G_apply_393, self.currentError)
        def _G_or_394():
            _G_apply_395, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError)
            return (_G_apply_395, self.currentError)
        _G_or_396, lastError = self._or([_G_or_392, _G_or_394])
        self.considerError(lastError)
        _locals['c'] = _G_or_396
        _G_python_397, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_398, lastError = self._apply(self.rule_token, "token", [_G_python_397])
        self.considerError(lastError)
        _G_python_399, lastError = eval('t.Exactly(c)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_399, self.currentError)


    def rule_string(self):
        _locals = {'self': self}
        self.locals['string'] = _locals
        _G_python_400, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_401, lastError = self._apply(self.rule_token, "token", [_G_python_400])
        self.considerError(lastError)
        def _G_many_402():
            def _G_or_403():
                _G_apply_404, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                self.considerError(lastError)
                return (_G_apply_404, self.currentError)
            def _G_or_405():
                def _G_not_406():
                    _G_exactly_407, lastError = self.exactly('"')
                    self.considerError(lastError)
                    return (_G_exactly_407, self.currentError)
                _G_not_408, lastError = self._not(_G_not_406)
                self.considerError(lastError)
                _G_apply_409, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                return (_G_apply_409, self.currentError)
            _G_or_410, lastError = self._or([_G_or_403, _G_or_405])
            self.considerError(lastError)
            return (_G_or_410, self.currentError)
        _G_many_411, lastError = self.many(_G_many_402)
        self.considerError(lastError)
        _locals['c'] = _G_many_411
        _G_python_412, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_413, lastError = self._apply(self.rule_token, "token", [_G_python_412])
        self.considerError(lastError)
        _G_python_414, lastError = eval("t.Exactly(''.join(c))", self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_414, self.currentError)


    def rule_name(self):
        _locals = {'self': self}
        self.locals['name'] = _locals
        def _G_consumedby_415():
            _G_apply_416, lastError = self._apply(self.rule_letter, "letter", [])
            self.considerError(lastError)
            def _G_many_417():
                _G_apply_418, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                self.considerError(lastError)
                return (_G_apply_418, self.currentError)
            _G_many_419, lastError = self.many(_G_many_417)
            self.considerError(lastError)
            return (_G_many_419, self.currentError)
        _G_consumedby_420, lastError = self.consumedby(_G_consumedby_415)
        self.considerError(lastError)
        return (_G_consumedby_420, self.currentError)


    def rule_application(self):
        _locals = {'self': self}
        self.locals['application'] = _locals
        def _G_optional_421():
            _G_apply_422, lastError = self._apply(self.rule_indentation, "indentation", [])
            self.considerError(lastError)
            return (_G_apply_422, self.currentError)
        def _G_optional_423():
            return (None, self.input.nullError())
        _G_or_424, lastError = self._or([_G_optional_421, _G_optional_423])
        self.considerError(lastError)
        _G_apply_425, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['name'] = _G_apply_425
        def _G_or_426():
            _G_exactly_427, lastError = self.exactly('(')
            self.considerError(lastError)
            _G_python_428, lastError = eval("self.applicationArgs(finalChar=')')", self.globals, _locals), None
            self.considerError(lastError)
            _locals['args'] = _G_python_428
            _G_exactly_429, lastError = self.exactly(')')
            self.considerError(lastError)
            _G_python_430, lastError = eval('t.Apply(name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_430, self.currentError)
        def _G_or_431():
            _G_python_432, lastError = eval('t.Apply(name, self.rulename, [])', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_432, self.currentError)
        _G_or_433, lastError = self._or([_G_or_426, _G_or_431])
        self.considerError(lastError)
        return (_G_or_433, self.currentError)


    def rule_expr1(self):
        _locals = {'self': self}
        self.locals['expr1'] = _locals
        def _G_or_434():
            _G_apply_435, lastError = self._apply(self.rule_application, "application", [])
            self.considerError(lastError)
            return (_G_apply_435, self.currentError)
        def _G_or_436():
            _G_apply_437, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
            self.considerError(lastError)
            return (_G_apply_437, self.currentError)
        def _G_or_438():
            _G_apply_439, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
            self.considerError(lastError)
            return (_G_apply_439, self.currentError)
        def _G_or_440():
            _G_apply_441, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
            self.considerError(lastError)
            return (_G_apply_441, self.currentError)
        def _G_or_442():
            _G_apply_443, lastError = self._apply(self.rule_number, "number", [])
            self.considerError(lastError)
            return (_G_apply_443, self.currentError)
        def _G_or_444():
            _G_apply_445, lastError = self._apply(self.rule_character, "character", [])
            self.considerError(lastError)
            return (_G_apply_445, self.currentError)
        def _G_or_446():
            _G_apply_447, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            return (_G_apply_447, self.currentError)
        def _G_or_448():
            _G_python_449, lastError = eval("'('", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_450, lastError = self._apply(self.rule_token, "token", [_G_python_449])
            self.considerError(lastError)
            _G_apply_451, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_451
            _G_python_452, lastError = eval("')'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_453, lastError = self._apply(self.rule_token, "token", [_G_python_452])
            self.considerError(lastError)
            _G_python_454, lastError = eval('e', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_454, self.currentError)
        def _G_or_455():
            _G_python_456, lastError = eval("'<'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_457, lastError = self._apply(self.rule_token, "token", [_G_python_456])
            self.considerError(lastError)
            _G_apply_458, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_458
            _G_python_459, lastError = eval("'>'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_460, lastError = self._apply(self.rule_token, "token", [_G_python_459])
            self.considerError(lastError)
            _G_python_461, lastError = eval('t.ConsumedBy(e)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_461, self.currentError)
        def _G_or_462():
            _G_python_463, lastError = eval("'['", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_464, lastError = self._apply(self.rule_token, "token", [_G_python_463])
            self.considerError(lastError)
            _G_apply_465, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_465
            _G_python_466, lastError = eval("']'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_467, lastError = self._apply(self.rule_token, "token", [_G_python_466])
            self.considerError(lastError)
            _G_python_468, lastError = eval('t.List(e)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_468, self.currentError)
        _G_or_469, lastError = self._or([_G_or_434, _G_or_436, _G_or_438, _G_or_440, _G_or_442, _G_or_444, _G_or_446, _G_or_448, _G_or_455, _G_or_462])
        self.considerError(lastError)
        return (_G_or_469, self.currentError)


    def rule_expr2(self):
        _locals = {'self': self}
        self.locals['expr2'] = _locals
        def _G_or_470():
            _G_python_471, lastError = eval("'~'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_472, lastError = self._apply(self.rule_token, "token", [_G_python_471])
            self.considerError(lastError)
            def _G_or_473():
                _G_python_474, lastError = eval("'~'", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_475, lastError = self._apply(self.rule_token, "token", [_G_python_474])
                self.considerError(lastError)
                _G_apply_476, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_476
                _G_python_477, lastError = eval('t.Lookahead(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_477, self.currentError)
            def _G_or_478():
                _G_apply_479, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_479
                _G_python_480, lastError = eval('t.Not(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_480, self.currentError)
            _G_or_481, lastError = self._or([_G_or_473, _G_or_478])
            self.considerError(lastError)
            return (_G_or_481, self.currentError)
        def _G_or_482():
            _G_apply_483, lastError = self._apply(self.rule_expr1, "expr1", [])
            self.considerError(lastError)
            return (_G_apply_483, self.currentError)
        _G_or_484, lastError = self._or([_G_or_470, _G_or_482])
        self.considerError(lastError)
        return (_G_or_484, self.currentError)


    def rule_repeatTimes(self):
        _locals = {'self': self}
        self.locals['repeatTimes'] = _locals
        def _G_or_485():
            _G_apply_486, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_486
            _G_python_487, lastError = eval('int(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_487, self.currentError)
        def _G_or_488():
            _G_apply_489, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            return (_G_apply_489, self.currentError)
        _G_or_490, lastError = self._or([_G_or_485, _G_or_488])
        self.considerError(lastError)
        return (_G_or_490, self.currentError)


    def rule_expr3(self):
        _locals = {'self': self}
        self.locals['expr3'] = _locals
        def _G_or_491():
            _G_apply_492, lastError = self._apply(self.rule_expr2, "expr2", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_492
            def _G_or_493():
                _G_exactly_494, lastError = self.exactly('*')
                self.considerError(lastError)
                _G_python_495, lastError = eval('t.Many(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_495, self.currentError)
            def _G_or_496():
                _G_exactly_497, lastError = self.exactly('+')
                self.considerError(lastError)
                _G_python_498, lastError = eval('t.Many1(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_498, self.currentError)
            def _G_or_499():
                _G_exactly_500, lastError = self.exactly('?')
                self.considerError(lastError)
                _G_python_501, lastError = eval('t.Optional(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_501, self.currentError)
            def _G_or_502():
                _G_exactly_503, lastError = self.exactly('{')
                self.considerError(lastError)
                _G_apply_504, lastError = self._apply(self.rule_spaces, "spaces", [])
                self.considerError(lastError)
                _G_apply_505, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                self.considerError(lastError)
                _locals['start'] = _G_apply_505
                _G_apply_506, lastError = self._apply(self.rule_spaces, "spaces", [])
                self.considerError(lastError)
                def _G_or_507():
                    _G_exactly_508, lastError = self.exactly(',')
                    self.considerError(lastError)
                    _G_apply_509, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_apply_510, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                    self.considerError(lastError)
                    _locals['end'] = _G_apply_510
                    _G_apply_511, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_exactly_512, lastError = self.exactly('}')
                    self.considerError(lastError)
                    _G_python_513, lastError = eval('t.Repeat(start, end, e)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_513, self.currentError)
                def _G_or_514():
                    _G_apply_515, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_exactly_516, lastError = self.exactly('}')
                    self.considerError(lastError)
                    _G_python_517, lastError = eval('t.Repeat(start, start, e)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_517, self.currentError)
                _G_or_518, lastError = self._or([_G_or_507, _G_or_514])
                self.considerError(lastError)
                return (_G_or_518, self.currentError)
            def _G_or_519():
                _G_python_520, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_520, self.currentError)
            _G_or_521, lastError = self._or([_G_or_493, _G_or_496, _G_or_499, _G_or_502, _G_or_519])
            self.considerError(lastError)
            _locals['r'] = _G_or_521
            def _G_or_522():
                _G_exactly_523, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_524, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError)
                _locals['n'] = _G_apply_524
                _G_python_525, lastError = eval('t.Bind(n, r)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_525, self.currentError)
            def _G_or_526():
                _G_python_527, lastError = eval('r', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_527, self.currentError)
            _G_or_528, lastError = self._or([_G_or_522, _G_or_526])
            self.considerError(lastError)
            return (_G_or_528, self.currentError)
        def _G_or_529():
            _G_python_530, lastError = eval("':'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_531, lastError = self._apply(self.rule_token, "token", [_G_python_530])
            self.considerError(lastError)
            _G_apply_532, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_532
            _G_python_533, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_533, self.currentError)
        _G_or_534, lastError = self._or([_G_or_491, _G_or_529])
        self.considerError(lastError)
        return (_G_or_534, self.currentError)


    def rule_expr4(self):
        _locals = {'self': self}
        self.locals['expr4'] = _locals
        def _G_many_535():
            _G_apply_536, lastError = self._apply(self.rule_expr3, "expr3", [])
            self.considerError(lastError)
            return (_G_apply_536, self.currentError)
        _G_many_537, lastError = self.many(_G_many_535)
        self.considerError(lastError)
        _locals['es'] = _G_many_537
        _G_python_538, lastError = eval('t.And(es)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_538, self.currentError)


    def rule_expr(self):
        _locals = {'self': self}
        self.locals['expr'] = _locals
        _G_apply_539, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['e'] = _G_apply_539
        def _G_many_540():
            _G_python_541, lastError = eval("'|'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_542, lastError = self._apply(self.rule_token, "token", [_G_python_541])
            self.considerError(lastError)
            _G_apply_543, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError)
            return (_G_apply_543, self.currentError)
        _G_many_544, lastError = self.many(_G_many_540)
        self.considerError(lastError)
        _locals['es'] = _G_many_544
        _G_python_545, lastError = eval('t.Or([e] + es)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_545, self.currentError)


    def rule_ruleValue(self):
        _locals = {'self': self}
        self.locals['ruleValue'] = _locals
        _G_python_546, lastError = eval('"->"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_547, lastError = self._apply(self.rule_token, "token", [_G_python_546])
        self.considerError(lastError)
        _G_python_548, lastError = eval('self.ruleValueExpr(True)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_548, self.currentError)


    def rule_semanticPredicate(self):
        _locals = {'self': self}
        self.locals['semanticPredicate'] = _locals
        _G_python_549, lastError = eval('"?("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_550, lastError = self._apply(self.rule_token, "token", [_G_python_549])
        self.considerError(lastError)
        _G_python_551, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_551, self.currentError)


    def rule_semanticAction(self):
        _locals = {'self': self}
        self.locals['semanticAction'] = _locals
        _G_python_552, lastError = eval('"!("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_553, lastError = self._apply(self.rule_token, "token", [_G_python_552])
        self.considerError(lastError)
        _G_python_554, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_554, self.currentError)


    def rule_ruleEnd(self):
        _locals = {'self': self}
        self.locals['ruleEnd'] = _locals
        def _G_or_555():
            def _G_many_556():
                _G_apply_557, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError)
                return (_G_apply_557, self.currentError)
            _G_many_558, lastError = self.many(_G_many_556)
            self.considerError(lastError)
            def _G_many1_559():
                _G_apply_560, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError)
                return (_G_apply_560, self.currentError)
            _G_many1_561, lastError = self.many(_G_many1_559, _G_many1_559())
            self.considerError(lastError)
            return (_G_many1_561, self.currentError)
        def _G_or_562():
            _G_apply_563, lastError = self._apply(self.rule_end, "end", [])
            self.considerError(lastError)
            return (_G_apply_563, self.currentError)
        _G_or_564, lastError = self._or([_G_or_555, _G_or_562])
        self.considerError(lastError)
        return (_G_or_564, self.currentError)


    def rule_rulePart(self):
        _locals = {'self': self}
        self.locals['rulePart'] = _locals
        _G_apply_565, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['requiredName'] = _G_apply_565
        _G_apply_566, lastError = self._apply(self.rule_noindentation, "noindentation", [])
        self.considerError(lastError)
        _G_apply_567, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['n'] = _G_apply_567
        def _G_pred_568():
            _G_python_569, lastError = eval('n == requiredName', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_569, self.currentError)
        _G_pred_570, lastError = self.pred(_G_pred_568)
        self.considerError(lastError)
        _G_python_571, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_572, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['args'] = _G_apply_572
        def _G_or_573():
            _G_python_574, lastError = eval('"="', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_575, lastError = self._apply(self.rule_token, "token", [_G_python_574])
            self.considerError(lastError)
            _G_apply_576, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_576
            _G_apply_577, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
            self.considerError(lastError)
            _G_python_578, lastError = eval('t.And([args, e])', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_578, self.currentError)
        def _G_or_579():
            _G_apply_580, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
            self.considerError(lastError)
            _G_python_581, lastError = eval('args', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_581, self.currentError)
        _G_or_582, lastError = self._or([_G_or_573, _G_or_579])
        self.considerError(lastError)
        return (_G_or_582, self.currentError)


    def rule_rule(self):
        _locals = {'self': self}
        self.locals['rule'] = _locals
        _G_apply_583, lastError = self._apply(self.rule_noindentation, "noindentation", [])
        self.considerError(lastError)
        def _G_lookahead_584():
            _G_apply_585, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_585
            return (_locals['n'], self.currentError)
        _G_lookahead_586, lastError = self.lookahead(_G_lookahead_584)
        self.considerError(lastError)
        _G_python_587, lastError = eval('n', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_588, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_587])
        self.considerError(lastError)
        _locals['r'] = _G_apply_588
        def _G_or_589():
            def _G_many1_590():
                _G_python_591, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_592, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_591])
                self.considerError(lastError)
                return (_G_apply_592, self.currentError)
            _G_many1_593, lastError = self.many(_G_many1_590, _G_many1_590())
            self.considerError(lastError)
            _locals['rs'] = _G_many1_593
            _G_python_594, lastError = eval('t.Rule(n, t.Or([r] + rs))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_594, self.currentError)
        def _G_or_595():
            _G_python_596, lastError = eval('t.Rule(n, r)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_596, self.currentError)
        _G_or_597, lastError = self._or([_G_or_589, _G_or_595])
        self.considerError(lastError)
        return (_G_or_597, self.currentError)


    def rule_grammar(self):
        _locals = {'self': self}
        self.locals['grammar'] = _locals
        def _G_many_598():
            _G_apply_599, lastError = self._apply(self.rule_rule, "rule", [])
            self.considerError(lastError)
            return (_G_apply_599, self.currentError)
        _G_many_600, lastError = self.many(_G_many_598)
        self.considerError(lastError)
        _locals['rs'] = _G_many_600
        _G_apply_601, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_python_602, lastError = eval('t.Grammar(self.name, rs)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_602, self.currentError)
