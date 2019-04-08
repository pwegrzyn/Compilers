# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

class Node(object):
    
    def accept(self, visitor):
        return visitor.visit(self)


class IntNum(Node):

    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col


class FloatNum(Node):

    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col


class String(Node):

    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col


class Vector(Node):

    def __init__(self, elems, line=-1, col=-1):
        self.elems = elems
        self.line = line
        self.col = col

    def addElem(self, elem):
        self.elems.append(elem)


class RelBinExpr(Node):

    def __init__(self, op, left, right, line, col):
        self.op = op
        self.left = left
        self.right = right
        self.line = line
        self.col = col


class ArithBinExpr(Node):

    def __init__(self, op, left, right, line, col):
        self.op = op
        self.left = left
        self.right = right
        self.line = line
        self.col = col


class IfStmt(Node):
    
    def __init__(self, cond, stmt, line, col):
        self.cond = cond
        self.stmts = stmt
        self.line = line
        self.col = col


class AssignmentStmt(Node):

    def __init__(self, op, left, right, line, col):
        self.left = left
        self.right = right
        self.op = op
        self.line = line
        self.col = col


class IfElseStmt(Node):

    def __init__(self, cond, stmt, elseStmt, line, col):
        self.cond = cond
        self.stmts = stmt
        self.elseStmts = elseStmt
        self.line = line
        self.col = col


class WhileStmt(Node):

    def __init__(self, cond, stmt, line, col):
        self.cond = cond
        self.stmts = stmt
        self.line = line
        self.col = col


class ForStmt(Node):

    def __init__(self, iterator, range, stmt, line, col):
        self.iterator = iterator
        self.range = range
        self.stmts = stmt
        self.line = line
        self.col = col


class StmtList(Node):

    def __init__(self, stmts):
        self.stmts = stmts

    def addStmt(self, stmt):
        self.stmts.append(stmt)


class BreakStmt(Node):

    def __init__(self, line, col):
        self.line = line
        self.col = col


class ContinueStmt(Node):

    def __init__(self, line, col):
        self.line = line
        self.col = col


class ReturnStmt(Node):

    def __init__(self, line, col, expr=None):
        self.expr = expr
        self.line = line
        self.col = col


class PrintStmt(Node):

    def __init__(self, args, line, col):
        self.args = args
        self.line = line
        self.col = col


class ReferenceStmt(Node):

    def __init__(self, id, selector, line, col):
        self.id = id
        self.selector = selector
        self.line = line
        self.col = col
        

class RangeExpr(Node):

    def __init__(self, left, right, line, col):
        self.left = left
        self.right = right
        self.line = line
        self.col = col


class UnaryExpr(Node):

    def __init__(self, op, val, line, col):
        self.op = op
        self.val = val
        self.line = line
        self.col = col


class FunctionCall(Node):

    def __init__(self, name, args, line, col):
        self.name = name
        self.args = args
        self.line = line
        self.col = col


class ArgList(Node):

    def __init__(self, args):
        self.args = args

    def addArg(self, arg):
        self.args.append(arg)


class Id(Node):

    def __init__(self, identifier, line, col):
        self.identifier = identifier
        self.line = line
        self.col = col


class Error(Node):

    def __init__(self):
        pass
      
