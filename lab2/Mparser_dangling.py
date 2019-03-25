#!/usr/bin/python

# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

start = 'stmtList'

precedence = (
    ("nonassoc", '<', '>', 'LTE', 'GTE', 'EQ', 'NEQ'),
    ("left", '+', '-', 'DOTADD', 'DOTSUB'),
    ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
    ("right", 'UMINUS'),
    ('right', 'TRANSPOSE')
)

def p_error(p):
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
    """stmtList : stmtList protoStmt
                | empty """
    add_node(p, 'stmtList')

def p_protoStmt(p):
    """protoStmt : openProtoStmt
                 | closedProtoStmt """
    add_node(p, 'protoStmt')

def p_openProtoStmt(p):
    """openProtoStmt : IF '(' simpleExpression ')' protoStmt
                     | IF '(' simpleExpression ')' closedProtoStmt ELSE openProtoStmt"""
    add_node(p, 'openProtoStmt')
                    
def p_closedProtoStmt(p):
    """closedProtoStmt : stmt
                       | IF '(' simpleExpression ')' closedProtoStmt ELSE closedProtoStmt"""
    add_node(p, 'closedProtoStmt')

def p_stmt(p):
    """stmt : expressionStmt
            | compundStmt
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

def p_iterationStmt(p):
    """iterationStmt : whileIterationStmt
                     | forIterationStmt"""
    add_node(p, 'iterationStmt')

def p_whileIterationStmt(p):
    """whileIterationStmt : WHILE '(' simpleExpression ')' stmt"""
    add_node(p, 'whileIterationStmt')

def p_forIterationStmt(p):
    """forIterationStmt : FOR ID '=' rangeExpression stmt"""
    add_node(p, 'forIterationStmt')

def p_rangeExpression(p):
    """rangeExpression : simpleExpression ':' simpleExpression"""
    add_node(p, 'rangeExpression')

def p_returnStmt(p):
    """returnStmt : RETURN returnRest
       returnRest : ';'
                  | expression ';'"""
    add_node(p, 'returnStmt')

def p_breakStmt(p):
    """breakStmt : BREAK ';'"""
    add_node(p, 'breakStmt')

def p_continueStmt(p):
    """continueStmt : CONTINUE ';'"""
    add_node(p, 'continueStmt')

def p_printStmt(p):
    """printStmt : PRINT args ';'"""
    add_node(p, 'printStmt')

def p_expression(p):
    """expression : mutable '=' expression
                  | mutable ADDASSIGN expression
                  | mutable SUBASSIGN expression
                  | mutable MULASSIGN expression
                  | mutable DIVASSIGN expression
                  | simpleExpression"""
    add_node(p, 'expression')

def p_simpleExpression(p):
    """simpleExpression : arithExpression relop arithExpression
                        | arithExpression"""
    add_node(p, 'simpleExpression')

def p_relop(p):
    """relop : LTE
             | '<'
             | '>'
             | GTE
             | EQ
             | NEQ"""
    add_node(p, 'relop')

def p_arithExpression(p):
    """arithExpression : arithExpression binArithOp arithExpression
                       | uminusExpression
                       | arithExpression TRANSPOSE
                       | value"""
    add_node(p, 'arithExpression')

def p_uminusExpression(p):
    """uminusExpression : '-' arithExpression %prec UMINUS"""
    add_node(p, 'uminusExpression')

def p_binArithOp(p):
    """binArithOp : '+'
                  | '-'
                  | '*'
                  | '/'
                  | DOTADD
                  | DOTSUB
                  | DOTMUL
                  | DOTDIV"""
    add_node(p, 'binArithOp')

def p_value(p):
    """value : immutable
             | mutable"""
    add_node(p, 'value')

def p_mutable(p):
    """mutable : ID
               | mutable '[' vectorItem ']'
               | mutable '[' vectorItem ',' vectorItem ']'"""
    add_node(p, 'mutable')

def p_immutable(p):
    """immutable : '(' expression ')'
                 | constant
                 | call"""
    add_node(p, 'immutable')

def p_call(p):
    """call : functionId '(' args ')'"""
    add_node(p, 'call')

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

parser = yacc.yacc()