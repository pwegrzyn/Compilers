# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

import AST
from SymbolTable import SymbolTable, VariableSymbol, MatrixType, VectorType, ErrorType 
from collections import defaultdict


operatoreration_results = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for operatorerator in ['.+', '.-', '.*', './']:
    operatoreration_results[operatorerator]['matrix']['matrix'] = 'matrix'

for operator in ['*=', '*', '/=', '/']:
    operatoreration_results[operator]['matrix']['int'] = 'matrix'
    operatoreration_results[operator]['matrix']['float'] = 'matrix'

for operator in ['<', '>', '<=', '>=', '==', '!=']:
    operatoreration_results[operator]['int']['float'] = 'int'
    operatoreration_results[operator]['float']['int'] = 'int'
    operatoreration_results[operator]['float']['float'] = 'int'
    operatoreration_results[operator]['int']['int'] = 'int'

for operator in ['+', '-', '*', '/', '+=', '-=', '*=', '/=']:
    operatoreration_results[operator]['int']['float'] = 'float'
    operatoreration_results[operator]['float']['int'] = 'float'
    operatoreration_results[operator]['float']['float'] = 'float'
    operatoreration_results[operator]['matrix']['matrix'] = 'matrix'
    operatoreration_results[operator]['int']['int'] = 'int'

operatoreration_results['\'']['matrix'][None] = 'matrix'
operatoreration_results['-']['matrix'][None] = 'matrix'
operatoreration_results['-']['int'][None] = 'int'
operatoreration_results['-']['float'][None] = 'float'

