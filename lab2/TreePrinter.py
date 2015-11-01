import ast


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(ast.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(ast.BinExpr)
    def printTree(self):
        pass
        # ...

    # @addToClass ...
    # ...