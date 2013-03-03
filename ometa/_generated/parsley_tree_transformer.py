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
            _G_apply_13, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'subtransform')
            _G_exactly_14, lastError = self.exactly('@')
            self.considerError(lastError, 'subtransform')
            _G_apply_15, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'subtransform')
            _locals['n'] = _G_apply_15
            _G_python_16, lastError = eval("t.Bind(n, t.Apply('transform', self.rulename, []))", self.globals, _locals), None
            self.considerError(lastError, 'subtransform')
            return (_G_python_16, self.currentError)


        def rule_wide_templatedValue(self):
            _locals = {'self': self}
            self.locals['wide_templatedValue'] = _locals
            _G_apply_17, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'wide_templatedValue')
            _G_exactly_18, lastError = self.exactly('-->')
            self.considerError(lastError, 'wide_templatedValue')
            def _G_many_19():
                _G_exactly_20, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                return (_G_exactly_20, self.currentError)
            _G_many_21, lastError = self.many(_G_many_19)
            self.considerError(lastError, 'wide_templatedValue')
            _G_apply_22, lastError = self._apply(self.rule_wideTemplateBits, "wideTemplateBits", [])
            self.considerError(lastError, 'wide_templatedValue')
            _locals['contents'] = _G_apply_22
            _G_python_23, lastError = eval('t.StringTemplate(contents)', self.globals, _locals), None
            self.considerError(lastError, 'wide_templatedValue')
            return (_G_python_23, self.currentError)


        def rule_tall_templatedValue(self):
            _locals = {'self': self}
            self.locals['tall_templatedValue'] = _locals
            def _G_optional_24():
                _G_apply_25, lastError = self._apply(self.rule_hspace, "hspace", [])
                self.considerError(lastError, None)
                return (_G_apply_25, self.currentError)
            def _G_optional_26():
                return (None, self.input.nullError())
            _G_or_27, lastError = self._or([_G_optional_24, _G_optional_26])
            self.considerError(lastError, 'tall_templatedValue')
            _G_exactly_28, lastError = self.exactly('{{{')
            self.considerError(lastError, 'tall_templatedValue')
            def _G_many_29():
                def _G_or_30():
                    _G_exactly_31, lastError = self.exactly(' ')
                    self.considerError(lastError, None)
                    return (_G_exactly_31, self.currentError)
                def _G_or_32():
                    _G_exactly_33, lastError = self.exactly('\t')
                    self.considerError(lastError, None)
                    return (_G_exactly_33, self.currentError)
                _G_or_34, lastError = self._or([_G_or_30, _G_or_32])
                self.considerError(lastError, None)
                return (_G_or_34, self.currentError)
            _G_many_35, lastError = self.many(_G_many_29)
            self.considerError(lastError, 'tall_templatedValue')
            def _G_optional_36():
                _G_apply_37, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError, None)
                return (_G_apply_37, self.currentError)
            def _G_optional_38():
                return (None, self.input.nullError())
            _G_or_39, lastError = self._or([_G_optional_36, _G_optional_38])
            self.considerError(lastError, 'tall_templatedValue')
            _G_apply_40, lastError = self._apply(self.rule_tallTemplateBits, "tallTemplateBits", [])
            self.considerError(lastError, 'tall_templatedValue')
            _locals['contents'] = _G_apply_40
            _G_exactly_41, lastError = self.exactly('}}}')
            self.considerError(lastError, 'tall_templatedValue')
            _G_python_42, lastError = eval('t.StringTemplate(contents)', self.globals, _locals), None
            self.considerError(lastError, 'tall_templatedValue')
            return (_G_python_42, self.currentError)


        def rule_tallTemplateBits(self):
            _locals = {'self': self}
            self.locals['tallTemplateBits'] = _locals
            def _G_many_43():
                def _G_or_44():
                    _G_apply_45, lastError = self._apply(self.rule_exprHole, "exprHole", [])
                    self.considerError(lastError, None)
                    return (_G_apply_45, self.currentError)
                def _G_or_46():
                    _G_apply_47, lastError = self._apply(self.rule_tallTemplateText, "tallTemplateText", [])
                    self.considerError(lastError, None)
                    return (_G_apply_47, self.currentError)
                _G_or_48, lastError = self._or([_G_or_44, _G_or_46])
                self.considerError(lastError, None)
                return (_G_or_48, self.currentError)
            _G_many_49, lastError = self.many(_G_many_43)
            self.considerError(lastError, 'tallTemplateBits')
            return (_G_many_49, self.currentError)


        def rule_tallTemplateText(self):
            _locals = {'self': self}
            self.locals['tallTemplateText'] = _locals
            def _G_or_50():
                def _G_consumedby_51():
                    def _G_many1_52():
                        def _G_or_53():
                            def _G_not_54():
                                def _G_or_55():
                                    _G_exactly_56, lastError = self.exactly('}}}')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_56, self.currentError)
                                def _G_or_57():
                                    _G_exactly_58, lastError = self.exactly('$')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_58, self.currentError)
                                def _G_or_59():
                                    _G_exactly_60, lastError = self.exactly('\r')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_60, self.currentError)
                                def _G_or_61():
                                    _G_exactly_62, lastError = self.exactly('\n')
                                    self.considerError(lastError, None)
                                    return (_G_exactly_62, self.currentError)
                                _G_or_63, lastError = self._or([_G_or_55, _G_or_57, _G_or_59, _G_or_61])
                                self.considerError(lastError, None)
                                return (_G_or_63, self.currentError)
                            _G_not_64, lastError = self._not(_G_not_54)
                            self.considerError(lastError, None)
                            _G_apply_65, lastError = self._apply(self.rule_anything, "anything", [])
                            self.considerError(lastError, None)
                            return (_G_apply_65, self.currentError)
                        def _G_or_66():
                            _G_exactly_67, lastError = self.exactly('$')
                            self.considerError(lastError, None)
                            _G_exactly_68, lastError = self.exactly('$')
                            self.considerError(lastError, None)
                            return (_G_exactly_68, self.currentError)
                        _G_or_69, lastError = self._or([_G_or_53, _G_or_66])
                        self.considerError(lastError, None)
                        return (_G_or_69, self.currentError)
                    _G_many1_70, lastError = self.many(_G_many1_52, _G_many1_52())
                    self.considerError(lastError, None)
                    def _G_many_71():
                        _G_apply_72, lastError = self._apply(self.rule_vspace, "vspace", [])
                        self.considerError(lastError, None)
                        return (_G_apply_72, self.currentError)
                    _G_many_73, lastError = self.many(_G_many_71)
                    self.considerError(lastError, None)
                    return (_G_many_73, self.currentError)
                _G_consumedby_74, lastError = self.consumedby(_G_consumedby_51)
                self.considerError(lastError, None)
                return (_G_consumedby_74, self.currentError)
            def _G_or_75():
                _G_apply_76, lastError = self._apply(self.rule_vspace, "vspace", [])
                self.considerError(lastError, None)
                return (_G_apply_76, self.currentError)
            _G_or_77, lastError = self._or([_G_or_50, _G_or_75])
            self.considerError(lastError, 'tallTemplateText')
            return (_G_or_77, self.currentError)


        def rule_wideTemplateBits(self):
            _locals = {'self': self}
            self.locals['wideTemplateBits'] = _locals
            def _G_many_78():
                def _G_or_79():
                    _G_apply_80, lastError = self._apply(self.rule_exprHole, "exprHole", [])
                    self.considerError(lastError, None)
                    return (_G_apply_80, self.currentError)
                def _G_or_81():
                    _G_apply_82, lastError = self._apply(self.rule_wideTemplateText, "wideTemplateText", [])
                    self.considerError(lastError, None)
                    return (_G_apply_82, self.currentError)
                _G_or_83, lastError = self._or([_G_or_79, _G_or_81])
                self.considerError(lastError, None)
                return (_G_or_83, self.currentError)
            _G_many_84, lastError = self.many(_G_many_78)
            self.considerError(lastError, 'wideTemplateBits')
            return (_G_many_84, self.currentError)


        def rule_wideTemplateText(self):
            _locals = {'self': self}
            self.locals['wideTemplateText'] = _locals
            def _G_consumedby_85():
                def _G_many1_86():
                    def _G_or_87():
                        def _G_not_88():
                            def _G_or_89():
                                _G_apply_90, lastError = self._apply(self.rule_vspace, "vspace", [])
                                self.considerError(lastError, None)
                                return (_G_apply_90, self.currentError)
                            def _G_or_91():
                                _G_apply_92, lastError = self._apply(self.rule_end, "end", [])
                                self.considerError(lastError, None)
                                return (_G_apply_92, self.currentError)
                            def _G_or_93():
                                _G_exactly_94, lastError = self.exactly('$')
                                self.considerError(lastError, None)
                                return (_G_exactly_94, self.currentError)
                            _G_or_95, lastError = self._or([_G_or_89, _G_or_91, _G_or_93])
                            self.considerError(lastError, None)
                            return (_G_or_95, self.currentError)
                        _G_not_96, lastError = self._not(_G_not_88)
                        self.considerError(lastError, None)
                        _G_apply_97, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_97, self.currentError)
                    def _G_or_98():
                        _G_exactly_99, lastError = self.exactly('$')
                        self.considerError(lastError, None)
                        _G_exactly_100, lastError = self.exactly('$')
                        self.considerError(lastError, None)
                        return (_G_exactly_100, self.currentError)
                    _G_or_101, lastError = self._or([_G_or_87, _G_or_98])
                    self.considerError(lastError, None)
                    return (_G_or_101, self.currentError)
                _G_many1_102, lastError = self.many(_G_many1_86, _G_many1_86())
                self.considerError(lastError, None)
                return (_G_many1_102, self.currentError)
            _G_consumedby_103, lastError = self.consumedby(_G_consumedby_85)
            self.considerError(lastError, 'wideTemplateText')
            return (_G_consumedby_103, self.currentError)


        def rule_exprHole(self):
            _locals = {'self': self}
            self.locals['exprHole'] = _locals
            _G_exactly_104, lastError = self.exactly('$')
            self.considerError(lastError, 'exprHole')
            _G_apply_105, lastError = self._apply(self.rule_name, "name", [])
            self.considerError(lastError, 'exprHole')
            _locals['n'] = _G_apply_105
            _G_python_106, lastError = eval('t.QuasiExprHole(n)', self.globals, _locals), None
            self.considerError(lastError, 'exprHole')
            return (_G_python_106, self.currentError)


        def rule_expr1(self):
            _locals = {'self': self}
            self.locals['expr1'] = _locals
            def _G_or_107():
                _G_apply_108, lastError = self._apply(self.rule_foreignApply, "foreignApply", [])
                self.considerError(lastError, None)
                return (_G_apply_108, self.currentError)
            def _G_or_109():
                _G_apply_110, lastError = self._apply(self.rule_termPattern, "termPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_110, self.currentError)
            def _G_or_111():
                _G_apply_112, lastError = self._apply(self.rule_subtransform, "subtransform", [])
                self.considerError(lastError, None)
                return (_G_apply_112, self.currentError)
            def _G_or_113():
                _G_apply_114, lastError = self._apply(self.rule_application, "application", [])
                self.considerError(lastError, None)
                return (_G_apply_114, self.currentError)
            def _G_or_115():
                _G_apply_116, lastError = self._apply(self.rule_ruleValue, "ruleValue", [])
                self.considerError(lastError, None)
                return (_G_apply_116, self.currentError)
            def _G_or_117():
                _G_apply_118, lastError = self._apply(self.rule_wide_templatedValue, "wide_templatedValue", [])
                self.considerError(lastError, None)
                return (_G_apply_118, self.currentError)
            def _G_or_119():
                _G_apply_120, lastError = self._apply(self.rule_tall_templatedValue, "tall_templatedValue", [])
                self.considerError(lastError, None)
                return (_G_apply_120, self.currentError)
            def _G_or_121():
                _G_apply_122, lastError = self._apply(self.rule_semanticPredicate, "semanticPredicate", [])
                self.considerError(lastError, None)
                return (_G_apply_122, self.currentError)
            def _G_or_123():
                _G_apply_124, lastError = self._apply(self.rule_semanticAction, "semanticAction", [])
                self.considerError(lastError, None)
                return (_G_apply_124, self.currentError)
            def _G_or_125():
                _G_apply_126, lastError = self._apply(self.rule_number, "number", [])
                self.considerError(lastError, None)
                _locals['n'] = _G_apply_126
                _G_python_127, lastError = eval('self.isTree()', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_python_128, lastError = eval('n', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_128, self.currentError)
            def _G_or_129():
                _G_apply_130, lastError = self._apply(self.rule_character, "character", [])
                self.considerError(lastError, None)
                return (_G_apply_130, self.currentError)
            def _G_or_131():
                _G_apply_132, lastError = self._apply(self.rule_string, "string", [])
                self.considerError(lastError, None)
                return (_G_apply_132, self.currentError)
            def _G_or_133():
                _G_apply_134, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_135, lastError = self.exactly('(')
                self.considerError(lastError, None)
                _G_apply_136, lastError = self._apply(self.rule_expr, "expr", [])
                self.considerError(lastError, None)
                _locals['e'] = _G_apply_136
                _G_apply_137, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_138, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_139, lastError = eval('e', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_139, self.currentError)
            def _G_or_140():
                _G_apply_141, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_142, lastError = self.exactly('[')
                self.considerError(lastError, None)
                def _G_optional_143():
                    _G_apply_144, lastError = self._apply(self.rule_expr, "expr", [])
                    self.considerError(lastError, None)
                    return (_G_apply_144, self.currentError)
                def _G_optional_145():
                    return (None, self.input.nullError())
                _G_or_146, lastError = self._or([_G_optional_143, _G_optional_145])
                self.considerError(lastError, None)
                _locals['e'] = _G_or_146
                _G_apply_147, lastError = self._apply(self.rule_ws, "ws", [])
                self.considerError(lastError, None)
                _G_exactly_148, lastError = self.exactly(']')
                self.considerError(lastError, None)
                _G_python_149, lastError = eval('t.TermPattern(".tuple.", e or t.And([]))', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_149, self.currentError)
            _G_or_150, lastError = self._or([_G_or_107, _G_or_109, _G_or_111, _G_or_113, _G_or_115, _G_or_117, _G_or_119, _G_or_121, _G_or_123, _G_or_125, _G_or_129, _G_or_131, _G_or_133, _G_or_140])
            self.considerError(lastError, 'expr1')
            return (_G_or_150, self.currentError)


        def rule_grammar(self):
            _locals = {'self': self}
            self.locals['grammar'] = _locals
            def _G_many_151():
                _G_apply_152, lastError = self._apply(self.rule_rule, "rule", [])
                self.considerError(lastError, None)
                return (_G_apply_152, self.currentError)
            _G_many_153, lastError = self.many(_G_many_151)
            self.considerError(lastError, 'grammar')
            _locals['rs'] = _G_many_153
            _G_apply_154, lastError = self._apply(self.rule_ws, "ws", [])
            self.considerError(lastError, 'grammar')
            _G_python_155, lastError = eval('t.Grammar(self.name, True, rs)', self.globals, _locals), None
            self.considerError(lastError, 'grammar')
            return (_G_python_155, self.currentError)


    if parsley_tree_transformer.globals is not None:
        parsley_tree_transformer.globals = parsley_tree_transformer.globals.copy()
        parsley_tree_transformer.globals.update(ruleGlobals)
    else:
        parsley_tree_transformer.globals = ruleGlobals
    return parsley_tree_transformer