# Timothy Colaneri
# Assignment for CSC402/ fall 2019
# Lexer for Vintage BASIC

import re            #Regular expressions
from ply import lex  #Ply tools lexxer

##################################################### Reserved keywords
reserved = {
    'END'       : 'END',
    'STOP'      : 'STOP',
    'FOR'       : 'FOR',
    'TO'        : 'TO',
    'STEP'      : 'STEP',
    'NEXT'      : 'NEXT',
    'LET'       : 'LET',
    'GOTO'      : 'GOTO',
    'PRINT'     : 'PRINT',
    'IF'        : 'IF',
    'THEN'      : 'THEN',
    'INPUT'     : 'INPUT',
    'GOSUB'     : 'GOSUB',
    'FN'        : 'FN',
    'DEF'       : 'DEF',
    'DATA'      : 'DATA',
    'READ'      : 'READ',
    'DIM'       : 'DIM',
    'REM'       : 'REM',
    'ON'        : 'ON',
    'RETURN'    : 'RETURN',
    'RESTORE'   : 'RESTORE',
    'NOT'       : 'NOT',
    'AND'       : 'AND',
    'OR'        : 'OR',
    'ABS'       : 'ABS',
    'ASC'       : 'ASC',
    'ATN'       : 'ATN',
    'CHR'       : 'CHR',
    'COS'       : 'COS',
    'EXP'       : 'EXP',
    'INT'       : 'INT',
    'LEFT'      : 'LEFT',
    'LEN'       : 'LEN',
    'LOG'       : 'LOG',
    'MID'       : 'MID',
    'RIGHT'     : 'RIGHT',
    'RND'       : 'RND',
    'SGN'       : 'SGN',
    'SIN'       : 'SIN',
    'SPC'       : 'SPC',
    'SQR'       : 'SQR',
    'STR'       : 'STR',
    'TAN'       : 'TAN',
    'VAL'       : 'VAL',   
}

# Listerals List
literals = [',',';',':','(',')','[',']','=',]

# Tokens List
tokens = [
          'PLUS','MINUS','MULT','DIVIDE', 'EQ','LE',
          'NUMBER','ID','EXPP','INEQ', 'LT','GT','GE',
          'STRING','INTEGER','REAL'
          
          ] + list(reserved.values())
# Token REs
t_PLUS    = r'\+'
t_EQ      = r'=='
t_MINUS   = r'-'
t_MULT   = r'\*'
t_DIVIDE  = r'/'
t_LE      = r'<='
t_EXPP     = r'\^'
t_INEQ    = r'<>'
t_LT      = r'<'
t_GT      = r'>'
t_GE      = r'>='
t_ignore = ' \t'

############################################################ ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check if reserved
    return t

############################################################ is_ID
def is_ID(s):
    m = re.match(r'[a-zA-Z_][a-zA-Z_0-9]*', s)   
    if s in list(reserved.keys()):
        return False
    elif m and len(m.group(0)) == len(s):
        return True
    else:
        return False
    
############################################################ NUMBER
def t_NUMBER(t):
    r'([0-9]*[.])?[0-9]+'
    t.type = 'REAL' if '.' in t.value else 'INTEGER'
    return t

############################################################ STRING
def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1] 
    return t

############################################################ NEWLINE
def t_NEWLINE(t):
    r'\n'
    pass

############################################################ ERROR
def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# Create lexer
lexer = lex.lex(debug=0)

