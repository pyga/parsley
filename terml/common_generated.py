from ometa.runtime import OMetaBase as GrammarBase
class Parser(GrammarBase):
    def rule_horizontal_space(self):
        _locals = {'self': self}
        self.locals['horizontal_space'] = _locals
        def _G_or_1():
            _G_exactly_2, lastError = self.exactly(' ')
            self.considerError(lastError)
            return (_G_exactly_2, self.currentError)
        def _G_or_3():
            _G_exactly_4, lastError = self.exactly('\t')
            self.considerError(lastError)
            return (_G_exactly_4, self.currentError)
        def _G_or_5():
            _G_exactly_6, lastError = self.exactly('\x0c')
            self.considerError(lastError)
            return (_G_exactly_6, self.currentError)
        def _G_or_7():
            _G_exactly_8, lastError = self.exactly('#')
            self.considerError(lastError)
            def _G_many_9():
                def _G_not_10():
                    _G_apply_11, lastError = self._apply(self.rule_eol, "eol", [])
                    self.considerError(lastError)
                    return (_G_apply_11, self.currentError)
                _G_not_12, lastError = self._not(_G_not_10)
                self.considerError(lastError)
                _G_apply_13, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                return (_G_apply_13, self.currentError)
            _G_many_14, lastError = self.many(_G_many_9)
            self.considerError(lastError)
            return (_G_many_14, self.currentError)
        _G_or_15, lastError = self._or([_G_or_1, _G_or_3, _G_or_5, _G_or_7])
        self.considerError(lastError)
        return (_G_or_15, self.currentError)


    def rule_spaces(self):
        _locals = {'self': self}
        self.locals['spaces'] = _locals
        def _G_many_16():
            _G_apply_17, lastError = self._apply(self.rule_horizontal_space, "horizontal_space", [])
            self.considerError(lastError)
            return (_G_apply_17, self.currentError)
        _G_many_18, lastError = self.many(_G_many_16)
        self.considerError(lastError)
        return (_G_many_18, self.currentError)


    def rule_number(self):
        _locals = {'self': self}
        self.locals['number'] = _locals
        _G_apply_19, lastError = self._apply(self.rule_spaces, "spaces", [])
        self.considerError(lastError)
        _G_apply_20, lastError = self._apply(self.rule_barenumber, "barenumber", [])
        self.considerError(lastError)
        return (_G_apply_20, self.currentError)


    def rule_barenumber(self):
        _locals = {'self': self}
        self.locals['barenumber'] = _locals
        def _G_optional_21():
            _G_exactly_22, lastError = self.exactly('-')
            self.considerError(lastError)
            return (_G_exactly_22, self.currentError)
        def _G_optional_23():
            return (None, self.input.nullError())
        _G_or_24, lastError = self._or([_G_optional_21, _G_optional_23])
        self.considerError(lastError)
        _locals['sign'] = _G_or_24
        def _G_or_25():
            _G_exactly_26, lastError = self.exactly('0')
            self.considerError(lastError)
            def _G_or_27():
                def _G_or_28():
                    _G_exactly_29, lastError = self.exactly('x')
                    self.considerError(lastError)
                    return (_G_exactly_29, self.currentError)
                def _G_or_30():
                    _G_exactly_31, lastError = self.exactly('X')
                    self.considerError(lastError)
                    return (_G_exactly_31, self.currentError)
                _G_or_32, lastError = self._or([_G_or_28, _G_or_30])
                self.considerError(lastError)
                def _G_many_33():
                    _G_apply_34, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                    self.considerError(lastError)
                    return (_G_apply_34, self.currentError)
                _G_many_35, lastError = self.many(_G_many_33)
                self.considerError(lastError)
                _locals['hs'] = _G_many_35
                _G_python_36, lastError = eval('makeHex(sign, hs)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_36, self.currentError)
            def _G_or_37():
                _G_python_38, lastError = eval('sign', self.globals, _locals), None
                self.considerError(lastError)
                _G_python_39, lastError = eval("'0'", self.globals, _locals), None
                self.considerError(lastError)
                _G_apply_40, lastError = self._apply(self.rule_floatPart, "floatPart", [_G_python_38, _G_python_39])
                self.considerError(lastError)
                return (_G_apply_40, self.currentError)
            def _G_or_41():
                def _G_many_42():
                    _G_apply_43, lastError = self._apply(self.rule_octaldigit, "octaldigit", [])
                    self.considerError(lastError)
                    return (_G_apply_43, self.currentError)
                _G_many_44, lastError = self.many(_G_many_42)
                self.considerError(lastError)
                _locals['ds'] = _G_many_44
                _G_python_45, lastError = eval('makeOctal(sign, ds)', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_45, self.currentError)
            _G_or_46, lastError = self._or([_G_or_27, _G_or_37, _G_or_41])
            self.considerError(lastError)
            return (_G_or_46, self.currentError)
        def _G_or_47():
            _G_apply_48, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            _locals['ds'] = _G_apply_48
            _G_python_49, lastError = eval('sign', self.globals, _locals), None
            self.considerError(lastError)
            _G_python_50, lastError = eval('ds', self.globals, _locals), None
            self.considerError(lastError)
            _G_apply_51, lastError = self._apply(self.rule_floatPart, "floatPart", [_G_python_49, _G_python_50])
            self.considerError(lastError)
            return (_G_apply_51, self.currentError)
        def _G_or_52():
            _G_apply_53, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            _locals['ds'] = _G_apply_53
            _G_python_54, lastError = eval('signedInt(sign, ds)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_54, self.currentError)
        _G_or_55, lastError = self._or([_G_or_25, _G_or_47, _G_or_52])
        self.considerError(lastError)
        return (_G_or_55, self.currentError)


    def rule_exponent(self):
        _locals = {'self': self}
        self.locals['exponent'] = _locals
        def _G_consumedby_56():
            def _G_or_57():
                _G_exactly_58, lastError = self.exactly('e')
                self.considerError(lastError)
                return (_G_exactly_58, self.currentError)
            def _G_or_59():
                _G_exactly_60, lastError = self.exactly('E')
                self.considerError(lastError)
                return (_G_exactly_60, self.currentError)
            _G_or_61, lastError = self._or([_G_or_57, _G_or_59])
            self.considerError(lastError)
            def _G_optional_62():
                def _G_or_63():
                    _G_exactly_64, lastError = self.exactly('+')
                    self.considerError(lastError)
                    return (_G_exactly_64, self.currentError)
                def _G_or_65():
                    _G_exactly_66, lastError = self.exactly('-')
                    self.considerError(lastError)
                    return (_G_exactly_66, self.currentError)
                _G_or_67, lastError = self._or([_G_or_63, _G_or_65])
                self.considerError(lastError)
                return (_G_or_67, self.currentError)
            def _G_optional_68():
                return (None, self.input.nullError())
            _G_or_69, lastError = self._or([_G_optional_62, _G_optional_68])
            self.considerError(lastError)
            _G_apply_70, lastError = self._apply(self.rule_decdigits, "decdigits", [])
            self.considerError(lastError)
            return (_G_apply_70, self.currentError)
        _G_consumedby_71, lastError = self.consumedby(_G_consumedby_56)
        self.considerError(lastError)
        return (_G_consumedby_71, self.currentError)


    def rule_floatPart(self):
        _locals = {'self': self}
        self.locals['floatPart'] = _locals
        _G_apply_72, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['sign'] = _G_apply_72
        _G_apply_73, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['ds'] = _G_apply_73
        def _G_consumedby_74():
            def _G_or_75():
                _G_exactly_76, lastError = self.exactly('.')
                self.considerError(lastError)
                _G_apply_77, lastError = self._apply(self.rule_decdigits, "decdigits", [])
                self.considerError(lastError)
                def _G_optional_78():
                    _G_apply_79, lastError = self._apply(self.rule_exponent, "exponent", [])
                    self.considerError(lastError)
                    return (_G_apply_79, self.currentError)
                def _G_optional_80():
                    return (None, self.input.nullError())
                _G_or_81, lastError = self._or([_G_optional_78, _G_optional_80])
                self.considerError(lastError)
                return (_G_or_81, self.currentError)
            def _G_or_82():
                _G_apply_83, lastError = self._apply(self.rule_exponent, "exponent", [])
                self.considerError(lastError)
                return (_G_apply_83, self.currentError)
            _G_or_84, lastError = self._or([_G_or_75, _G_or_82])
            self.considerError(lastError)
            return (_G_or_84, self.currentError)
        _G_consumedby_85, lastError = self.consumedby(_G_consumedby_74)
        self.considerError(lastError)
        _locals['tail'] = _G_consumedby_85
        _G_python_86, lastError = eval('makeFloat(sign, ds, tail)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_86, self.currentError)


    def rule_decdigits(self):
        _locals = {'self': self}
        self.locals['decdigits'] = _locals
        _G_apply_87, lastError = self._apply(self.rule_digit, "digit", [])
        self.considerError(lastError)
        _locals['d'] = _G_apply_87
        def _G_many_88():
            def _G_or_89():
                _G_apply_90, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                _locals['x'] = _G_apply_90
                def _G_pred_91():
                    _G_python_92, lastError = eval('isDigit(x)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_92, self.currentError)
                _G_pred_93, lastError = self.pred(_G_pred_91)
                self.considerError(lastError)
                _G_python_94, lastError = eval('x', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_94, self.currentError)
            def _G_or_95():
                _G_exactly_96, lastError = self.exactly('_')
                self.considerError(lastError)
                _G_python_97, lastError = eval('""', self.globals, _locals), None
                self.considerError(lastError)
                return (_G_python_97, self.currentError)
            _G_or_98, lastError = self._or([_G_or_89, _G_or_95])
            self.considerError(lastError)
            return (_G_or_98, self.currentError)
        _G_many_99, lastError = self.many(_G_many_88)
        self.considerError(lastError)
        _locals['ds'] = _G_many_99
        _G_python_100, lastError = eval('concat(d, join(ds))', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_100, self.currentError)


    def rule_octaldigit(self):
        _locals = {'self': self}
        self.locals['octaldigit'] = _locals
        _G_apply_101, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_101
        def _G_pred_102():
            _G_python_103, lastError = eval('isOctDigit(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_103, self.currentError)
        _G_pred_104, lastError = self.pred(_G_pred_102)
        self.considerError(lastError)
        _G_python_105, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_105, self.currentError)


    def rule_hexdigit(self):
        _locals = {'self': self}
        self.locals['hexdigit'] = _locals
        _G_apply_106, lastError = self._apply(self.rule_anything, "anything", [])
        self.considerError(lastError)
        _locals['x'] = _G_apply_106
        def _G_pred_107():
            _G_python_108, lastError = eval('isHexDigit(x)', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_108, self.currentError)
        _G_pred_109, lastError = self.pred(_G_pred_107)
        self.considerError(lastError)
        _G_python_110, lastError = eval('x', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_110, self.currentError)


    def rule_string(self):
        _locals = {'self': self}
        self.locals['string'] = _locals
        _G_python_111, lastError = eval('\'"\'', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_112, lastError = self._apply(self.rule_token, "token", [_G_python_111])
        self.considerError(lastError)
        def _G_many_113():
            def _G_or_114():
                _G_apply_115, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                self.considerError(lastError)
                return (_G_apply_115, self.currentError)
            def _G_or_116():
                def _G_not_117():
                    _G_exactly_118, lastError = self.exactly('"')
                    self.considerError(lastError)
                    return (_G_exactly_118, self.currentError)
                _G_not_119, lastError = self._not(_G_not_117)
                self.considerError(lastError)
                _G_apply_120, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                return (_G_apply_120, self.currentError)
            _G_or_121, lastError = self._or([_G_or_114, _G_or_116])
            self.considerError(lastError)
            return (_G_or_121, self.currentError)
        _G_many_122, lastError = self.many(_G_many_113)
        self.considerError(lastError)
        _locals['c'] = _G_many_122
        _G_exactly_123, lastError = self.exactly('"')
        self.considerError(lastError)
        _G_python_124, lastError = eval('join(c)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_124, self.currentError)


    def rule_character(self):
        _locals = {'self': self}
        self.locals['character'] = _locals
        _G_python_125, lastError = eval('"\'"', self.globals, _locals), None
        self.considerError(lastError)
        _G_apply_126, lastError = self._apply(self.rule_token, "token", [_G_python_125])
        self.considerError(lastError)
        def _G_or_127():
            _G_apply_128, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
            self.considerError(lastError)
            return (_G_apply_128, self.currentError)
        def _G_or_129():
            def _G_not_130():
                def _G_or_131():
                    _G_exactly_132, lastError = self.exactly("'")
                    self.considerError(lastError)
                    return (_G_exactly_132, self.currentError)
                def _G_or_133():
                    _G_exactly_134, lastError = self.exactly('\n')
                    self.considerError(lastError)
                    return (_G_exactly_134, self.currentError)
                def _G_or_135():
                    _G_exactly_136, lastError = self.exactly('\r')
                    self.considerError(lastError)
                    return (_G_exactly_136, self.currentError)
                def _G_or_137():
                    _G_exactly_138, lastError = self.exactly('\\')
                    self.considerError(lastError)
                    return (_G_exactly_138, self.currentError)
                _G_or_139, lastError = self._or([_G_or_131, _G_or_133, _G_or_135, _G_or_137])
                self.considerError(lastError)
                return (_G_or_139, self.currentError)
            _G_not_140, lastError = self._not(_G_not_130)
            self.considerError(lastError)
            _G_apply_141, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError)
            return (_G_apply_141, self.currentError)
        _G_or_142, lastError = self._or([_G_or_127, _G_or_129])
        self.considerError(lastError)
        _locals['c'] = _G_or_142
        _G_exactly_143, lastError = self.exactly("'")
        self.considerError(lastError)
        _G_python_144, lastError = eval('Character(c)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_144, self.currentError)


    def rule_escapedUnicode(self):
        _locals = {'self': self}
        self.locals['escapedUnicode'] = _locals
        def _G_or_145():
            _G_exactly_146, lastError = self.exactly('u')
            self.considerError(lastError)
            def _G_consumedby_147():
                _G_apply_148, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_149, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_150, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_151, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                return (_G_apply_151, self.currentError)
            _G_consumedby_152, lastError = self.consumedby(_G_consumedby_147)
            self.considerError(lastError)
            _locals['hs'] = _G_consumedby_152
            _G_python_153, lastError = eval('unichr(int(hs, 16))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_153, self.currentError)
        def _G_or_154():
            _G_exactly_155, lastError = self.exactly('U')
            self.considerError(lastError)
            def _G_consumedby_156():
                _G_apply_157, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_158, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_159, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_160, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_161, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_162, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_163, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                _G_apply_164, lastError = self._apply(self.rule_hexdigit, "hexdigit", [])
                self.considerError(lastError)
                return (_G_apply_164, self.currentError)
            _G_consumedby_165, lastError = self.consumedby(_G_consumedby_156)
            self.considerError(lastError)
            _locals['hs'] = _G_consumedby_165
            _G_python_166, lastError = eval('unichr(int(hs, 16))', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_166, self.currentError)
        _G_or_167, lastError = self._or([_G_or_145, _G_or_154])
        self.considerError(lastError)
        return (_G_or_167, self.currentError)


    def rule_escapedOctal(self):
        _locals = {'self': self}
        self.locals['escapedOctal'] = _locals
        def _G_or_168():
            def _G_consumedby_169():
                _G_apply_170, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                _locals['a'] = _G_apply_170
                def _G_pred_171():
                    _G_python_172, lastError = eval('contains("0123", a)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_172, self.currentError)
                _G_pred_173, lastError = self.pred(_G_pred_171)
                self.considerError(lastError)
                def _G_optional_174():
                    _G_apply_175, lastError = self._apply(self.rule_octdigit, "octdigit", [])
                    self.considerError(lastError)
                    return (_G_apply_175, self.currentError)
                def _G_optional_176():
                    return (None, self.input.nullError())
                _G_or_177, lastError = self._or([_G_optional_174, _G_optional_176])
                self.considerError(lastError)
                def _G_optional_178():
                    _G_apply_179, lastError = self._apply(self.rule_octdigit, "octdigit", [])
                    self.considerError(lastError)
                    return (_G_apply_179, self.currentError)
                def _G_optional_180():
                    return (None, self.input.nullError())
                _G_or_181, lastError = self._or([_G_optional_178, _G_optional_180])
                self.considerError(lastError)
                return (_G_or_181, self.currentError)
            _G_consumedby_182, lastError = self.consumedby(_G_consumedby_169)
            self.considerError(lastError)
            return (_G_consumedby_182, self.currentError)
        def _G_or_183():
            def _G_consumedby_184():
                _G_apply_185, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError)
                _locals['a'] = _G_apply_185
                def _G_pred_186():
                    _G_python_187, lastError = eval('contains("4567", a)', self.globals, _locals), None
                    self.considerError(lastError)
                    return (_G_python_187, self.currentError)
                _G_pred_188, lastError = self.pred(_G_pred_186)
                self.considerError(lastError)
                def _G_optional_189():
                    _G_apply_190, lastError = self._apply(self.rule_octdigit, "octdigit", [])
                    self.considerError(lastError)
                    return (_G_apply_190, self.currentError)
                def _G_optional_191():
                    return (None, self.input.nullError())
                _G_or_192, lastError = self._or([_G_optional_189, _G_optional_191])
                self.considerError(lastError)
                return (_G_or_192, self.currentError)
            _G_consumedby_193, lastError = self.consumedby(_G_consumedby_184)
            self.considerError(lastError)
            return (_G_consumedby_193, self.currentError)
        _G_or_194, lastError = self._or([_G_or_168, _G_or_183])
        self.considerError(lastError)
        _locals['os'] = _G_or_194
        _G_python_195, lastError = eval('int(os, 8)', self.globals, _locals), None
        self.considerError(lastError)
        return (_G_python_195, self.currentError)


    def rule_escapedChar(self):
        _locals = {'self': self}
        self.locals['escapedChar'] = _locals
        _G_exactly_196, lastError = self.exactly('\\')
        self.considerError(lastError)
        def _G_or_197():
            _G_exactly_198, lastError = self.exactly('n')
            self.considerError(lastError)
            _G_python_199, lastError = eval("'\\n'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_199, self.currentError)
        def _G_or_200():
            _G_exactly_201, lastError = self.exactly('r')
            self.considerError(lastError)
            _G_python_202, lastError = eval("'\\r'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_202, self.currentError)
        def _G_or_203():
            _G_exactly_204, lastError = self.exactly('t')
            self.considerError(lastError)
            _G_python_205, lastError = eval("'\\t'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_205, self.currentError)
        def _G_or_206():
            _G_exactly_207, lastError = self.exactly('b')
            self.considerError(lastError)
            _G_python_208, lastError = eval("'\\b'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_208, self.currentError)
        def _G_or_209():
            _G_exactly_210, lastError = self.exactly('f')
            self.considerError(lastError)
            _G_python_211, lastError = eval("'\\f'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_211, self.currentError)
        def _G_or_212():
            _G_exactly_213, lastError = self.exactly('"')
            self.considerError(lastError)
            _G_python_214, lastError = eval('\'"\'', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_214, self.currentError)
        def _G_or_215():
            _G_exactly_216, lastError = self.exactly("'")
            self.considerError(lastError)
            _G_python_217, lastError = eval("'\\''", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_217, self.currentError)
        def _G_or_218():
            _G_exactly_219, lastError = self.exactly('?')
            self.considerError(lastError)
            _G_python_220, lastError = eval("'?'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_220, self.currentError)
        def _G_or_221():
            _G_exactly_222, lastError = self.exactly('\\')
            self.considerError(lastError)
            _G_python_223, lastError = eval("'\\\\'", self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_223, self.currentError)
        def _G_or_224():
            _G_apply_225, lastError = self._apply(self.rule_escapedUnicode, "escapedUnicode", [])
            self.considerError(lastError)
            return (_G_apply_225, self.currentError)
        def _G_or_226():
            _G_apply_227, lastError = self._apply(self.rule_escapedOctal, "escapedOctal", [])
            self.considerError(lastError)
            return (_G_apply_227, self.currentError)
        def _G_or_228():
            _G_apply_229, lastError = self._apply(self.rule_eol, "eol", [])
            self.considerError(lastError)
            _G_python_230, lastError = eval('""', self.globals, _locals), None
            self.considerError(lastError)
            return (_G_python_230, self.currentError)
        _G_or_231, lastError = self._or([_G_or_197, _G_or_200, _G_or_203, _G_or_206, _G_or_209, _G_or_212, _G_or_215, _G_or_218, _G_or_221, _G_or_224, _G_or_226, _G_or_228])
        self.considerError(lastError)
        return (_G_or_231, self.currentError)


    def rule_eol(self):
        _locals = {'self': self}
        self.locals['eol'] = _locals
        def _G_many_232():
            _G_apply_233, lastError = self._apply(self.rule_horizontal_space, "horizontal_space", [])
            self.considerError(lastError)
            return (_G_apply_233, self.currentError)
        _G_many_234, lastError = self.many(_G_many_232)
        self.considerError(lastError)
        def _G_or_235():
            _G_exactly_236, lastError = self.exactly('\r')
            self.considerError(lastError)
            _G_exactly_237, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_237, self.currentError)
        def _G_or_238():
            _G_exactly_239, lastError = self.exactly('\r')
            self.considerError(lastError)
            return (_G_exactly_239, self.currentError)
        def _G_or_240():
            _G_exactly_241, lastError = self.exactly('\n')
            self.considerError(lastError)
            return (_G_exactly_241, self.currentError)
        _G_or_242, lastError = self._or([_G_or_235, _G_or_238, _G_or_240])
        self.considerError(lastError)
        return (_G_or_242, self.currentError)


    def rule_uriBody(self):
        _locals = {'self': self}
        self.locals['uriBody'] = _locals
        def _G_consumedby_243():
            def _G_many1_244():
                def _G_or_245():
                    _G_apply_246, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                    self.considerError(lastError)
                    return (_G_apply_246, self.currentError)
                def _G_or_247():
                    _G_exactly_248, lastError = self.exactly(';')
                    self.considerError(lastError)
                    return (_G_exactly_248, self.currentError)
                def _G_or_249():
                    _G_exactly_250, lastError = self.exactly('/')
                    self.considerError(lastError)
                    return (_G_exactly_250, self.currentError)
                def _G_or_251():
                    _G_exactly_252, lastError = self.exactly('?')
                    self.considerError(lastError)
                    return (_G_exactly_252, self.currentError)
                def _G_or_253():
                    _G_exactly_254, lastError = self.exactly(':')
                    self.considerError(lastError)
                    return (_G_exactly_254, self.currentError)
                def _G_or_255():
                    _G_exactly_256, lastError = self.exactly('@')
                    self.considerError(lastError)
                    return (_G_exactly_256, self.currentError)
                def _G_or_257():
                    _G_exactly_258, lastError = self.exactly('&')
                    self.considerError(lastError)
                    return (_G_exactly_258, self.currentError)
                def _G_or_259():
                    _G_exactly_260, lastError = self.exactly('=')
                    self.considerError(lastError)
                    return (_G_exactly_260, self.currentError)
                def _G_or_261():
                    _G_exactly_262, lastError = self.exactly('+')
                    self.considerError(lastError)
                    return (_G_exactly_262, self.currentError)
                def _G_or_263():
                    _G_exactly_264, lastError = self.exactly('$')
                    self.considerError(lastError)
                    return (_G_exactly_264, self.currentError)
                def _G_or_265():
                    _G_exactly_266, lastError = self.exactly(',')
                    self.considerError(lastError)
                    return (_G_exactly_266, self.currentError)
                def _G_or_267():
                    _G_exactly_268, lastError = self.exactly('-')
                    self.considerError(lastError)
                    return (_G_exactly_268, self.currentError)
                def _G_or_269():
                    _G_exactly_270, lastError = self.exactly('.')
                    self.considerError(lastError)
                    return (_G_exactly_270, self.currentError)
                def _G_or_271():
                    _G_exactly_272, lastError = self.exactly('!')
                    self.considerError(lastError)
                    return (_G_exactly_272, self.currentError)
                def _G_or_273():
                    _G_exactly_274, lastError = self.exactly('~')
                    self.considerError(lastError)
                    return (_G_exactly_274, self.currentError)
                def _G_or_275():
                    _G_exactly_276, lastError = self.exactly('*')
                    self.considerError(lastError)
                    return (_G_exactly_276, self.currentError)
                def _G_or_277():
                    _G_exactly_278, lastError = self.exactly("'")
                    self.considerError(lastError)
                    return (_G_exactly_278, self.currentError)
                def _G_or_279():
                    _G_exactly_280, lastError = self.exactly('(')
                    self.considerError(lastError)
                    return (_G_exactly_280, self.currentError)
                def _G_or_281():
                    _G_exactly_282, lastError = self.exactly(')')
                    self.considerError(lastError)
                    return (_G_exactly_282, self.currentError)
                def _G_or_283():
                    _G_exactly_284, lastError = self.exactly('%')
                    self.considerError(lastError)
                    return (_G_exactly_284, self.currentError)
                def _G_or_285():
                    _G_exactly_286, lastError = self.exactly('\\')
                    self.considerError(lastError)
                    return (_G_exactly_286, self.currentError)
                def _G_or_287():
                    _G_exactly_288, lastError = self.exactly('|')
                    self.considerError(lastError)
                    return (_G_exactly_288, self.currentError)
                def _G_or_289():
                    _G_exactly_290, lastError = self.exactly('#')
                    self.considerError(lastError)
                    return (_G_exactly_290, self.currentError)
                _G_or_291, lastError = self._or([_G_or_245, _G_or_247, _G_or_249, _G_or_251, _G_or_253, _G_or_255, _G_or_257, _G_or_259, _G_or_261, _G_or_263, _G_or_265, _G_or_267, _G_or_269, _G_or_271, _G_or_273, _G_or_275, _G_or_277, _G_or_279, _G_or_281, _G_or_283, _G_or_285, _G_or_287, _G_or_289])
                self.considerError(lastError)
                return (_G_or_291, self.currentError)
            _G_many1_292, lastError = self.many(_G_many1_244, _G_many1_244())
            self.considerError(lastError)
            return (_G_many1_292, self.currentError)
        _G_consumedby_293, lastError = self.consumedby(_G_consumedby_243)
        self.considerError(lastError)
        return (_G_consumedby_293, self.currentError)
