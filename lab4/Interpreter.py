
import AST
import SymbolTable
from lab4.Memory import *
from lab4.Exceptions import *
from lab4.visit import *

import sys

sys.setrecursionlimit(10000)


class Interpreter(object):

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        self.global_memory = MemoryStack()
        self.function_memory = None
        for instr in node.body:
            instr.accept(self)

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

    @when(AST.Instruction)
    def visit(self, node):
        node.accept(self)

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
        pass

    @when(AST.ContinueInstr)
    def visit(self, node):
        pass

    @when(AST.BreakInstr)
    def visit(self, node):
        raise BreakException()

    @when(AST.CompoundInstr)
    def visit(self, node):
        pass


    @when(AST.BinaryExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.MethodCallExpr)
    def visit(self, node):
        old_memory = self.function_memory
        self.function_memory = MemoryStack()

        # szukamy w "symbol table" odniesienia do FunctionDef dla tej funkcji
        # wywolujemy z parametrami. - wrzucamy do function_memory
        # fundef.args - zip - parameters

        try:
            pass
        except ReturnValueException:
            self.function_memory = old_memory
            # ...

    @when(AST.FunctionDef)
    def visit(self, node):
        # symbol table?
        # lista definicji funkcji  - zapisujemy w nich node
        pass






