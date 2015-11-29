import ply.yacc as yacc
from Cparser import Cparser
import TreePrinter
from TypeChecker import TypeChecker
import os
from cStringIO import StringIO
import sys


if __name__ == '__main__':

    Cparser = Cparser()

    test_dir = "tests_err"

    test_in = []
    for dirpath, dirnames, filenames in os.walk(test_dir):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            elif filename.endswith('.in'):
                test_in.append(filename)

    # test_in = ["control_transfer.in"]
    # test_in = ["funs1.in"]
    # test_in = ["funs2.in"]
    # test_in = ["funs3.in"]
    # test_in = ["funs4.in"]
    # test_in = ["funs5.in"]
    # test_in = ["funs6.in"]
    # test_in = ["funs7.in"]                # shadowing
    # test_in = ["funs8.in"]                # shadowing
    # test_in = ["opers.in"]                # lineno nie dziala
    # test_in = ["vars_redeclared.in"]
    # test_in = ["vars_undef.in"]           # undeclared variable w princie

    parser = yacc.yacc(module=Cparser)

    try:
        file_path = os.path.join(test_dir, filename)
        file = open(file_path, "r")
    except IOError:
        print("Cannot open {0} file".format(file_path))
        sys.exit(0)

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    text = file.read()
    ast = parser.parse(text, lexer=Cparser.scanner, debug=False)
    if ast:
        printer = TreePrinter.TreePrinter()
        ast.print_tree()

    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    sys.stdout = old_stdout

    name = os.path.join(test_dir, os.path.splitext(filename)[0])
    file_expected = "{0}.expected".format(name)
    actual_content = mystdout.getvalue()
    expected_content = open(file_expected).read()
    res = cmp(actual_content, expected_content)
    assert res == 0, "test output and file {0} differ\n---ACTUAL---\n{1}\n---EXPECTED---\n{2}\n---".format(
        file_expected, actual_content, expected_content)
    print("Passed test for file '%s'." % filename)
