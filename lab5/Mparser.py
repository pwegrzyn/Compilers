#!/usr/bin/python

# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens
error_encountered = False

start = 'stmtList'

precedence = (
    # Dangling-else solution
    ("left", 'IF'),
    ("left", 'ELSE'),
    ("nonassoc", '<', '>', 'LTE', 'GTE', 'EQ', 'NEQ'),
    ("left", '+', '-', 'DOTADD', 'DOTSUB'),
    ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
    ("right", 'UMINUS'),
    ("left", 'TRANSPOSE')
)

def p_error(p):
    global error_encountered
    error_encountered = True
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")

# empty string (use this or nothing)
def p_empty(p):
    'empty :'
    pass

# grammar specification
def p_stmtList(p):
    """stmtList : stmtList stmt
                | empty """
    if len(p) == 2:
        p[0] = AST.StmtList([p[1]])
    else:
        p[0] = p[1]
        p[0].addStmt(p[2])

def p_stmt(p):
    """stmt : expressionStmt
            | compundStmt
            | selectionStmt
            | iterationStmt
            | returnStmt
            | breakStmt
            | continueStmt
            | printStmt"""
    p[0] = p[1]

def p_compundStmt(p):
    """compundStmt : '{' stmtList '}'"""
    p[0] = p[2]

def p_expressionStmt(p):
    """expressionStmt : expression ';'
                      | ';'"""
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = None

