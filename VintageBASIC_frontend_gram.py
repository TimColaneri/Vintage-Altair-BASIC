# Timothy Colaneri
# CSC402 Project/ Fall 2019
# grammar for Vintage Basic

from ply import yacc
from VintageBASIC_lex import tokens, lexer
from VintageBASIC_state import state

# set precedence and associativity
precedence = (
              ('left', 'OR'),
              ('left', 'AND'),
              ('left', 'NOT'),
              ('left', 'EQ', 'INEQ', 'LT', 'LE', 'GT', 'GE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'MULT', 'DIVIDE'),
              ('right', 'EXPP'),
              ('left', 'UMINUS')
             )
###################################################################
def p_prog(p):
    '''
    program : sentence_list
    '''
    state.AST = p[1]
###################################################################   
def p_sentence_list(p):
    '''
    sentence_list : INTEGER stmts sentence_list
                  | INTEGER stmts
    '''
    if (len(p) > 3):
        p[0] = ('line', p[1], p[2], p[3])
        state.instr_list.append(p[2])
        state.instr_labels.append(p[1])
    else:
        p[0] = ('line', p[1], p[2])
        state.instr_list.append(p[2])
        state.instr_labels.append(p[1])
###################################################################
def p_statements(p):
    '''
    stmts : stmt ':' stmts
          | stmt
    '''
    if len(p) > 2:
        p[0] = ('seq', p[1],p[3])
    else:
        p[0] = ('seq',p[1])
###################################################################
def p_loop_sentence_list(p):
    '''
    loop_sentence_list : INTEGER stmts loop_sentence_list
                       | INTEGER NEXT opt_var
    '''
    p[0] = ('line',p[1],p[2],p[3])
    if p[2] != 'next':
        state.instr_list.append(p[2])
        state.instr_labels.append(p[1])
 ###################################################################   
def p_loop_statements(p):
    '''
    loop_statements : stmt ':' loop_statements
                    | stmt ':'
    '''
    if len(p) > 3:
        p[0] = (p[1],p[3])
    else:
        p[0] = (p[1],)
###################################################################
def p_for_stmt(p):
    '''
     stmt  : FOR ID '=' expr TO expr opt_step loop_sentence_list
           | FOR ID '=' expr TO expr opt_step ':' loop_statements NEXT opt_var
    '''
    if p[8] != ':':
        p[0] = ('for',p[2],p[4],p[6],p[7],p[8])
    else:
        p[0] = ('for',p[2],p[4],p[6],p[7],p[9],p[11])
###################################################################
def p_func_stmt(p):
    '''
    stmt : DEF FN ID '(' opt_formal_args ')' '=' expr
    '''
    p[0] = ('fundecl', p[3], p[5], p[8])
####################################################################
def p_rem_stmt(p):
    '''
    stmt : REM text
    '''
    p[0] = ('rem',)
###################################################################
def p_text_exp(p):
    '''
    text : ID text
         | empty
    '''
    p[0] = p[1]
#########################################################################
def p_opt_actual_args(p):
    '''
    opt_actual_args : actual_args
                    | empty
    '''
    p[0] = p[1]
#########################################################################
def p_actual_args(p):
    '''
    actual_args : expr ',' actual_args
                | expr
    '''
    if (len(p) == 4):
        p[0] = ('seq', p[1], p[3])
    elif (len(p) == 2):
        p[0] = ('seq', p[1], ('nil',))
#########################################################################
def p_call_exp(p):
    '''
    expr : ID '(' opt_actual_args ')'
    '''
    p[0] = ('callexp', p[1], p[3])
###################################################################
def p_opt_formal_args(p):
    '''
    opt_formal_args : formal_args
                    | empty
    '''
    p[0] = p[1]
###################################################################
def p_formal_args(p):
    '''
    formal_args : ID ',' formal_args
                | ID
    '''
    if (len(p) == 4):
        p[0] = ('seq', ('id', p[1]), p[3])
    elif (len(p) == 2):
        p[0] = ('seq', ('id', p[1]), ('nil',))
###################################################################
def p_binop_exp(p):
    '''
    expr : expr PLUS expr
         | expr MINUS expr
         | expr MULT expr
         | expr DIVIDE expr
         | expr EQ expr
         | expr EXPP expr
         | expr LE expr
         | expr LT expr
         | expr GT expr
         | expr GE expr
         | expr INEQ expr
         | expr AND expr
         | expr OR expr
    '''
    p[0] = (p[2], p[1], p[3])
###################################################################
def p_uminus_exp(p):
    '''
    expr : MINUS expr %prec UMINUS
    '''
    p[0] = ('uminus', p[2])
###################################################################
def p_abs_exp(p):
    '''
    expr : ABS '(' expr ')'
    '''
    p[0] = ('abs',p[3])
###################################################################
def p_asc_exp(p):
    '''
    expr : ASC '(' STRING ')'
         | ASC '(' storable ')'
    '''
    p[0] = ('asc',p[3])
###################################################################
def p_atn_exp(p):
    '''
    expr : ATN '(' expr ')'
    '''
    p[0] = ('atn',p[3])
###################################################################
def p_chr_exp(p):
    '''
    expr : CHR '(' expr ')'
    '''
    p[0] = ('chr',p[3])
###################################################################
def p_cos_exp(p):
    '''
    expr : COS '(' expr ')'
    '''
    p[0] = ('cos',p[3])
###################################################################
def p_e_exp(p):
    '''
    expr : EXP '(' expr ')'
    '''
    p[0] = ('eExp',p[3])
###################################################################
def p_int_exp(p):
    '''
    expr : INT '(' expr ')'
    '''
    p[0] = ('int',p[3])
###################################################################
def p_left_exp(p):
    '''
    expr : LEFT '(' STRING ',' INTEGER ')'
         | LEFT '(' storable ',' INTEGER ')'
    '''
    p[0] = ('left',p[3],p[5])
###################################################################
def p_len_exp(p):
    '''
    expr : LEN '(' STRING ')'
         | LEN '(' storable ')'
    '''
    p[0] = ('len',p[3])
###################################################################
def p_log_exp(p):
    '''
    expr : LOG '(' expr ')'
    '''
    p[0] = ('log',p[3])
###################################################################
def p_mid_exp(p):
    '''
    expr : MID '(' STRING ',' expr ')'
         | MID '(' storable ',' expr ')'
         | MID '(' STRING ',' expr ',' expr ')'
         | MID '(' storable ',' expr ',' expr ')'
    '''
    if not p[6] == ',':
        p[0] = ('mid',p[3],p[5])
    else:
        p[0] = ('mid',p[3],p[5],p[7])
###################################################################
def p_right_exp(p):
    '''
    expr : RIGHT '(' STRING ',' expr ')'
         | RIGHT '(' storable ',' expr ')'
    '''
    p[0] = ('right',p[3],p[5])
###################################################################
def p_rnd_exp(p):
    '''
    expr : RND '(' expr ')'
    '''
    p[0] = ('rnd',p[3])
###################################################################
def p_sgn_exp(p):
    '''
    expr : SGN '(' expr ')'
    '''
    p[0] = ('sgn',p[3])
###################################################################
def p_sin_exp(p):
    '''
    expr : SIN '(' expr ')'
    '''
    p[0] = ('sin',p[3])
###################################################################
def p_spc_exp(p):
    '''
    expr : SPC '(' expr ')'
    '''
    p[0] = ('spc',p[3])
###################################################################
def p_sqr_exp(p):
    '''
    expr : SQR '(' expr ')'
    '''
    p[0] = ('sqr',p[3])
###################################################################
def p_str_exp(p):
    '''
    expr : STR '(' expr ')'
    '''
    p[0] = ('str',p[3])
###################################################################
def p_tan_exp(p):
    '''
    expr : TAN '(' expr ')'
    '''
    p[0] = ('tan',p[3])
###################################################################
def p_val_exp(p):
    '''
    expr : VAL '(' STRING ')'
         | VAL '(' storable ')'
    '''
    p[0] = ('val',p[3])
 ###################################################################   
def p_on_statement(p):
    '''
    stmt : ON expr GOTO label_list
         | ON expr GOSUB label_list
    '''
    p[0] = ('on',p[2],p[3],p[4])
###################################################################
def p_label_list(p):
    '''
    label_list : INTEGER ',' label_list
               | INTEGER
    '''
    if len(p) > 2:
        p[0] = ('labelList',p[1],p[3])
    else:
        p[0] = ('label',p[1])
###################################################################
def p_input_statement(p):
    '''
    stmt : INPUT opt_str ';' var_list
    '''
    if p[2] != ';':
        p[0] = ('input',p[2],p[4])
    else:
        p[0] = ('input',p[2])
###################################################################
def p_return_statement(p):
    '''
    stmt : RETURN
    '''
    p[0] = ('return',)
###################################################################   
def p_dim_statement(p):
    '''
    stmt : DIM ID '(' int_list ')'
    '''
    p[0] = ('dim',p[2],p[4])
###################################################################
def p_int_list(p):
    '''
    int_list : INTEGER ',' int_list
             | INTEGER
             | empty
    '''
    if len(p) > 2:
        p[0] = ('intlist',p[1],p[3])
    else:
        p[0] = ('int',p[1])
###################################################################
def p_let_statement(p):
    '''
    stmt :  LET storable '=' expr
         |  LET storable '=' STRING
         |  storable '=' expr
         |  storable '=' STRING
    '''
    if len(p) > 4:
        p[0] = ('let',p[2],p[4])
    else:
        p[0] = ('let',p[1],p[3])
###################################################################
def p_if_statement(p):
    '''
    stmt : IF expr THEN stmts
         | IF expr THEN INTEGER
    '''
    p[0] = ('if',p[2],p[4])
###################################################################
def p_goto_statement(p):
    '''
    stmt : GOTO INTEGER
    '''
    p[0] = ('goto',p[2])
###################################################################
def p_gosub_statement(p):
    '''
    stmt : GOSUB INTEGER
    '''
    p[0] = ('gosub',p[2])
###################################################################
def p_data_statement(p):
    '''
    stmt : DATA val_list
    '''
    p[0] = ('data',p[2])
###################################################################
def p_restore_statement(p):
    '''
    stmt : RESTORE 
    '''
    if len(p) > 2:
        p[0] = ('restore',p[2])
    else:
        p[0] = ('restore',)
###################################################################
def p_read_statement(p):
    '''
    stmt : READ var_list
    '''
    p[0] = ('read',p[2])
###################################################################    
def p_val_list(p):
    '''
    val_list : STRING ',' val_list
             | INTEGER ',' val_list
             | REAL ',' val_list
             | REAL
             | STRING
             | INTEGER
             | empty
    '''
    if len(p) > 2:
        p[0] = ('vallist',p[1],p[3])
    else:
        p[0] = ('val',p[1])
################################################################### 
def p_print_statement(p):
    '''
    stmt : PRINT print_list
    '''
    p[0] = ('print',p[2])
###################################################################
def p_end_statement(p):
    '''
    stmt : END
    '''
    p[0] = ('end',)
###################################################################
def p_stop_statement(p):
    '''
    stmt : STOP
    '''
    p[0] = ('end',)
###################################################################
def p_not_exp(p):
    '''
    expr : NOT expr
    '''
    p[0] = ('not',p[2])
###################################################################
def p_opt_string(p):
    '''
    opt_str : STRING
            | empty
    '''
    p[0] = ('string',p[1])    
###################################################################
def p_opt_var(p):
    '''
    opt_var : ID
            | empty
    '''
    p[0] = (p[1],)
###################################################################
def p_opt_step(p):
    '''
    opt_step : STEP expr
             | empty
    '''
    if len(p) > 2:
        p[0] = (p[1],p[2])
    else:
        p[0] = (p[1],)
###################################################################
def p_integer_exp(p):
    '''
    expr : INTEGER
    '''
    p[0] = ('integer', int(p[1]))
###################################################################
def p_real_exp(p):
    '''
    expr : REAL
    '''
    p[0] = ('real',p[1])
###################################################################
def p_storable_exp(p):
    '''
    expr : storable
    '''
    p[0] = p[1]
###################################################################
def p_storable_1(p):
    '''
    storable : ID
    '''
    p[0] = ('id', p[1])
###################################################################
def p_storable_2(p):
    '''
    storable : ID '[' expr ']'
    '''
    p[0] = ('arr', p[1], p[3])
###################################################################
def p_id_exp(p):
    '''
    expr : ID
    '''
    p[0] = ('id', p[1])
###################################################################
def p_varlist(p):
    '''
    var_list    : storable ',' var_list
                | storable
    '''
    if len(p) > 2:
        p[0] = ('varlist',p[1],p[3])
    else:
        p[0] = ('var',p[1])
###################################################################
def p_empty(p):
    '''
    empty :
    '''
    p[0] = ('nil',)
###################################################################
def p_printlist(p):
    '''
    print_list : STRING ';' print_list
               | STRING ',' print_list
               | expr ';' print_list
               | expr ',' print_list
               | STRING
               | expr
    '''
    if (len(p) > 2):
        p[0] = ('printlist',p[1],p[2],p[3])
    else:
        p[0] = ('print',p[1])
###################################################################    
def p_error(t):
    print("Syntax error at '%s'" % t.value)
###################################################################
parser = yacc.yacc(debug=False,tabmodule='VintageBASICparsetab')



       
   
  
            






