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
            _G_apply_28, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'tall_templatedValue')
            _G_apply_29, lastError = self._apply(self.rule_tallTemplateBits, "tallTemplateBits", [])
            self.considerError(lastError, 'tall_templatedValue')
            _locals['contents'] = _G_apply_29
            _G_exactly_30, lastError = self.exactly('}}}')
            self.considerError(lastError, 'tall_templatedValue')
            _G_python_31, lastError = eval('t.StringTemplate(contents)', self.globals, _locals), None
            self.considerError(lastError, 'tall_templatedValue')
            return (_G_python_31, self.currentError)


        def rule_tallTemplateBits(self):
            _locals = {'self': self}
            self.locals['tallTemplateBits'] = _locals
            def _G_many_32():
                def _G_or_33():
                    _G_apply_34, lastError = self._apply(self.rule_exprHole, "exprHole", [])
                    self.considerError(lastError, None)
                    return (_G_apply_34, self.currentError)
                def _G_or_35():
                    _G_apply_36, lastError = self._apply(self.rule_tallTemplateText, "tallTemplateText", [])
                    self.considerError(lastError, None)
                    return (_G_apply_36, self.currentError)
                _G_or_37, lastError = self._or([_G_or_33, _G_or_35])
                self.considerError(lastError, None)
                return (_G_or_37, self.currentError)
            _G_many_38, lastError = self.many(_G_many_32)
            self.considerError(lastError, 'tallTemplateBits')
            return (_G_many_38, self.currentError)


        def rule_tallTemplateText(self):
            _locals = {'self': self}
            self.locals['tallTemplateText'] = _locals
            def _G_or_39():
                def _G_consumedby_40():
                    def _G_many1_41():
                        def _G_or_42():
                            def _G_not_43():
                                def _G_or_44():
                                    _G_exactly_45, lastError = self.exactly('}}}')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_45, self.currentError)
                                def _G_or_46():
                                    _G_exactly_47, lastError = self.exactly('$')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_47, self.currentError)
                                def _G_or_48():
                                    _G_exactly_49, lastError = self.exactly('\r')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_49, self.currentError)
                                def _G_or_50():
                                    _G_exactly_51, lastError = self.exactly('\n')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_51, self.currentError)
                                _G_or_52, lastError = self._or([_G_or_44, _G_or_46, _G_or_48, _G_or_50])
                                self.considerError(lastError, None)
                                return (_G_or_52, self.currentError)
                            _G_not_53, lastError = self._not(_G_not_43)
                            self.considerError(lastError, None)
                            _G_apply_54, lastError = self._apply(self.rule_anything, "anything", [])
                            self.considerError(lastError, None)
                            return (_G_apply_54, self.currentError)
                        def _G_or_55():
                            _G_exactly_56, lastError = self.exactly('$')
                            self.considerError(lastError, None)
                            _G_exactly_57, lastError = self.exactly('$')
                            self.considerError(lastError, None)
                            return (_G_exactly_57, self.currentError)
                        _G_or_58, lastError = self._or([_G_or_42, _G_or_55])
                        self.considerError(lastError, None)
                        return (_G_or_58, self.currentError)
                    _G_many1_59, lastError = self.many(_G_many1_41, _G_many1_41())
                    self.considerError(lastError, None)
                    def _G_optional_60():
                        _G_apply_61, lastError = self._apply(self.rule_vspace, "vspace", [])
                        self.considerError(lastError, None)
                        return (_G_apply_61, self.currentError)
                    def _G_optional_62():
                        return (None, self.input.nullError())
                    _G_or_63, lastError = self._or([_G_optional_60, _G_optional_62])
                    self.considerError(lastError, None)
                    return (_G_or_63, self.currentError)
                _G_consumedby_64, lastError = self.consumedby(_G_consumedby_40)
                self.considerError(lastError, None)
                return (_G_consumedby_64, self.currentError)
            def _G_or_65():
                _G_apply_66, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError, None)
                return (_G_apply_66, self.currentError)
            _G_or_67, lastError = self._or([_G_or_39, _G_or_65])
            self.considerError(lastError, 'tallTemplateText')
            return (_G_or_67, self.currentError)


        def rule_wideTemplateBits(self):
            _locals = {'self': self}
            self.locals['wideTemplateBits'] = _locals
            def _G_many_68():
                def _G_or_69():
                    _G_apply_70, lastError = self._apply(self.rule_exprHole, "exprHole", [])
                    self.considerError(lastError, None)
                    return (_G_apply_70, self.currentError)
                def _G_or_71():
                    _G_apply_72, lastError = self._apply(self.rule_wideTemplateText, "wideTemplateText", [])
                    self.considerError(lastError, None)
                    return (_G_apply_72, self.currentError)
                _G_or_73, lastError = self._or([_G_or_69, _G_or_71])
                self.considerError(lastError, None)
                return (_G_or_73, self.currentError)
            _G_many_74, lastError = self.many(_G_many_68)
            self.considerError(lastError, 'wideTemplateBits')
            return (_G_many_74, self.currentError)


        def rule_wideTemplateText(self):
            _locals = {'self': self}
            self.locals['wideTemplateText'] = _locals
            def _G_consumedby_75():
                def _G_many1_76():
                    def _G_or_77():
                        def _G_not_78():
                            def _G_or_79():
                                _G_apply_80, lastError = self._apply(self.rule_vspace, "vspace", [])
                                self.considerError(lastError, None)
                                return (_G_apply_80, self.currentError)
                            def _G_or_81():
                                _G_apply_82, lastError = self._apply(self.rule_end, "end", [])
                                self.considerError(lastError, None)
                                return (_G_apply_82, self.currentError)
                            def _G_or_83():
                                _G_exactly_84, lastError = self.exactly('$')
                                self.considerError(lastError, None)
                                return (_G_exactly_84, self.currentError)
                            _G_or_85, lastError = self._or([_G_or_79, _G_or_81, _G_or_83])
                            self.considerError(lastError, None)
                            return (_G_or_85, self.currentError)
                        _G_not_86, lastError = self._not(_G_not_78)
                        self.considerError(lastError, None)
                        _G_apply_87, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_87, self.currentError)
                    def _G_or_88():
                        _G_exactly_89, lastError = self.exactly('$')
                        self.considerError(lastError, None)
                        _G_exactly_90, lastError = self.exactly('$')
                        self.considerError(lastError, None)
                        return (_G_exactly_90, self.currentError)
                    _G_or_91, lastError = self._or([_G_or_77, _G_or_88])
                    self.considerError(lastError, None)
                    return (_G_or_91, self.currentError)
                _G_many1_92, lastError = self.many(_G_many1_76, _G_many1_76())
                self.considerError(lastError, None)
                return (_G_many1_92, self.currentError)
            _G_consumedby_93, lastError = self.consumedby(_G_consumedby_75)
            self.considerError(lastError, 'wideTemplateText')
            return (_G_consumedby_93, self.currentError)


        def rule_exprHole(self):
            _locals = {'self': self}
            self.locals['exprHole'] = _locals
            _G_exactly_94, lastError = self.exactly('$')
            self.considerError(lastError, 'exprHole')
            _G_apply_95, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'exprHole')
            _locals['n'] = _G_apply_95
            _G_python_96, lastError = eval('t.QuasiExprHole(n)', self.globals, _locals), None
            self.considerError(lastError, 'exprHole')
            return (_G_python_96, self.currentError)


        def rule_expr1(self):
            _locals = {'self': self}
            self.locals['expr1'] = _locals
            def _G_or_97():
                _G_apply_98, lastError = self._apply(self.rule_foreignApply, "foreignApply", [])
                self.considerError(lastError, None)
                return (_G_apply_98, self.currentError)
            def _G_or_99():
                _G_apply_100, lastError = self._apply(self.rule_termPattern, "termPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_100, self.currentError)
            def _G_or_101():
                _G_apply_102, lastError = self._apply(self.rule_subtransform, "subtransform", [])
                self.considerError(lastError, None)
                return (_G_apply_102, self.currentError)
            def _G_or_103():
                _G_apply_104, lastError = self._apply(self.rule_application, "application", [])
                self.considerError(lastError, None)
                return (_G_apply_104, self.currentError)
            def _G_or_105():
                _G_apply_106, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
                self.considerError(lastError, None)
                return (_G_apply_106, self.currentError)
            def _G_or_107():
                _G_apply_108, lastError = self._apply(self.rule_wide_templatedValue, "wide_templatedValue", [])
                self.considerError(lastError, None)
                return (_G_apply_108, self.currentError)
            def _G_or_109():
                _G_apply_110, lastError = self._apply(self.rule_tall_templatedValue, "tall_templatedValue", [])
                self.considerError(lastError, None)
                return (_G_apply_110, self.currentError)
            def _G_or_111():
                _G_apply_112, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
                self.considerError(lastError, None)
                return (_G_apply_112, self.currentError)
            def _G_or_113():
                _G_apply_114, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
                self.considerError(lastError, None)
                return (_G_apply_114, self.currentError)
            def _G_or_115():
                _G_apply_116, lastError = self._apply(self.rule_number, "number", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_116
                _G_python_117, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_118, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_118, self.currentError)
            def _G_or_119():
                _G_apply_120, lastError = self._apply(self.rule_character, "character", [])
                self.considerError(lastError, None)
                return (_G_apply_120, self.currentError)
            def _G_or_121():
                _G_apply_122, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                return (_G_apply_122, self.currentError)
            def _G_or_123():
                _G_python_124, lastError = '(', None
                self.considerError(lastError, None)
                _G_apply_125, lastError = self._apply(self.rule_token, "token", [_G_python_124])
                self.considerError(lastError, None)
                _G_apply_126, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_126
                _G_python_127, lastError = ')', None
                self.considerError(lastError, None)
                _G_apply_128, lastError = self._apply(self.rule_token, "token", [_G_python_127])
                self.considerError(lastError, None)
                _G_python_129, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_129, self.currentError)
            def _G_or_130():
                _G_python_131, lastError = '[', None
                self.considerError(lastError, None)
                _G_apply_132, lastError = self._apply(self.rule_token, "token", [_G_python_131])
                self.considerError(lastError, None)
                _G_apply_133, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_133
                _G_python_134, lastError = ']', None
                self.considerError(lastError, None)
                _G_apply_135, lastError = self._apply(self.rule_token, "token", [_G_python_134])
                self.considerError(lastError, None)
                _G_python_136, lastError = eval('t.TermPattern(".tuple.", e)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_136, self.currentError)
            _G_or_137, lastError = self._or([_G_or_97, _G_or_99, _G_or_101, _G_or_103, _G_or_105, _G_or_107, _G_or_109, _G_or_111, _G_or_113, _G_or_115, _G_or_119, _G_or_121, _G_or_123, _G_or_130])
            self.considerError(lastError, 'expr1')
            return (_G_or_137, self.currentError)


        def rule_grammar(self):
            _locals = {'self': self}
            self.locals['grammar'] = _locals
            def _G_many_138():
                _G_apply_139, lastError = self._apply(self.rule_rule, "rule", [])
                self.considerError(lastError, None)
                return (_G_apply_139, self.currentError)
            _G_many_140, lastError = self.many(_G_many_138)
            self.considerError(lastError, 'grammar')
            _locals['rs'] = _G_many_140
            _G_apply_141, lastError = self._apply(self.rule_spaces, "spaces", [])
            self.considerError(lastError, 'grammar')
            _G_python_142, lastError = eval('t.Grammar(self.name, True, rs)', self.globals, _locals), None
            self.considerError(lastError, 'grammar')
            return (_G_python_142, self.currentError)


    if parsley_tree_transformer.globals is not None:
        parsley_tree_transformer.globals = parsley_tree_transformer.globals.copy()
        parsley_tree_transformer.globals.update(ruleGlobals)
    else:
        parsley_tree_transformer.globals = ruleGlobals
    return parsley_tree_transformer