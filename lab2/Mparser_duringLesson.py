#!/usr/bin/python

# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

import scanner
import ply.yacc as yacc

tokens = scanner.tokens
error_encountered = False

start = 'stmtList'

precedence = (
    ("left", 'IF'),
    ("left", 'ELSE'),
    ("left", '<', '>', 'LTE', 'GTE', 'EQ', 'NEQ'),
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

# helper method for generating concrete syntax tree
def add_node(p, desc):
    p[0] = (desc, )
    for node in p[1:]:
        p[0] += (node,)

# grammar specification
def p_stmtList(p):
    """stmtList : stmtList stmt
                | empty """
    add_node(p, 'stmtList')

def p_stmt(p):
    """stmt : expressionStmt
            | compundStmt
            | selectionStmt
            | iterationStmt
            | returnStmt
            | breakStmt
            | continueStmt
            | printStmt"""
    add_node(p, 'stmt')

def p_compundStmt(p):
    """compundStmt : '{' stmtList '}'"""
    add_node(p, 'compundStmt')

def p_expressionStmt(p):
    """expressionStmt : expression ';'
                      | ';'"""
    add_node(p, 'expressionStmt')

def p_selectionStmt(p):
    """selectionStmt : IF '(' simpleExpression ')' stmt %prec IF
                     | IF '(' simpleExpression ')' stmt ELSE stmt"""
    add_node(p, 'selectionStmt')

def p_selectionStmt_error(p):
    """selectionStmt : IF '(' simpleExpression ')' error %prec IF
                     | IF '(' simpleExpression ')' error ELSE stmt
                     | IF '(' error ')' stmt %prec IF
                     | IF '(' error ')' stmt ELSE stmt"""
    print('Malformed IF-statement!')

def p_iterationStmt(p):
    """iterationStmt : whileIterationStmt
                     | forIterationStmt"""
    add_node(p, 'iterationStmt')

def p_whileIterationStmt(p):
    """whileIterationStmt : WHILE '(' simpleExpression ')' stmt"""
    add_node(p, 'whileIterationStmt')

def p_whileIterationStmt_error(p):
    """whileIterationStmt : WHILE '(' error ')' stmt"""
    print('Malformed condition expression in WHILE statement!')

def p_forIterationStmt(p):
    """forIterationStmt : FOR ID '=' rangeExpression stmt"""
    add_node(p, 'forIterationStmt')

def p_forIterationStmt_error(p):
    """forIterationStmt : FOR ID '=' error stmt"""
    print('Error in range expression in for statement!')

def p_rangeExpression(p):
    """rangeExpression : simpleExpression ':' simpleExpression"""
    add_node(p, 'rangeExpression')

def p_returnStmt(p):
    """returnStmt : RETURN expression ';'
                  | RETURN ';'"""
    add_node(p, 'returnStmt')

def p_returnStmt_error(p):
    """returnStmt : RETURN error ';'"""
    print('Malformed expression in return statement!')

def p_breakStmt(p):
    """breakStmt : BREAK ';'"""
    add_node(p, 'breakStmt')

def p_breakStmt_error(p):
    """breakStmt : BREAK error ';'"""
    print('Encountered malformed expression after break statement!')

def p_continueStmt(p):
    """continueStmt : CONTINUE ';'"""
    add_node(p, 'continueStmt')

def p_continueStmt_error(p):
    """continueStmt : CONTINUE error ';'"""
    print('Encountered malformed expression after continue statement!')

def p_printStmt(p):
    """printStmt : PRINT args ';'"""
    add_node(p, 'printStmt')

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
    add_node(p, 'expression')

def p_expression_error(p):
    """expression : mutable '=' error
                  | mutable ADDASSIGN error
                  | mutable SUBASSIGN error
                  | mutable MULASSIGN error
                  | mutable DIVASSIGN error"""
    print('Malformed  assignment expression!')

def p_simpleExpression(p):
    """simpleExpression : simpleExpression '-' simpleExpression
                       | simpleExpression '*' simpleExpression
                       | simpleExpression '/' simpleExpression
                       | simpleExpression '+' simpleExpression
                       | simpleExpression DOTADD simpleExpression
                       | simpleExpression DOTSUB simpleExpression
                       | simpleExpression DOTMUL simpleExpression
                       | simpleExpression DOTDIV simpleExpression
                       | simpleExpression '<' simpleExpression
                       | simpleExpression '>' simpleExpression
                       | simpleExpression GTE simpleExpression
                       | simpleExpression EQ simpleExpression
                       | simpleExpression NEQ simpleExpression
                       | simpleExpression LTE simpleExpression
                       | uminusExpression
                       | simpleExpression TRANSPOSE
                       | value"""
    add_node(p, 'simpleExpression')

def p_uminusExpression(p):
    """uminusExpression : '-' simpleExpression %prec UMINUS"""
    add_node(p, 'uminusExpression')

def p_uminusExpression_error(p):
    """uminusExpression : '-' error %prec UMINUS"""
    print('Malformed expression after negation operator!')

def p_value(p):
    """value : immutable
             | mutable"""
    add_node(p, 'value')

def p_mutable(p):
    """mutable : ID
               | ID '[' vectorItem ']'
               | ID '[' vectorItem ',' vectorItem ']'"""
    add_node(p, 'mutable')

def p_mutable_error(p):
    """mutable : ID '[' error ']'
               | ID '[' error ',' vectorItem ']'"""
    print('Malformed index in matrix/vector selection operator!')

def p_immutable(p):
    """immutable : '(' expression ')'
                 | constant
                 | call"""
    add_node(p, 'immutable')

def p_call(p):
    """call : functionId '(' args ')'"""
    add_node(p, 'call')

def p_call_error(p):
    """call : functionId '(' error ')'"""
    print('Malformed function call!')

def p_args(p):
    """args : argList
            | empty"""
    add_node(p, 'args')

def p_argList(p):
    """argList : argList ',' simpleExpression
               | simpleExpression"""
    add_node(p, 'argList')

def p_constant(p):
    """constant : scalarConst
                | STRINGCONST
                | matrixConst"""
    add_node(p, 'constant')

def p_functionId(p):
    """functionId : EYE
                  | ZEROS
                  | ONES"""
    add_node(p, 'functionId')

def p_scalarConst(p):
    """scalarConst : INTCONST
                   | FLOATCONST"""
    add_node(p, 'scalarConst')

def p_matrixConst(p):
    """matrixConst : '[' matrixItems ']'"""
    add_node(p, 'matrixConst')

def p_matrixConst_error(p):
    """matrixConst : '[' error ']'"""
    print('Wrong item in matrix constant!')

def p_matrixItems(p):
    """matrixItems : matrixItems ';' vectorItems
                   | vectorItems"""
    add_node(p, 'matrixItems')

def p_vectorItems(p):
    """vectorItems : vectorItems ',' vectorItem 
                   | vectorItem"""
    add_node(p, 'vectorItems')

def p_vectorItem(p):
    """vectorItem : scalarConst
                  | STRINGCONST"""
    add_node(p, 'vectorItem')

parser = yacc.yacc(debug=True)