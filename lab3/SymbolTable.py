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

    def get(self, name):    # get variable symbol or fundef from <name> entry
        if name in self.items:
            return self.items[name]
        return None

    def get_parent_scope(self):
        return self.parent

    def push_scope(self, name):
        return SymbolTable(self, name, self.items)

    def pop_scope(self):
        return self.get_parent_scope()