def p_selectionStmt(p):
    """selectionStmt : IF '(' simpleExpression ')' stmt %prec IF
                     | IF '(' simpleExpression ')' stmt ELSE stmt"""
    if len(p) == 6:
        p[0] = AST.IfStmt(p[3], p[5], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))
    else:
        p[0] = AST.IfElseStmt(p[3], p[5], p[7], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_selectionStmt_error(p):
    """selectionStmt : IF '(' error ')' stmt %prec IF
                     | IF '(' error ')' stmt ELSE stmt"""
    print('Malformed IF-statement!')

def p_iterationStmt(p):
    """iterationStmt : whileIterationStmt
                     | forIterationStmt"""
    p[0] = p[1]

def p_whileIterationStmt(p):
    """whileIterationStmt : WHILE '(' simpleExpression ')' stmt"""
    p[0] = AST.WhileStmt(p[3], p[5], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_whileIterationStmt_error(p):
    """whileIterationStmt : WHILE '(' error ')' stmt"""
    print('Malformed condition expression in WHILE statement!')

def p_forIterationStmt(p):
    """forIterationStmt : FOR ID '=' rangeExpression stmt"""
    p[0] = AST.ForStmt(AST.Id(p[2], p.lineno(2), scanner.find_tok_column_by_lexpos(p.lexpos(2))), 
        p[4], p[5], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_rangeExpressionAllowable(p):
    """rangeExpressionAllowable : scalarConst
                                | ID"""
    if type(p[1]) != str:
        p[0] = p[1]
    else:
        p[0] = AST.Id(p[1], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_rangeExpression(p):
    """rangeExpression : rangeExpressionAllowable ':' rangeExpressionAllowable"""
    p[0] = AST.RangeExpr(p[1], p[3], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_returnStmt(p):
    """returnStmt : RETURN expression ';'
                  | RETURN ';'"""
    if len(p) == 4:
        p[0] = AST.ReturnStmt(p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)), p[2])
    else:
        p[0] = AST.ReturnStmt(p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_returnStmt_error(p):
    """returnStmt : RETURN error ';'"""
    print('Malformed expression in return statement!')

def p_breakStmt(p):
    """breakStmt : BREAK ';'"""
    p[0] = AST.BreakStmt(p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_breakStmt_error(p):
    """breakStmt : BREAK error ';'"""
    print('Encountered malformed expression after break statement!')

def p_continueStmt(p):
    """continueStmt : CONTINUE ';'"""
    p[0] = AST.ContinueStmt(p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_continueStmt_error(p):
    """continueStmt : CONTINUE error ';'"""
    print('Encountered malformed expression after continue statement!')

def p_printStmt(p):
    """printStmt : PRINT argList ';'"""
    p[0] = AST.PrintStmt(p[2], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_printStmt_error(p):
    """printStmt : PRINT error ';'"""
    print('Malfored agruments of the print operator!')

def p_expression(p):
    """expression : mutable '=' expression
                  | mutable ADDASSIGN expression
                  | mutable SUBASSIGN expression
                  | mutable MULASSIGN expression
                  | mutable DIVASSIGN expression
                  | simpleExpression"""
    if len(p) == 4:
        p[0] = AST.AssignmentStmt(p[2], p[1], p[3], p.lineno(2), scanner.find_tok_column_by_lexpos(p.lexpos(2)))
    else:
        p[0] = p[1]

def p_simpleExpression(p):
    """simpleExpression : arithExpression LTE arithExpression
                        | arithExpression '<' arithExpression
                        | arithExpression '>' arithExpression
                        | arithExpression GTE arithExpression
                        | arithExpression EQ arithExpression
                        | arithExpression NEQ arithExpression
                        | arithExpression"""
    if len(p) == 4:
        p[0] = AST.RelBinExpr(p[2], p[1], p[3], p.lineno(2), scanner.find_tok_column_by_lexpos(p.lexpos(2)))
    else:
        p[0] = p[1]

def p_arithExpression(p):
    """arithExpression : arithExpression '+' arithExpression
                       | arithExpression '-' arithExpression
                       | arithExpression '*' arithExpression
                       | arithExpression '/' arithExpression
                       | arithExpression DOTADD arithExpression
                       | arithExpression DOTSUB arithExpression
                       | arithExpression DOTMUL arithExpression
                       | arithExpression DOTDIV arithExpression
                       | uminusExpression
                       | arithExpression TRANSPOSE
                       | value"""
    if len(p) == 4:
        p[0] = AST.ArithBinExpr(p[2], p[1], p[3], p.lineno(2), scanner.find_tok_column_by_lexpos(p.lexpos(2)))
    elif len(p) == 3:
        p[0] = AST.UnaryExpr(p[2], p[1], p.lineno(2), scanner.find_tok_column_by_lexpos(p.lexpos(2)))
    else:
        p[0] = p[1]

def p_uminusExpression(p):
    """uminusExpression : '-' arithExpression %prec UMINUS"""
    p[0] = AST.UnaryExpr(p[1], p[2], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_value(p):
    """value : immutable
             | mutable"""
    p[0] = p[1]

def p_mutable(p):
    """mutable : ID
               | reference"""
    if type(p[1]) == str:
        p[0] = AST.Id(p[1], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))
    else:
        p[0] = p[1]

def p_reference(p):
    """reference : ID '[' argList ']'"""
    p[0] = AST.ReferenceStmt(AST.Id(p[1], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1))), 
        p[3], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_immutable(p):
    """immutable : '(' expression ')'
                 | constant
                 | call"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_call(p):
    """call : functionId '(' argList ')'"""
    p[0] = AST.FunctionCall(p[1], p[3], p.lineno(2), scanner.find_tok_column_by_lexpos(p.lexpos(2)))

def p_call_error(p):
    """call : functionId '(' error ')'"""
    print('Malformed function call!')

def p_argList(p):
    """argList : argList ',' simpleExpression
               | simpleExpression"""
    if len(p) == 2:
        p[0] = AST.ArgList([p[1]])
    else:
        p[0] = p[1]
        p[0].addArg(p[3])

def p_constant(p):
    """constant : scalarConst
                | STRINGCONST
                | matrixConst
                | vectorConst"""
    if type(p[1]) == str:
        p[0] = AST.String(p[1], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))
    else:
        p[0] = p[1]

def p_functionId(p):
    """functionId : EYE
                  | ZEROS
                  | ONES"""
    p[0] = AST.Id(p[1], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_scalarConst(p):
    """scalarConst : INTCONST
                   | FLOATCONST"""
    if type(p[1]) == int:
        p[0] = AST.IntNum(p[1], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))
    elif type(p[1]) == float:
        p[0] = AST.FloatNum(p[1], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))

def p_matrixConst(p):
    """matrixConst : '[' matrixItems ']'"""
    p[0] = p[2]
    p[0].line = p.lineno(1)
    p[0].col = scanner.find_tok_column_by_lexpos(p.lexpos(1))

def p_matrixConst_error(p):
    """matrixConst : '[' error ']'"""
    print('Wrong matrix/vector const!')

def p_matrixItems(p):
    """matrixItems : matrixItems ',' vectorConst
                   | vectorConst"""
    if len(p) == 2:
        p[0] = AST.Vector([p[1]])
    else:
        p[0] = p[1]
        p[0].addElem(p[3])

def p_vectorConst(p):
    """vectorConst : '[' vectorItems ']'"""
    p[0] = p[2]

def p_vectorItems(p):    
    """vectorItems : vectorItems ',' vectorItem 
                   | vectorItem"""
    if len(p) == 2:
        p[0] = AST.Vector([p[1]], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))
    else:
        p[0] = p[1]
        p[0].addElem(p[3])

def p_vectorItem(p):
    """vectorItem : scalarConst
                  | STRINGCONST"""
    if type(p[1]) == str:
        p[0] = AST.String(p[1], p.lineno(1), scanner.find_tok_column_by_lexpos(p.lexpos(1)))
    else:
        p[0] = p[1]

parser = yacc.yacc(debug=True)
