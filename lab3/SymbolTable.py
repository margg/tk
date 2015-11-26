#!/usr/bin/python


class Symbol:
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.type = type
        self.name = name


class FundefSymbol(Symbol):

    def __init__(self, name, type, args):
        self.type = type
        self.name = name
        self.args = args


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.items = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.items[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.items:
            return self.items[name]
        return None

    def getParentScope(self): # ???
        pass

    def pushScope(self, name): # ???
        pass

    def popScope(self): # ???
        pass

