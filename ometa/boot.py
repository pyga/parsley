from ometa.runtime import OMetaGrammarBase as GrammarBase
from terml.nodes import termMaker as t

class BootOMetaGrammar(GrammarBase):
    def __init__(self, *a, **kw):
        GrammarBase.__init__(self, *a, **kw)
        self.globals['t'] = t

    def rule_comment(self):
        _locals = {'self': self}
        self.locals['comment'] = _locals
        _G_exactly_1, lastError = self.exactly('#')
        self.considerError(lastError)
        def _G_many_2():
            def _G_not_3():
                _G_exactly_4, lastError = self.exactly('\n')
                self.considerError(lastError)
                return (_G_exactly_4, self.currentError)
            _G_not_5, lastError = self._not(_G_not_3)
            self.considerError(lastError)
            _G_apply_6, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError)
            return (_G_apply_6, self.currentError)
        _G_many_7, lastError = self.many(_G_many_2)
        self.considerError(lastError)
        return (_G_many_7, self.currentError)


    def rule_hspace(self):
        _locals = {'self': self}
        self.locals['hspace'] = _locals
        def _G_or_8():
            _G_exactly_9, lastError = self.exactly(' ')
            self.considerError(lastError)
            return (_G_exactly_9, self.currentError)
        def _G_or_10():
            _G_exactly_11, lastError = self.exactly('\t')
            self.considerError(lastError)
            return (_G_exactly_11, self.currentError)
        def _G_or_12():
            _G_apply_13, lastError = self._apply(self.rule_comment, "comment", [])
            self.considerError(lastError)
            return (_G_apply_13, self.currentError)
        _G_or_14, lastError = self._or([_G_or_8, _G_or_10, _G_or_12])
        self.considerError(lastError)
        return (_G_or_14, self.currentError)


    def rule_vspace(self):
        _locals = {'self': self}
        self.locals['vspace'] = _locals
        def _G_or_15():
            _G_python_16, lastError = eval('"\\r\\n"', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_17, lastError = self._apply(self.rule_token, "token", [_G_python_16])
            self.considerError(lastError)
            return (_G_apply_17, self.currentError)
        def _G_or_18():
            _G_exactly_19, lastError = self.exactly('\r')
            self.considerError(lastError)
            return (_G_exactly_19, self.currentError)
        def _G_or_20():
            _G_exactly_21, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_21, self.currentError)
        _G_or_22, lastError = self._or([_G_or_15, _G_or_18, _G_or_20])
        self.considerError(lastError)
        return (_G_or_22, self.currentError)


    def rule_emptyline(self):
        _locals = {'self': self}
        self.locals['emptyline'] = _locals
        def _G_many_23():
            _G_apply_24, lastError = self._apply(self.rule_hspace, "hspace", [])
            self.considerError(lastError)
            return (_G_apply_24, self.currentError)
        _G_many_25, lastError = self.many(_G_many_23)
        self.considerError(lastError)
        _G_apply_26, lastError = self._apply(self.rule_vspace, "vspace", [])
        self.considerError(lastError)
        return (_G_apply_26, self.currentError)


    def rule_indentation(self):
        _locals = {'self': self}
        self.locals['indentation'] = _locals
        def _G_many_27():
            _G_apply_28, lastError = self._apply(self.rule_emptyline, "emptyline", [])
            self.considerError(lastError)
            return (_G_apply_28, self.currentError)
        _G_many_29, lastError = self.many(_G_many_27)
        self.considerError(lastError)
        def _G_many1_30():
            _G_apply_31, lastError = self._apply(self.rule_hspace, "hspace", [])
            self.considerError(lastError)
            return (_G_apply_31, self.currentError)
        _G_many1_32, lastError = self.many(_G_many1_30, _G_many1_30())
        self.considerError(lastError)
        return (_G_many1_32, self.currentError)


    def rule_noindentation(self):
        _locals = {'self': self}
        self.locals['noindentation'] = _locals
        def _G_many_33():
            _G_apply_34, lastError = self._apply(self.rule_emptyline, "emptyline", [])
            self.considerError(lastError)
            return (_G_apply_34, self.currentError)
        _G_many_35, lastError = self.many(_G_many_33)
        self.considerError(lastError)
        def _G_lookahead_36():
            def _G_not_37():
                _G_apply_38, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError)
                return (_G_apply_38, self.currentError)
            _G_not_39, lastError = self._not(_G_not_37)
            self.considerError(lastError)
            return (_G_not_39, self.currentError)
        _G_lookahead_40, lastError = self.lookahead(_G_lookahead_36)
        self.considerError(lastError)
        return (_G_lookahead_40, self.currentError)


    def rule_number(self):
        _locals = {'self': self}
        self.locals['number'] = _locals
        _G_apply_41, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_python_42, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_42
        def _G_or_43():
            _G_exactly_44, lastError = self.exactly('-')
            self.considerError(lastError)
            _G_apply_45, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_45
            _G_python_46, lastError = eval('t.Exactly(-x, span=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_46, self.currentError)
        def _G_or_47():
            _G_apply_48, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_48
            _G_python_49, lastError = eval('t.Exactly(x, span=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_49, self.currentError)
        _G_or_50, lastError = self._or([_G_or_43, _G_or_47])
        self.considerError(lastError)
        return (_G_or_50, self.currentError)


    def rule_barenumber(self):
        _locals = {'self': self}
        self.locals['barenumber'] = _locals
        def _G_or_51():
            _G_exactly_52, lastError = self.exactly('0')
            self.considerError(lastError)
            def _G_or_53():
                def _G_or_54():
                    _G_exactly_55, lastError = self.exactly('x')
                    self.considerError(lastError)
                    return (_G_exactly_55, self.currentError)
                def _G_or_56():
                    _G_exactly_57, lastError = self.exactly('X')
                    self.considerError(lastError)
                    return (_G_exactly_57, self.currentError)
                _G_or_58, lastError = self._or([_G_or_54, _G_or_56])
                self.considerError(lastError)
                def _G_consumedby_59():
                    def _G_many1_60():
                        _G_apply_61, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                        self.considerError(lastError)
                        return (_G_apply_61, self.currentError)
                    _G_many1_62, lastError = self.many(_G_many1_60, _G_many1_60())
                    self.considerError(lastError)
                    return (_G_many1_62, self.currentError)
                _G_consumedby_63, lastError = self.consumedby(_G_consumedby_59)
                self.considerError(lastError)
                _locals['hs'] = _G_consumedby_63
                _G_python_64, lastError = eval('int(hs, 16)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_64, self.currentError)
            def _G_or_65():
                def _G_consumedby_66():
                    def _G_many1_67():
                        _G_apply_68, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                        self.considerError(lastError)
                        return (_G_apply_68, self.currentError)
                    _G_many1_69, lastError = self.many(_G_many1_67, _G_many1_67())
                    self.considerError(lastError)
                    return (_G_many1_69, self.currentError)
                _G_consumedby_70, lastError = self.consumedby(_G_consumedby_66)
                self.considerError(lastError)
                _locals['ds'] = _G_consumedby_70
                _G_python_71, lastError = eval('int(ds, 8)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_71, self.currentError)
            _G_or_72, lastError = self._or([_G_or_53, _G_or_65])
            self.considerError(lastError)
            return (_G_or_72, self.currentError)
        def _G_or_73():
            def _G_consumedby_74():
                def _G_many1_75():
                    _G_apply_76, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError)
                    return (_G_apply_76, self.currentError)
                _G_many1_77, lastError = self.many(_G_many1_75, _G_many1_75())
                self.considerError(lastError)
                return (_G_many1_77, self.currentError)
            _G_consumedby_78, lastError = self.consumedby(_G_consumedby_74)
            self.considerError(lastError)
            _locals['ds'] = _G_consumedby_78
            _G_python_79, lastError = eval('int(ds)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_79, self.currentError)
        _G_or_80, lastError = self._or([_G_or_51, _G_or_73])
        self.considerError(lastError)
        return (_G_or_80, self.currentError)


    def rule_octaldigit(self):
        _locals = {'self': self}
        self.locals['octaldigit'] = _locals
        _G_apply_81, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_81
        def _G_pred_82():
            _G_python_83, lastError = eval("x in '01234567'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_83, self.currentError)
        _G_pred_84, lastError = self.pred(_G_pred_82)
        self.considerError(lastError)
        _G_python_85, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_85, self.currentError)


    def rule_hexdigit(self):
        _locals = {'self': self}
        self.locals['hexdigit'] = _locals
        _G_apply_86, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_86
        def _G_pred_87():
            _G_python_88, lastError = eval("x in '0123456789ABCDEFabcdef'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_88, self.currentError)
        _G_pred_89, lastError = self.pred(_G_pred_87)
        self.considerError(lastError)
        _G_python_90, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_90, self.currentError)


    def rule_escapedChar(self):
        _locals = {'self': self}
        self.locals['escapedChar'] = _locals
        _G_exactly_91, lastError = self.exactly('\\')
        self.considerError(lastError)
        def _G_or_92():
            _G_exactly_93, lastError = self.exactly('n')
            self.considerError(lastError)
            _G_python_94, lastError = eval('"\\n"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_94, self.currentError)
        def _G_or_95():
            _G_exactly_96, lastError = self.exactly('r')
            self.considerError(lastError)
            _G_python_97, lastError = eval('"\\r"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_97, self.currentError)
        def _G_or_98():
            _G_exactly_99, lastError = self.exactly('t')
            self.considerError(lastError)
            _G_python_100, lastError = eval('"\\t"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_100, self.currentError)
        def _G_or_101():
            _G_exactly_102, lastError = self.exactly('b')
            self.considerError(lastError)
            _G_python_103, lastError = eval('"\\b"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_103, self.currentError)
        def _G_or_104():
            _G_exactly_105, lastError = self.exactly('f')
            self.considerError(lastError)
            _G_python_106, lastError = eval('"\\f"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_106, self.currentError)
        def _G_or_107():
            _G_exactly_108, lastError = self.exactly('"')
            self.considerError(lastError)
            _G_python_109, lastError = eval('\'"\'', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_109, self.currentError)
        def _G_or_110():
            _G_exactly_111, lastError = self.exactly("'")
            self.considerError(lastError)
            _G_python_112, lastError = eval('"\'"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_112, self.currentError)
        def _G_or_113():
            _G_exactly_114, lastError = self.exactly('\\')
            self.considerError(lastError)
            _G_python_115, lastError = eval('"\\\\"', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_115, self.currentError)
        _G_or_116, lastError = self._or([_G_or_92, _G_or_95, _G_or_98, _G_or_101, _G_or_104, _G_or_107, _G_or_110, _G_or_113])
        self.considerError(lastError)
        return (_G_or_116, self.currentError)


    def rule_character(self):
        _locals = {'self': self}
        self.locals['character'] = _locals
        _G_python_117, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_117
        _G_python_118, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_119, lastError = self._apply(self.rule_token, "token", [_G_python_118])
        self.considerError(lastError)
        def _G_or_120():
            _G_apply_121, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
            self.considerError(lastError)
            return (_G_apply_121, self.currentError)
        def _G_or_122():
            _G_apply_123, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError)
            return (_G_apply_123, self.currentError)
        _G_or_124, lastError = self._or([_G_or_120, _G_or_122])
        self.considerError(lastError)
        _locals['c'] = _G_or_124
        _G_python_125, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_126, lastError = self._apply(self.rule_token, "token", [_G_python_125])
        self.considerError(lastError)
        _G_python_127, lastError = eval('t.Exactly(c, span=self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_127, self.currentError)


    def rule_string(self):
        _locals = {'self': self}
        self.locals['string'] = _locals
        _G_python_128, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_128
        _G_python_129, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_130, lastError = self._apply(self.rule_token, "token", [_G_python_129])
        self.considerError(lastError)
        def _G_many_131():
            def _G_or_132():
                _G_apply_133, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                self.considerError(lastError)
                return (_G_apply_133, self.currentError)
            def _G_or_134():
                def _G_not_135():
                    _G_exactly_136, lastError = self.exactly('"')
                    self.considerError(lastError)
                    return (_G_exactly_136, self.currentError)
                _G_not_137, lastError = self._not(_G_not_135)
                self.considerError(lastError)
                _G_apply_138, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                return (_G_apply_138, self.currentError)
            _G_or_139, lastError = self._or([_G_or_132, _G_or_134])
            self.considerError(lastError)
            return (_G_or_139, self.currentError)
        _G_many_140, lastError = self.many(_G_many_131)
        self.considerError(lastError)
        _locals['c'] = _G_many_140
        _G_python_141, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_142, lastError = self._apply(self.rule_token, "token", [_G_python_141])
        self.considerError(lastError)
        _G_python_143, lastError = eval("t.Exactly(''.join(c), span=self.span(s))", self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_143, self.currentError)


    def rule_name(self):
        _locals = {'self': self}
        self.locals['name'] = _locals
        def _G_consumedby_144():
            _G_apply_145, lastError = self._apply(self.rule_letter, "letter", [])
            self.considerError(lastError)
            def _G_many_146():
                _G_apply_147, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                self.considerError(lastError)
                return (_G_apply_147, self.currentError)
            _G_many_148, lastError = self.many(_G_many_146)
            self.considerError(lastError)
            return (_G_many_148, self.currentError)
        _G_consumedby_149, lastError = self.consumedby(_G_consumedby_144)
        self.considerError(lastError)
        return (_G_consumedby_149, self.currentError)


    def rule_application(self):
        _locals = {'self': self}
        self.locals['application'] = _locals
        def _G_optional_150():
            _G_apply_151, lastError = self._apply(self.rule_indentation, "indentation", [])
            self.considerError(lastError)
            return (_G_apply_151, self.currentError)
        def _G_optional_152():
            return (None, self.input.nullError())
        _G_or_153, lastError = self._or([_G_optional_150, _G_optional_152])
        self.considerError(lastError)
        _G_python_154, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_154
        _G_apply_155, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['name'] = _G_apply_155
        def _G_or_156():
            _G_exactly_157, lastError = self.exactly('(')
            self.considerError(lastError)
            _G_python_158, lastError = eval("self.applicationArgs(finalChar=')')", self.globals, _locals), None
            self.considerError(lastError)
            _locals['args'] = _G_python_158
            _G_exactly_159, lastError = self.exactly(')')
            self.considerError(lastError)
            _G_python_160, lastError = eval('t.Apply(name, self.rulename, args, span=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_160, self.currentError)
        def _G_or_161():
            _G_python_162, lastError = eval('t.Apply(name, self.rulename, [], span=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_162, self.currentError)
        _G_or_163, lastError = self._or([_G_or_156, _G_or_161])
        self.considerError(lastError)
        return (_G_or_163, self.currentError)


    def rule_expr1(self):
        _locals = {'self': self}
        self.locals['expr1'] = _locals
        def _G_or_164():
            _G_apply_165, lastError = self._apply(self.rule_application, "application", [])
            self.considerError(lastError)
            return (_G_apply_165, self.currentError)
        def _G_or_166():
            _G_apply_167, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
            self.considerError(lastError)
            return (_G_apply_167, self.currentError)
        def _G_or_168():
            _G_apply_169, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
            self.considerError(lastError)
            return (_G_apply_169, self.currentError)
        def _G_or_170():
            _G_apply_171, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
            self.considerError(lastError)
            return (_G_apply_171, self.currentError)
        def _G_or_172():
            _G_apply_173, lastError = self._apply(self.rule_number, "number", [])
            self.considerError(lastError)
            return (_G_apply_173, self.currentError)
        def _G_or_174():
            _G_apply_175, lastError = self._apply(self.rule_character, "character", [])
            self.considerError(lastError)
            return (_G_apply_175, self.currentError)
        def _G_or_176():
            _G_apply_177, lastError = self._apply(self.rule_string, "string", [])
            self.considerError(lastError)
            return (_G_apply_177, self.currentError)
        def _G_or_178():
            _G_python_179, lastError = eval("'('", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_180, lastError = self._apply(self.rule_token, "token", [_G_python_179])
            self.considerError(lastError)
            _G_apply_181, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_181
            _G_python_182, lastError = eval("')'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_183, lastError = self._apply(self.rule_token, "token", [_G_python_182])
            self.considerError(lastError)
            _G_python_184, lastError = eval('e', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_184, self.currentError)
        def _G_or_185():
            _G_python_186, lastError = eval('self.startSpan()', self.globals, _locals), None
            self.considerError(lastError)
            _locals['s'] = _G_python_186
            _G_python_187, lastError = eval("'<'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_188, lastError = self._apply(self.rule_token, "token", [_G_python_187])
            self.considerError(lastError)
            _G_apply_189, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_189
            _G_python_190, lastError = eval("'>'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_191, lastError = self._apply(self.rule_token, "token", [_G_python_190])
            self.considerError(lastError)
            _G_python_192, lastError = eval('t.ConsumedBy(e, s=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_192, self.currentError)
        def _G_or_193():
            _G_python_194, lastError = eval('self.startSpan()', self.globals, _locals), None
            self.considerError(lastError)
            _locals['s'] = _G_python_194
            _G_python_195, lastError = eval("'['", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_196, lastError = self._apply(self.rule_token, "token", [_G_python_195])
            self.considerError(lastError)
            _G_apply_197, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_197
            _G_python_198, lastError = eval("']'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_199, lastError = self._apply(self.rule_token, "token", [_G_python_198])
            self.considerError(lastError)
            _G_python_200, lastError = eval('t.List(e, s=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_200, self.currentError)
        _G_or_201, lastError = self._or([_G_or_164, _G_or_166, _G_or_168, _G_or_170, _G_or_172, _G_or_174, _G_or_176, _G_or_178, _G_or_185, _G_or_193])
        self.considerError(lastError)
        return (_G_or_201, self.currentError)


    def rule_expr2(self):
        _locals = {'self': self}
        self.locals['expr2'] = _locals
        _G_python_202, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_202
        def _G_or_203():
            _G_python_204, lastError = eval("'~'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_205, lastError = self._apply(self.rule_token, "token", [_G_python_204])
            self.considerError(lastError)
            def _G_or_206():
                _G_python_207, lastError = eval("'~'", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_208, lastError = self._apply(self.rule_token, "token", [_G_python_207])
                self.considerError(lastError)
                _G_apply_209, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_209
                _G_python_210, lastError = eval('t.Lookahead(e, span=self.span(s))', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_210, self.currentError)
            def _G_or_211():
                _G_apply_212, lastError = self._apply(self.rule_expr2, "expr2", [])
                self.considerError(lastError)
                _locals['e'] = _G_apply_212
                _G_python_213, lastError = eval('t.Not(e, span=self.span(s))', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_213, self.currentError)
            _G_or_214, lastError = self._or([_G_or_206, _G_or_211])
            self.considerError(lastError)
            return (_G_or_214, self.currentError)
        def _G_or_215():
            _G_apply_216, lastError = self._apply(self.rule_expr1, "expr1", [])
            self.considerError(lastError)
            return (_G_apply_216, self.currentError)
        _G_or_217, lastError = self._or([_G_or_203, _G_or_215])
        self.considerError(lastError)
        return (_G_or_217, self.currentError)


    def rule_repeatTimes(self):
        _locals = {'self': self}
        self.locals['repeatTimes'] = _locals
        def _G_or_218():
            _G_apply_219, lastError = self._apply(self.rule_barenumber, "barenumber", [])
            self.considerError(lastError)
            _locals['x'] = _G_apply_219
            _G_python_220, lastError = eval('int(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_220, self.currentError)
        def _G_or_221():
            _G_apply_222, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            return (_G_apply_222, self.currentError)
        _G_or_223, lastError = self._or([_G_or_218, _G_or_221])
        self.considerError(lastError)
        return (_G_or_223, self.currentError)


    def rule_expr3(self):
        _locals = {'self': self}
        self.locals['expr3'] = _locals
        def _G_or_224():
            _G_python_225, lastError = eval('self.startSpan()', self.globals, _locals), None
            self.considerError(lastError)
            _locals['s'] = _G_python_225
            _G_apply_226, lastError = self._apply(self.rule_expr2, "expr2", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_226
            def _G_or_227():
                _G_exactly_228, lastError = self.exactly('*')
                self.considerError(lastError)
                _G_python_229, lastError = eval('t.Many(e, span=self.span(s))', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_229, self.currentError)
            def _G_or_230():
                _G_exactly_231, lastError = self.exactly('+')
                self.considerError(lastError)
                _G_python_232, lastError = eval('t.Many1(e, span=self.span(s))', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_232, self.currentError)
            def _G_or_233():
                _G_exactly_234, lastError = self.exactly('?')
                self.considerError(lastError)
                _G_python_235, lastError = eval('t.Optional(e, span=self.span(s))', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_235, self.currentError)
            def _G_or_236():
                _G_exactly_237, lastError = self.exactly('{')
                self.considerError(lastError)
                _G_apply_238, lastError = self._apply(self.rule_spaces, "spaces", [])
                self.considerError(lastError)
                _G_apply_239, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                self.considerError(lastError)
                _locals['start'] = _G_apply_239
                _G_apply_240, lastError = self._apply(self.rule_spaces, "spaces", [])
                self.considerError(lastError)
                def _G_or_241():
                    _G_exactly_242, lastError = self.exactly(',')
                    self.considerError(lastError)
                    _G_apply_243, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_apply_244, lastError = self._apply(self.rule_repeatTimes, "repeatTimes", [])
                    self.considerError(lastError)
                    _locals['end'] = _G_apply_244
                    _G_apply_245, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_exactly_246, lastError = self.exactly('}')
                    self.considerError(lastError)
                    _G_python_247, lastError = eval('t.Repeat(start, end, e, span=self.span(s))', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_247, self.currentError)
                def _G_or_248():
                    _G_apply_249, lastError = self._apply(self.rule_spaces, "spaces", [])
                    self.considerError(lastError)
                    _G_exactly_250, lastError = self.exactly('}')
                    self.considerError(lastError)
                    _G_python_251, lastError = eval('t.Repeat(start, start, e, span=self.span(s))', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_251, self.currentError)
                _G_or_252, lastError = self._or([_G_or_241, _G_or_248])
                self.considerError(lastError)
                return (_G_or_252, self.currentError)
            def _G_or_253():
                _G_python_254, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_254, self.currentError)
            _G_or_255, lastError = self._or([_G_or_227, _G_or_230, _G_or_233, _G_or_236, _G_or_253])
            self.considerError(lastError)
            _locals['r'] = _G_or_255
            def _G_or_256():
                _G_exactly_257, lastError = self.exactly(':')
                self.considerError(lastError)
                _G_apply_258, lastError = self._apply(self.rule_name, "name", [])
                self.considerError(lastError)
                _locals['n'] = _G_apply_258
                _G_python_259, lastError = eval('t.Bind(n, r, span=self.span(s))', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_259, self.currentError)
            def _G_or_260():
                _G_python_261, lastError = eval('r', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_261, self.currentError)
            _G_or_262, lastError = self._or([_G_or_256, _G_or_260])
            self.considerError(lastError)
            return (_G_or_262, self.currentError)
        def _G_or_263():
            _G_python_264, lastError = eval("':'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_265, lastError = self._apply(self.rule_token, "token", [_G_python_264])
            self.considerError(lastError)
            _G_apply_266, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_266
            _G_python_267, lastError = eval('t.Bind(n, t.Apply("anything", self.rulename, []),\n                     span=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_267, self.currentError)
        _G_or_268, lastError = self._or([_G_or_224, _G_or_263])
        self.considerError(lastError)
        return (_G_or_268, self.currentError)


    def rule_expr4(self):
        _locals = {'self': self}
        self.locals['expr4'] = _locals
        _G_python_269, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_269
        def _G_many_270():
            _G_apply_271, lastError = self._apply(self.rule_expr3, "expr3", [])
            self.considerError(lastError)
            return (_G_apply_271, self.currentError)
        _G_many_272, lastError = self.many(_G_many_270)
        self.considerError(lastError)
        _locals['es'] = _G_many_272
        _G_python_273, lastError = eval('t.And(es, span=self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_273, self.currentError)


    def rule_expr(self):
        _locals = {'self': self}
        self.locals['expr'] = _locals
        _G_python_274, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_274
        _G_apply_275, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['e'] = _G_apply_275
        def _G_many_276():
            _G_python_277, lastError = eval("'|'", self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_278, lastError = self._apply(self.rule_token, "token", [_G_python_277])
            self.considerError(lastError)
            _G_apply_279, lastError = self._apply(self.rule_expr4, "expr4", [])
            self.considerError(lastError)
            return (_G_apply_279, self.currentError)
        _G_many_280, lastError = self.many(_G_many_276)
        self.considerError(lastError)
        _locals['es'] = _G_many_280
        _G_python_281, lastError = eval('t.Or([e] + es, span=self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_281, self.currentError)


    def rule_ruleValue(self):
        _locals = {'self': self}
        self.locals['ruleValue'] = _locals
        _G_python_282, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_282
        _G_python_283, lastError = eval('"->"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_284, lastError = self._apply(self.rule_token, "token", [_G_python_283])
        self.considerError(lastError)
        _G_python_285, lastError = eval('self.ruleValueExpr(True, span=self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_285, self.currentError)


    def rule_semanticPredicate(self):
        _locals = {'self': self}
        self.locals['semanticPredicate'] = _locals
        _G_python_286, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_286
        _G_python_287, lastError = eval('"?("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_288, lastError = self._apply(self.rule_token, "token", [_G_python_287])
        self.considerError(lastError)
        _G_python_289, lastError = eval('self.semanticPredicateExpr(span=self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_289, self.currentError)


    def rule_semanticAction(self):
        _locals = {'self': self}
        self.locals['semanticAction'] = _locals
        _G_python_290, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_290
        _G_python_291, lastError = eval('"!("', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_292, lastError = self._apply(self.rule_token, "token", [_G_python_291])
        self.considerError(lastError)
        _G_python_293, lastError = eval('self.semanticActionExpr(span=self.span(s))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_293, self.currentError)


    def rule_ruleEnd(self):
        _locals = {'self': self}
        self.locals['ruleEnd'] = _locals
        def _G_or_294():
            def _G_many_295():
                _G_apply_296, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError)
                return (_G_apply_296, self.currentError)
            _G_many_297, lastError = self.many(_G_many_295)
            self.considerError(lastError)
            def _G_many1_298():
                _G_apply_299, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError)
                return (_G_apply_299, self.currentError)
            _G_many1_300, lastError = self.many(_G_many1_298, _G_many1_298())
            self.considerError(lastError)
            return (_G_many1_300, self.currentError)
        def _G_or_301():
            _G_apply_302, lastError = self._apply(self.rule_end, "end", [])
            self.considerError(lastError)
            return (_G_apply_302, self.currentError)
        _G_or_303, lastError = self._or([_G_or_294, _G_or_301])
        self.considerError(lastError)
        return (_G_or_303, self.currentError)


    def rule_rulePart(self):
        _locals = {'self': self}
        self.locals['rulePart'] = _locals
        _G_apply_304, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['requiredName'] = _G_apply_304
        _G_apply_305, lastError = self._apply(self.rule_noindentation, "noindentation", [])
        self.considerError(lastError)
        _G_apply_306, lastError = self._apply(self.rule_name, "name", [])
        self.considerError(lastError)
        _locals['n'] = _G_apply_306
        def _G_pred_307():
            _G_python_308, lastError = eval('n == requiredName', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_308, self.currentError)
        _G_pred_309, lastError = self.pred(_G_pred_307)
        self.considerError(lastError)
        _G_python_310, lastError = eval('setattr(self, "rulename", n)', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_311, lastError = self._apply(self.rule_expr4, "expr4", [])
        self.considerError(lastError)
        _locals['args'] = _G_apply_311
        def _G_or_312():
            _G_python_313, lastError = eval('"="', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_314, lastError = self._apply(self.rule_token, "token", [_G_python_313])
            self.considerError(lastError)
            _G_apply_315, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError)
            _locals['e'] = _G_apply_315
            _G_apply_316, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
            self.considerError(lastError)
            _G_python_317, lastError = eval('t.And([args, e])', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_317, self.currentError)
        def _G_or_318():
            _G_apply_319, lastError = self._apply(self.rule_ruleEnd, "ruleEnd", [])
            self.considerError(lastError)
            _G_python_320, lastError = eval('args', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_320, self.currentError)
        _G_or_321, lastError = self._or([_G_or_312, _G_or_318])
        self.considerError(lastError)
        return (_G_or_321, self.currentError)


    def rule_rule(self):
        _locals = {'self': self}
        self.locals['rule'] = _locals
        _G_apply_322, lastError = self._apply(self.rule_noindentation, "noindentation", [])
        self.considerError(lastError)
        def _G_lookahead_323():
            _G_apply_324, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError)
            _locals['n'] = _G_apply_324
            return (_locals['n'], self.currentError)
        _G_lookahead_325, lastError = self.lookahead(_G_lookahead_323)
        self.considerError(lastError)
        _G_python_326, lastError = eval('self.startSpan()', self.globals, _locals), None
        self.considerError(lastError)
        _locals['s'] = _G_python_326
        _G_python_327, lastError = eval('n', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_328, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_327])
        self.considerError(lastError)
        _locals['r'] = _G_apply_328
        def _G_or_329():
            def _G_many1_330():
                _G_python_331, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_332, lastError = self._apply(self.rule_rulePart, "rulePart", [_G_python_331])
                self.considerError(lastError)
                return (_G_apply_332, self.currentError)
            _G_many1_333, lastError = self.many(_G_many1_330, _G_many1_330())
            self.considerError(lastError)
            _locals['rs'] = _G_many1_333
            _G_python_334, lastError = eval('t.Rule(n, t.Or([r] + rs), span=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_334, self.currentError)
        def _G_or_335():
            _G_python_336, lastError = eval('t.Rule(n, r, span=self.span(s))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_336, self.currentError)
        _G_or_337, lastError = self._or([_G_or_329, _G_or_335])
        self.considerError(lastError)
        return (_G_or_337, self.currentError)


    def rule_grammar(self):
        _locals = {'self': self}
        self.locals['grammar'] = _locals
        def _G_many_338():
            _G_apply_339, lastError = self._apply(self.rule_rule, "rule", [])
            self.considerError(lastError)
            return (_G_apply_339, self.currentError)
        _G_many_340, lastError = self.many(_G_many_338)
        self.considerError(lastError)
        _locals['rs'] = _G_many_340
        _G_apply_341, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_python_342, lastError = eval('t.Grammar(self.name, rs)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_342, self.currentError)
