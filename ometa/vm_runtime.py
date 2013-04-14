from ometa.runtime import ArgInput, OMetaBase, EOFError, ParseError, InputStream, expected
fail = object()

class Success(Exception):
    pass

class VM(object):

    def __init__(self, rules, input, isTree, GrammarBase=OMetaBase,
                 globals=None, parent=None):
        self.rules = rules
        self.input = input
        self.isTree = isTree
        self.code = None
        self.rulename = None
        self.choiceStack = []
        self.inputStack = []
        self.sliceStack = []
        self.listStack = []
        self.currentValue = None
        self.currentError = self.input.nullError()
        self.pc = 0
        if globals is not None:
            self.globals = globals
        else:
            self.globals = {}
        self.locals = {}
        self.parent = parent
        self.runtime = GrammarBase(None)
        self.runtime.input = self.input
        self.runtime.globals = globals

    def apply(self, name):
        self.code = self.rules[name]
        #print "->", name, self.code, getattr(self.input, 'position', None)
        self.rulename = name
        while self.pc < len(self.code):
            self.next()
        #print "<-", name, self.currentValue
        return self.currentValue, self.currentError

    def read(self):
        bc = self.bytecode[self.pc]
        self.pc += 1
        return bc

    def fail(self, err):
        self.runtime.considerError(err)
        self.currentError = self.runtime.currentError
        if not self.choiceStack:
            raise self.currentError
        choice = self.choiceStack.pop()
        #print "Fail", choice[1].position, "<-", getattr(self.input, 'position', None)
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

    def next(self):
        instr = self.code[self.pc]
        #print "Exec", instr
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
            target = instr.args[0].data
            try:
                if target in self.rules:
                    newvm = VM(self.rules, self.input, self.isTree,
                               globals=self.globals, parent=self.parent)
                    newvm.runtime = self.runtime
                    self.currentValue, self.currentError = newvm.apply(target)
                    self.input = newvm.input
                else:
                    bltn = getattr(self.runtime, 'rule_' + target, None)
                    self.runtime.input = self.input
                    self.currentValue, self.currentError = bltn()
                    self.input = self.runtime.input
            except ParseError, e:
                #print "Raise ->", self.rulename
                return self.fail(e)
        elif name == "SuperCall":
            target = instr.args[0].data
            newvm = VM(self.parent.rules, self.input)
            newvm.apply(target)
        elif name == "ForeignCall":
            foreignName = instr.args[0].data
            ruleName = instr.args[1].data
            newvm = self.globals.get(foreignName,
                                     self.local.get(foreignName, None))
            newvm.apply(ruleName)
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
        elif name == "Ascend":
            try:
                self.runtime.end()
            except ParseError, e:
                return self.fail(e)
            self.input = self.inputStack.pop()
        elif name == "Predicate":
            if not self.currentValue:
                return self.fail(self.input.nullError())
        elif name == "RepeatChoice":
            maxval = self.input.head()
            self.input = self.input.tail()
            minval = self.input.head()
            self.input = self.input.tail()
            target = instr.args[0].data
            self.choiceStack.append((target, self.input, minval, maxval, 0))
        elif name == "RepeatCommit":
            target = instr.args[0].data
            choiceTarget, inp, minval, maxval, current = self.choiceStack.pop()
            current += 1
            if current >= maxval:
                self.pc += 1
            else:
                self.pc += target + 1
                self.choiceStack.append((target, inp, minval, maxval, current))
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
        self.pc += 1

def VMWrapper(v):
    return v













