#!/usr/bin/python

import AST
from SymbolTable import SymbolTable, Symbol, VariableSymbol, FunctionDefSymbol
from collections import defaultdict


class NodeVisitor:

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, "TypeChecker", {})
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

    def add_ttype(self, operation, operand1, operand2, returned):
        self.ttypes[operation][operand1][operand2] = returned

    def visit_Name(self, node):
        return node.name

    def visit_CheckedName(self, node):
        if self.symbol_table.get(node.name):
            return node.name
        else:
            print("Error: Usage of undeclared variable '%s': line %s" % (node.name, node.lineno))
            return node.name

    def visit_Operator(self, node):
        return node.op

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Program(self, node):
        self.symbol_table = self.symbol_table.push_scope("Program")
        for item in node.body:
            self.visit(item)
        self.symbol_table = self.symbol_table.pop_scope()

    def visit_Declaration(self, node):
        for init in node.inits:
            name = self.visit(init.name)
            var = self.symbol_table.get_declared_var(name)
            if var:
                if isinstance(var, FunctionDefSymbol):
                    print("Error: Function identifier '%s' used as a variable: line %d" % (name, node.lineno))
                else:
                    print("Error: Variable '%s' already declared: line %d" % (name, node.lineno))
            else:
                self.symbol_table.put(name, VariableSymbol(init.name, node.var_type))
            self.visit(init)

    def visit_Initializer(self, node):
        expression_ret_type = self.get_return_type(node.expression)
        declared_type = self.get_return_type(node.name)
        if expression_ret_type and declared_type:
            TypeChecker.check_type_consistency(node, declared_type, expression_ret_type)

    def visit_PrintInstr(self, node):
        for item in node.expr_list:
            self.visit(item)

    def visit_LabeledInstr(self, node):
        self.visit(node.instruction)

    def visit_Assignment(self, node):
        declared_type = self.get_return_type(node.target)
        expression_ret_type = self.get_return_type(node.value)
        if not declared_type:
            print("Error: Variable '%s' undefined in current scope: line %d" % (self.visit(node.target), node.lineno))
        elif expression_ret_type:
            TypeChecker.check_type_consistency(node, declared_type, expression_ret_type)

    def visit_IfInstr(self, node):
        self.visit(node.condition)
        self.visit(node.body)
        if node.else_body:
            self.visit(node.else_body)

    def visit_WhileInstr(self, node):
        self.visit(node.condition)
        self.symbol_table.set_inside_loop(1)
        self.visit(node.body)
        self.symbol_table.set_inside_loop(0)

    def visit_RepeatInstr(self, node):
        self.symbol_table.set_inside_loop(1)
        for item in node.body:
            self.visit(item)
        self.visit(node.condition)
        self.symbol_table.set_inside_loop(0)


    def visit_ReturnInstr(self, node):
        ret_type = self.get_return_type(node.expression)
        scope = self.symbol_table
        while scope and scope.name != "FunctionDef":
            scope = scope.get_parent_scope()
        if scope:
            fun_def = scope.get(scope.function_name)
            if fun_def:
                function_ret_type = fun_def.type.name
                scope.set_return_present(1)
                if ret_type and function_ret_type:
                    if function_ret_type == 'int' and ret_type == 'float':
                        print("Warning: Possible loss of precision: returning %s from function returning %s: line %s" %
                              (ret_type, function_ret_type, node.lineno))
                    elif function_ret_type == 'float' and ret_type == 'int':
                        pass
                    elif ret_type != function_ret_type:
                        print("Error: Improper returned type, expected %s, got %s: line %s" %
                              (function_ret_type, ret_type, node.lineno))
            else:
                # should not happen...
                print("something bad happened while parsing or checking")
        else:
            print("Error: return instruction outside a function: line %s" % node.lineno)

    def visit_ContinueInstr(self, node):
        if not self.symbol_table.is_inside_loop():
            print("Error: continue instruction outside a loop: line %s" % node.lineno)

    def visit_BreakInstr(self, node):
        if not self.symbol_table.is_inside_loop():
            print("Error: break instruction outside a loop: line %s" % node.lineno)

    def visit_CompoundInstr(self, node):
        self.symbol_table = self.symbol_table.push_scope("CompoundInstr")
        for item in node.declarations:
            self.visit(item)
        for item in node.instructions:
            self.visit(item)
        self.symbol_table = self.symbol_table.pop_scope()

    def visit_BinaryExpr(self, node):
        type_1 = self.get_return_type(node.left)
        if not type_1:
            print("Error: Usage of undeclared variable '%s': line %s" % (self.visit(node.left), node.lineno))
        type_2 = self.get_return_type(node.right)
        if not type_2:
            print("Error: Usage of undeclared variable '%s': line %s" % (self.visit(node.right), node.lineno))
        op = self.visit(node.op)
        ret = self.ttypes[op][type_1][type_2]
        if not ret:
            print("Error: Illegal operation, %s %s %s: line %s" % (type_1, op, type_2, node.left.lineno))
        return ret

    def visit_MethodCallExpr(self, node):
        name = self.visit(node.name)
        fun_def = self.symbol_table.get(name)
        if fun_def:
            if len(fun_def.args) != len(node.args):
                print("Error: Improper number of args in %s call: line %s" % (fun_def.name.name, node.lineno))
            else:
                for (fun_arg, call_arg) in zip(fun_def.args, node.args):
                    fun_arg_type = fun_arg.arg_type.name
                    call_arg_type = self.get_return_type(call_arg)
                    if fun_arg_type and call_arg_type:
                        if fun_arg_type == 'int' and call_arg_type == 'float':
                            print("Warning: Possible loss of precision: passing %s instead of %s: line %s" %
                                  (call_arg_type, fun_arg_type, node.lineno))
                        elif fun_arg_type == 'float' and call_arg_type == 'int':
                            pass
                        elif call_arg_type != fun_arg_type:
                            print("Error: Improper type of args in %s call: line %s" % (name, node.lineno))
                            break
            return fun_def.type.name
        else:
            print("Error: Call of undefined function: '%s': line %s" % (name, node.lineno))

    def visit_FunctionDef(self, node):
        name = self.visit(node.name)
        if self.symbol_table.get(name):
            print("Error: Redefinition of function '%s': line %s" % (name, node.lineno))
        self.symbol_table.put(name, FunctionDefSymbol(node.name, node.return_type, node.args))
        self.symbol_table = self.symbol_table.push_scope("FunctionDef")
        self.symbol_table.put(name, FunctionDefSymbol(node.name, node.return_type, node.args))
        self.symbol_table.function_name = name
        for arg in node.args:
            self.visit(arg)
        self.symbol_table.set_return_present(0)
        self.visit(node.body)
        if not self.symbol_table.get_return_present():
            print("Error: Missing return statement in function '%s' returning %s: line %s" %
                  (name, self.visit(node.return_type), node.lineno))
        self.symbol_table = self.symbol_table.pop_scope()

    def visit_Argument(self, node):
        name = self.visit(node.name)
        if self.symbol_table.name == "FunctionDef":
            self.symbol_table.put(name, VariableSymbol(node.name, node.arg_type))

    def get_return_type(self, node):
        if isinstance(node, AST.Name):
            var = self.symbol_table.get(node.name)
            return None if not var else var.type.name
        return self.visit(node)

    @staticmethod
    def check_type_consistency(node, declared_type, expression_ret_type):
        if declared_type == 'int' and expression_ret_type == 'float':
            print("Warning: Possible loss of precision: assignment of %s to %s: line %s" %
                  (expression_ret_type, declared_type, node.lineno))
        elif declared_type == 'float' and expression_ret_type == 'int':
            pass
        elif declared_type != expression_ret_type:
            print("Error: Assignment of %s to %s: line %s" % (expression_ret_type, declared_type, node.lineno))

