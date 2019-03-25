# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

class Node(object):
    pass


class IntNum(Node):

    def __init__(self, value):
        self.value = value


class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class String(Node):

    def __init__(self, value):
        self.value = value


class Vector(Node):

    def __init__(self, elems):
        self.elems = elems

    def addElem(self, elem):
        self.elems.append(elem)


class RelBinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class ArithBinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class IfStmt(Node):
    
    def __init__(self, cond, stmt):
        self.cond = cond
        self.stmts = stmt


class AssignmentStmt(Node):

    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.op = op


class IfElseStmt(Node):

    def __init__(self, cond, stmt, elseStmt):
        self.cond = cond
        self.stmts = stmt
        self.elseStmts = elseStmt


class WhileStmt(Node):

    def __init__(self, cond, stmt):
        self.cond = cond
        self.stmts = stmt


class ForStmt(Node):

    def __init__(self, iterator, range, stmt):
        self.iterator = iterator
        self.range = range
        self.stmts = stmt


class StmtList(Node):

    def __init__(self, stmts):
        self.stmts = stmts

    def addStmt(self, stmt):
        self.stmts.append(stmt)


class BreakStmt(Node):

    def __init__(self):
        pass


class ContinueStmt(Node):

    def __init__(self):
        pass


class ReturnStmt(Node):

    def __init__(self, expr=None):
        self.expr = expr


class PrintStmt(Node):

    def __init__(self, args):
        self.args = args


class ReferenceStmt(Node):

    def __init__(self, id, row, column=None):
        self.id = id
        self.row = row
        self.column = column
        

class RangeExpr(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class UnaryExpr(Node):

    def __init__(self, op, val):
        self.op = op
        self.val = val


class FunctionCall(Node):

    def __init__(self, name, args):
        self.name = name
        self.args = args


class ArgList(Node):

    def __init__(self, args):
        self.args = args

    def addArg(self, arg):
        self.args.append(arg)


class Id(Node):

    def __init__(self, identifier):
        self.identifier = identifier


class Error(Node):

    def __init__(self):
        pass
      