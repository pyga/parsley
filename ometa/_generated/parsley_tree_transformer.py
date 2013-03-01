def createParserClass(GrammarBase, ruleGlobals):
    if ruleGlobals is None:
        ruleGlobals = {}
    class parsley_tree_transformer(GrammarBase):
        def rule_termPattern(self):
            _locals = {'self': self}
            self.locals['termPattern'] = _locals
            def _G_optional_1():
                _G_apply_2, lastError = self._apply(self.rule_indentation, "indentation", [])
                self.considerError(lastError, None)
                return (_G_apply_2, self.currentError)
            def _G_optional_3():
                return (None, self.input.nullError())
            _G_or_4, lastError = self._or([_G_optional_1, _G_optional_3])
            self.considerError(lastError, 'termPattern')
            _G_apply_5, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'termPattern')
            _locals['name'] = _G_apply_5
            def _G_pred_6():
                _G_python_7, lastError = eval('name[0].isupper()', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_7, self.currentError)
            _G_pred_8, lastError = self.pred(_G_pred_6)
            self.considerError(lastError, 'termPattern')
            _G_exactly_9, lastError = self.exactly('(')
            self.considerError(lastError, 'termPattern')
            _G_apply_10, lastError = self._apply(self.rule_expr, "expr", [])
            self.considerError(lastError, 'termPattern')
            _locals['patts'] = _G_apply_10
            _G_exactly_11, lastError = self.exactly(')')
            self.considerError(lastError, 'termPattern')
            _G_python_12, lastError = eval('t.TermPattern(name, patts)', self.globals, _locals), None
            self.considerError(lastError, 'termPattern')
            return (_G_python_12, self.currentError)


        def rule_subtransform(self):
            _locals = {'self': self}
            self.locals['subtransform'] = _locals
            _G_apply_13, lastError = self._apply(self.rule_token, "token", ["@"])
            self.considerError(lastError, 'subtransform')
            _G_apply_14, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'subtransform')
            _locals['n'] = _G_apply_14
            _G_python_15, lastError = eval("t.Bind(n, t.Apply('transform', self.rulename, []))", self.globals, _locals), None
            self.considerError(lastError, 'subtransform')
            return (_G_python_15, self.currentError)


        def rule_wide_templatedValue(self):
            _locals = {'self': self}
            self.locals['wide_templatedValue'] = _locals
            _G_python_16, lastError = "-->", None
            self.considerError(lastError, 'wide_templatedValue')
            _G_apply_17, lastError = self._apply(self.rule_token, "token", [_G_python_16])
            self.considerError(lastError, 'wide_templatedValue')
            def _G_many_18():
                _G_exactly_19, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                return (_G_exactly_19, self.currentError)
            _G_many_20, lastError = self.many(_G_many_18)
            self.considerError(lastError, 'wide_templatedValue')
            _G_apply_21, lastError = self._apply(self.rule_wideTemplateBits, "wideTemplateBits", [])
            self.considerError(lastError, 'wide_templatedValue')
            _locals['contents'] = _G_apply_21
            _G_python_22, lastError = eval('t.StringTemplate(contents)', self.globals, _locals), None
            self.considerError(lastError, 'wide_templatedValue')
            return (_G_python_22, self.currentError)


        def rule_tall_templatedValue(self):
            _locals = {'self': self}
            self.locals['tall_templatedValue'] = _locals
            def _G_optional_23():
                _G_apply_24, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError, None)
                return (_G_apply_24, self.currentError)
            def _G_optional_25():
                return (None, self.input.nullError())
            _G_or_26, lastError = self._or([_G_optional_23, _G_optional_25])
            self.considerError(lastError, 'tall_templatedValue')
            _G_exactly_27, lastError = self.exactly('{{{')
            self.considerError(lastError, 'tall_templatedValue')
            def _G_many_28():
                def _G_or_29():
                    _G_exactly_30, lastError = self.exactly(' ')
                    self.considerError(lastError, None)
                    return (_G_exactly_30, self.currentError)
                def _G_or_31():
                    _G_exactly_32, lastError = self.exactly('\t')
                    self.considerError(lastError, None)
                    return (_G_exactly_32, self.currentError)
                _G_or_33, lastError = self._or([_G_or_29, _G_or_31])
                self.considerError(lastError, None)
                return (_G_or_33, self.currentError)
            _G_many_34, lastError = self.many(_G_many_28)
            self.considerError(lastError, 'tall_templatedValue')
            def _G_optional_35():
                _G_apply_36, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError, None)
                return (_G_apply_36, self.currentError)
            def _G_optional_37():
                return (None, self.input.nullError())
            _G_or_38, lastError = self._or([_G_optional_35, _G_optional_37])
            self.considerError(lastError, 'tall_templatedValue')
            _G_apply_39, lastError = self._apply(self.rule_tallTemplateBits, "tallTemplateBits", [])
            self.considerError(lastError, 'tall_templatedValue')
            _locals['contents'] = _G_apply_39
            _G_exactly_40, lastError = self.exactly('}}}')
            self.considerError(lastError, 'tall_templatedValue')
            _G_python_41, lastError = eval('t.StringTemplate(contents)', self.globals, _locals), None
            self.considerError(lastError, 'tall_templatedValue')
            return (_G_python_41, self.currentError)


        def rule_tallTemplateBits(self):
            _locals = {'self': self}
            self.locals['tallTemplateBits'] = _locals
            def _G_many_42():
                def _G_or_43():
                    _G_apply_44, lastError = self._apply(self.rule_exprHole, "exprHole", [])
                    self.considerError(lastError, None)
                    return (_G_apply_44, self.currentError)
                def _G_or_45():
                    _G_apply_46, lastError = self._apply(self.rule_tallTemplateText, "tallTemplateText", [])
                    self.considerError(lastError, None)
                    return (_G_apply_46, self.currentError)
                _G_or_47, lastError = self._or([_G_or_43, _G_or_45])
                self.considerError(lastError, None)
                return (_G_or_47, self.currentError)
            _G_many_48, lastError = self.many(_G_many_42)
            self.considerError(lastError, 'tallTemplateBits')
            return (_G_many_48, self.currentError)


        def rule_tallTemplateText(self):
            _locals = {'self': self}
            self.locals['tallTemplateText'] = _locals
            def _G_or_49():
                def _G_consumedby_50():
                    def _G_many1_51():
                        def _G_or_52():
                            def _G_not_53():
                                def _G_or_54():
                                    _G_exactly_55, lastError = self.exactly('}}}')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_55, self.currentError)
                                def _G_or_56():
                                    _G_exactly_57, lastError = self.exactly('$')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_57, self.currentError)
                                def _G_or_58():
                                    _G_exactly_59, lastError = self.exactly('\r')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_59, self.currentError)
                                def _G_or_60():
                                    _G_exactly_61, lastError = self.exactly('\n')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_61, self.currentError)
                                _G_or_62, lastError = self._or([_G_or_54, _G_or_56, _G_or_58, _G_or_60])
                                self.considerError(lastError, None)
                                return (_G_or_62, self.currentError)
                            _G_not_63, lastError = self._not(_G_not_53)
                            self.considerError(lastError, None)
                            _G_apply_64, lastError = self._apply(self.rule_anything, "anything", [])
                            self.considerError(lastError, None)
                            return (_G_apply_64, self.currentError)
                        def _G_or_65():
                            _G_exactly_66, lastError = self.exactly('$')
                            self.considerError(lastError, None)
                            _G_exactly_67, lastError = self.exactly('$')
                            self.considerError(lastError, None)
                            return (_G_exactly_67, self.currentError)
                        _G_or_68, lastError = self._or([_G_or_52, _G_or_65])
                        self.considerError(lastError, None)
                        return (_G_or_68, self.currentError)
                    _G_many1_69, lastError = self.many(_G_many1_51, _G_many1_51())
                    self.considerError(lastError, None)
                    def _G_many_70():
                        _G_apply_71, lastError = self._apply(self.rule_vspace, "vspace", [])
                        self.considerError(lastError, None)
                        return (_G_apply_71, self.currentError)
                    _G_many_72, lastError = self.many(_G_many_70)
                    self.considerError(lastError, None)
                    return (_G_many_72, self.currentError)
                _G_consumedby_73, lastError = self.consumedby(_G_consumedby_50)
                self.considerError(lastError, None)
                return (_G_consumedby_73, self.currentError)
            def _G_or_74():
                _G_apply_75, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError, None)
                return (_G_apply_75, self.currentError)
            _G_or_76, lastError = self._or([_G_or_49, _G_or_74])
            self.considerError(lastError, 'tallTemplateText')
            return (_G_or_76, self.currentError)


        def rule_wideTemplateBits(self):
            _locals = {'self': self}
            self.locals['wideTemplateBits'] = _locals
            def _G_many_77():
                def _G_or_78():
                    _G_apply_79, lastError = self._apply(self.rule_exprHole, "exprHole", [])
                    self.considerError(lastError, None)
                    return (_G_apply_79, self.currentError)
                def _G_or_80():
                    _G_apply_81, lastError = self._apply(self.rule_wideTemplateText, "wideTemplateText", [])
                    self.considerError(lastError, None)
                    return (_G_apply_81, self.currentError)
                _G_or_82, lastError = self._or([_G_or_78, _G_or_80])
                self.considerError(lastError, None)
                return (_G_or_82, self.currentError)
            _G_many_83, lastError = self.many(_G_many_77)
            self.considerError(lastError, 'wideTemplateBits')
            return (_G_many_83, self.currentError)


        def rule_wideTemplateText(self):
            _locals = {'self': self}
            self.locals['wideTemplateText'] = _locals
            def _G_consumedby_84():
                def _G_many1_85():
                    def _G_or_86():
                        def _G_not_87():
                            def _G_or_88():
                                _G_apply_89, lastError = self._apply(self.rule_vspace, "vspace", [])
                                self.considerError(lastError, None)
                                return (_G_apply_89, self.currentError)
                            def _G_or_90():
                                _G_apply_91, lastError = self._apply(self.rule_end, "end", [])
                                self.considerError(lastError, None)
                                return (_G_apply_91, self.currentError)
                            def _G_or_92():
                                _G_exactly_93, lastError = self.exactly('$')
                                self.considerError(lastError, None)
                                return (_G_exactly_93, self.currentError)
                            _G_or_94, lastError = self._or([_G_or_88, _G_or_90, _G_or_92])
                            self.considerError(lastError, None)
                            return (_G_or_94, self.currentError)
                        _G_not_95, lastError = self._not(_G_not_87)
                        self.considerError(lastError, None)
                        _G_apply_96, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_96, self.currentError)
                    def _G_or_97():
                        _G_exactly_98, lastError = self.exactly('$')
                        self.considerError(lastError, None)
                        _G_exactly_99, lastError = self.exactly('$')
                        self.considerError(lastError, None)
                        return (_G_exactly_99, self.currentError)
                    _G_or_100, lastError = self._or([_G_or_86, _G_or_97])
                    self.considerError(lastError, None)
                    return (_G_or_100, self.currentError)
                _G_many1_101, lastError = self.many(_G_many1_85, _G_many1_85())
                self.considerError(lastError, None)
                return (_G_many1_101, self.currentError)
            _G_consumedby_102, lastError = self.consumedby(_G_consumedby_84)
            self.considerError(lastError, 'wideTemplateText')
            return (_G_consumedby_102, self.currentError)


        def rule_exprHole(self):
            _locals = {'self': self}
            self.locals['exprHole'] = _locals
            _G_exactly_103, lastError = self.exactly('$')
            self.considerError(lastError, 'exprHole')
            _G_apply_104, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'exprHole')
            _locals['n'] = _G_apply_104
            _G_python_105, lastError = eval('t.QuasiExprHole(n)', self.globals, _locals), None
            self.considerError(lastError, 'exprHole')
            return (_G_python_105, self.currentError)


        def rule_expr1(self):
            _locals = {'self': self}
            self.locals['expr1'] = _locals
            def _G_or_106():
                _G_apply_107, lastError = self._apply(self.rule_foreignApply, "foreignApply", [])
                self.considerError(lastError, None)
                return (_G_apply_107, self.currentError)
            def _G_or_108():
                _G_apply_109, lastError = self._apply(self.rule_termPattern, "termPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_109, self.currentError)
            def _G_or_110():
                _G_apply_111, lastError = self._apply(self.rule_subtransform, "subtransform", [])
                self.considerError(lastError, None)
                return (_G_apply_111, self.currentError)
            def _G_or_112():
                _G_apply_113, lastError = self._apply(self.rule_application, "application", [])
                self.considerError(lastError, None)
                return (_G_apply_113, self.currentError)
            def _G_or_114():
                _G_apply_115, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
                self.considerError(lastError, None)
                return (_G_apply_115, self.currentError)
            def _G_or_116():
                _G_apply_117, lastError = self._apply(self.rule_wide_templatedValue, "wide_templatedValue", [])
                self.considerError(lastError, None)
                return (_G_apply_117, self.currentError)
            def _G_or_118():
                _G_apply_119, lastError = self._apply(self.rule_tall_templatedValue, "tall_templatedValue", [])
                self.considerError(lastError, None)
                return (_G_apply_119, self.currentError)
            def _G_or_120():
                _G_apply_121, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
                self.considerError(lastError, None)
                return (_G_apply_121, self.currentError)
            def _G_or_122():
                _G_apply_123, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
                self.considerError(lastError, None)
                return (_G_apply_123, self.currentError)
            def _G_or_124():
                _G_apply_125, lastError = self._apply(self.rule_number, "number", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_125
                _G_python_126, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_127, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_127, self.currentError)
            def _G_or_128():
                _G_apply_129, lastError = self._apply(self.rule_character, "character", [])
                self.considerError(lastError, None)
                return (_G_apply_129, self.currentError)
            def _G_or_130():
                _G_apply_131, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                return (_G_apply_131, self.currentError)
            def _G_or_132():
                _G_python_133, lastError = '(', None
                self.considerError(lastError, None)
                _G_apply_134, lastError = self._apply(self.rule_token, "token", [_G_python_133])
                self.considerError(lastError, None)
                _G_apply_135, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_135
                _G_python_136, lastError = ')', None
                self.considerError(lastError, None)
                _G_apply_137, lastError = self._apply(self.rule_token, "token", [_G_python_136])
                self.considerError(lastError, None)
                _G_python_138, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_138, self.currentError)
            def _G_or_139():
                _G_python_140, lastError = '[', None
                self.considerError(lastError, None)
                _G_apply_141, lastError = self._apply(self.rule_token, "token", [_G_python_140])
                self.considerError(lastError, None)
                def _G_optional_142():
                    _G_apply_143, lastError = self._apply(self.rule_expr, "expr", [])
                    self.considerError(lastError, None)
                    return (_G_apply_143, self.currentError)
                def _G_optional_144():
                    return (None, self.input.nullError())
                _G_or_145, lastError = self._or([_G_optional_142, _G_optional_144])
                self.considerError(lastError, None)
                _locals['e'] = _G_or_145
                _G_python_146, lastError = ']', None
                self.considerError(lastError, None)
                _G_apply_147, lastError = self._apply(self.rule_token, "token", [_G_python_146])
                self.considerError(lastError, None)
                _G_python_148, lastError = eval('t.TermPattern(".tuple.", e or t.And([]))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_148, self.currentError)
            _G_or_149, lastError = self._or([_G_or_106, _G_or_108, _G_or_110, _G_or_112, _G_or_114, _G_or_116, _G_or_118, _G_or_120, _G_or_122, _G_or_124, _G_or_128, _G_or_130, _G_or_132, _G_or_139])
            self.considerError(lastError, 'expr1')
            return (_G_or_149, self.currentError)


        def rule_grammar(self):
            _locals = {'self': self}
            self.locals['grammar'] = _locals
            def _G_many_150():
                _G_apply_151, lastError = self._apply(self.rule_rule, "rule", [])
                self.considerError(lastError, None)
                return (_G_apply_151, self.currentError)
            _G_many_152, lastError = self.many(_G_many_150)
            self.considerError(lastError, 'grammar')
            _locals['rs'] = _G_many_152
            _G_apply_153, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'grammar')
            _G_python_154, lastError = eval('t.Grammar(self.name, True, rs)', self.globals, _locals), None
            self.considerError(lastError, 'grammar')
            return (_G_python_154, self.currentError)


    if parsley_tree_transformer.globals is not None:
        parsley_tree_transformer.globals = parsley_tree_transformer.globals.copy()
        parsley_tree_transformer.globals.update(ruleGlobals)
    else:
        parsley_tree_transformer.globals = ruleGlobals
    return parsley_tree_transformer