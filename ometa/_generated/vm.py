def createParserClass(GrammarBase, ruleGlobals):
    if ruleGlobals is None:
        ruleGlobals = {}
    class vm(GrammarBase):
        def rule_Exactly(self):
            _locals = {'self': self}
            self.locals['Exactly'] = _locals
            def _G_termpattern_1():
                _G_apply_2, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_2
                return (_locals['x'], self.currentError)
            _G_termpattern_3, lastError = self.termpattern('Exactly', _G_termpattern_1)
            self.considerError(lastError, 'Exactly')
            _G_python_4, lastError = eval('[t.Match(x)]', self.globals, _locals), None
            self.considerError(lastError, 'Exactly')
            return (_G_python_4, self.currentError)


        def rule_Token(self):
            _locals = {'self': self}
            self.locals['Token'] = _locals
            def _G_termpattern_5():
                _G_apply_6, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_6
                return (_locals['x'], self.currentError)
            _G_termpattern_7, lastError = self.termpattern('Token', _G_termpattern_5)
            self.considerError(lastError, 'Token')
            _G_python_8, lastError = eval("[t.Call('ws'), t.Match(x)]", self.globals, _locals), None
            self.considerError(lastError, 'Token')
            return (_G_python_8, self.currentError)


        def rule_Many(self):
            _locals = {'self': self}
            self.locals['Many'] = _locals
            def _G_termpattern_9():
                _G_apply_10, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_10
                return (_locals['x'], self.currentError)
            _G_termpattern_11, lastError = self.termpattern('Many', _G_termpattern_9)
            self.considerError(lastError, 'Many')
            _G_python_12, lastError = eval('[t.Choice(len(x) + 3)] + x + [t.ListAppend(), t.Commit(-len(x) - 2), t.CollectList()]', self.globals, _locals), None
            self.considerError(lastError, 'Many')
            return (_G_python_12, self.currentError)


        def rule_Many1(self):
            _locals = {'self': self}
            self.locals['Many1'] = _locals
            def _G_termpattern_13():
                _G_apply_14, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_14
                return (_locals['x'], self.currentError)
            _G_termpattern_15, lastError = self.termpattern('Many1', _G_termpattern_13)
            self.considerError(lastError, 'Many1')
            _G_python_16, lastError = eval('x + [t.ListAppend(), t.Choice(len(x) + 3)] + x + [t.ListAppend(), t.Commit(-len(x) - 2), t.CollectList()]', self.globals, _locals), None
            self.considerError(lastError, 'Many1')
            return (_G_python_16, self.currentError)


        def rule_Repeat(self):
            _locals = {'self': self}
            self.locals['Repeat'] = _locals
            def _G_termpattern_17():
                _G_apply_18, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['min'] = _G_apply_18
                _G_apply_19, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['max'] = _G_apply_19
                _G_apply_20, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_20
                return (_locals['x'], self.currentError)
            _G_termpattern_21, lastError = self.termpattern('Repeat', _G_termpattern_17)
            self.considerError(lastError, 'Repeat')
            _G_python_22, lastError = eval('[t.Python(repr(int(min))), t.Push(), t.Python(repr(int(max))),\n        t.Push(), t.RepeatChoice(len(x) + 2)] + x + [t.RepeatCommit(-len(x) - 1)]', self.globals, _locals), None
            self.considerError(lastError, 'Repeat')
            return (_G_python_22, self.currentError)


        def rule_Optional(self):
            _locals = {'self': self}
            self.locals['Optional'] = _locals
            def _G_termpattern_23():
                _G_apply_24, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_24
                return (_locals['x'], self.currentError)
            _G_termpattern_25, lastError = self.termpattern('Optional', _G_termpattern_23)
            self.considerError(lastError, 'Optional')
            _G_python_26, lastError = eval('[t.Choice(len(x) + 2)] + x + [t.Commit(2), t.Python("None")]', self.globals, _locals), None
            self.considerError(lastError, 'Optional')
            return (_G_python_26, self.currentError)


        def rule_Or(self):
            _locals = {'self': self}
            self.locals['Or'] = _locals
            def _G_or_27():
                def _G_termpattern_28():
                    def _G_termpattern_29():
                        def _G_many_30():
                            _G_apply_31, lastError = self._apply(self.rule_anything, "anything", [])
                            self.considerError(lastError, None)
                            return (_G_apply_31, self.currentError)
                        _G_many_32, lastError = self.many(_G_many_30)
                        self.considerError(lastError, None)
                        _locals['xs'] = _G_many_32
                        return (_locals['xs'], self.currentError)
                    _G_termpattern_33, lastError = self.termpattern('.tuple.', _G_termpattern_29)
                    self.considerError(lastError, None)
                    return (_G_termpattern_33, self.currentError)
                _G_termpattern_34, lastError = self.termpattern('Or', _G_termpattern_28)
                self.considerError(lastError, None)
                def _G_or_35():
                    def _G_pred_36():
                        _G_python_37, lastError = eval('len(xs) == 1', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_37, self.currentError)
                    _G_pred_38, lastError = self.pred(_G_pred_36)
                    self.considerError(lastError, None)
                    _G_python_39, lastError = eval('xs[0]', self.globals, _locals), None
                    self.considerError(lastError, None)
                    _G_apply_40, lastError = self._apply(self.rule_transform, "transform", [_G_python_39])
                    self.considerError(lastError, None)
                    return (_G_apply_40, self.currentError)
                def _G_or_41():
                    def _G_pred_42():
                        _G_python_43, lastError = eval('len(xs) == 2', self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_43, self.currentError)
                    _G_pred_44, lastError = self.pred(_G_pred_42)
                    self.considerError(lastError, None)
                    _G_python_45, lastError = eval('t.Or(xs[0], xs[1])', self.globals, _locals), None
                    self.considerError(lastError, None)
                    _G_apply_46, lastError = self._apply(self.rule_transform, "transform", [_G_python_45])
                    self.considerError(lastError, None)
                    return (_G_apply_46, self.currentError)
                def _G_or_47():
                    _G_python_48, lastError = eval('t.Or(xs[0], t.Or(xs[1:]))', self.globals, _locals), None
                    self.considerError(lastError, None)
                    _G_apply_49, lastError = self._apply(self.rule_transform, "transform", [_G_python_48])
                    self.considerError(lastError, None)
                    return (_G_apply_49, self.currentError)
                _G_or_50, lastError = self._or([_G_or_35, _G_or_41, _G_or_47])
                self.considerError(lastError, None)
                return (_G_or_50, self.currentError)
            def _G_or_51():
                def _G_termpattern_52():
                    _G_apply_53, lastError = self._apply(self.rule_transform, "transform", [])
                    self.considerError(lastError, None)
                    _locals['left'] = _G_apply_53
                    _G_apply_54, lastError = self._apply(self.rule_transform, "transform", [])
                    self.considerError(lastError, None)
                    _locals['right'] = _G_apply_54
                    return (_locals['right'], self.currentError)
                _G_termpattern_55, lastError = self.termpattern('Or', _G_termpattern_52)
                self.considerError(lastError, None)
                _G_python_56, lastError = eval('[t.Choice(len(left) + 2)] + left + [t.Commit(len(right) + 1)] + right', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_56, self.currentError)
            _G_or_57, lastError = self._or([_G_or_27, _G_or_51])
            self.considerError(lastError, 'Or')
            return (_G_or_57, self.currentError)


        def rule_Not(self):
            _locals = {'self': self}
            self.locals['Not'] = _locals
            def _G_termpattern_58():
                _G_apply_59, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_59
                return (_locals['x'], self.currentError)
            _G_termpattern_60, lastError = self.termpattern('Not', _G_termpattern_58)
            self.considerError(lastError, 'Not')
            _G_python_61, lastError = eval('[t.Choice(len(x) + 3)] + x + [t.Commit(1), t.Fail()]', self.globals, _locals), None
            self.considerError(lastError, 'Not')
            return (_G_python_61, self.currentError)


        def rule_Lookahead(self):
            _locals = {'self': self}
            self.locals['Lookahead'] = _locals
            def _G_termpattern_62():
                _G_apply_63, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_63
                return (_locals['x'], self.currentError)
            _G_termpattern_64, lastError = self.termpattern('Lookahead', _G_termpattern_62)
            self.considerError(lastError, 'Lookahead')
            _G_python_65, lastError = eval('t.Not(t.Not(x))', self.globals, _locals), None
            self.considerError(lastError, 'Lookahead')
            _G_apply_66, lastError = self._apply(self.rule_transform, "transform", [_G_python_65])
            self.considerError(lastError, 'Lookahead')
            return (_G_apply_66, self.currentError)


        def rule_And(self):
            _locals = {'self': self}
            self.locals['And'] = _locals
            def _G_termpattern_67():
                _G_apply_68, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['xs'] = _G_apply_68
                return (_locals['xs'], self.currentError)
            _G_termpattern_69, lastError = self.termpattern('And', _G_termpattern_67)
            self.considerError(lastError, 'And')
            _G_python_70, lastError = eval('sum(xs, [])', self.globals, _locals), None
            self.considerError(lastError, 'And')
            return (_G_python_70, self.currentError)


        def rule_Bind(self):
            _locals = {'self': self}
            self.locals['Bind'] = _locals
            def _G_termpattern_71():
                _G_apply_72, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['name'] = _G_apply_72
                _G_apply_73, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_73
                return (_locals['x'], self.currentError)
            _G_termpattern_74, lastError = self.termpattern('Bind', _G_termpattern_71)
            self.considerError(lastError, 'Bind')
            _G_python_75, lastError = eval('x + [t.Bind(name)]', self.globals, _locals), None
            self.considerError(lastError, 'Bind')
            return (_G_python_75, self.currentError)


        def rule_Predicate(self):
            _locals = {'self': self}
            self.locals['Predicate'] = _locals
            def _G_termpattern_76():
                _G_apply_77, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_77
                return (_locals['x'], self.currentError)
            _G_termpattern_78, lastError = self.termpattern('Predicate', _G_termpattern_76)
            self.considerError(lastError, 'Predicate')
            _G_python_79, lastError = eval('x + [t.Predicate()]', self.globals, _locals), None
            self.considerError(lastError, 'Predicate')
            return (_G_python_79, self.currentError)


        def rule_Action(self):
            _locals = {'self': self}
            self.locals['Action'] = _locals
            def _G_termpattern_80():
                _G_apply_81, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_81
                return (_locals['x'], self.currentError)
            _G_termpattern_82, lastError = self.termpattern('Action', _G_termpattern_80)
            self.considerError(lastError, 'Action')
            _G_python_83, lastError = eval('[t.Python(x.data)]', self.globals, _locals), None
            self.considerError(lastError, 'Action')
            return (_G_python_83, self.currentError)


        def rule_Python(self):
            _locals = {'self': self}
            self.locals['Python'] = _locals
            def _G_termpattern_84():
                _G_apply_85, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_85
                return (_locals['x'], self.currentError)
            _G_termpattern_86, lastError = self.termpattern('Python', _G_termpattern_84)
            self.considerError(lastError, 'Python')
            _G_python_87, lastError = eval('[t.Python(x.data)]', self.globals, _locals), None
            self.considerError(lastError, 'Python')
            return (_G_python_87, self.currentError)


        def rule_List(self):
            _locals = {'self': self}
            self.locals['List'] = _locals
            def _G_termpattern_88():
                _G_apply_89, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_89
                return (_locals['x'], self.currentError)
            _G_termpattern_90, lastError = self.termpattern('List', _G_termpattern_88)
            self.considerError(lastError, 'List')
            _G_python_91, lastError = eval('[t.Descend()] + x + [t.Ascend()]', self.globals, _locals), None
            self.considerError(lastError, 'List')
            return (_G_python_91, self.currentError)


        def rule_ConsumedBy(self):
            _locals = {'self': self}
            self.locals['ConsumedBy'] = _locals
            def _G_termpattern_92():
                _G_apply_93, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_93
                return (_locals['x'], self.currentError)
            _G_termpattern_94, lastError = self.termpattern('ConsumedBy', _G_termpattern_92)
            self.considerError(lastError, 'ConsumedBy')
            _G_python_95, lastError = eval('[t.StartSlice()] + x + [t.EndSlice()]', self.globals, _locals), None
            self.considerError(lastError, 'ConsumedBy')
            return (_G_python_95, self.currentError)


        def rule_pushes(self):
            _locals = {'self': self}
            self.locals['pushes'] = _locals
            _G_apply_96, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'pushes')
            _locals['xs'] = _G_apply_96
            _G_python_97, lastError = eval('[inner for x in xs for inner in [x[0], t.Push()]]', self.globals, _locals), None
            self.considerError(lastError, 'pushes')
            return (_G_python_97, self.currentError)


        def rule_Apply(self):
            _locals = {'self': self}
            self.locals['Apply'] = _locals
            def _G_or_98():
                def _G_termpattern_99():
                    _G_exactly_100, lastError = self.exactly('super')
                    self.considerError(lastError, None)
                    _G_apply_101, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    _locals['code'] = _G_apply_101
                    _G_apply_102, lastError = self._apply(self.rule_transform, "transform", [])
                    self.considerError(lastError, None)
                    _locals['args'] = _G_apply_102
                    return (_locals['args'], self.currentError)
                _G_termpattern_103, lastError = self.termpattern('Apply', _G_termpattern_99)
                self.considerError(lastError, None)
                _G_python_104, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_apply_105, lastError = self._apply(self.rule_pushes, "pushes", [_G_python_104])
                self.considerError(lastError, None)
                _locals['xs'] = _G_apply_105
                _G_python_106, lastError = eval('xs + [t.SuperCall(code)]', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_106, self.currentError)
            def _G_or_107():
                def _G_termpattern_108():
                    _G_apply_109, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    _locals['rule'] = _G_apply_109
                    _G_apply_110, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    _locals['code'] = _G_apply_110
                    _G_apply_111, lastError = self._apply(self.rule_transform, "transform", [])
                    self.considerError(lastError, None)
                    _locals['args'] = _G_apply_111
                    return (_locals['args'], self.currentError)
                _G_termpattern_112, lastError = self.termpattern('Apply', _G_termpattern_108)
                self.considerError(lastError, None)
                _G_python_113, lastError = eval('args', self.globals, _locals), None
                self.considerError(lastError, None)
                _G_apply_114, lastError = self._apply(self.rule_pushes, "pushes", [_G_python_113])
                self.considerError(lastError, None)
                _locals['xs'] = _G_apply_114
                _G_python_115, lastError = eval('xs + [t.Call(rule)]', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_115, self.currentError)
            _G_or_116, lastError = self._or([_G_or_98, _G_or_107])
            self.considerError(lastError, 'Apply')
            return (_G_or_116, self.currentError)


        def rule_ForeignApply(self):
            _locals = {'self': self}
            self.locals['ForeignApply'] = _locals
            def _G_termpattern_117():
                _G_apply_118, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['grammar'] = _G_apply_118
                _G_apply_119, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['rule'] = _G_apply_119
                _G_apply_120, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['code'] = _G_apply_120
                _G_apply_121, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['args'] = _G_apply_121
                return (_locals['args'], self.currentError)
            _G_termpattern_122, lastError = self.termpattern('ForeignApply', _G_termpattern_117)
            self.considerError(lastError, 'ForeignApply')
            _G_python_123, lastError = eval('args', self.globals, _locals), None
            self.considerError(lastError, 'ForeignApply')
            _G_apply_124, lastError = self._apply(self.rule_pushes, "pushes", [_G_python_123])
            self.considerError(lastError, 'ForeignApply')
            _locals['xs'] = _G_apply_124
            _G_python_125, lastError = eval('(xs +\n    [t.ForeignCall(grammar, rule)])', self.globals, _locals), None
            self.considerError(lastError, 'ForeignApply')
            return (_G_python_125, self.currentError)


        def rule_Rule(self):
            _locals = {'self': self}
            self.locals['Rule'] = _locals
            def _G_termpattern_126():
                _G_apply_127, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['name'] = _G_apply_127
                _G_apply_128, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['xs'] = _G_apply_128
                return (_locals['xs'], self.currentError)
            _G_termpattern_129, lastError = self.termpattern('Rule', _G_termpattern_126)
            self.considerError(lastError, 'Rule')
            _G_python_130, lastError = eval('t.Rule(name, xs)', self.globals, _locals), None
            self.considerError(lastError, 'Rule')
            return (_G_python_130, self.currentError)


        def rule_Grammar(self):
            _locals = {'self': self}
            self.locals['Grammar'] = _locals
            def _G_termpattern_131():
                _G_apply_132, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['name'] = _G_apply_132
                _G_apply_133, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['tree'] = _G_apply_133
                _G_apply_134, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['rules'] = _G_apply_134
                return (_locals['rules'], self.currentError)
            _G_termpattern_135, lastError = self.termpattern('Grammar', _G_termpattern_131)
            self.considerError(lastError, 'Grammar')
            _G_python_136, lastError = eval('t.Grammar(name, tree, rules)', self.globals, _locals), None
            self.considerError(lastError, 'Grammar')
            return (_G_python_136, self.currentError)


        tree = True
    if vm.globals is not None:
        vm.globals = vm.globals.copy()
        vm.globals.update(ruleGlobals)
    else:
        vm.globals = ruleGlobals
    return vm