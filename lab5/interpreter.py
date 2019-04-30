# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

import AST
import SymbolTable
from memory import *
from exceptions import *
from visit import *
import sys
import numpy

sys.setrecursionlimit(10000)

matrix_matrix_op = {
    '*': (lambda x, y: numpy.array(numpy.matmul(x, y)).tolist()),
    '*=': (lambda x, y: numpy.array(numpy.matmul(x, y)).tolist()),
    '/': (lambda x, y: numpy.array(numpy.matmul(numpy.matrix(x), numpy.linalg.inv(y))).tolist()),
    '/=': (lambda x, y: numpy.array(numpy.matmul(numpy.matrix(x), numpy.linalg.inv(y))).tolist()),
    '+': (lambda x, y: (numpy.matrix(x) + numpy.matrix(y)).tolist()),
    '+=': (lambda x, y: (numpy.matrix(x) + numpy.matrix(y)).tolist()),
    '.+': (lambda x, y: (numpy.matrix(x) + numpy.matrix(y)).tolist()),
    '-': (lambda x, y: (numpy.matrix(x) - numpy.matrix(y)).tolist()),
    '-=': (lambda x, y: (numpy.matrix(x) - numpy.matrix(y)).tolist()),
    '.-': (lambda x, y: (numpy.matrix(x) - numpy.matrix(y)).tolist()),
    '.*': (lambda x, y: numpy.multiply(numpy.array(x), numpy.array(y)).tolist()),
    './': (lambda x, y: numpy.divide(numpy.array(x), numpy.array(y)).tolist()),
}

simple_op = {
    "+": (lambda x, y: x + y),
    "+=": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "-=": (lambda x, y: x - y),
    "*": (lambda x, y: x * y),
    "*=": (lambda x, y: x * y),
    "/": (lambda x, y: x / y),
    "/=": (lambda x, y: x / y),
    "==": (lambda x, y: x == y),
    "!=": (lambda x, y: x != y),
    ">": (lambda x, y: x > y),
    "<": (lambda x, y: x < y),
    "<=": (lambda x, y: x <= y),
    ">=": (lambda x, y: x >= y)
}

matrix_op = {
    "*": (lambda x, y: [[elem * x for elem in row] for row in y]),
    '/': (lambda x, y: [[elem / x for elem in row] for row in y])
}


