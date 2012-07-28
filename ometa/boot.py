from ometa.runtime import OMetaGrammarBase as GrammarBase
from ometa.builder import termMaker as t

class BootOMetaGrammar(GrammarBase):
    def __init__(self, *a, **kw):
        super(BootOMetaGrammar, self).__init__(*a, **kw)
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
        _G_or_5, lastError = self._or([_G_or_1, _G_or_3])
        self.considerError(lastError)
        return (_G_or_5, self.currentError)


    def rule_vspace(self):
        _locals = {'self': self}
        self.locals['vspace'] = _locals
        def _G_or_6():
            _G_python_7, lastError = eval('"\\r\\n"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_8, lastError = self._apply(self.rule_token, "token", [_G_python_7])
            self.considerError(lastError)
            return (_G_apply_8, self.currentError)
        def _G_or_9():
            _G_exactly_10, lastError = self.exactly('\r')
            self.considerError(lastError)
            return (_G_exactly_10, self.currentError)
        def _G_or_11():
            _G_exactly_12, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_12, self.currentError)
        _G_or_13, lastError = self._or([_G_or_6, _G_or_9, _G_or_11])
        self.considerError(lastError)
        return (_G_or_13, self.currentError)


    def rule_emptyline(self):
        _locals = {'self': self}
        self.locals['emptyline'] = _locals
        def _G_many_14():
            _G_apply_15, lastError = self._apply(self.rule_hspace, "hspace", [])
            self.considerError(lastError)
            return (_G_apply_15, self.currentError)
        _G_many_16, lastError = self.many(_G_many_14)
        self.considerError(lastError)
        _G_apply_17, lastError = self._apply(self.rule_vspace, "vspace", [])
        self.considerError(lastError)
        return (_G_apply_17, self.currentError)


    def rule_indentation(self):
        _locals = {'self': self}
        self.locals['indentation'] = _locals
        def _G_many_18():
            _G_apply_19, lastError = self._apply(self.rule_emptyline, "emptyline", [])
            self.considerError(lastError)
            return (_G_apply_19, self.currentError)
        _G_many_20, lastError = self.many(_G_many_18)
        self.considerError(lastError)
        def _G_many1_21():
            _G_apply_22, lastError = self._apply(self.rule_hspace, "hspace", [])
            self.considerError(lastError)
            return (_G_apply_22, self.currentError)
        _G_many1_23, lastError = self.many(_G_many1_21, _G_many1_21())
        self.considerError(lastError)
        return (_G_many1_23, self.currentError)


    def rule_noindentation(self):
        _locals = {'self': self}
        self.locals['noindentation'] = _locals
        def _G_many_24():
            _G_apply_25, lastError = self._apply(self.rule_emptyline, "emptyline", [])
            self.considerError(lastError)
            return (_G_apply_25, self.currentError)
        _G_many_26, lastError = self.many(_G_many_24)
        self.considerError(lastError)
        def _G_lookahead_27():
            def _G_not_28():
                _G_apply_29, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError)
                return (_G_apply_29, self.currentError)
            _G_not_30, lastError = self._not(_G_not_28)
            self.considerError(lastError)
            return (_G_not_30, self.currentError)
        _G_lookahead_31, lastError = self.lookahead(_G_lookahead_27)
        self.considerError(lastError)
        return (_G_lookahead_31, self.currentError)


    def rule_number(self):
        _locals = {'self': self}
        self.locals['number'] = _locals
        _G_apply_32, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        def _G_or_33():
            _G_exactly_34, lastError = self.exactly('-')
            self.considerError(lastError)
            _G_apply_35, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_35
            _G_python_36, lastError = eval('t.Exactly(-x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_36, self.currentError)
        def _G_or_37():
            _G_apply_38, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_38
            _G_python_39, lastError = eval('t.Exactly(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_39, self.currentError)
        _G_or_40, lastError = self._or([_G_or_33, _G_or_37])
        self.considerError(lastError)
        return (_G_or_40, self.currentError)


    def rule_barenumber(self):
        _locals = {'self': self}
        self.locals['barenumber'] = _locals
        def _G_or_41():
            _G_exactly_42, lastError = self.exactly('0')
            self.considerError(lastError)
            def _G_or_43():
                def _G_or_44():
                    _G_exactly_45, lastError = self.exactly('x')
                    self.considerError(lastError)
                    return (_G_exactly_45, self.currentError)
                def _G_or_46():
                    _G_exactly_47, lastError = self.exactly('X')
                    self.considerError(lastError)
                    return (_G_exactly_47, self.currentError)
                _G_or_48, lastError = self._or([_G_or_44, _G_or_46])
                self.considerError(lastError)
                def _G_consumedby_49():
                    def _G_many1_50():
                        _G_apply_51, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                        self.considerError(lastError)
                        return (_G_apply_51, self.currentError)
                    _G_many1_52, lastError = self.many(_G_many1_50, _G_many1_50())
                    self.considerError(lastError)
                    return (_G_many1_52, self.currentError)
                _G_consumedby_53, lastError = self.consumedby(_G_consumedby_49)
                self.considerError(lastError)
                _locals['hs'] = _G_consumedby_53
                _G_python_54, lastError = eval('int(hs, 16)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_54, self.currentError)
            def _G_or_55():
                def _G_consumedby_56():
                    def _G_many1_57():
                        _G_apply_58, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                        self.considerError(lastError)
                        return (_G_apply_58, self.currentError)
                    _G_many1_59, lastError = self.many(_G_many1_57, _G_many1_57())
                    self.considerError(lastError)
                    return (_G_many1_59, self.currentError)
                _G_consumedby_60, lastError = self.consumedby(_G_consumedby_56)
                self.considerError(lastError)
                _locals['ds'] = _G_consumedby_60
                _G_python_61, lastError = eval('int(ds, 8)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_61, self.currentError)
            _G_or_62, lastError = self._or([_G_or_43, _G_or_55])
            self.considerError(lastError)
            return (_G_or_62, self.currentError)
        def _G_or_63():
            def _G_consumedby_64():
                def _G_many1_65():
                    _G_apply_66, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError)
                    return (_G_apply_66, self.currentError)
                _G_many1_67, lastError = self.many(_G_many1_65, _G_many1_65())
                self.considerError(lastError)
                return (_G_many1_67, self.currentError)
            _G_consumedby_68, lastError = self.consumedby(_G_consumedby_64)
            self.considerError(lastError)
            _locals['ds'] = _G_consumedby_68
            _G_python_69, lastError = eval('int(ds)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_69, self.currentError)
        _G_or_70, lastError = self._or([_G_or_41, _G_or_63])
        self.considerError(lastError)
        return (_G_or_70, self.currentError)


    def rule_octaldigit(self):
        _locals = {'self': self}
        self.locals['octaldigit'] = _locals
        _G_apply_71, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_71
        def _G_pred_72():
            _G_python_73, lastError = eval("x in '01234567'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_73, self.currentError)
        _G_pred_74, lastError = self.pred(_G_pred_72)
        self.considerError(lastError)
        _G_python_75, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_75, self.currentError)


    def rule_hexdigit(self):
        _locals = {'self': self}
        self.locals['hexdigit'] = _locals
        _G_apply_76, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_76
        def _G_pred_77():
            _G_python_78, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_78, self.currentError)
        _G_pred_79, lastError = self.pred(_G_pred_77)
        self.considerError(lastError)
        _G_python_80, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_80, self.currentError)


    def rule_escapedChar(self):
        _locals = {'self': self}
        self.locals['escapedChar'] = _locals
        _G_exactly_81, lastError = self.exactly('\\')
        self.considerError(lastError)
        def _G_or_82():
            _G_exactly_83, lastError = self.exactly('n')
            self.considerError(lastError)
            _G_python_84, lastError = eval('"\\n"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_84, self.currentError)
        def _G_or_85():
            _G_exactly_86, lastError = self.exactly('r')
            self.considerError(lastError)
            _G_python_87, lastError = eval('"\\r"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_87, self.currentError)
        def _G_or_88():
            _G_exactly_89, lastError = self.exactly('t')
            self.considerError(lastError)
            _G_python_90, lastError = eval('"\\t"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_90, self.currentError)
        def _G_or_91():
            _G_exactly_92, lastError = self.exactly('b')
            self.considerError(lastError)
            _G_python_93, lastError = eval('"\\b"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_93, self.currentError)
        def _G_or_94():
            _G_exactly_95, lastError = self.exactly('f')
            self.considerError(lastError)
            _G_python_96, lastError = eval('"\\f"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_96, self.currentError)
        def _G_or_97():
            _G_exactly_98, lastError = self.exactly('"')
            self.considerError(lastError)
            _G_python_99, lastError = eval('\'"\'', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_99, self.currentError)
        def _G_or_100():
            _G_exactly_101, lastError = self.exactly("'")
            self.considerError(lastError)
            _G_python_102, lastError = eval('"\'"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_102, self.currentError)
        def _G_or_103():
            _G_exactly_104, lastError = self.exactly('\\')
            self.considerError(lastError)
            _G_python_105, lastError = eval('"\\\\"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_105, self.currentError)
        _G_or_106, lastError = self._or([_G_or_82, _G_or_85, _G_or_88, _G_or_91, _G_or_94, _G_or_97, _G_or_100, _G_or_103])
        self.considerError(lastError)
        return (_G_or_106, self.currentError)


    def rule_character(self):
        _locals = {'self': self}
        self.locals['character'] = _locals
        _G_python_107, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_108, lastError = self._apply(self.rule_token, "token", [_G_python_107])
        self.considerError(lastError)
        def _G_or_109():
            _G_apply_110, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
            self.considerError(lastError)
            return (_G_apply_110, self.currentError)
        def _G_or_111():
            _G_apply_112, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError)
            return (_G_apply_112, self.currentError)
        _G_or_113, lastError = self._or([_G_or_109, _G_or_111])
        self.considerError(lastError)
        _locals['c'] = _G_or_113
        _G_python_114, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_115, lastError = self._apply(self.rule_token, "token", [_G_python_114])
        self.considerError(lastError)
        _G_python_116, lastError = eval('t.Exactly(c)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_116, self.currentError)


    def rule_string(self):
        _locals = {'self': self}
        self.locals['string'] = _locals
        _G_python_117, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_118, lastError = self._apply(self.rule_token, "token", [_G_python_117])
        self.considerError(lastError)
        def _G_many_119():
            def _G_or_120():
                _G_apply_121, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                self.considerError(lastError)
                return (_G_apply_121, self.currentError)
            def _G_or_122():
                def _G_not_123():
                    _G_exactly_124, lastError = self.exactly('"')
                    self.considerError(lastError)
                    return (_G_exactly_124, self.currentError)
                _G_not_125, lastError = self._not(_G_not_123)
                self.considerError(lastError)
                _G_apply_126, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                return (_G_apply_126, self.currentError)
            _G_or_127, lastError = self._or([_G_or_120, _G_or_122])
            self.considerError(lastError)
            return (_G_or_127, self.currentError)
        _G_many_128, lastError = self.many(_G_many_119)
        self.considerError(lastError)
        _locals['c'] = _G_many_128
        _G_python_129, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_130, lastError = self._apply(self.rule_token, "token", [_G_python_129])
        self.considerError(lastError)
        _G_python_131, lastError = eval("t.Exactly(''.join(c))", self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_131, self.currentError)


    def rule_name(self):
        _locals = {'self': self}
        self.locals['name'] = _locals
        def _G_consumedby_132():
            _G_apply_133, lastError = self._apply(self.rule_letter, "letter", [])
            self.considerError(lastError)
            def _G_many_134():
                _G_apply_135, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                self.considerError(lastError)
                return (_G_apply_135, self.currentError)
            _G_many_136, lastError = self.many(_G_many_134)
            self.considerError(lastError)
            return (_G_many_136, self.currentError)
        _G_consumedby_137, lastError = self.consumedby(_G_consumedby_132)
        self.considerError(lastError)
        return (_G_consumedby_137, self.currentError)


    def rule_application(self):
        _locals = {'self': self}
        self.locals['application'] = _locals
        def _G_optional_138():
            _G_apply_139, lastError = self._apply(self.rule_indentation, "indentation", [])
            self.considerError(lastError)
            return (_G_apply_139, self.currentError)
        def _G_optional_140():
            return (None, self.input.nullError())
        _G_or_141, lastError = self._or([_G_optional_138, _G_optional_140])
        self.considerError(lastError)
        _G_apply_142, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['name'] = _G_apply_142
        def _G_or_143():
            _G_exactly_144, lastError = self.exactly('(')
            self.considerError(lastError)
            _G_python_145, lastError = eval("self.applicationArgs(finalChar=')')", self.globals, _locals), None
            self.considerError(lastError)
            _locals['args'] = _G_python_145
            _G_exactly_146, lastError = self.exactly(')')
            self.considerError(lastError)
            _G_python_147, lastError = eval('t.Apply(name, self.rulename, args)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_147, self.currentError)
        def _G_or_148():
            _G_python_149, lastError = eval('t.Apply(name, self.rulename, [])', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_149, self.currentError)
        _G_or_150, lastError = self._or([_G_or_143, _G_or_148])
        self.considerError(lastError)
        return (_G_or_150, self.currentError)


    def rule_expr1(self):
        _locals = {'self': self}
        self.locals['expr1'] = _locals
        def _G_or_151():
            _G_apply_152, lastError = self._apply(self.rule_application, "application", [])
            self.considerError(lastError)
            return (_G_apply_152, self.currentError)
        def _G_or_153():
            _G_apply_154, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
            self.considerError(lastError)
            return (_G_apply_154, self.currentError)
        def _G_or_155():
            _G_apply_156, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
            self.considerError(lastError)
            return (_G_apply_156, self.currentError)
        def _G_or_157():
            _G_apply_158, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
            self.considerError(lastError)
            return (_G_apply_158, self.currentError)
        def _G_or_159():
            _G_apply_160, lastError = self._apply(self.rule_number, "number", [])
            self.considerError(lastError)
            return (_G_apply_160, self.currentError)
        def _G_or_161():
            _G_apply_162, lastError = self._apply(self.rule_character, "character", [])
            self.considerError(lastError)
            return (_G_apply_162, self.currentError)
        def _G_or_163():
            _G_apply_164, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            return (_G_apply_164, self.currentError)
        def _G_or_165():
            _G_python_166, lastError = eval("'('", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_167, lastError = self._apply(self.rule_token, "token", [_G_python_166])
            self.considerError(lastError)
            _G_apply_168, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_168
            _G_python_169, lastError = eval("')'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_170, lastError = self._apply(self.rule_token, "token", [_G_python_169])
            self.considerError(lastError)
            _G_python_171, lastError = eval('e', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_171, self.currentError)
        def _G_or_172():
            _G_python_173, lastError = eval("'<'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_174, lastError = self._apply(self.rule_token, "token", [_G_python_173])
            self.considerError(lastError)
            _G_apply_175, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_175
            _G_python_176, lastError = eval("'>'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_177, lastError = self._apply(self.rule_token, "token", [_G_python_176])
            self.considerError(lastError)
            _G_python_178, lastError = eval('t.ConsumedBy(e)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_178, self.currentError)
        def _G_or_179():
            _G_python_180, lastError = eval("'['", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_181, lastError = self._apply(self.rule_token, "token", [_G_python_180])
            self.considerError(lastError)
            _G_apply_182, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_182
            _G_python_183, lastError = eval("']'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_184, lastError = self._apply(self.rule_token, "token", [_G_python_183])
            self.considerError(lastError)
            _G_python_185, lastError = eval('t.List(e)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_185, self.currentError)
        _G_or_186, lastError = self._or([_G_or_151, _G_or_153, _G_or_155, _G_or_157, _G_or_159, _G_or_161, _G_or_163, _G_or_165, _G_or_172, _G_or_179])
        self.considerError(lastError)
        return (_G_or_186, self.currentError)


    def rule_expr2(self):
        _locals = {'self': self}
        self.locals['expr2'] = _locals
        def _G_or_187():
            _G_python_188, lastError = eval("'~'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_189, lastError = self._apply(self.rule_token, "token", [_G_python_188])
            self.considerError(lastError)
            def _G_or_190():
                _G_python_191, lastError = eval("'~'", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_192, lastError = self._apply(self.rule_token, "token", [_G_python_191])
                self.considerError(lastError)
                _G_apply_193, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_193
                _G_python_194, lastError = eval('t.Lookahead(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_194, self.currentError)
            def _G_or_195():
                _G_apply_196, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_196
                _G_python_197, lastError = eval('t.Not(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_197, self.currentError)
            _G_or_198, lastError = self._or([_G_or_190, _G_or_195])
            self.considerError(lastError)
            return (_G_or_198, self.currentError)
        def _G_or_199():
            _G_apply_200, lastError = self._apply(self.rule_expr1, "expr1", [])
            self.considerError(lastError)
            return (_G_apply_200, self.currentError)
        _G_or_201, lastError = self._or([_G_or_187, _G_or_199])
        self.considerError(lastError)
        return (_G_or_201, self.currentError)


    def rule_expr3(self):
        _locals = {'self': self}
        self.locals['expr3'] = _locals
        def _G_or_202():
            _G_apply_203, lastError = self._apply(self.rule_expr2, "expr2", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_203
            def _G_or_204():
                _G_exactly_205, lastError = self.exactly('*')
                self.considerError(lastError)
                _G_python_206, lastError = eval('t.Many(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_206, self.currentError)
            def _G_or_207():
                _G_exactly_208, lastError = self.exactly('+')
                self.considerError(lastError)
                _G_python_209, lastError = eval('t.Many1(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_209, self.currentError)
            def _G_or_210():
                _G_exactly_211, lastError = self.exactly('?')
                self.considerError(lastError)
                _G_python_212, lastError = eval('t.Optional(e)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_212, self.currentError)
            def _G_or_213():
                _G_exactly_214, lastError = self.exactly('{')
                self.considerError(lastError)
                _G_apply_215, lastError = self._apply(self.rule_spaces, "spaces", [])
                self.considerError(lastError)
                _G_apply_216, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                self.considerError(lastError)
                _locals['start'] = _G_apply_216
                _G_apply_217, lastError = self._apply(self.rule_spaces, "spaces", [])
                self.considerError(lastError)
                def _G_or_218():
                    _G_exactly_219, lastError = self.exactly(',')
                    self.considerError(lastError)
                    _G_apply_220, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_apply_221, lastError = self._apply(self.rule_barenumber, "barenumber", [])
                    self.considerError(lastError)
                    _locals['end'] = _G_apply_221
                    _G_apply_222, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_exactly_223, lastError = self.exactly('}')
                    self.considerError(lastError)
                    _G_python_224, lastError = eval('t.Repeat(start, end, e)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_224, self.currentError)
                def _G_or_225():
                    _G_apply_226, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_exactly_227, lastError = self.exactly('}')
                    self.considerError(lastError)
                    _G_python_228, lastError = eval('t.Repeat(start, start, e)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_228, self.currentError)
                _G_or_229, lastError = self._or([_G_or_218, _G_or_225])
                self.considerError(lastError)
                return (_G_or_229, self.currentError)
            def _G_or_230():
                _G_python_231, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_231, self.currentError)
            _G_or_232, lastError = self._or([_G_or_204, _G_or_207, _G_or_210, _G_or_213, _G_or_230])
            self.considerError(lastError)
            _locals['r'] = _G_or_232
            def _G_or_233():
                _G_exactly_234, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_235, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError)
                _locals['n'] = _G_apply_235
                _G_python_236, lastError = eval('t.Bind(n, r)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_236, self.currentError)
            def _G_or_237():
                _G_python_238, lastError = eval('r', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_238, self.currentError)
            _G_or_239, lastError = self._or([_G_or_233, _G_or_237])
            self.considerError(lastError)
            return (_G_or_239, self.currentError)
        def _G_or_240():
            _G_python_241, lastError = eval("':'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_242, lastError = self._apply(self.rule_token, "token", [_G_python_241])
            self.considerError(lastError)
            _G_apply_243, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_243
            _G_python_244, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_244, self.currentError)
        _G_or_245, lastError = self._or([_G_or_202, _G_or_240])
        self.considerError(lastError)
        return (_G_or_245, self.currentError)


    def rule_expr4(self):
        _locals = {'self': self}
        self.locals['expr4'] = _locals
        def _G_many_246():
            _G_apply_247, lastError = self._apply(self.rule_expr3, "expr3", [])
            self.considerError(lastError)
            return (_G_apply_247, self.currentError)
        _G_many_248, lastError = self.many(_G_many_246)
        self.considerError(lastError)
        _locals['es'] = _G_many_248
        _G_python_249, lastError = eval('t.And(es)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_249, self.currentError)


    def rule_expr(self):
        _locals = {'self': self}
        self.locals['expr'] = _locals
        _G_apply_250, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['e'] = _G_apply_250
        def _G_many_251():
            _G_python_252, lastError = eval("'|'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_253, lastError = self._apply(self.rule_token, "token", [_G_python_252])
            self.considerError(lastError)
            _G_apply_254, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError)
            return (_G_apply_254, self.currentError)
        _G_many_255, lastError = self.many(_G_many_251)
        self.considerError(lastError)
        _locals['es'] = _G_many_255
        _G_python_256, lastError = eval('t.Or([e] + es)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_256, self.currentError)


    def rule_ruleValue(self):
        _locals = {'self': self}
        self.locals['ruleValue'] = _locals
        _G_python_257, lastError = eval('"->"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_258, lastError = self._apply(self.rule_token, "token", [_G_python_257])
        self.considerError(lastError)
        _G_python_259, lastError = eval('self.ruleValueExpr(True)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_259, self.currentError)


    def rule_semanticPredicate(self):
        _locals = {'self': self}
        self.locals['semanticPredicate'] = _locals
        _G_python_260, lastError = eval('"?("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_261, lastError = self._apply(self.rule_token, "token", [_G_python_260])
        self.considerError(lastError)
        _G_python_262, lastError = eval('self.semanticPredicateExpr()', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_262, self.currentError)


    def rule_semanticAction(self):
        _locals = {'self': self}
        self.locals['semanticAction'] = _locals
        _G_python_263, lastError = eval('"!("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_264, lastError = self._apply(self.rule_token, "token", [_G_python_263])
        self.considerError(lastError)
        _G_python_265, lastError = eval('self.semanticActionExpr()', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_265, self.currentError)


    def rule_ruleEnd(self):
        _locals = {'self': self}
        self.locals['ruleEnd'] = _locals
        def _G_or_266():
            def _G_many_267():
                _G_apply_268, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError)
                return (_G_apply_268, self.currentError)
            _G_many_269, lastError = self.many(_G_many_267)
            self.considerError(lastError)
            def _G_many1_270():
                _G_apply_271, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError)
                return (_G_apply_271, self.currentError)
            _G_many1_272, lastError = self.many(_G_many1_270, _G_many1_270())
            self.considerError(lastError)
            return (_G_many1_272, self.currentError)
        def _G_or_273():
            _G_apply_274, lastError = self._apply(self.rule_end, "end", [])
            self.considerError(lastError)
            return (_G_apply_274, self.currentError)
        _G_or_275, lastError = self._or([_G_or_266, _G_or_273])
        self.considerError(lastError)
        return (_G_or_275, self.currentError)


    def rule_rulePart(self):
        _locals = {'self': self}
        self.locals['rulePart'] = _locals
        _G_apply_276, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['requiredName'] = _G_apply_276
        _G_apply_277, lastError = self._apply(self.rule_noindentation, "noindentation", [])
        self.considerError(lastError)
        _G_apply_278, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['n'] = _G_apply_278
        def _G_pred_279():
            _G_python_280, lastError = eval('n == requiredName', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_280, self.currentError)
        _G_pred_281, lastError = self.pred(_G_pred_279)
        self.considerError(lastError)
        _G_python_282, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_283, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['args'] = _G_apply_283
        def _G_or_284():
            _G_python_285, lastError = eval('"="', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_286, lastError = self._apply(self.rule_token, "token", [_G_python_285])
            self.considerError(lastError)
            _G_apply_287, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_287
            _G_apply_288, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
            self.considerError(lastError)
            _G_python_289, lastError = eval('t.And([args, e])', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_289, self.currentError)
        def _G_or_290():
            _G_apply_291, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
            self.considerError(lastError)
            _G_python_292, lastError = eval('args', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_292, self.currentError)
        _G_or_293, lastError = self._or([_G_or_284, _G_or_290])
        self.considerError(lastError)
        return (_G_or_293, self.currentError)


    def rule_rule(self):
        _locals = {'self': self}
        self.locals['rule'] = _locals
        _G_apply_294, lastError = self._apply(self.rule_noindentation, "noindentation", [])
        self.considerError(lastError)
        def _G_lookahead_295():
            _G_apply_296, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_296
            return (_locals['n'], self.currentError)
        _G_lookahead_297, lastError = self.lookahead(_G_lookahead_295)
        self.considerError(lastError)
        _G_python_298, lastError = eval('n', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_299, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_298])
        self.considerError(lastError)
        _locals['r'] = _G_apply_299
        def _G_or_300():
            def _G_many1_301():
                _G_python_302, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_303, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_302])
                self.considerError(lastError)
                return (_G_apply_303, self.currentError)
            _G_many1_304, lastError = self.many(_G_many1_301, _G_many1_301())
            self.considerError(lastError)
            _locals['rs'] = _G_many1_304
            _G_python_305, lastError = eval('t.Rule(n, t.Or([r] + rs))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_305, self.currentError)
        def _G_or_306():
            _G_python_307, lastError = eval('t.Rule(n, r)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_307, self.currentError)
        _G_or_308, lastError = self._or([_G_or_300, _G_or_306])
        self.considerError(lastError)
        return (_G_or_308, self.currentError)


    def rule_grammar(self):
        _locals = {'self': self}
        self.locals['grammar'] = _locals
        def _G_many_309():
            _G_apply_310, lastError = self._apply(self.rule_rule, "rule", [])
            self.considerError(lastError)
            return (_G_apply_310, self.currentError)
        _G_many_311, lastError = self.many(_G_many_309)
        self.considerError(lastError)
        _locals['rs'] = _G_many_311
        _G_apply_312, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_python_313, lastError = eval('t.Grammar(self.name, rs)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_313, self.currentError)
