# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

import ply.lex as lex

text = None

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = [
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'LTE',
    'GTE',
    'NEQ',
    'EQ',
    'ID',
    'INTCONST',
    'FLOATCONST',
    'STRINGCONST',
    'TRANSPOSE'
 ] + list(reserved.values())

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LTE = r'<='
t_GTE = r'>='
t_NEQ = r'!='
t_EQ = r'=='
t_TRANSPOSE = r'\''

t_ignore = '  \t'

literals = "+-*/=<>()[]}{:,;"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_FLOATCONST(t):
    r'([0-9]*\.[0-9]+([eE][-+]?[0-9]+)?|[0-9]+\.[0-9]*)'
    t.value = float(t.value)
    return t

def t_INTCONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRINGCONST(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID') #check if the identifiers is not a reserved keyword
    return t

def t_error(t):
    print("line %d: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)

def find_column(input, token):
    start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - start) + 1

def find_tok_column(p):
    start = text.rfind('\n', 0, p.lexpos) + 1
    return (p.lexpos - start) + 1

lexer = lex.lex()