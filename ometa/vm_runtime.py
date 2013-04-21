from ometa.runtime import ArgInput, OMetaBase, EOFError, ParseError, InputStream, expected, LeftRecursion, ArgInput
from terml.nodes import Term, coerceToTerm
DEBUG = False

class VM(object):

    FRAME_VARS = ['choiceStack', 'inputStack', 'sliceStack', 'listStack',
                  'currentValue', 'currentError', 'pc', 'locals', 'code']

    def __init__(self, rules, input, isTree, GrammarBase=OMetaBase,
                 globals=None, parent=None):
        self.rules = rules
        self.input = input
        self.isTree = isTree
        if globals is not None:
            self.globals = globals
        else:
            self.globals = {}
        self.parent = parent
        self.runtime = GrammarBase(None)
        self.runtime.input = self.input
        self.runtime.globals = globals
        self.callStack = []
        self.cleanState()

    def cleanState(self):
        self.choiceStack = []
        self.inputStack = []
        self.sliceStack = []
        self.listStack = []
        self.currentValue = None
        self.currentError = self.input.nullError()
        self.pc = 0
        self.locals = {}
        self.code = None
        self.rulename = None

    def pushState(self):
        frame = {}
        for n in self.FRAME_VARS:
            frame[n] = getattr(self, n)
        self.callStack.append(frame)
        self.cleanState()

    def popState(self):
        frame = self.callStack.pop()
        for (k, v) in frame.iteritems():
            setattr(self, k, v)

    def apply(self, name):
        if name in self.rules:
            return self._apply(name)
        else:
            return self._native(name)

    def _native(self, name):
        bltn = getattr(self, 'rule_' + name, None)
        return bltn()

    def _apply(self, name):
        memoRec = self.input.getMemo(name)
        if memoRec is None:
            oldPosition = self.input
            lr = LeftRecursion()
            self.input.setMemo(name, lr)
            try:
                memoRec = oldPosition.setMemo(name, [self._subInvoke(name),
                                                     self.input])
            except ParseError, e:
                e.trail.append(name)
                if DEBUG:
                    print "Raise ->", self.rulename
                raise
            if lr.detected:
                if DEBUG:
                    print "Left recursion in", self.rulename
                sentinel = self.input
                while True:
                    try:
                        self.input = oldPosition
                        ans = self._subInvoke(name)
                        if self.input == sentinel:
                            break
                        memoRec = oldPosition.setMemo(name,
                                                     [ans, self.input])
                        if DEBUG:
                            print "Recursion in", self.rulename, "collected", memoRec[0][0]
                    except ParseError:
                        break
                if DEBUG:
                    print "Exited recursion"
            self.input = oldPosition
        elif isinstance(memoRec, LeftRecursion):
            memoRec.detected = True
            raise self.input.nullError()
        self.input = memoRec[1]
        return memoRec[0]


    def _subeval(self, name):
        self.code = self.rules[name]
        if DEBUG:
            print "->", name, self.code, getattr(self.input, 'position', None)
            self.rulename = name
        while self.pc < len(self.code):
            self.next()
        if DEBUG:
            print "<-", name, self.currentValue
        return self.currentValue, self.currentError

    def _subInvoke(self, ruleName):
        self.pushState()
        try:
            return self._subeval(ruleName)
        finally:
            self.popState()

    def next(self):
        instr = self.code[self.pc]
        if DEBUG:
            print "Exec", instr
        name = instr.tag.name

        if name == "Match":
            wanted = instr.args[0].data
            i = self.input
            try:
                if not self.isTree and len(wanted) > 1:
                        val, p, self.input = self.input.slice(len(wanted))
                else:
                    val, p = self.input.head()
                    self.input = self.input.tail()
            except EOFError, e:
                return self.fail(e)
            if wanted == val:
                self.currentValue, currentError = val, p
            else:
                self.input = i
                return self.fail(p.withMessage(expected(None, wanted)))

        elif name == "Choice":
            target = instr.args[0].data
            self.choiceStack.append((self.pc + target, self.input, None))
        elif name == "Call":
            ruleName = instr.args[0].data
            try:
                self.currentValue, self.currentError = self.apply(ruleName)
            except ParseError, e:
                return self.fail(e)
        elif name == "SuperCall":
            target = instr.args[0].data
            newvm = VM(self.parent.rules, self.input)
            try:
                newvm.apply(target)
            except ParseError, e:
                return self.fail(e)
        elif name == "ForeignCall":
            foreignName = instr.args[0].data
            ruleName = instr.args[1].data
            newvm = self.globals.get(foreignName,
                                     self.local.get(foreignName, None))
            try:
                newvm.apply(ruleName)
            except ParseError, e:
                return self.fail(e)
        elif name == "Commit":
            target = instr.args[0].data
            self.pc += target
            self.choiceStack.pop()
            return
        elif name == "Fail":
            return self.fail(self.input.nullError())
        elif name == "Python":
            target = instr.args[0].data
            self.currentValue = eval(target, self.globals, self.locals)
        elif name == "Push":
            self.input = ArgInput(self.currentValue, self.input)
        elif name == "Bind":
            name = instr.args[0].data
            self.locals[name] = self.currentValue
        elif name == "Descend":
            inp, self.currentError = self.input.head()
            self.inputStack.append(self.input.tail())
            try:
                self.input = InputStream.fromIterable(inp)
            except TypeError:
                return self.fail(self.currentError)
        elif name == "TermDescend":
            wanted = instr.args[0].data
            inp, p = self.input.head()
            if not isinstance(inp, Term) or wanted != inp.tag.name:
                return self.fail(
                    p.withMessage(expected("a Term named " + wanted)))
            self.inputStack.append(self.input.tail())
            try:
                self.input = InputStream.fromIterable(inp.args)
            except TypeError:
                return self.fail(self.currentError)
        elif name == "Ascend":
            try:
                self.input.head()
            except EOFError, e:
                self.currentValue = self.input.data
                self.input = self.inputStack.pop()
            else:
                return self.fail(e)
        elif name == "Predicate":
            if not self.currentValue:
                return self.fail(self.input.nullError())
        elif name == "RepeatChoice":
            maxval, _ = self.input.head()
            self.input = self.input.tail()
            minval, _ = self.input.head()
            self.input = self.input.tail()
            target = instr.args[0].data
            if isinstance(minval, basestring):
                minval = self.locals[minval]
            if isinstance(maxval, basestring):
                minval = self.locals[maxvall]
            if maxval == 0:
                self.currentValue = self.input.data[0:0] # empty container of same type as input
                self.pc += target
            else:
                self.choiceStack.append((self.pc + target, self.input, minval, maxval, 0))
        elif name == "RepeatCommit":
            target = instr.args[0].data
            choiceTarget, inp, minval, maxval, current = self.choiceStack.pop()
            current += 1
            if current >= maxval:
                self.pc += 1
            else:
                self.pc += target + 1
                self.choiceStack.append((choiceTarget, inp, minval, maxval, current))
            return
        elif name == "StartSlice":
            self.sliceStack.append(self.input)
        elif name == "EndSlice":
            oldInput = self.sliceStack.pop()
            self.currentValue = oldInput.data[
                oldInput.position:self.input.position]
        elif name == "CollectList":
            self.currentValue = self.listStack
            self.listStack = []
        elif name == "ListAppend":
            self.listStack.append(self.currentValue)
        else:
            raise ValueError("Unrecognized opcode " + name)
        self.pc += 1

    def fail(self, err):
        self.runtime.considerError(err)
        self.currentError = self.runtime.currentError
        if not self.choiceStack:
            raise self.currentError
        choice = self.choiceStack.pop()
        if DEBUG:
            print "Fail", getattr(choice[1], 'position', None), "<-", getattr(self.input, 'position', None)
        newpc = choice[0]
        self.input = choice[1]
        minval = choice[2]
        if minval is not None and choice[4] < minval:
            # we're in a repeat and we didn't match enough to meet the
            # minimum. Invoke the failure handler outside the repeat.
            self.fail(err)
        else:
            # either not in a repeat, or made it to the minimum. Jump
            # to the target in the last Choice/RepeatChoice.
            self.pc = newpc

    def rule_anything(self):
        """
        Match a single item from the input of any kind.
        """
        h, p = self.input.head()
        self.input = self.input.tail()
        return h, p

    def rule_ws(self):
        while True:
            try:
                c, e = self.input.head()
            except EOFError, e:
                break
            t = self.input.tail()
            if c.isspace():
                self.input = t
            else:
                break
        return True, e

    def rule_letter(self):
        """
        Match a single letter.
        """
        x, e = self.rule_anything()
        if x.isalpha():
            return x, e
        else:
            raise e.withMessage(expected("letter"))

    def rule_letterOrDigit(self):
        """
        Match a single alphanumeric character.
        """
        x, e = self.rule_anything()
        if x.isalnum():
            return x, e
        else:
            raise e.withMessage(expected("letter or digit"))

    def rule_digit(self):
        """
        Match a single digit.
        """
        x, e = self.rule_anything()
        if x.isdigit():
            return x, e
        else:
            raise e.withMessage(expected("digit"))

    def rule_transform(self):
        tt, e = self.rule_anything()
        if isinstance(tt, Term):
            try:
                return self._transform_data(tt), e
            except ValueError:
                name = tt.tag.name
                if name == '.tuple.':
                    return self._transform_iterable(tt.args)
                else:
                    self.input = ArgInput(tt, self.input)
                    if getattr(self, 'rule_' + name, name in self.rules):
                        return self.apply(name)
                    else:
                        return self.apply("unknown_term")
        else:
            return self._transform_iterable(tt)

    def _transform_data(self, tt):
        if tt.data is not None:
            return tt.data
        name = tt.tag.name
        if name == 'null':
            return None
        if name == 'true':
            return True
        if name == 'false':
            return False
        raise ValueError()

    def _transform_iterable(self, contents):
        oldInput = self.input
        self.input = InputStream.fromIterable(contents)
        v = []
        while True:
            try:
                m = self.input
                item, _ = self.rule_transform()
                v.append(item)
            except ParseError:
                self.input = m
                break
        if not self.input.atEnd():
            return self.fail(e.withMessage(
                    expected("a list with transformable contents"
                             % (tt.tag.name,))))
        self.input = oldInput
        return v

    def rule_unknown_term(self):
        tt, _ = self.rule_anything()
        oldInput = self.input
        self.input = InputStream.fromIterable(tt.args)
        newargs = []
        while True:
            try:
                m = self.input
                item, _ = self.rule_transform()
                newargs.append(item)
            except ParseError, e:
                self.input = m
                break
        if not self.input.atEnd():
            return self.fail(e.withMessage(
                    expected("a Term %r with transformable args"
                             % (tt.tag.name,))))
        self.input = oldInput
        return Term(tt.tag, None, tuple(coerceToTerm(a) for a in newargs)), e

    def rule_null(self):
        tt, e = self.rule_anything()
        if not tt.tag.name == "null":
            raise self.input.nullError()
        return None, self.input.nullError()


def VMWrapper(v):
    return v
