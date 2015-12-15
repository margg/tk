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
        self.global_memory.push(Memory("global"))
        self.function_memory = None
        self.binary_ops = {
            "+": (lambda a, b: a + b),
            "-": (lambda a, b: a - b),
            "*": (lambda a, b: a * b),
            "/": (lambda a, b: a / b),
            "%": (lambda a, b: a % b),
            "==": (lambda a, b: a == b),
            "<=": (lambda a, b: a <= b),
            ">=": (lambda a, b: a >= b),
            ">": (lambda a, b: a > b),
            "<": (lambda a, b: a < b),
            "!=": (lambda a, b: a != b),
            "||": (lambda a, b: a or b),
            "&&": (lambda a, b: a and b),
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
        if self.function_memory:
            ret = self.function_memory.get(node.name)
            if ret is not None:
                return ret
        return self.global_memory.get(node.name)

    @when(AST.CheckedName)
    def visit(self, node):
        if self.function_memory:
            ret = self.function_memory.get(node.name)
            if ret is not None:
                return ret
        return self.global_memory.get(node.name)

    @when(AST.Operator)
    def visit(self, node):
        return node.op

    @when(AST.Declaration)
    def visit(self, node):
        for init in node.inits:
            init.accept(self)

    @when(AST.Initializer)
    def visit(self, node):
        name = node.name.name
        value = node.expression.accept(self)
        if self.function_memory:
            self.function_memory.insert(name, value)
        else:
            self.global_memory.insert(name, value)

    @when(AST.PrintInstr)
    def visit(self, node):
        for expression in node.expr_list:
            print(expression.accept(self))

    @when(AST.LabeledInstr)
    def visit(self, node):
        pass

    @when(AST.Assignment)
    def visit(self, node):
        target = node.target.name
        value = node.value.accept(self)
        if self.function_memory:
            self.function_memory.insert(target, value)
        else:
            self.global_memory.insert(target, value)

    @when(AST.IfInstr)
    def visit(self, node):
        if node.condition.accept(self):
            node.body.accept(self)
        else:
            node.else_body.accept(self)

    @when(AST.WhileInstr)
    def visit(self, node):
        try:
            while node.condition.accept(self):
                try:
                    for instr in node.body:
                        instr.accept(self)
                except ContinueException:
                    continue
        except BreakException:
            return

    @when(AST.RepeatInstr)
    def visit(self, node):
        try:
            for instr in node.body:
                instr.accept(self)
            while not node.condition.accept(self):
                try:
                    for instr in node.body:
                        instr.accept(self)
                except ContinueException:
                    continue
        except BreakException:
            return

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
        if self.function_memory:
            self.function_memory.push(Memory("compound_function"))
        else:
            self.global_memory.push(Memory("compound_global"))
        for decl in node.declarations:
            decl.accept(self)
        for instr in node.instructions:
            instr.accept(self)
        if self.function_memory:
            self.function_memory.pop()
        else:
            self.global_memory.pop()

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.BinaryExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return self.binary_ops[node.op.accept(self)](r1, r2)

    @when(AST.MethodCallExpr)
    def visit(self, node):
        old_memory = self.function_memory
        evaluated_args = [call_arg.accept(self) for call_arg in node.args]
        self.function_memory = MemoryStack()
        self.function_memory.push(Memory("function"))
        fun_def = self.fun_defs.get(node.name.name)
        for call_arg, fun_arg in zip(evaluated_args, fun_def.args):
            self.function_memory.insert(fun_arg.name.name, call_arg)
        try:
            fun_def.body.accept(self)
        except ReturnValueException as e:
            self.function_memory = old_memory
            return e.value

    @when(AST.Argument)
    def visit(self, node):
        return node.name.name

    @when(AST.FunctionDef)
    def visit(self, node):
        self.fun_defs.put(node.name.name, node)