class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    @when(AST.Vector)
    def visit(self, node):
        if all([type(elem) != AST.Vector for elem in node.elems]):
            return [elem.accept(self) for elem in node.elems]
        else:
            return [[val.accept(self) for val in row.elems] for row in node.elems]

    @when(AST.RelBinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if type(left) is not list and type(right) is not list:
            return simple_op[node.op](left, right)
        if type(left) is not list and type(right) is list:
            return matrix_op[node.op](left, right)
        if type(left) is list and type(right) is not list:
            return matrix_op[node.op](right, left)
        if type(left) is list and type(right) is list:
            return matrix_matrix_op[node.op](left, right)

    @when(AST.ArithBinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if type(left) is not list and type(right) is not list:
            return simple_op[node.op](left, right)
        if type(left) is not list and type(right) is list:
            return matrix_op[node.op](left, right)
        if type(left) is list and type(right) is not list:
            return matrix_op[node.op](right, left)
        if type(left) is list and type(right) is list:
            return matrix_matrix_op[node.op](left, right)

    @when(AST.IfStmt)
    def visit(self, node):
        if node.cond.accept(self):
            return node.stmts.accept(self)

    @when(AST.ArgList)
    def visit(self, node):
        return [arg.accept(self) for arg in node.args]

    @when(AST.AssignmentStmt)
    def visit(self, node):
        expr = node.right.accept(self)
        if node.op in ['+=', '-=', '*=', '/=']:
            if isinstance(node.left, AST.Id):
                left = self.memory_stack.get(node.left.identifier)
                result = None
                if type(left) is not list and type(expr) is not list:
                    result = simple_op[node.op](left, expr)
                elif type(left) is list and type(expr) is list:
                    result = matrix_matrix_op[node.op](left, expr)
                self.memory_stack.set(node.left.identifier, result)
            elif isinstance(node.left, AST.ReferenceStmt):
                matrix_name = node.left.id.identifier
                matrix = self.memory_stack.get(matrix_name)
                selector_list = node.left.selector.accept(self)
                left = None
                if len(selector_list) == 1:
                    left = matrix[selector_list[0]]
                elif len(selector_list) == 2:
                    left = matrix[selector_list[0]-1][selector_list[1]-1]
                result = None
                if type(left) is not list and type(expr) is not list:
                    result = simple_op[node.op](left, expr)
                if len(selector_list) == 1:
                    matrix[selector_list[0]] = result
                elif len(selector_list) == 2:
                    matrix[selector_list[0]-1][selector_list[1]-1] = result
        else:
            if isinstance(node.left, AST.Id):
                if self.memory_stack.get(node.left.identifier) is None:
                    self.memory_stack.insert(node.left.identifier, expr)
                else:
                    self.memory_stack.set(node.left.identifier, expr)
            elif isinstance(node.left, AST.ReferenceStmt):
                matrix_name = node.left.id.identifier
                matrix = self.memory_stack.get(matrix_name)
                selector_list = node.left.selector.accept(self)
                if len(selector_list) == 1:
                    matrix[selector_list[0]] = expr
                elif len(selector_list) == 2:
                    matrix[selector_list[0]-1][selector_list[1]-1] = expr

    @when(AST.IfElseStmt)
    def visit(self, node):
        if node.cond.accept(self):
            return node.stmts.accept(self)
        else:
            return node.elseStmts.accept(self)

    @when(AST.WhileStmt)
    def visit(self, node):
        while node.cond.accept(self):
            try:
                node.stmts.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.ForStmt)
    def visit(self, node):
        rangeExpression = node.range.accept(self)
        if self.memory_stack.get(node.iterator.identifier) is None:
            self.memory_stack.insert(node.iterator.identifier, rangeExpression[0])
        else:
            self.memory_stack.set(node.iterator.identifier, rangeExpression[0])
        while self.memory_stack.get(node.iterator.identifier) <= rangeExpression[1]:
            try:
                node.stmts.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
            counter = self.memory_stack.get(node.iterator.identifier)
            counter += 1
            self.memory_stack.set(node.iterator.identifier, counter)

    @when(AST.StmtList)
    def visit(self, node):
        new_memory = Memory("innerMemory")
        self.memory_stack.push(new_memory)
        try:
            for stmt in node.stmts:
                stmt.accept(self)
        finally:
            self.memory_stack.pop()

    @when(AST.BreakStmt)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueStmt)
    def visit(self, node):
        raise ContinueException()

    @when(AST.ReturnStmt)
    def visit(self, node):
        value = node.expr.accept(self)
        raise ReturnValueException(value)

    @when(AST.PrintStmt)
    def visit(self, node):
        expressions = node.args.accept(self)
        to_print = [str(expression) for expression in expressions if expression]
        print(', '.join(to_print))

    @when(AST.ReferenceStmt)
    def visit(self, node):
        matrix_name = node.id.identifier
        matrix = self.memory_stack.get(matrix_name)
        selector_list = node.selector.accept(self)
        if len(selector_list) == 1:
            return matrix[selector_list[0]]
        elif len(selector_list) == 2:
            return matrix[selector_list[0]][selector_list[1]]

    @when(AST.RangeExpr)
    def visit(self, node):
        left_expr = node.left.accept(self)
        right_expr = node.right.accept(self)
        return (left_expr, right_expr)

    @when(AST.UnaryExpr)
    def visit(self, node):
        value = node.val.accept(self)
        if node.op == '-':
            if type(value) is list:
                negate = list()
                for row in value:
                    inner = []
                    for elem in row:
                        inner.append(-elem)
                    negate.append(inner)
                return negate
            return - value
        elif node.op == '\'':
            return [list(x) for x in zip(*value)]

    @when(AST.FunctionCall)
    def visit(self, node):
        expression = node.args.accept(self)[0]
        if node.name.identifier == "zeros":
            return [[0 for column in range(expression)] for row in range(expression)]
        elif node.name.identifier == "ones":
            return [[1 for column in range(expression)] for row in range(expression)]
        elif node.name.identifier == "eye":
            eye = [[0 for column in range(expression)] for row in range(expression)]
            for i in range(0, expression - 1):
                eye[i][i] = 1
            return eye

    @when(AST.Id)
    def visit(self, node):
        return self.memory_stack.get(node.identifier)

    @when(AST.Error)
    def visit(self, node):
        pass
