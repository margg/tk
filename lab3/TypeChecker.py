#!/usr/bin/python

import AST


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        print(method)
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)
        print("generic visit of {0}", node.__class__.__name__)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.correct_ttypes = {}
        self.fill_ttypes()

    def fill_ttypes(self):
        # arithmetic int operations
        self.add_ttype('+','int','int','int')
        self.add_ttype('-','int','int','int')
        self.add_ttype('*','int','int','int')
        self.add_ttype('/','int','int','int')
        self.add_ttype('%','int','int','int')
        # binary int operations
        self.add_ttype('&','int','int','int')
        self.add_ttype('|','int','int','int')
        self.add_ttype('^','int','int','int')
        self.add_ttype('<<','int','int','int')
        self.add_ttype('>>','int','int','int')
        # arithmetic float operations
        self.add_ttype('+','float','float','float')
        self.add_ttype('-','float','float','float')
        self.add_ttype('*','float','float','float')
        self.add_ttype('/','float','float','float')
        self.add_ttype('%','float','float','float')
        self.add_ttype('+','int','float','float')
        self.add_ttype('-','int','float','float')
        self.add_ttype('*','int','float','float')
        self.add_ttype('/','int','float','float')
        self.add_ttype('%','int','float','float')
        self.add_ttype('+','float','int','float')
        self.add_ttype('-','float','int','float')
        self.add_ttype('*','float','int','float')
        self.add_ttype('/','float','int','float')
        self.add_ttype('%','float','int','float')
        # relational int operations
        self.add_ttype('==','int','int','int')
        self.add_ttype('!=','int','int','int')
        self.add_ttype('<','int','int','int')
        self.add_ttype('>','int','int','int')
        self.add_ttype('<=','int','int','int')
        self.add_ttype('>=','int','int','int')
        # relational float operations
        self.add_ttype('==','float','float','float')
        self.add_ttype('!=','float','float','float')
        self.add_ttype('<','float','float','float')
        self.add_ttype('>','float','float','float')
        self.add_ttype('<=','float','float','float')
        self.add_ttype('>=','float','float','float')
        self.add_ttype('==','int','float','float')
        self.add_ttype('!=','int','float','float')
        self.add_ttype('<','int','float','float')
        self.add_ttype('>','int','float','float')
        self.add_ttype('<=','int','float','float')
        self.add_ttype('>=','int','float','float')
        self.add_ttype('==','float','int','float')
        self.add_ttype('!=','float','int','float')
        self.add_ttype('<','float','int','float')
        self.add_ttype('>','float','int','float')
        self.add_ttype('<=','float','int','float')
        self.add_ttype('>=','float','int','float')
        # string operations
        self.add_ttype('+','string','string','string')
        self.add_ttype('+','string','int','string')
        self.add_ttype('==','string','string','string')
        self.add_ttype('!=','string','string','string')
        self.add_ttype('<','string','string','string')
        self.add_ttype('>','string','string','string')
        self.add_ttype('<=','string','string','string')
        self.add_ttype('>=','string','string','string')



    def add_ttype(self, operation, operand1, operand2, returned):
        self.correct_ttypes[operation][operand1][operand2] = returned

    def visit_Program(self, node):
        pass

    # def visit_BinExpr(self, node):
    #                                       # alternative usage,
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

    def visit_Const(self, node):
        # if type(node.value) == str:
        #     self.visit(node.value)
        # elif type(node.value) == int:
        #     self.visit(node.value)
        # elif type(node.value) == float:
        #     self.visit(node.value)

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'
