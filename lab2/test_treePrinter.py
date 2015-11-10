from unittest import TestCase
from lab2 import AST
from lab2.TreePrinter import TreePrinter


class TestTreePrinter(TestCase):

    def setUp(self):
        self.printer = TreePrinter()

    def test_print_initializer(self):
        init = AST.Initializer(AST.Name("a"), AST.Integer(0))
        printed = """=
| a
| 0
"""
        result = init.print_tree()
        assert result == printed

    def test_print_declaration(self):
        decl = AST.Declaration(AST.Name("float"), [AST.Initializer(AST.Name("a"), AST.Integer(0))])
        printed = """DECL (float)
| =
| | a
| | 0
"""
        result = decl.print_tree()
        assert result == printed

    def test_print_declarations(self):
        decl = AST.Declaration(AST.Name("float"), [AST.Initializer(AST.Name("a"), AST.Integer(0)),
                                                   AST.Initializer(AST.Name("a"), AST.Integer(0))])
        printed = """DECL (float)
| =
| | a
| | 0
| =
| | a
| | 0
"""
        result = decl.print_tree()
        assert result == printed
