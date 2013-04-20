def createParserClass(GrammarBase, ruleGlobals):
    if ruleGlobals is None:
        ruleGlobals = {}
    class vm_emit(GrammarBase):
        def rule_Grammar(self):
            _locals = {'self': self}
            self.locals['Grammar'] = _locals
            def _G_termpattern_1():
                _G_apply_2, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['name'] = _G_apply_2
                _G_apply_3, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['tree'] = _G_apply_3
                _G_apply_4, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['rules'] = _G_apply_4
                return (_locals['rules'], self.currentError)
            _G_termpattern_5, lastError = self.termpattern('Grammar', _G_termpattern_1)
            self.considerError(lastError, 'Grammar')
            from terml.parser import parseTerm as term
            _G_stringtemplate_6, lastError = self.stringtemplate(term('["from terml.nodes import termMaker as t\n", "from ometa.runtime import InputStream\n", "from ometa.vm_runtime import VM, VMWrapper\n", "def createParserClass(GrammarBase, ruleGlobals):\n", "    rules = {\n", "        ", QuasiExprHole("rules"), "\n", "    }\n", "    if ", QuasiExprHole("tree"), ":\n", "        mkInput = InputStream.fromIterable\n", "    else:\n", "        mkInput = InputStream.fromText\n", "    def makeParser(data):\n", "        vm = VM(rules, mkInput(data), ", QuasiExprHole("tree"), ", GrammarBase, ruleGlobals)\n", "        return VMWrapper(vm)\n", "    return makeParser\n"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_6, self.currentError)


        def rule_Rule(self):
            _locals = {'self': self}
            self.locals['Rule'] = _locals
            def _G_termpattern_7():
                _G_apply_8, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['name'] = _G_apply_8
                _G_apply_9, lastError = self._apply(self.rule_transform, "transform", [])
                self.considerError(lastError, None)
                _locals['instrs'] = _G_apply_9
                return (_locals['instrs'], self.currentError)
            _G_termpattern_10, lastError = self.termpattern('Rule', _G_termpattern_7)
            self.considerError(lastError, 'Rule')
            from terml.parser import parseTerm as term
            _G_stringtemplate_11, lastError = self.stringtemplate(term('["\'", QuasiExprHole("name"), "\': [\n", "    ", QuasiExprHole("instrs"), "\n", "],\n"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_11, self.currentError)


        def rule_Ascend(self):
            _locals = {'self': self}
            self.locals['Ascend'] = _locals
            def _G_termpattern_12():
                return (None, self.currentError)
            _G_termpattern_13, lastError = self.termpattern('Ascend', _G_termpattern_12)
            self.considerError(lastError, 'Ascend')
            from terml.parser import parseTerm as term
            _G_stringtemplate_14, lastError = self.stringtemplate(term('["t.Ascend(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_14, self.currentError)


        def rule_Bind(self):
            _locals = {'self': self}
            self.locals['Bind'] = _locals
            def _G_termpattern_15():
                _G_apply_16, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_16
                return (_locals['x'], self.currentError)
            _G_termpattern_17, lastError = self.termpattern('Bind', _G_termpattern_15)
            self.considerError(lastError, 'Bind')
            from terml.parser import parseTerm as term
            _G_stringtemplate_18, lastError = self.stringtemplate(term('["t.Bind(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_18, self.currentError)


        def rule_Call(self):
            _locals = {'self': self}
            self.locals['Call'] = _locals
            def _G_termpattern_19():
                _G_apply_20, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_20
                return (_locals['x'], self.currentError)
            _G_termpattern_21, lastError = self.termpattern('Call', _G_termpattern_19)
            self.considerError(lastError, 'Call')
            from terml.parser import parseTerm as term
            _G_stringtemplate_22, lastError = self.stringtemplate(term('["t.Call(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_22, self.currentError)


        def rule_Choice(self):
            _locals = {'self': self}
            self.locals['Choice'] = _locals
            def _G_termpattern_23():
                _G_apply_24, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_24
                return (_locals['x'], self.currentError)
            _G_termpattern_25, lastError = self.termpattern('Choice', _G_termpattern_23)
            self.considerError(lastError, 'Choice')
            from terml.parser import parseTerm as term
            _G_stringtemplate_26, lastError = self.stringtemplate(term('["t.Choice(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_26, self.currentError)


        def rule_RepeatChoice(self):
            _locals = {'self': self}
            self.locals['RepeatChoice'] = _locals
            def _G_termpattern_27():
                _G_apply_28, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_28
                return (_locals['x'], self.currentError)
            _G_termpattern_29, lastError = self.termpattern('RepeatChoice', _G_termpattern_27)
            self.considerError(lastError, 'RepeatChoice')
            from terml.parser import parseTerm as term
            _G_stringtemplate_30, lastError = self.stringtemplate(term('["t.RepeatChoice(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_30, self.currentError)


        def rule_RepeatCommit(self):
            _locals = {'self': self}
            self.locals['RepeatCommit'] = _locals
            def _G_termpattern_31():
                _G_apply_32, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_32
                return (_locals['x'], self.currentError)
            _G_termpattern_33, lastError = self.termpattern('RepeatCommit', _G_termpattern_31)
            self.considerError(lastError, 'RepeatCommit')
            from terml.parser import parseTerm as term
            _G_stringtemplate_34, lastError = self.stringtemplate(term('["t.RepeatCommit(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_34, self.currentError)


        def rule_Commit(self):
            _locals = {'self': self}
            self.locals['Commit'] = _locals
            def _G_termpattern_35():
                _G_apply_36, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_36
                return (_locals['x'], self.currentError)
            _G_termpattern_37, lastError = self.termpattern('Commit', _G_termpattern_35)
            self.considerError(lastError, 'Commit')
            from terml.parser import parseTerm as term
            _G_stringtemplate_38, lastError = self.stringtemplate(term('["t.Commit(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_38, self.currentError)


        def rule_Descend(self):
            _locals = {'self': self}
            self.locals['Descend'] = _locals
            def _G_termpattern_39():
                return (None, self.currentError)
            _G_termpattern_40, lastError = self.termpattern('Descend', _G_termpattern_39)
            self.considerError(lastError, 'Descend')
            from terml.parser import parseTerm as term
            _G_stringtemplate_41, lastError = self.stringtemplate(term('["t.Descend(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_41, self.currentError)


        def rule_EndSlice(self):
            _locals = {'self': self}
            self.locals['EndSlice'] = _locals
            def _G_termpattern_42():
                return (None, self.currentError)
            _G_termpattern_43, lastError = self.termpattern('EndSlice', _G_termpattern_42)
            self.considerError(lastError, 'EndSlice')
            from terml.parser import parseTerm as term
            _G_stringtemplate_44, lastError = self.stringtemplate(term('["t.EndSlice(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_44, self.currentError)


        def rule_Fail(self):
            _locals = {'self': self}
            self.locals['Fail'] = _locals
            def _G_termpattern_45():
                return (None, self.currentError)
            _G_termpattern_46, lastError = self.termpattern('Fail', _G_termpattern_45)
            self.considerError(lastError, 'Fail')
            from terml.parser import parseTerm as term
            _G_stringtemplate_47, lastError = self.stringtemplate(term('["t.Fail(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_47, self.currentError)


        def rule_ForeignCall(self):
            _locals = {'self': self}
            self.locals['ForeignCall'] = _locals
            def _G_termpattern_48():
                _G_apply_49, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_49
                _G_apply_50, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['y'] = _G_apply_50
                return (_locals['y'], self.currentError)
            _G_termpattern_51, lastError = self.termpattern('ForeignCall', _G_termpattern_48)
            self.considerError(lastError, 'ForeignCall')
            from terml.parser import parseTerm as term
            _G_stringtemplate_52, lastError = self.stringtemplate(term('["t.ForeignCall(", QuasiExprHole("x"), ", ", QuasiExprHole("y"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_52, self.currentError)


        def rule_Match(self):
            _locals = {'self': self}
            self.locals['Match'] = _locals
            def _G_termpattern_53():
                _G_apply_54, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_54
                return (_locals['x'], self.currentError)
            _G_termpattern_55, lastError = self.termpattern('Match', _G_termpattern_53)
            self.considerError(lastError, 'Match')
            from terml.parser import parseTerm as term
            _G_stringtemplate_56, lastError = self.stringtemplate(term('["t.Match(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_56, self.currentError)


        def rule_Predicate(self):
            _locals = {'self': self}
            self.locals['Predicate'] = _locals
            def _G_termpattern_57():
                return (None, self.currentError)
            _G_termpattern_58, lastError = self.termpattern('Predicate', _G_termpattern_57)
            self.considerError(lastError, 'Predicate')
            from terml.parser import parseTerm as term
            _G_stringtemplate_59, lastError = self.stringtemplate(term('["t.Predicate(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_59, self.currentError)


        def rule_Push(self):
            _locals = {'self': self}
            self.locals['Push'] = _locals
            def _G_termpattern_60():
                return (None, self.currentError)
            _G_termpattern_61, lastError = self.termpattern('Push', _G_termpattern_60)
            self.considerError(lastError, 'Push')
            from terml.parser import parseTerm as term
            _G_stringtemplate_62, lastError = self.stringtemplate(term('["t.Push(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_62, self.currentError)


        def rule_Python(self):
            _locals = {'self': self}
            self.locals['Python'] = _locals
            def _G_termpattern_63():
                _G_apply_64, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_64
                return (_locals['x'], self.currentError)
            _G_termpattern_65, lastError = self.termpattern('Python', _G_termpattern_63)
            self.considerError(lastError, 'Python')
            from terml.parser import parseTerm as term
            _G_stringtemplate_66, lastError = self.stringtemplate(term('["t.Python(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_66, self.currentError)


        def rule_StartSlice(self):
            _locals = {'self': self}
            self.locals['StartSlice'] = _locals
            def _G_termpattern_67():
                return (None, self.currentError)
            _G_termpattern_68, lastError = self.termpattern('StartSlice', _G_termpattern_67)
            self.considerError(lastError, 'StartSlice')
            from terml.parser import parseTerm as term
            _G_stringtemplate_69, lastError = self.stringtemplate(term('["t.StartSlice(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_69, self.currentError)


        def rule_StringTemplate(self):
            _locals = {'self': self}
            self.locals['StringTemplate'] = _locals
            def _G_termpattern_70():
                def _G_many_71():
                    _G_apply_72, lastError = self._apply(self.rule_stPart, "stPart", [])
                    self.considerError(lastError, None)
                    return (_G_apply_72, self.currentError)
                _G_many_73, lastError = self.many(_G_many_71)
                self.considerError(lastError, None)
                _locals['parts'] = _G_many_73
                return (_locals['parts'], self.currentError)
            _G_termpattern_74, lastError = self.termpattern('StringTemplate', _G_termpattern_70)
            self.considerError(lastError, 'StringTemplate')
            _G_python_75, lastError = eval("', '.join(parts)", self.globals, _locals), None
            self.considerError(lastError, 'StringTemplate')
            _locals['partsStr'] = _G_python_75
            from terml.parser import parseTerm as term
            _G_stringtemplate_76, lastError = self.stringtemplate(term('["t.StringTemplate(", QuasiExprHole("partsStr"), ")"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_76, self.currentError)


        def rule_SuperCall(self):
            _locals = {'self': self}
            self.locals['SuperCall'] = _locals
            def _G_termpattern_77():
                _G_apply_78, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_78
                return (_locals['x'], self.currentError)
            _G_termpattern_79, lastError = self.termpattern('SuperCall', _G_termpattern_77)
            self.considerError(lastError, 'SuperCall')
            from terml.parser import parseTerm as term
            _G_stringtemplate_80, lastError = self.stringtemplate(term('["t.SuperCall(", QuasiExprHole("x"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_80, self.currentError)


        def rule_TermDescend(self):
            _locals = {'self': self}
            self.locals['TermDescend'] = _locals
            def _G_termpattern_81():
                _G_apply_82, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['name'] = _G_apply_82
                return (_locals['name'], self.currentError)
            _G_termpattern_83, lastError = self.termpattern('TermDescend', _G_termpattern_81)
            self.considerError(lastError, 'TermDescend')
            from terml.parser import parseTerm as term
            _G_stringtemplate_84, lastError = self.stringtemplate(term('["t.TermDescend(", QuasiExprHole("name"), "),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_84, self.currentError)


        def rule_ListAppend(self):
            _locals = {'self': self}
            self.locals['ListAppend'] = _locals
            def _G_termpattern_85():
                return (None, self.currentError)
            _G_termpattern_86, lastError = self.termpattern('ListAppend', _G_termpattern_85)
            self.considerError(lastError, 'ListAppend')
            from terml.parser import parseTerm as term
            _G_stringtemplate_87, lastError = self.stringtemplate(term('["t.ListAppend(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_87, self.currentError)


        def rule_CollectList(self):
            _locals = {'self': self}
            self.locals['CollectList'] = _locals
            def _G_termpattern_88():
                return (None, self.currentError)
            _G_termpattern_89, lastError = self.termpattern('CollectList', _G_termpattern_88)
            self.considerError(lastError, 'CollectList')
            from terml.parser import parseTerm as term
            _G_stringtemplate_90, lastError = self.stringtemplate(term('["t.CollectList(),"]'), _locals)
            self.considerError(lastError, None)
            return (_G_stringtemplate_90, self.currentError)


        def rule_repr(self):
            _locals = {'self': self}
            self.locals['repr'] = _locals
            def _G_or_91():
                _G_apply_92, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_92
                def _G_pred_93():
                    _G_python_94, lastError = eval("s.tag.name == 'true'", self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_94, self.currentError)
                _G_pred_95, lastError = self.pred(_G_pred_93)
                self.considerError(lastError, None)
                _G_python_96, lastError = 'True', None
                self.considerError(lastError, None)
                return (_G_python_96, self.currentError)
            def _G_or_97():
                _G_apply_98, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_98
                def _G_pred_99():
                    _G_python_100, lastError = eval("s.tag.name == 'false'", self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_100, self.currentError)
                _G_pred_101, lastError = self.pred(_G_pred_99)
                self.considerError(lastError, None)
                _G_python_102, lastError = 'False', None
                self.considerError(lastError, None)
                return (_G_python_102, self.currentError)
            def _G_or_103():
                _G_apply_104, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_104
                def _G_pred_105():
                    _G_python_106, lastError = eval("s.tag.name == 'null'", self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_106, self.currentError)
                _G_pred_107, lastError = self.pred(_G_pred_105)
                self.considerError(lastError, None)
                _G_python_108, lastError = 'None', None
                self.considerError(lastError, None)
                return (_G_python_108, self.currentError)
            def _G_or_109():
                _G_apply_110, lastError = self._apply(self.rule_anything, "anything", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_110
                def _G_pred_111():
                    _G_python_112, lastError = eval('s.data is not None', self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_112, self.currentError)
                _G_pred_113, lastError = self.pred(_G_pred_111)
                self.considerError(lastError, None)
                _G_python_114, lastError = eval('repr(s.data)', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_114, self.currentError)
            _G_or_115, lastError = self._or([_G_or_91, _G_or_97, _G_or_103, _G_or_109])
            self.considerError(lastError, 'repr')
            return (_G_or_115, self.currentError)


        def rule_stPart(self):
            _locals = {'self': self}
            self.locals['stPart'] = _locals
            def _G_or_116():
                def _G_termpattern_117():
                    _G_apply_118, lastError = self._apply(self.rule_repr, "repr", [])
                    self.considerError(lastError, None)
                    _locals['n'] = _G_apply_118
                    return (_locals['n'], self.currentError)
                _G_termpattern_119, lastError = self.termpattern('QuasiExprHole', _G_termpattern_117)
                self.considerError(lastError, None)
                from terml.parser import parseTerm as term
                _G_stringtemplate_120, lastError = self.stringtemplate(term('["t.QuasiExprHole(", QuasiExprHole("n"), ")"]'), _locals)
                self.considerError(lastError, None)
                return (_G_stringtemplate_120, self.currentError)
            def _G_or_121():
                _G_apply_122, lastError = self._apply(self.rule_repr, "repr", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_122
                _G_python_123, lastError = eval('s', self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_123, self.currentError)
            _G_or_124, lastError = self._or([_G_or_116, _G_or_121])
            self.considerError(lastError, 'stPart')
            return (_G_or_124, self.currentError)


        tree = True
    if vm_emit.globals is not None:
        vm_emit.globals = vm_emit.globals.copy()
        vm_emit.globals.update(ruleGlobals)
    else:
        vm_emit.globals = ruleGlobals
    return vm_emit