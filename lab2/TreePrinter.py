import ast


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(ast.Node)
    def print_tree(self):
        raise Exception("print_tree not defined in class " + self.__class__.__name__)

    @addToClass(ast.Name)
    def print_tree(self):
        return self.name

    @addToClass(ast.Operator)
    def print_tree(self):
        return "" + self.op

    @addToClass(ast.Program)
    def print_tree(self):
        res = ""
        for i in self.body:
            res += i.print_tree()
        return res

    @addToClass(ast.Declaration)
    def print_tree(self):
        res = self.var_type.print_tree()
        for i in self.inits:
            res += i.print_tree()
        return res

    @addToClass(ast.Initializator)
    def print_tree(self):
        return self.name.print_tree() + "=" + self.expression.print_tree()

    # @addToClass(ast.Instruction)
    # def print_tree(self):
    #     pass

    @addToClass(ast.PrintInstr)
    def print_tree(self):
        res = "print "
        for e in self.expr_list:
            res += e.print_tree()
        return res

    @addToClass(ast.LabeledInstr)
    def print_tree(self):
        return self.label.print_tree() + ": " + self.instruction.print_tree()

    @addToClass(ast.Assignment)
    def print_tree(self):
        return self.target.print_tree() + " = " + self.value.print_tree()

    @addToClass(ast.IfInstr)
    def print_tree(self):
        res = "if (" + self.condition.print_tree() + ") "
        for i in self.body:
            res += i.print_tree()
        if self.else_body:
            res += "else "
            for i in self.else_body:
                res += i.print_tree()
        return res

    @addToClass(ast.WhileInstr)
    def print_tree(self):
        res = "while (" + self.condition.print_tree() + ")"
        for i in self.body:
            res += i.print_tree()
        return res

    @addToClass(ast.RepeatInstr)
    def print_tree(self):
        res = "repeat {"
        for i in self.body:
            res += i.print_tree()
        res += "} until (" + self.condition.print_tree() + ")"
        return res

    @addToClass(ast.ReturnInstr)
    def print_tree(self):
        return "return " + self.expression.print_tree()

    @addToClass(ast.ContinueInstr)
    def print_tree(self):
        return "continue;"


    @addToClass(ast.BreakInstr)
    def print_tree(self):
        return "break;"

    # @addToClass(ast.Expression)
    # def print_tree(self):
    #     pass

    @addToClass(ast.Const)
    def print_tree(self):
        return self.value

    @addToClass(ast.Integer)
    def print_tree(self):
        return self.value

    @addToClass(ast.Float)
    def print_tree(self):
        return self.value

    @addToClass(ast.String)
    def print_tree(self):
        return self.value

    @addToClass(ast.BinaryExpr)
    def print_tree(self):
        return self.left.print_tree() + self.op.print_tree() + self.right.print_tree()

    @addToClass(ast.EnclosedExpr)
    def print_tree(self):
        return "(" + self.expr.print_tree() + ")"

    @addToClass(ast.MethodCallExpr)
    def print_tree(self):
        res = self.name.print_tree() + "("
        for a in self.args:
            res += a.print_tree()
        return res + ")"

    @addToClass(ast.FunctionDef)
    def print_tree(self):
        res = self.return_type.print_tree() + " " + self.name.print_tree() + "("
        for a in self.args:
            res += a.print_tree() + ", "
        res += ") {"
        for i in self.body:
            res += i.print_tree()
        return res + "}"

    @addToClass(ast.Argument)
    def print_tree(self):
        return self.arg_type.print_tree() + " " + self.name.print_tree()