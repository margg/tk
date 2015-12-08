class Node(object):

    def add_lineno(self, lineno):
        self.lineno = lineno
        return self

    def __str__(self):
        return self.print_tree()


class Name(Node):
    def __init__(self, name):
        super(Name, self).__init__()
        self.name = name


class CheckedName(Name):
    pass


class Operator(Node):
    def __init__(self, op):
        super(Operator, self).__init__()
        self.op = op


class Program(Node):
    def __init__(self, body):
        super(Program, self).__init__()
        self.body = []
        if body:
            self.body.extend(body)


class Declaration(Node):
    def __init__(self, var_type, inits):
        super(Declaration, self).__init__()
        self.var_type = var_type
        self.inits = []
        if inits:
            self.inits.extend(inits)


class Initializer(Node):
    def __init__(self, name, expression):
        super(Initializer, self).__init__()
        self.name = name
        self.expression = expression


class Instruction(Node):
    pass


class PrintInstr(Instruction):
    def __init__(self, expr_list):
        super(PrintInstr, self).__init__()
        self.expr_list = []
        if expr_list:
            self.expr_list.extend(expr_list)


class LabeledInstr(Instruction):
    def __init__(self, label, instruction):
        super(LabeledInstr, self).__init__()
        self.label = label
        self.instruction = instruction


class Assignment(Instruction):
    def __init__(self, target, value):
        super(Assignment, self).__init__()
        self.target = target
        self.value = value


class IfInstr(Instruction):
    def __init__(self, condition, body, else_body):
        super(IfInstr, self).__init__()
        self.condition = condition
        self.body = body
        self.else_body = else_body


class WhileInstr(Instruction):
    def __init__(self, condition, body):
        super(WhileInstr, self).__init__()
        self.condition = condition
        self.body = body


class RepeatInstr(Instruction):
    def __init__(self, body, condition):
        super(RepeatInstr, self).__init__()
        self.condition = condition
        self.body = []
        if body:
            self.body.extend(body)


class ReturnInstr(Instruction):
    def __init__(self, expression):
        super(ReturnInstr, self).__init__()
        self.expression = expression


class ContinueInstr(Instruction):
    def __init__(self):
        super(ContinueInstr, self).__init__()


class BreakInstr(Instruction):
    def __init__(self):
        super(BreakInstr, self).__init__()


class CompoundInstr(Instruction):
    def __init__(self, declarations, instructions):
        super(CompoundInstr, self).__init__()
        self.declarations = []
        self.instructions = []
        if declarations:
            self.declarations.extend(declarations)
        if instructions:
            self.instructions.extend(instructions)


class Expression(Node):
    pass


class Const(Expression):
    def __init__(self, value):
        super(Const, self).__init__()
        self.value = value


class Integer(Const):
    def __init__(self, value):
        super(Integer, self).__init__(value)


class Float(Const):
    def __init__(self, value):
        super(Float, self).__init__(value)


class String(Const):
    def __init__(self, value):
        super(String, self).__init__(value)


class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        super(BinaryExpr, self).__init__()
        self.op = op
        self.left = left
        self.right = right


class MethodCallExpr(Expression):
    def __init__(self, name, args):
        super(MethodCallExpr, self).__init__()
        self.name = name
        self.args = []
        if args:
            self.args.extend(args)


class FunctionDef(Node):
    def __init__(self, return_type, name, args, body):
        super(FunctionDef, self).__init__()
        self.return_type = return_type
        self.name = name
        self.args = []
        self.body = body
        if args:
            self.args.extend(args)


class Argument(Node):
    def __init__(self, arg_type, name):
        super(Argument, self).__init__()
        self.arg_type = arg_type
        self.name = name
