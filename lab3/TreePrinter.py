# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

from __future__ import print_function
import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print(self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print(self.value)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print(self.value)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        raise Exception('Cannot print tree when an error has occured!')

    @addToClass(AST.Id)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print(self.identifier)

    @addToClass(AST.ArgList)
    def printTree(self, indent=0):
        for arg in self.args:
            if arg:
                arg.printTree(indent)

    @addToClass(AST.FunctionCall)
    def printTree(self, indent=0):
        self.name.printTree(indent)
        self.args.printTree(indent+1)

    @addToClass(AST.AssignmentStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print(self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.StmtList)
    def printTree(self, indent=0):
        for stmt in self.stmts:
            if stmt:
                stmt.printTree(indent)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('VECTOR')
        for elem in self.elems:
            if elem:
                if type(elem) == list:
                    for val in elem:
                        print(val)
                else:
                    elem.printTree(indent+1)

    @addToClass(AST.ReferenceStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('REF')
        self.id.printTree(indent+1)
        self.row.printTree(indent+1)
        if self.column:
            self.column.printTree(indent+1)

    @addToClass(AST.PrintStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('PRINT')
        self.args.printTree(indent+1)

    @addToClass(AST.ArithBinExpr)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print(self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print(self.op)
        self.val.printTree(indent+1)

    @addToClass(AST.ForStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('FOR')
        self.iterator.printTree(indent+1)
        self.range.printTree(indent+1)
        self.stmts.printTree(indent+1)

    @addToClass(AST.RangeExpr)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('RANGE')
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.WhileStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('WHILE')
        self.cond.printTree(indent+1)
        self.stmts.printTree(indent+1)

    @addToClass(AST.RelBinExpr)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print(self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.IfElseStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('IF')
        self.cond.printTree(indent+1)
        for _ in range(indent):
            print("| ", end='')
        print('THEN')
        self.stmts.printTree(indent+1)
        for _ in range(indent):
            print("| ", end='')
        print('ELSE')
        self.elseStmts.printTree(indent+1)

    @addToClass(AST.IfStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('IF')
        self.cond.printTree(indent+1)
        for _ in range(indent):
            print("| ", end='')
        print('THEN')
        self.stmts.printTree(indent+1)

    @addToClass(AST.BreakStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('BREAK')

    @addToClass(AST.ContinueStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('CONTINUE')

    @addToClass(AST.ReturnStmt)
    def printTree(self, indent=0):
        for _ in range(indent):
            print("| ", end='')
        print('RETURN')
        if self.expr:
            self.expr.printTree(indent+1)