import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter
import os
from cStringIO import StringIO
import sys


def test_file(test_dir, filename):
    cparser = Cparser()
    parser = yacc.yacc(module=cparser)

    try:
        file_path = os.path.join(test_dir, filename)
        file = open(file_path, "r")
    except IOError:
        print("Cannot open {0} file".format(file_path))
        sys.exit(0)

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    text = file.read()
    ast = parser.parse(text, lexer=cparser.scanner, debug=False)

    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    ast.accept(Interpreter())

    sys.stdout = old_stdout

    name = os.path.join(test_dir, os.path.splitext(filename)[0])
    file_expected = "{0}.expected".format(name)
    actual_content = mystdout.getvalue()
    expected_content = open(file_expected).read().replace("\r", "")
    res = cmp(actual_content, expected_content)
    assert res == 0, "test output and file {0} differ\n---ACTUAL---\n{1}\n---EXPECTED---\n{2}\n---"\
        .format(file_expected, actual_content, expected_content)
    print("Passed test for file '%s'." % filename)


if __name__ == '__main__':

    test_dir = "tests"
    # test_dir = "run_test"

    test_in = []
    for dirpath, dirnames, filenames in os.walk(test_dir):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            elif filename.endswith('.in'):
                test_in.append(filename)

    for filename in test_in:
        try:
            test_file(test_dir, filename)
        except AssertionError as e:
            print(e.message)
