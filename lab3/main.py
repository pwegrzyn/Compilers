# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

import sys
import scanner
import Mparser
from TreePrinter import TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    scanner.text = text
    ast = parser.parse(text, lexer=scanner.lexer)
    if not Mparser.error_encountered:
        ast.printTree()