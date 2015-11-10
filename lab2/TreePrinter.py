import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def print_tabs(self, tabs=0):
        return tabs * "| " if tabs else ""

    @addToClass(AST.Node)
    def print_tree(self, tabs=0):
        raise Exception("print_tree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Name)
    def print_tree(self, tabs=0):
        return self.print_tabs(tabs) + self.name + "\n"

    @addToClass(AST.Operator)
    def print_tree(self, tabs=0):
        return self.print_tabs(tabs) + self.op + "\n"

    @addToClass(AST.Program)
    def print_tree(self, tabs=0):
        res = ""
        for i in self.body:
            res += i.print_tree(tabs)
        return res

    @addToClass(AST.Declaration)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "DECL (" + self.var_type.name + ")\n"
        tabs += 1
        for i in self.inits:
            res += i.print_tree(tabs)
        return res

    @addToClass(AST.Initializer)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "=\n"
        tabs += 1
        res += str(self.name.print_tree(tabs))
        res += str(self.expression.print_tree(tabs))
        return res

    @addToClass(AST.PrintInstr)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "PRINT\n"
        tabs += 1
        for e in self.expr_list:
            res += e.print_tree(tabs)
        return res

    @addToClass(AST.LabeledInstr)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "LABELED\n"
        tabs += 1
        res += self.print_tabs(tabs) + "LAB" + self.label + "\n"
        res += self.instruction.print_tree(tabs)
        return res

    @addToClass(AST.Assignment)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "=\n"
        tabs += 1
        res += self.target.print_tree(tabs)
        res += self.value.print_tree(tabs)
        return res

    @addToClass(AST.IfInstr)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "IF\n"
        tabs += 1
        res += self.condition.print_tree(tabs)
        res += self.body.print_tree(tabs)
        if self.else_body:
            res += self.print_tabs(tabs - 1) + "ELSE\n"
            res += self.else_body.print_tree(tabs)
        return res

    @addToClass(AST.WhileInstr)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "WHILE\n"
        tabs += 1
        res += self.condition.print_tree(tabs)
        res += self.body.print_tree(tabs)
        return res

    @addToClass(AST.RepeatInstr)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "REPEAT\n"
        for i in self.body:
            res += i.print_tree(tabs + 1)
        res += self.print_tabs(tabs) + "UNTIL\n"
        res += self.condition.print_tree(tabs + 1)
        return res

    @addToClass(AST.ReturnInstr)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "RETURN\n"
        res += self.expression.print_tree(tabs + 1)
        return res

    @addToClass(AST.ContinueInstr)
    def print_tree(self, tabs=0):
        return self.print_tabs(tabs) + "CONTINUE\n"

    @addToClass(AST.BreakInstr)
    def print_tree(self, tabs=0):
        return self.print_tabs(tabs) + "BREAK\n"

    @addToClass(AST.Const)
    def print_tree(self, tabs=0):
        return self.print_tabs(tabs) + "CONST " + str(self.value) + "\n"

    @addToClass(AST.Integer)
    def print_tree(self, tabs=0):
        return self.print_tabs(tabs) + str(self.value) + "\n"

    @addToClass(AST.Float)
    def print_tree(self, tabs=0):
        return self.print_tabs(tabs) + str(self.value) + "\n"

    @addToClass(AST.String)
    def print_tree(self, tabs=0):
        return self.print_tabs(tabs) + self.value + "\n"

    @addToClass(AST.BinaryExpr)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + str(self.op)
        tabs += 1
        res += self.left.print_tree(tabs)
        res += self.right.print_tree(tabs)
        return res

    @addToClass(AST.EnclosedExpr)
    def print_tree(self, tabs=0):
        return self.expr.print_tree(tabs)

    @addToClass(AST.MethodCallExpr)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "FUNCALL\n"
        tabs += 1
        res += self.name.print_tree(tabs)
        for a in self.args:
            res += a.print_tree(tabs)
        return res

    @addToClass(AST.FunctionDef)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "FUNDEF\n"
        tabs += 1
        res += self.name.print_tree(tabs)
        res += self.print_tabs(tabs) + "RET " + self.return_type.name + "\n"
        for a in self.args:
            res += a.print_tree(tabs)
        res += self.body.print_tree(tabs)
        return res

    @addToClass(AST.Argument)
    def print_tree(self, tabs=0):
        res = self.print_tabs(tabs) + "ARG \n"
        tabs += 1
        res += self.arg_type.print_tree(tabs)
        res += self.name.print_tree(tabs)
        return res

    @addToClass(AST.CompoundExpr)
    def print_tree(self, tabs=0):
        res = ""
        for d in self.declarations:
            res += d.print_tree(tabs)
        for f in self.fundefs:
            res += f.print_tree(tabs)
        return res
