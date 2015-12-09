#!/usr/bin/python


class Symbol:
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class FunctionDefSymbol(Symbol):

    def __init__(self, name, type, args):
        self.name = name
        self.type = type
        self.args = args


class SymbolTable:

    def __init__(self, parent, name, items=None):   # parent scope and symbol table name
        self.parent = parent
        self.name = name
        if items is None:
            self.items = {}
        else:
            self.items = dict(items)

    def put(self, name, symbol):    # put variable symbol or fundef under <name> entry
        self.items[name] = symbol

    def get(self, name):    # get variable symbol or fundef from <name> entry - through all scopes up
        if name in self.items:
            return self.items[name]
        else:
            return None if not self.get_parent_scope() else self.get_parent_scope().get(name)

    def get_declared_var(self, name):    # get variable symbol or fundef from <name> entry
        if name in self.items:           # - vars in the scope, fundefs through all scopes up
            return self.items[name]
        else:
            return self.get_fun_def(name)

    def get_fun_def(self, name):    # get fundef from <name> entry - through all scopes up
        if name in self.items:
            if isinstance(self.items[name], FunctionDefSymbol):
                return self.items[name]
        else:
            return None if not self.get_parent_scope() else self.get_parent_scope().get_fun_def(name)

    def get_parent_scope(self):
        return self.parent

    def push_scope(self, name):
        return SymbolTable(self, name)

    def pop_scope(self):
        return self.get_parent_scope()

    def set_return_present(self, value):
        self.return_present = value

    def get_return_present(self):
        return 1 if hasattr(self, 'return_present') and self.return_present else 0

    def set_inside_loop(self, value):
        self.inside_loop = value

    def is_inside_loop(self):
        if hasattr(self, 'inside_loop') and self.inside_loop:
            return 1
        else:
            return self.get_parent_scope() and self.get_parent_scope().is_inside_loop()

