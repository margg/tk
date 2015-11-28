#!/usr/bin/python

import AST
from SymbolTable import SymbolTable, Symbol, VariableSymbol, FunctionDefSymbol
from collections import defaultdict


class NodeVisitor:

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        print(method)
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        # else:
        #     for child in node.children:
        #         if isinstance(child, list):
        #             for item in child:
        #                 if isinstance(item, AST.Node):
        #                     self.visit(item)
        #         elif isinstance(child, AST.Node):
        #             self.visit(child)
        print("generic visit of %s" % node.__class__.__name__)

        # simpler version of generic_visit, not so general
        # def generic_visit(self, node):
        # for child in node.children:
        #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, "TypeChecker")
        self.ttypes = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
        self.fill_ttypes()

    def fill_ttypes(self):
        # arithmetic int operations
        self.add_ttype('+', 'int', 'int', 'int')
        self.add_ttype('-', 'int', 'int', 'int')
        self.add_ttype('*', 'int', 'int', 'int')
        self.add_ttype('/', 'int', 'int', 'int')
        self.add_ttype('%', 'int', 'int', 'int')
        # binary int operations
        self.add_ttype('&', 'int', 'int', 'int')
        self.add_ttype('|', 'int', 'int', 'int')
        self.add_ttype('^', 'int', 'int', 'int')
        self.add_ttype('<<', 'int', 'int', 'int')
        self.add_ttype('>>', 'int', 'int', 'int')
        # arithmetic float operations
        self.add_ttype('+', 'float', 'float', 'float')
        self.add_ttype('-', 'float', 'float', 'float')
        self.add_ttype('*', 'float', 'float', 'float')
        self.add_ttype('/', 'float', 'float', 'float')
        self.add_ttype('%', 'float', 'float', 'float')
        self.add_ttype('+', 'int', 'float', 'float')
        self.add_ttype('-', 'int', 'float', 'float')
        self.add_ttype('*', 'int', 'float', 'float')
        self.add_ttype('/', 'int', 'float', 'float')
        self.add_ttype('%', 'int', 'float', 'float')
        self.add_ttype('+', 'float', 'int', 'float')
        self.add_ttype('-', 'float', 'int', 'float')
        self.add_ttype('*', 'float', 'int', 'float')
        self.add_ttype('/', 'float', 'int', 'float')
        self.add_ttype('%', 'float', 'int', 'float')
        # relational int operations
        self.add_ttype('==', 'int', 'int', 'int')
        self.add_ttype('!=', 'int', 'int', 'int')
        self.add_ttype('<', 'int', 'int', 'int')
        self.add_ttype('>', 'int', 'int', 'int')
        self.add_ttype('<=', 'int', 'int', 'int')
        self.add_ttype('>=', 'int', 'int', 'int')
        # relational float operations
        self.add_ttype('==', 'float', 'float', 'float')
        self.add_ttype('!=', 'float', 'float', 'float')
        self.add_ttype('<', 'float', 'float', 'float')
        self.add_ttype('>', 'float', 'float', 'float')
        self.add_ttype('<=', 'float', 'float', 'float')
        self.add_ttype('>=', 'float', 'float', 'float')
        self.add_ttype('==', 'int', 'float', 'float')
        self.add_ttype('!=', 'int', 'float', 'float')
        self.add_ttype('<', 'int', 'float', 'float')
        self.add_ttype('>', 'int', 'float', 'float')
        self.add_ttype('<=', 'int', 'float', 'float')
        self.add_ttype('>=', 'int', 'float', 'float')
        self.add_ttype('==', 'float', 'int', 'float')
        self.add_ttype('!=', 'float', 'int', 'float')
        self.add_ttype('<', 'float', 'int', 'float')
        self.add_ttype('>', 'float', 'int', 'float')
        self.add_ttype('<=', 'float', 'int', 'float')
        self.add_ttype('>=', 'float', 'int', 'float')
        # string operations
        self.add_ttype('+', 'string', 'string', 'string')
        self.add_ttype('*', 'string', 'int', 'string')
        self.add_ttype('==', 'string', 'string', 'string')
        self.add_ttype('!=', 'string', 'string', 'string')
        self.add_ttype('<', 'string', 'string', 'string')
        self.add_ttype('>', 'string', 'string', 'string')
        self.add_ttype('<=', 'string', 'string', 'string')
        self.add_ttype('>=', 'string', 'string', 'string')
        self.add_ttype('*', 'string', 'int', 'string')

    def add_ttype(self, operation, operand1, operand2, returned):
        self.ttypes[operation][operand1][operand2] = returned

    def visit_Name(self, node):
        return node.name

    def visit_Operator(self, node):
        return node.op

    def visit_Program(self, node):
        self.visit(node.body)

    def visit_Declaration(self, node):
        for init in node.inits:
            name = self.visit(init.name)
            if self.symbol_table.get(name) is not None:
                print("multiple definition of '%s' on line %d" % (init.name, node.lineno))
            self.symbol_table.put(name, VariableSymbol(init.name, node.var_type))
            self.visit(init)

    def visit_Initializer(self, node):
        name = self.visit(node.name)
        expression = self.visit(node.expression)
        declared_type = self.symbol_table.get(name).type.name
        if declared_type == 'int' and expression == 'float':
            print("possible loss of precision on line %s: assigning %s to %s" % (node.lineno, expression, declared_type))
        elif declared_type == 'float' and expression == 'int':
            pass
        elif declared_type != expression:
            print("type mismatch on line %s: assigning %s to %s" % (node.lineno, expression, declared_type))


    # def visit_BinExpr(self, node):
    # # alternative usage,
    #                                       # requires definition of accept method in class Node
    #     type1 = self.visit(node.left)     # type1 = node.left.accept(self)
    #     type2 = self.visit(node.right)    # type2 = node.right.accept(self)
    #     op    = node.op;
    #     # ...
    #     #
    #
    # def visit_RelExpr(self, node):
    #     type1 = self.visit(node.left)     # type1 = node.left.accept(self)
    #     type2 = self.visit(node.right)    # type2 = node.right.accept(self)
    #     # ...
    #     #
    #

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'
