from runtime import OMetaBase, ParseError

class BootOMetaGrammar(OMetaBase):
    """
    Grammar parser.
    """
    def __init__(self, input):
        OMetaBase.__init__(self, input)
        self._ruleNames = []
        self.__ometa_rules__ = {}
    def rule_application(self):
        self.token("<")
        self.eatWhitespace()
        name = self.rule_name()
        try:
            self.exactly(" ")
            args = []
            while True:
                try:
                    arg, endchar = self.pythonExpr(" >")
                    if not arg:
                        break
                    args.append(arg)
                    if endchar == '>':
                        break
                except ParseError:
                    break
        except ParseError:
            args = []
            self.token(">")

        return self.builder.apply(name, self.name, *args)


    def rule_number(self):
        self.eatWhitespace()
        isHex = 0
        isOctal = 0
        buf = []
        try:
            buf.append(self.exactly("-"))
        except ParseError:
            pass
        d = self.digit()
        buf.append(d)
        if d == '0':
            isOctal = 1
        try:
            try:
                buf.append(self.digit())
            except ParseError:
                if isOctal:
                    try:
                        buf.append(self.exactly('x'))
                    except ParseError:
                        buf.append(self.exactly('X'))
                    isHex = 1
                    isOctal = 0
            while True:
                try:
                    buf.append(self.hexdigit())
                except ParseError:
                    break

        except ParseError:
            pass
        s = ''.join(buf)
        if isHex:
            i = int(s, 16)
        elif isOctal:
            i = int(s, 8)
        else:
            i = int(s)
        return self.builder.exactly(i)
    def rule_character(self):
        self.token("'")
        r = self.apply("anything")
        if (r == "\\"):
            r += self.apply("anything")
        self.token("'")
        return self.builder.exactly(r)


    def rule_name(self):
        x  = self.letter()
        xs = self.many(self.letterOrDigit)
        xs.insert(0, x)
        return ''.join(xs)

    def rule_expr1(self):
        try:
            r = self.apply("application")
        except ParseError:
            try:
                r = self.builder.compilePythonExpr(self.name,
                                              self.apply("ruleValue"))
            except ParseError:
                try:
                    r = self.apply("semanticPredicate")
                except ParseError:
                    try:
                        r = self.apply("semanticAction")
                    except ParseError:
                        try:
                            r = self.apply("number")
                        except ParseError:
                            try:
                                r = self.apply("character")
                            except ParseError:
                                try:
                                    self.token("(")
                                    r = self.apply("expr")
                                    self.token(")")
                                except ParseError:
                                    self.token("[")
                                    try:
                                        self.token("]")
                                        r = self.builder.listpattern([])
                                    except ParseError:
                                        e = self.apply("expr")
                                        self.token("]")
                                        r = self.builder.listpattern(e)
        return r

    def rule_expr2(self):
        try:
            self.token("~")
            try:
                self.token("~")
                r = self.apply("expr2")
                return self.builder.lookahead(r)
            except ParseError:
                r = self.apply("expr2")
                return self.builder._not(r)
        except ParseError:
            pass
        return self.apply("expr1")


    def rule_expr3(self):
        try:
            r = self.apply("expr2")
            try:
                self.token("*")
                r = self.builder.many(r)
            except ParseError:
                try:
                    self.token("+")
                    r = self.builder.many1(r)
                except ParseError:
                    pass
            try:
                self.exactly(":")
                name = self.apply("name")
                r = self.builder.bind(r, name)
            except ParseError:
                pass
            return r
        except ParseError:
            self.token(":")
            name = self.apply("name")
            r = self.builder.apply("anything")
            return self.builder.bind(r, name)

    def rule_expr4(self):
        return self.builder.sequence(self.many(lambda: self.apply("expr3")))


    def rule_expr(self):
        ans = [self.apply("expr4")]
        m = -1
        try:
            while True:
                m = self.input.mark()
                self.token("|")
                ans.append(self.apply("expr4"))
                self.input.unmark(m)
        except ParseError:
            if m >= 0:
                self.input.rewind(m)

        return self.builder._or(ans)

    def rule_ruleValue(self):
        self.token("=>")
        #this feels a bit hackish...
        expr, endchar = self.pythonExpr(endChars="\r\n)]")
        if str(endchar) in ")]":
            self.input.prev()
        return expr

    def rule_semanticPredicate(self):
        self.token("?(")
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.pred(expr)

    def rule_semanticAction(self):
        self.token("!(")
        expr = self.builder.compilePythonExpr(self.name, self.pythonExpr(')')[0])
        return self.builder.action(expr)

    def rule_rulePart(self):
        requiredName = self.apply("anything")
        self.eatWhitespace()
        m = self.input.mark()
        name = self.apply("name")
        if (name != requiredName):
            self.input.rewind(m)
            raise ParseError()
        else:
            self.input.unmark(m)

        self.name = name
        argPatterns = self.apply("expr4")
        try:
            self.token("::=")
        except ParseError:
            return argPatterns
        else:
            body = self.builder.sequence([argPatterns, self.apply("expr")])
            return body

    def rule_rule(self):
        self.eatWhitespace()
        name = self.lookahead(lambda: self.apply("name"))
        if name in self._ruleNames:
            raise SyntaxError("Multiple definitions of "+name)
        r = self.apply("rulePart", name)
        rs = self.many(lambda: self.apply("rulePart", name), r)
        self._ruleNames.append(name)
        if len(rs) == 1:
            return (name, rs[0])
        else:
            return (name, self.builder._or(rs))


    def rule_grammar(self):
        x = self.builder.makeGrammar(self.many(lambda: self.apply("rule")))
        self.eatWhitespace()
        return x
