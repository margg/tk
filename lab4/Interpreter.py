import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *

import sys

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.fun_defs = SymbolTable.SymbolTable(None, "FunctionDefs")
        self.global_memory = MemoryStack()
        self.function_memory = None
        self.binary_ops = {
            "+": (lambda a, b: a + b),
            "-": (lambda a, b: a - b),
            "*": (lambda a, b: a * b),
            "/": (lambda a, b: a / b),
            "%": (lambda a, b: a % b),
        }

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        try:
            for instr in node.body:
                instr.accept(self)
        except ReturnValueException as e:
            return e.value

    @when(AST.Name)
    def visit(self, node):
        return node.name

    @when(AST.CheckedName)
    def visit(self, node):
        return node.name

    @when(AST.Operator)
    def visit(self, node):
        return node.op

    @when(AST.CheckedName)
    def visit(self, node):
        return node.name

    @when(AST.Declaration)
    def visit(self, node):
        for init in node.inits:
            init.accept(self)

    @when(AST.Initializer)
    def visit(self, node):
        name = node.name.accept(self)
        value = node.expression.accept(self)
        if self.function_memory:
            self.function_memory.insert(name, value)
        else:
            self.global_memory.insert(name, value)

    # @when(AST.Instruction)
    # def visit(self, node):
    #     node.accept(self)

    @when(AST.PrintInstr)
    def visit(self, node):
        for expression in node.expr_list:
            print(expression.accept(self))

    @when(AST.LabeledInstr)
    def visit(self, node):
        pass

    @when(AST.Assignment)
    def visit(self, node):
        target = node.target.accept(self)
        value = node.value.accept(self)
        if self.function_memory:
            self.function_memory.insert(target, value)
        else:
            self.global_memory.insert(target, value)

    @when(AST.IfInstr)
    def visit(self, node):
        if node.condition.accept(self):
            return node.body.accept(self)
        else:
            return node.else_body.accept(self)

    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        try:
            while node.condition.accept(self):
                try:
                    r = node.body.accept(self)
                except ContinueException:
                    continue
            return r
        except BreakException:
            return r

    @when(AST.RepeatInstr)
    def visit(self, node):
        r = None
        try:
            node.body.accept(self)
            while not node.condition.accept(self):
                try:
                    r = node.body.accept(self)
                except ContinueException:
                    continue
            return r
        except BreakException:
            return r

    @when(AST.ReturnInstr)
    def visit(self, node):
        raise ReturnValueException(node.expression.accept(self))

    @when(AST.ContinueInstr)
    def visit(self, node):
        raise ContinueException

    @when(AST.BreakInstr)
    def visit(self, node):
        raise BreakException

    @when(AST.CompoundInstr)
    def visit(self, node):
        # check other exceptions if something is wrong
        for decl in node.declarations:
            decl.accept(self)
        for instr in node.instructions:
            instr.accept(self)

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.BinaryExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return self.binary_ops[node.op.accept(self)](r1, r2)

    @when(AST.MethodCallExpr)
    def visit(self, node):
        old_memory = self.function_memory
        self.function_memory = MemoryStack()
        fun_def = self.fun_defs.get(node.name)
        for call_arg, fun_arg in zip(node.args, fun_def.args):
            self.function_memory.insert(fun_arg.accept(self), call_arg.accept(self))
        try:
            node.body.accept(self)
            # for decl in node.body.declarations:
            #     decl.accept(self)
            # for instr in node.body.instructions:
            #     instr.accept(self)
        except ReturnValueException as e:
            self.function_memory = old_memory
            return e.value

    @when(AST.Argument)
    def visit(self, node):
        return node.name


    @when(AST.FunctionDef)
    def visit(self, node):
        self.fun_defs.put(node.name, node)