operatoreration_results['+']['string']['string'] = 'string'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        print('TypeChecker.NodeVisitor: Generic Visit called!')
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        elif not node:
            print('TypeChecker.NodeVisitor: Tried to visit None!')


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, 'global')
        self.loop_nesting = 0
        self.errors_encountered = False

    def visit_StmtList(self, node):
        node.stmts = [stmt for stmt in node.stmts if stmt]
        for stmt in node.stmts:  
            self.visit(stmt)
  
    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'
    
    def visit_Vector(self, node):
        node.elems = [elem for elem in node.elems if elem]
        if all([type(elem) != AST.Vector for elem in node.elems]):
            return VectorType(len(node.elems), type(node.elems[0]))
        else:
            if all([len(row.elems) == len(node.elems[0].elems) for row in node.elems]):
                return MatrixType(len(node.elems), len(node.elems[0].elems), type(node.elems[0].elems[0]))
            else:
                print("Semantic error at line {0}, column {1}: matrix constant with non-equal row sizes"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()

    def visit_RelBinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        type_op = node.op
        if operatoreration_results[str(type_op)][str(type_left)][str(type_right)] is None:
            print("Semantic error at line {0}, column {1}: relational operation has invalid operand types"
                  .format(node.line, node.col))
            self.errors_encountered = True
            return ErrorType()
        return operatoreration_results[str(type_op)][str(type_left)][str(type_right)]
        
    def visit_ArithBinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        type_op = node.op
        if operatoreration_results[str(type_op)][str(type_left)][str(type_right)] is None:
            print("Semantic error at line {0}, column {1}: arithmetic operation has invalid operand types"
                  .format(node.line, node.col))
            self.errors_encountered = True
            return ErrorType()
        return operatoreration_results[str(type_op)][str(type_left)][str(type_right)]

    def visit_IfStmt(self, node):
        self.visit(node.cond)
        self.symbol_table = self.symbol_table.pushScope('if')
        self.visit(node.stmts)
        self.symbol_table = self.symbol_table.popScope()

    def visit_IfElseStmt(self, node):
        self.visit(node.cond)
        self.symbol_table = self.symbol_table.pushScope('if')
        self.visit(node.stmts)
        self.symbol_table = self.symbol_table.popScope()
        self.symbol_table = self.symbol_table.pushScope('else')
        self.visit(node.elseStmts)
        self.symbol_table = self.symbol_table.popScope()

    def visit_AssignmentStmt(self, node):
        expr_type = self.visit(node.right)
        if node.op in ['+=', '-=', '*=', '/=']:
            variable_type = self.visit(node.left)
            if operatoreration_results[str(node.op)][str(variable_type)][str(expr_type)] is None and variable_type is not None:
                print("Semantic error at line {0}, column {1}: this arithmetic assignment is not allowed"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
            else:
                return expr_type
        else:
            if isinstance(node.left, AST.Id):
                self.symbol_table.put(node.left.identifier, VariableSymbol(node.left.identifier, expr_type))
                return expr_type
            elif isinstance(node.left, AST.ReferenceStmt):
                tensor_content_type = self.visit(node.left)
                if tensor_content_type != expr_type and not isinstance(tensor_content_type, ErrorType):
                    print("Semantic error at line {0}, column {1}: trying to assign a value to a matrix cell with an invalid type"
                        .format(node.line, node.col))
                    self.errors_encountered = True
                    return ErrorType()
                if isinstance(tensor_content_type, ErrorType):
                    return ErrorType()
                return expr_type

    def visit_WhileStmt(self, node):
        self.loop_nesting += 1
        self.symbol_table = self.symbol_table.pushScope('while')
        self.visit(node.cond)
        self.visit(node.stmts)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_nesting -= 1

    def visit_ForStmt(self, node):
        self.loop_nesting += 1
        self.symbol_table = self.symbol_table.pushScope('for')
        type = self.visit(node.range)
        variable = VariableSymbol(node.iterator.identifier, type)
        self.symbol_table.put(node.iterator.identifier, variable)
        self.visit(node.stmts)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_nesting -= 1

    def visit_BreakStmt(self, node):
        if self.loop_nesting <= 0:
            print("Semantic error at line {0}, column {1}: break outside of any loop statement"
                  .format(node.line, node.col))
            self.errors_encountered = True
        return None

    def visit_ContinueStmt(self, node):
        if self.loop_nesting <= 0:
            print("Semantic error at line {0}, column {1}: continue outside of any loop statement"
                  .format(node.line, node.col))
            self.errors_encountered = True
        return None

    def visit_ReturnStmt(self, node):
        if node.expr:
            type = self.visit(node.expr)
        return type

    def visit_PrintStmt(self, node):
        self.visit(node.args)

    def visit_ReferenceStmt(self, node):
        from builtins import type
        variable_type = self.visit(node.id)
        if variable_type is None:
            return ErrorType()
        if not isinstance(variable_type.type, VectorType) and not isinstance(variable_type.type, MatrixType):
            print("Semantic error at line {0}, column {1}: trying to dereference a non-matrix/non-vector object"
                  .format(node.line, node.col))
            self.errors_encountered = True
            return ErrorType()
        self.visit(node.selector)
        selector_list = node.selector.args
        if len(selector_list) != 1 and len(selector_list) != 2:
            print("Semantic error at line {0}, column {1}: selector list has an invalid length"
                  .format(node.line, node.col))
            self.errors_encountered = True
            return ErrorType()
        if (len(selector_list) == 1 and not isinstance(variable_type.type, VectorType)) or (len(selector_list) == 2 and not isinstance(variable_type.type, MatrixType)):
            print("Semantic error at line {0}, column {1}: selector list references an incompatible rank tensor"
                  .format(node.line, node.col))
            self.errors_encountered = True
            return ErrorType()
        if(len(selector_list) == 1):
            selector_index = selector_list[0].value
            if type(selector_index) != int:
                print("Semantic error at line {0}, column {1}: selector index needs to be an integer"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
            vector_dim = variable_type.type.dim
            if not (selector_index >= 0 and selector_index < vector_dim):
                print("Semantic error at line {0}, column {1}: Vector index out of bound"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
            else:  # SUCCESS
                type = variable_type.type.content_type
                if(type == int):
                    return 'int'
                elif(type == float):
                    return 'float'
        elif(len(selector_list) == 2):
            selector_index_1 = selector_list[0].value
            selector_index_2 = selector_list[1].value
            if type(selector_index_1) != int or type(selector_index_2) != int:
                print("Semantic error at line {0}, column {1}: selector index needs to be an integer"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
            matrix_dim_1 = variable_type.type.dim_1
            matrix_dim_2 = variable_type.type.dim_2
            if not (selector_index_1 >= 0 and selector_index_1 < matrix_dim_1):
                print("Semantic error at line {0}, column {1}: Row index out of bound"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
            elif not (selector_index_2 >= 0 and selector_index_2 < matrix_dim_2):
                print("Semantic error at line {0}, column {1}: Column index out of bound"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
            else:   #SUCCESS
                type = variable_type.type.content_type
                if(type == int):
                    return 'int'
                elif(type == float):
                    return 'float'
        
    def visit_RangeExpr(self, node):
        type = self.visit(node.left)
        if str(type) != 'int':
            print("Semantic error at line {0}, column {1}: not allowed range expression type: {2}"
                  .format(node.left.line, node.left.col, str(type)))
            self.errors_encountered = True
        type = self.visit(node.right)
        if str(type) != 'int':
            print("Semantic error at line {0}, column {1}: not allowed range expression type: {2}"
                  .format(node.right.line, node.right.col, str(type)))
            self.errors_encountered = True
        return type

    def visit_UnaryExpr(self, node):
        type_val = self.visit(node.val)
        type_op = node.op
        if operatoreration_results[str(type_op)][str(type_val)][None] is None:
            print("Semantic error at line {0}, column {1}: unary operation has an invalid operand type"
                  .format(node.line, node.col))
            self.errors_encountered = True
            return ErrorType()
        return operatoreration_results[str(type_op)][str(type_val)][None]

    def visit_FunctionCall(self, node):
        from builtins import type
        args_type = self.visit(node.args)
        if not args_type:
            return ErrorType()
        if len(node.args.args) != 1:
            print("Semantic error at line {0}, column {1}: this function can only be called with one parameter"
                  .format(node.line, node.col))
            self.errors_encountered = True
            return ErrorType()
        parameter_type = node.args.args[0]
        # We dont hold the value of the variable so this is a workaround for variable parameters
        value = 5
        if isinstance(parameter_type, AST.Id):
            parameter_type_lookup = self.symbol_table.get(parameter_type.identifier)
            if str(parameter_type_lookup) != 'int':
                print("Semantic error at line {0}, column {1}: this function can only be called with a single integer parameter"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
        elif isinstance(parameter_type, AST.IntNum) or isinstance(parameter_type, AST.FloatNum) or isinstance(parameter_type, AST.String):
            value = node.args.args[0].value
            if type(value) != int:
                print("Semantic error at line {0}, column {1}: this function can only be called with a single integer parameter"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
            if value < 1:
                print("Semantic error at line {0}, column {1}: this function takes a positive parameter"
                      .format(node.line, node.col))
                self.errors_encountered = True
                return ErrorType()
        else:
            print("Semantic error at line {0}, column {1}: this function only accepts integer values"
                  .format(node.line, node.col))
            self.errors_encountered = True
            return ErrorType()
        #SUCCESS
        return MatrixType(value, value, int)

    def visit_ArgList(self, node):
        node.args = [arg for arg in node.args if arg]
        result = object()
        for arg in node.args:
            res = self.visit(arg)
            if not res:
                result = None
        return result

    def visit_Id(self, node):
        symbol_variable = self.symbol_table.get(node.identifier)
        if symbol_variable is None:
            print("Semantic error at line {0}, column {1}: unkown variable: {2}"
                  .format(node.line, node.col, node.identifier))
            self.errors_encountered = True
            return None
        else:
            return symbol_variable

    def visit_Error(self, node):
        pass

    
def transformTypeToStr(my_type):
    if type(my_type) == str:
        return my_type
    if my_type == int:
        return 'int'
    if my_type == float:
        return 'float'
    if my_type == str:
        return 'string'
    if isinstance(my_type, VariableSymbol):
        if type(my_type.type) == str:
            return my_type.type
        if my_type.type == int:
            return 'int'
        if my_type.type == float:
            return 'float'
        if my_type.type == str:
            return 'string'
        if isinstance(my_type.type, MatrixType):
            return 'matrix'
    if isinstance(my_type, MatrixType):
        return 'matrix'
