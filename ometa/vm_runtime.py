from ometa.runtime import ArgInput, OMetaBase, EOFError, ParseError
fail = object()

class Success(Exception):
    pass

class VM(object):

    def __init__(self, rules, input, globals=None, parent=None):
        self.code = None
        self.rulename = None
        self.choiceStack = []
        self.inputStack = []
        self.sliceStack = []
        self.input = input
        self.currentValue = None
        self.currentError = self.input.nullError()
        self.pc = 0
        if globals is not None:
            self.globals = globals
        self.locals = {}
        self.parent = parent
        self.runtime = OMetaBase(self.input)

    def start(self, name):
        self.code = self.rules[name]
        self.rulename = name

    def execute(self, name):
        self.start(name)
        while self.pc < len(self.bytecode):
            self.next()

        return self.currentValue, self.currentError

    def read(self):
        try:
            bc = self.bytecode[self.pc]
        except IndexError:
            raise Success()
        self.pc += 1
        return bc

    def fail(self, err):
        self.runtime.considerError(err)
        self.currentError = self.runtime.currentError
        if not self.choiceStack:
            raise self.currentError
        choice = self.choiceStack.pop()
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
        if self.pc >= len(self.code):
            return self.currentValue, self.currentError
        instr = self.code[self.pc]
        name = instr.tag.name

        if name == "Match":
            target = instr.args[0].data
            for c in target:
                v, e = self.input.head()
                if v == c:
                    self.input = self.input.tail()
                else:
                    self.fail(e)
        elif name == "Choice":
            target = instr.args[0].data
            self.choiceStack.append((target, self.input, None))
        elif name == "Call":
            target = instr.args[0].data
            bltn = getattr(self.runtime, 'rule_' + target, None)
            if bltn is not None:
                try:
                    self.currentValue = bltn()
                except ParseError, e:
                    self.fail(e)
            else:
                newvm = VM(self.rules, self.input)
                val, err = newvm.start(target)
        elif name == "SuperCall":
            target = instr.args[0].data
            newvm = VM(self.parent.rules, self.input)
            newvm.start(target)
        elif name == "ForeignCall":
            foreignName = instr.args[0].data
            ruleName = instr.args[1].data
            newvm = self.globals.get(foreignName,
                                     self.local.get(foreignName, None))
            newvm.start(ruleName)
        elif name == "Commit":
            target = instr.args[0].data
            self.pc = target
            self.choiceStack.pop()
        elif name == "Fail":
            self.fail(self.input.nullError())
        elif name == "Python":
            target = instr.args[0].data
            self.currentValue = eval(target, self.globals, self.locals)
        elif name == "Push":
            self.input = ArgInput(self.currentValue, self.input)
        elif name == "Bind":
            name = instr.args[0].data
            self.locals[name] = self.currentValue
        elif name == "Descend":
            self.inputStack.push(self.input)
            self.input = self.input.head()
        elif name == "Ascend":
            try:
                self.runtime.end()
            except ParseError, e:
                self.fail(e)
            self.input = self.inputStack.pop()
        elif name == "Predicate":
            if not self.currentValue:
                raise self.input.nullError()
        elif name == "RepeatChoice":
            maxval = self.input.head()
            self.input = self.input.tail()
            minval = self.input.head()
            self.input = self.input.tail()
            target = instr.args[0].data
            self.choiceStack.append((target, self.input, minval, maxval, 0))
        elif name == "RepeatCommit":
            target = instr.args[0].data
            choiceTarget, inp, minval, maxval, current = self.choicestack.pop()
            current += 1
            if current >= maxval:
                self.pc += 1
            else:
                self.pc = target + 1
                self.choiceStack.append((target, inp, minval, maxval, current))
        elif name == "StartSlice":
            self.sliceStack.append(self.input)
        elif name == "EndSlice":
            oldInput = self.sliceStack.pop()
            self.currentValue = oldInput.data[
                oldInput.position:self.input.position]
