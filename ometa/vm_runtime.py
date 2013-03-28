from ometa.runtime import ArgInput
fail = object()

class Success(Exception):
    pass

class VM(object):

    def __init__(self, rules, input, globals=None, parent=None):
        self.code = None
        self.rulename = None
        self.choice_stack = []
        self.current_value = None
        self.input = input
        self.pc = 0
        if globals is not None:
            self.globals = globals
        self.locals = {}
        self.parent = parent

    def start(self, name):
        self.code = self.rules[name]
        self.rulename = name

    def read(self):
        try:
            bc = self.bytecode[self.pc]
        except IndexError:
            raise Success()
        self.pc += 1
        return bc

    def next(self):
        if self.pc >= len(self.code):
            self.end_call()
        instr = self.code[self.pc]
        name = instr.tag.name

        if name == "Match":
            target = instr.args[0].data
            for c in target:
                v, e = self.input.head()
                if v == c:
                    self.input = self.input.tail()
                else:
                    raise e
        elif name == "Choice":
            target = instr.args[0].data
            self.choice_stack.append((target, self.input))
        elif name == "Call":
            target = instr.args[0].data
            newvm = VM(self.rules, self.input)
            newvm.start(target)
        elif name == "SuperCall":
            target = instr.args[0].data
            newvm = VM(self.parent.rules, self.input)
            newvm.start(target)
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
            self.choice_stack.pop()
        elif name == "Fail":
            raise self.input.nullError()
        elif name == "Python":
            target = instr.args[0].data
            self.current_value = eval(target, self.globals, self.locals)
        elif name == "Push":
            self.input = ArgInput(self.current_value, self.input)
        elif name == "Bind":
            name = instr.args[0].data
            self.locals[name] = self.current_value
        elif name == "RepeatChoice":
            pass
        elif name == "Predicate":
            pass
        elif name == "Descend":
            pass
        elif name == "Ascend":
            pass
        elif name == "StartSlice":
            pass
        elif name == "EndSlice":
            pass









