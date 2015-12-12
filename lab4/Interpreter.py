
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
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
        try:
            for instr in node.body:
                instr.accept(self)
        except ReturnValueException as e:
            return e.value


    @when(AST.Declaration)
    def visit(self, node):
        if self.function_memory:
            pass
            # wrzucamy do memory funkcji
        else:
            # do global
            pass

    @when(AST.BinaryExpr)
    def visit(self, node):
        r1 = node.left.accept(self) # self.visit(node.left)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
        pass

    @when(AST.Const)
    def visit(self, node):
        return node.value

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

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




