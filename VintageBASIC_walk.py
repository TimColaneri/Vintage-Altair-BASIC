# Timothy Colaneri
# CSC402 Project/ Fall 2019
# Vintage Basic Tree Walker


########################################IMPORTS
from VintageBASIC_state import state   #State objects holds refernces to tables/ect.
from helper_functions import assert_match #Used for input validation
import math                            #Used to map pre-built VB functions
from random import random, seed        #Used in random function

#Denotes a walkable node type
WALKABLE = ['id','+','-','/','*','callexp','integer','string','real','not','uminus','rnd']
lastRandom = 0 #Holds value of last generated random; function of random is to return last random
lastIndex = 0  #Holds index value of last program instruction; used in for statements to jump to next when complete
seed(1)        #Initialize random number generator


####################################################################SEQ
def seq(node):
    #Denotes begining of sequence; walks program statements
    #has 2 forms handled by if switch( One statement or >1 statements)
    
    if len(node) > 2:
        (SEQ, stmt, stmt_list) = node
        assert_match(SEQ, 'seq')
        
        walk(stmt)
        walk(stmt_list)
    else:
        (SEQ, stmt) = node
        assert_match(SEQ, 'seq')
        
        walk(stmt)
####################################################################LINE
def line(node):
    global lastIndex
    # We only real go here in this implementation in order to process
    # for loops as each line is seperatly stored in the state instr_list
    # HOWEVER, this walker is capable of walking entire programs with
    # this node

    # If switch determines which of 2 forms we recieved, one statement
    # or statements
    if len(node) > 3:
        
        (LINE,label,stmts, sentence_list) = node

        # If its a next, we don't want to walk it as it's not its own
        # node type, instead we want to store the last location so we know
        # where to jump to when the for loop is completed.
        if node[2] != 'NEXT':
            
            walk(stmts)
            walk(sentence_list)
            lastIndex = state.instr_labels.index(label)
    else:
        
        (LINE,label,stmts) = node
        walk(stmts)
####################################################################LET_STMT
def let_stmt(node):
    global WALKABLE
    # Assignment statement in Vintage BASIC

    (LET,var,expr) = node
    assert_match(LET,'let')
    
    # If the passed in expression is walkable, walk it; else its a string
    if len(expr[0]) > 1 or expr[0] in WALKABLE:
        val = walk(expr)
    else:
        val = str(expr)

    # If the assignment variable is an array location, grab it
    if (var[0] == 'arr'):
        name = var[1]
        memLocation = state.symbol_table.lookup_sym(name)
        
        index = walk(var[2]) # get the array index

        memLocation[index] = (val)# put the value in the memory space
    else:
        # Else its a normal varaible, declare it in the symbol table
        var = var[1]
        state.symbol_table.declare_sym(var,val)
####################################################################REM_STMT
def rem_stmt(node):
    # Vintage Basic comment statement
    # Nothing to do here

    (REM,) = node
    assert_match(REM,'rem')
    pass
####################################################################END_STMT
def end_stmt(node):
    # Vintage Basic End Statement
    # Stops execution of program when encountered
    
    (END,) = node
    assert_match(END,'end')
    
    # quit by custom exception
    raise StopExecution
####################################################################PRINT_STMT
def print_stmt(node):
    global WALKABLE
    outStr = '' #print output constructed in outStr
    # Vintage Basic print statement
    # Prints strings and numbers, also evauates and prints expressions
    # results

    (PRINT,print_list) = node
    assert_match(PRINT,'print')

    # If the print list is just 1 element 
    if print_list[0] == 'print':

        # If its and expression, walk it
        if (print_list[1])[0] in WALKABLE:
            var = walk(print_list[1])
            outStr += str( var )

        # If its an array element, get the location    
        elif (print_list[1])[0] == 'arr':
            arr = state.symbol_table.lookup_sym((print_list[1])[1])
            index = walk((print_list[1])[2])
            outStr += str(arr[index])

        # Else its a string
        else: 
            outStr += (str(print_list[1]))
    #Else it has more thne 1 thing to print
    else:
        
        nextInstr = print_list[0]
        nextTuple = 0

        # While there are more then 1 items in the print list
        while nextInstr == 'printlist':

            #If its not the first iteration
            if (nextTuple):

                #Determine what kind of print instruction we
                # we were sent and handle it
                nextStr = nextTuple[1]
                if nextStr[0] in WALKABLE:
                    var = walk(nextStr)
                    outStr += str( var )
                elif nextStr[0] == 'arr':#Handle array element
                    
                    arr = state.symbol_table.lookup_sym((print_list[1])[1])
                    index = walk((nextStr)[2])
                    outStr += str(arr[index])
                else:
                    outStr += str(nextStr)

               
                
                if (nextTuple[2] == ';'):#Add space if divider = ;
                    outStr += " "
                nextTuple = nextTuple[3]
                

            # Else its the first iteration
            else:
                
                #Determine what kind of print instruction we
                # we were sent and handle it
                nextStr = print_list[1]
                
                if nextStr[0] in WALKABLE:
                    var = walk(nextStr)
                    outStr += str( var )
                elif nextStr[0] == 'arr':#Handle array element
                    arr = state.symbol_table.lookup_sym((print_list[1])[1])
                    index = walk((print_list[1])[2])
                    outStr += str(arr[index])
                else:
                    outStr += str(nextStr)
                if (print_list[2] == ';'): #Add space if divider = ;
                    outStr += " "
                nextTuple = print_list[3]
                
            nextInstr = nextTuple[0]

        # Grab and print the last item after processing list
        if (nextTuple[1])[0] in WALKABLE:
            var = walk(nextTuple[1])
            outStr += str( var )
        elif (nextTuple[1])[0] == 'arr':
            arr = state.symbol_table.lookup_sym((print_list[1])[1])
            index = walk((nextTuple[1])[2])
            outStr += str(arr[index])
        else:
            outStr += str(nextTuple[1]) 

    #Output printed to console
    print(outStr)
    return
########################################################################DIM_STMT
def dim_stmt(node):
    # Vintage Basic declare array statement

    (DIM,name,intList) = node
    assert_match(DIM,'dim')

    state.symbol_table.declare_array(name,intList)
#########################################################################LEN_SEQ
def len_seq(seq_list):
    # Determines length of a sequence
    # Used in determining argument/parameters counts in function calls

    # No more nodes, return
    if seq_list[0] == 'nil':
        return 0

    # Else +1 the count then check for more
    elif seq_list[0] == 'seq':

        (SEQ, node, nodeList) = seq_list
        return 1 + len_seq(nodeList)

    else:
            raise ValueError("unknown node type: {}".format(seq_list[0]))
########################################################################INTEGER_EXP
def integer_exp(node):
    # Integer expression

    (INTEGER, value) = node
    assert_match(INTEGER, 'integer')

    return int(value)
########################################################################REAL_EXP
def real_exp(node):
    # Real number expression

    (REAL, value) = node
    assert_match(REAL, 'real')

    return float(value)
#########################################################################ARR_EXP
def arr_exp(node):
    # array id

    (ARR,name,inx) = node
    assert_match(ARR,'arr')

    memLocation = state.symbol_table.lookup_sym(name)
    
    index = walk(inx) # get the array index
            
    return memLocation[index]
#########################################################################GOTO_STMT
def goto_stmt(node):
    # Vintage Basic GOTO statement

    (GOTO, target) = node
    assert_match(GOTO,'goto')

    # Set the state objects current instruction for the desirsed destinations index
    state.instr_ix = state.instr_labels.index(target)-1
#########################################################################IF_STMT
def if_stmt(node):
    # Vintage Basic IF statement

    (IF,test,stmt) = node
    assert_match(IF, 'if')

    val = walk(test)

    # If the expression is false, skip it;
    # Else evaluate the expression
    if val == 0:
        return
    else:

        # If the expression is a label, then walk a GOTO label;
        # else walk expression
        if len(stmt[1]) == 1:
            walk(('goto',stmt))
        else:
            walk(stmt)
#########################################################################ADD_EXP
def add_exp(node):
    # Binary Operation: Addition

    (ADD,lhs,rhs) = node
    assert_match(ADD,'+')

    return (walk(lhs) + walk(rhs))
#########################################################################SUB_EXP
def sub_exp(node):
    # Binary Operation: Subtraction

    (SUB,lhs,rhs) = node
    assert_match(SUB,'-')

    return (walk(lhs) - walk(rhs))
#########################################################################DIV_EXP
def div_exp(node):
    # Binary Operation: Division

    (DIV,lhs,rhs) = node
    assert_match(DIV,'/')

    return(walk(lhs) / walk(rhs))
#########################################################################MEL_EXP
def mul_exp(node):
    # Binary Operation: Multiplication

    (MUL,lhs,rhs) = node
    assert_match(MUL,'*')

    return (walk(lhs) * walk(rhs))
#########################################################################ID_EXP
def id_exp(node):
    # This node grabs the value of a variable
    # Current implementation assigns 0 if variable unassigned
    
    (ID, name) = node
    assert_match(ID, 'id')
    
    try:
        
        val = state.symbol_table.lookup_sym(name)
    except KeyError:
        val = 0
        
    return val
#########################################################################VARIABLE_EXP
'''NOT IMPLEMENTED********
def variable_exp(node):
    (VAR,name) = node
    assert_match(VAR,'variable')
    
    node = node[1]

    try:
        (ID,inx,inxList) = node
        if (inxList[0] != 'nil'):
            val = state.symbol_table.lookup_sym(name)
            #print(val)

    except:
        (ID, name) = node
        assert_match(ID, 'id')
        try:
            val = state.symbol_table.lookup_sym(name)
        except KeyError:
            val = 0
        
        return val
        '''
#########################################################################FOR_STMT
def for_stmt(node):
    global lastIndex # holds index to return to when loop complete
    # Vintage Basic for loop

    # Try the 6 value form, except the 7 value
    # multi line for loop is size 6 tuple
    # single line for loop is size 7 tuple
    try:
        (FOR,var,varStart,varEnd,optStep,stmtList) = node
        assert_match(FOR,'for')
    except:
        (FOR,var,varStart,varEnd,optStep,stmtList,nextid) = node
        if (optStep[0])[0] == 'nil':
            step = 1
        else:
            step = walk(optStep[1])

        #Prime the loop conditions
        start = walk(varStart)           #Start value
        walk(('let',('id',var),varStart))#Declare start variable
        stop = walk(varEnd)              #End value
        strStmt = stmtList               # hold on to original statement list

        # If its a incrementing loop  
        if stop > start:
        
            #Loop executed until start value exceeds stop
            while start < stop:
                #Try walking statements until we are done
                try:
                     while 1:
                         walk(stmtList[0])
                         stmtList = stmtList[1]
                except:
                    stmtList = strStmt
                    
                start += step
                state.symbol_table.update_sym(var, (start))
        else:

            #Loop executed until stop value exceeds start value
            while stop < start:
                try:
                     while 1:
                         walk(stmtList[0])
                         stmtList = stmtList[1]
                except:
                    stmtList = strStmt
                
                walk(stmtList[0])
                start += step
                state.symbol_table.update_sym(var, (start))
                
        state.instr_ix = lastIndex
    else:
        #Prime the loop conditions
        start = walk(varStart)           #Start value
        walk(('let',('id',var),varStart))#Declare start variable
        stop = walk(varEnd)              #End value
    

        # Check for step value and assign it;Else step is + 1
        if (optStep[0])[0] == 'nil':
            step = 1
        else:
            step = walk(optStep[1])

        # If\Else catches incrementing or decrementing loops
        if stop > start:
        
            #Loop executed until start value exceeds stop
            while start < stop:
                walk(stmtList)
                start += step
                state.symbol_table.update_sym(var, (start))
        else:

            #Loop executed until stop value exceeds start value
            while stop < start:
                walk(stmtList)
                start += step
                state.symbol_table.update_sym(var, (start))

        # When loop has finished, we want to return to the end of the next statement
        state.instr_ix = lastIndex+1
#########################################################################FUNC_DECL_STMT
def func_decl_stmt(node):
    # Function declaration

    (FUNDECL,name,args,code) = node
    assert_match(FUNDECL,'fundecl')
    
        
    globalTable = state.symbol_table.get_config()   
    funcTuple = ('funval', args , code, globalTable)
    state.symbol_table.declare_fun(name, funcTuple)
#########################################################################DECLARE_FORMAL_ARGS
def declare_formal_args(formal_args, actual_val_args):
    # Formal argument declaration

    # If we don't have the right number of arguments, raise exception
    if len_seq(actual_val_args) != len_seq(formal_args):
        raise ValueError("actual and formal argument lists do not match")

    # BASE CASE
    # If we dont need any more formal arguments, return
    if formal_args[0] == 'nil':
        return

    # Unpack formal and actual argument tuples
    (SEQ, (ID, sym), p1) = formal_args
    (SEQ, val, p2) = actual_val_args

    # declare the variable
    state.symbol_table.declare_sym(sym, val)

    # Continue unpacking arguments
    declare_formal_args(p1, p2)
#########################################################################EVAL_ACTUAL_ARGS
def eval_actual_args(args):
    # Actual argument evaluation

    # If there is nothing there return nil node
    if args[0] == 'nil':
        return ('nil',)

    # If its an expression, walk it
    elif args[0] == 'seq':
        
        # unpack the seq node
        (SEQ, arg, arglist) = args

        # Get current argument value
        value = walk(arg)

        return ('seq', value , eval_actual_args(arglist))

    else:
        raise ValueError("unknown node type: {}".format(args[0]))
#########################################################################CALL_EXP
def call_exp(node):
    # Custom function call expression
    
    (CALLEXP, name, exp) = node
    assert_match(CALLEXP, 'callexp')

    # Get output of function evaluation
    value = handle_call(name, exp)
    
    if value is None:
        raise ValueError("No return value from function {}".format(name))
    
    return value
#########################################################################HANDLE_CALL
def handle_call(name, actual_arglist):
    # Custom function call helper
    
    (FUNC, val) = state.symbol_table.lookup_sym(name)
    assert_match(FUNC,'function')

    (FUNVAL, formal_arglist, body, context) = val

    if len_seq(formal_arglist) != len_seq(actual_arglist):
        raise ValueError("function {} expects {} arguments".format(sym, len_seq(formal_arglist)))

    # set up the environment for static scoping and then execute the function
    actual_val_args = eval_actual_args(actual_arglist)   # evaluate actuals in current symtab
    save_symtab = state.symbol_table.get_config()        # save current symtab
    state.symbol_table.set_config(context)               # make function context current symtab
    state.symbol_table.push_scope()                      # push new function scope
    declare_formal_args(formal_arglist, actual_val_args) # declare formals in function scope
    return_value = None
    try:
        return_value = walk(body)
    except ReturnValue as val:
        return_value = val.value

    # NOTE: popping the function scope is not necessary because we
    # are restoring the original symtab configuration
    state.symbol_table.set_config(save_symtab)           # restore original symtab config

    return return_value
#########################################################################INPUT_STMT
def input_stmt(node):
    # Vintage Basic input statement
    
    (INPUT,string,varList) = node
    assert_match(INPUT,'input')

    strValue = string[1] # Grab the value of the input string

    #If its 'nil' then there is no input string to process
    if(strValue[0] == 'nil'):
        
        (INPUT,nil,varList) = node
        assert_match(INPUT,'input')


        # If its 'var' then theres only 1 var
        if varList[0] == 'var':
            
            userInput = input("")   #Get input value
            if len((varList[1])[0]) > 1:
                actualID = (varList[1])[1]  #Get the name of the var)
            # Declare data in symbol table
            state.symbol_table.declare_sym(actualID,userInput)
            
        else:
        # Else we process through the list of vars to store into
        
            while 1:
                
                userInput = input("")   #Get input value
                actualID = varList[1]   #Get the name of the var
                                        #Declare data in symbol table
                state.symbol_table.declare_sym(actualID,userInput)
                varList = varList[2]

                # If the next var is the last one, process it and leave
                if varList[0] == 'var':
                    userInput = input("") #Get input value
                    actualID = varList[1] #Get the name of the var
                                          #Declare data in symbol table
                    state.symbol_table.declare_sym(actualID,userInput)
                    break

    #Else there is an input string to display
    else:
    
        if varList[0] == 'var':
            userInput = input(strValue+" ") #Get input value
            actualID = varList[1]       #Get the name of the var
                                        # Declare data in symbol table
            state.symbol_table.declare_sym(actualID,userInput)
        else:
            while 1:
                userInput = input(strValue+" ") #Get input value
                actualID = varList[1]           #Get the name of the var
                                                #Declare data in symbol table
                state.symbol_table.declare_sym(actualID,userInput)
                varList = varList[2]

                # If the next var is the last one, process it and leave
                if varList[0] == 'var':
                    userInput = input(strValue+" ") #Get input value
                    actualID = varList[1]           #Get the name of the var
                                                    # Declare data in symbol table
                    state.symbol_table.declare_sym(actualID,userInput)
                    break
########################################################################DATA_STMT
def data_stmt(node):
    # Vintage Basic data statement
    # This statement assigns data to be read at a later date in the program
    # In this interpreter, this is handles via a queue stored in the state object

    (DATA,valList) = node
    assert_match(DATA,'data')


    # While a list of values exists, store them in the queue
    while valList[0] == 'vallist':
        
        state.value_list.put(valList[1])
        valList = valList[2]

    # Grab the last value from the list and store it into the queue
    # single cases fall here too
    if (valList[1])[0] != 'nil':
        valList = valList[1]
        state.value_list.put(valList)

    # Copy the primary queue into the backup queue with most recent data
    for ctr in range( state.value_list.qsize() ):
        value = state.value_list.get()
        state.backup_value_list.put(value)
        state.value_list.put(value)
#########################################################################READ_STMT
def read_stmt(node):
    # Vintage Basic read statement
    # Takes in a list of variables to assign data from DATA statement into

    (READ,varList) = node
    assert_match(READ,'read')

    # While several objects exist in the list
    while varList[0] == 'varlist':
        # Check if empty
        if state.value_list.qsize() == 0:
            raise StopExecution("No values exist for READ statement")
        
        # If the assignment variable is an array location, grab it
        if ((varList[1])[0] == 'arr'):
            name = (varList[1])[1]
            memLocation = state.symbol_table.lookup_sym(name)
    
            index = walk((varList[1])[2]) # get the array index
            val = state.value_list.get()
            
            memLocation[index] = (val)# put the value in the memory space
        else:
            # get and assign the value
            varValue = state.value_list.get()
            name = (varList[1])[1]
            state.symbol_table.declare_sym(name,varValue)

        # grab next tuple
        varList = varList[2]

    # If a single variable exists
    if varList[0] == 'var':
        # Check if queue is empty
        if state.value_list.qsize() == 0:
            raise StopExecution("No values exist for READ statement")
        

        # Get and assign the value
        varValue = state.value_list.get()

        # If the assignment variable is an array location, grab it
        if ((varList[1])[0] == 'arr'):
            name = (varList[1])[1]
            memLocation = state.symbol_table.lookup_sym(name)
    
            index = walk((varList[1])[2]) # get the array index
            
            memLocation[index] = (varValue)# put the value in the memory space
        else:
            name = (varList[1])[1]
            state.symbol_table.declare_sym(name,varValue)
########################################################################EXPON_EXP
def expon_exp(node):
    # Exponential expression

    (EXPON,lhs,rhs) = node
    assert_match(EXPON,'^')

    # Deterine values of expression by walking associated nodes
    power = walk(rhs)
    base = walk(lhs)
    
    output = base # hold output

    # Factor output
    while (power-1):
        output *= base
        power -= 1

    return output
#########################################################################LE_EXP
def le_exp(node):
    # Logic Expression: Less then or Equal expression

    (LE,lhs,rhs) = node
    assert_match(LE,'<=')

    # Deterine values of expression by walking associated nodes
    left = walk(lhs)
    right = walk(rhs)

    # Factor output
    if(left <= right):
        return 1
    else:
        return 0
##########################################################################LT_EXP
def lt_exp(node):
    # Logic Expression: Less then expression

    (LT,lhs,rhs) = node
    assert_match(LT,'<')

    # Deterine values of expression by walking associated nodes
    left = walk(lhs)
    right = walk(rhs)

    # Factor output
    if (float(left) < float(right)):
        return 1
    else:
        return 0
#########################################################################GE_EXP
def ge_exp(node):
    # Logic Expression: Greater than or Equal expression

    (GE,lhs,rhs) = node
    assert_match(GE,'>=')

    # Deterine values of expression by walking associated nodes
    left = walk(lhs)
    right = walk(rhs)

    # Factor output
    if left >= right:
        return 1
    else:
        return 0
#########################################################################GT_EXP
def gt_exp(node):
    # Logic Expression: Greater than expression

    (GT,lhs,rhs) = node
    assert_match(GT,'>')

    # Deterine values of expression by walking associated nodes
    left=walk(lhs)
    right=walk(rhs)
    
    # Factor output
    if float(left) > float(right):
        return 1
    else:
        return 0
#########################################################################INEQ_EXP
def ineq_exp(node):
    # Logic Expression: Inequality expression

    (INEQ,lhs,rhs) = node
    assert_match(INEQ,'<>')

    # Deterine values of expression by walking associated nodes
    left = walk(lhs)
    right = walk(rhs)
    
    # Factor output
    if float(left) != float(right):
        return 1
    else:
        return 0
#########################################################################ON_STMT
def on_stmt(node):
    # Vintage Basic on statament

    (ON,exp,JUMPTYPE,labelList) = node
    assert_match(ON,'on')
    
    value = walk(exp)   # Get the value of the condition expression
    targets = []        # Holds list of target labels

    # Populate the list of targer labels from label list
    while labelList[0] == 'labelList':
        targets.append(labelList[1])
        labelList = labelList[2]
    # Grab the last label from the label list
    targets.append(labelList[1])

    # Evaluate which label we should jump to
    target = (targets[int(value-1)])

    # Jump
    walk((JUMPTYPE.lower(),target))
#########################################################################EQ_EXP  
def eq_exp(node):
    # Logic Expression: Exquality Expression

    (EQ,lhs,rhs) = node
    assert_match(EQ,'==')

    # Deterine values of expression by walking associated nodes
    left = walk(lhs)
    right = walk(rhs)

    # Determine and send appropriate output
    if left == right:
        return 1
    else:
        return 0
#########################################################################UMINUS_EXP
def uminus_exp(node):
    # Unary minus expression

    (UMINUS,exp) = node
    assert_match(UMINUS,'uminus')

    # Determing the value of the expression by walking the exp node
    value = walk(exp)

    # Return the value negated
    return (-1 * value)
#########################################################################GOSUB_STMT
def gosub_stmt(node):
    # Vintage Basic gosub expression

    (GOSUB,target) = node
    assert_match(GOSUB,'gosub')

    # Hold index we want to return to when gosub complete
    returnIndex = state.instr_ix + 1

    # Walk the target location instruction until a return statement node is encountered
    try:
        state.instr_ix = state.instr_labels.index(target)
        while state.instr_ix < len(state.instr_list):
            walk(state.instr_list[state.instr_ix])
            state.instr_ix += 1
            
    except ReturnStatement:

        #Return to statement following gosub statement
        state.instr_ix = returnIndex-1
        return
#########################################################################REST_STMT
def rest_stmt(node):
    #Vintage Basic restore statement
    # Restores values in the data statement queue to those of the
    # last data statement

    (REST,) = node
    assert_match(REST,'restore')
    
    # Copy values from backup queue into active queue
    for ctr in range(state.backup_value_list.qsize()):
        value = state.backup_value_list.get()
        state.backup_value_list.put(value)
        state.value_list.put(value)
#########################################################################NOT_STMT
def not_stmt(node):
    # Vintage Basic not statement

    (NOT,stmt) = node
    assert_match(NOT,'not')

    # Determine value of the expression by walking its node
    value = walk(stmt)

    # Return the logical negation of the expression
    if value == 0:
        return 1
    else:
        return 0
#########################################################################AND_STMT
def and_stmt(node):
    # Logical Expression: and statement

    (AND,lhs,rhs) = node
    assert_match(AND,'and')

    # Determine the values of the expression by walking their nodes
    left = walk(lhs)
    right = walk(rhs)

    # Return the logical output of the expression
    if (left == 0) or (right == 0):
        return 0
    else:
        return 1
#########################################################################OR_STMT 
def or_stmt(node):
    # Logical Expression: or statement
    
    (OR,lhs,rhs) = node
    assert_match(OR,'or')

    # Determine the values of the expression by walking their nodes
    left = walk(lhs)
    right = walk(rhs)

    # Factor and return the logical output of the expression
    if (left != 0) and (right != 0):
        return 1
    else:
        return 0
#########################################################################ABS_EXP
def abs_exp(node):
    global WALKABLE
    # Vintage basic prebuilt function
    # Returns absolute value of passed in expression

    (ABS,exp) = node
    assert_match(ABS,'abs')

    # If the expression is walkable, walk it to determine value
    if len(exp[0]) > 1 or exp[0] in WALKABLE:
        value = walk(exp)
    else:
        
        value = int(exp)

    # Return absolute value of passed in expression
    if value < 0:
        return (-1 * value)
    else:
        return value
#########################################################################ASC_EXP
def asc_exp(node):
    # Vintage basic prebuilt function
    # REturns ACSII value of the first character of the passed in string

    (ASC,string) = node
    assert_match(ASC,'asc')

    
    # if the input is walkable; walk it to determine value
    if len(string[0]) > 1:
        value = walk(string)
    else:
        value = string

    # Check to ensure input is string
    if isinstance(value, int):
        raise StopExecution("ASC input must be string")

    # Return ASCII value
    return ord(value[0])
#########################################################################ATN_EXP
def atn_exp(node):
    # Vintge basic prebuilt function
    # Returns the arctangent value of the passed in expression

    (ATN,exp) = node
    assert_match(ATN,'atn')

    # Determine value of the expression by walking its node
    value = walk(exp)

    return math.atan(value)
#########################################################################CHR_EXP
def chr_exp(node):
    # Vintage basic prebuilt function
    # returns a single character relating to the ascii value of the passed
    # in expression

    (CHR,exp) = node
    assert_match(CHR,'chr')

    # Determine the value of the expression by walking its node
    value = walk(exp)

    return chr(value)
#########################################################################COS_EXP
def cos_exp(node):
    # Vintage basic prebuilt function
    # Returns the cosine of the passed in expression

    (COS,exp) = node
    assert_match(COS,'cos')

    # Determine the value of the expression by walking its node
    value = walk(exp)

    return math.cos(value)
#########################################################################E_EXP
def e_exp(node):
    # Vintage basic prebuilt function
    # Returns the value of e raised to the power of the input expression

    (EEXP,exp) = node
    assert_match(EEXP,'eExp')

    # Determine the value of the expression by walking its node
    value = walk(exp)

    return math.pow(math.e,value)
#########################################################################INT_EXP
def int_exp(node):
    # Vintage basic prebuilt function
    # Returns the value of the input expression as an integer

    (INT,exp) = node
    assert_match(INT,'int')

    # Determine the value of the expression by walking its node
    value = walk(exp)

    return int(value)
#########################################################################LEFT_EXP
def left_exp(node):
    # Vintage basic prebuilt function
    # Returns a leftmost subsection of the passed in string

    (LEFT,exp,num) = node
    assert_match(LEFT,'left')

    #If the node is walkable, Determine the value of the expression by
    # walking its node
    if len(exp[0]) > 1:
        value = walk(exp)
    else:
        value = exp

    # If the subsection is the whole string, return it
    # Else return the subsection
    if len(value) <= int(num):
        return value
    else:
        return value[ int(num) :len(value) ]
#########################################################################LEN_EXP
def len_exp(node):
    # Vintage basic prebuilt function
    # Returns the length of the passed in string

    (LEN,exp) = node
    assert_match(LEN,'len')

    #If the node is walkable, Determine the value of the expression by
    # walking its node
    if len(exp[0]) > 1:
        value = walk(exp)
    else:
        value = exp

    return len(value)
#########################################################################LOG_EXP
def log_exp(node):
    # Vintage basic prebuilt function
    # Returns the logarithm, to base e, of the passed in expression

    (LOG,exp) = node
    assert_match(LOG,'log')

    # Determine the value of the expression by walking its node
    value = walk(exp)

    try:
        return math.log(value)
    except TypeError:
        raise StopExecution("LOG function input cannot be a string")
#########################################################################MID_EXP
def mid_exp(node):
    # Vintage basic prebuilt function
    # Returns a subsection of a string
    # With a single argument, a leftmost substring is returned
    # With 2 arguments, returns a substring with the left and right sides
    # cut off at the passed in expression values

    
    # try the form with 2 arguments
    # expect form with 1 argument
    try:
        (MID,string,left,right) = node
        assert_match(MID,'mid')
        
        # If the input string is a variable, walk it to get the value
        if len(string[0]) > 1:
            value = walk(string)
        else:
            value = string

        # Determine the values of the expressions by walking the nodes
        left = walk(left)
        right = walk(right)

        # Return substring
        return value[int(left):len(value) - int(right)]

    except:
        (MID,string,left) = node
        assert_match(MID,'mid')

        # If the input string is a variable, walk it to get the value
        if len(string[0]) > 1:
            value = walk(string)
        else:
            value = string

        # Determine the value of the expression by walking its node
        left = walk(left)

        # Return substring
        return value[0:int(left)]
#########################################################################RIGHT_EXP
def right_exp(node):
    # Vintage basic prebuilt function
    # Returns the right-most substring of the passed in string

    (RIGHT,string,exp) = node
    assert_match(RIGHT,'right')

    # If the number passed in is an expression, evaluate it to get the
    # value
    if not (isinstance(exp[0],int)):
        exp = walk(exp)

    # If the input is a variable, walk it to get the string
    # Else just grab the string
    if len(string[0]) > 1:
        value = walk(string)
    else:
        value = string

    # Return substring
    return value[0:len(value)-int(exp)]
#########################################################################RND_EXP
def rnd_exp(node):
    global lastRandom
    # Vintage basic prebuilt function
    # Random number function

    (RND,exp) = node
    assert_match(RND,'rnd')

    # Determine the value of the expression by walking its node
    exp = walk(exp)

    # Vintage basic random function has 3 different inputs
    # If the input is < 0: reseed the number generator
    # If the input is > 0: return a random number
    # If the input is = 0: return last random number
    if exp < 0:
        exp = -1 * int(exp)
        seed(exp)
    elif exp > 0:
        value = random()
        lastRandom = value
        return value
    else:
        return lastRandom
#########################################################################SGN_EXP
def sgn_exp(node):
    # Vintage basic prebuilt function
    # REturns the sign +/- of the passed in expression

    (SGN,exp) = node
    assert_match(SGN,'sgn')

    # Determine the value of the expression by walking its node
    exp = walk(exp)

    # Factor and return output
    if exp < 0:
        return -1
    elif exp > 0:
        return 1
    else:
        return 0
#########################################################################SIN_EXP
def sin_exp(node):
    # Vintage basic prebuilt function
    # Returns the sine of the passed in expression

    (SIN,exp) = node
    assert_match(SIN,'sin')

    # Determine the value of the expression by walking its node
    exp = walk(exp)

    return math.sin(exp)
#########################################################################SPC_EXP
def spc_exp(node):
    # Vintage basic prebuilt function
    # Returns a string with a number blank spaces consistant with the numerical
    # value of the passed in expression

    (SPC,exp) = node
    assert_match(SPC,'spc')

    # Determine the value of the expression by walking its node
    exp = walk(exp)

    # Check is expression is < 0
    if (exp < 0):
        raise StopExecution("SPC input must be a positive number")
    
    output = "" # output stored here

    # Otuput constructed
    for ctr in range(exp):
        output += " "

    # Output returned
    return output
#########################################################################SQR_EXP
def sqr_exp(node):
    # Vintage basic prebuilt function
    # Returns the square root of the passed in function

    (SQR,exp) = node
    assert_match(SQR,'sqr')

    # Determine the value of the expression by walking its node
    exp = walk(exp)

    return math.sqrt(exp)
#########################################################################STR_EXP
def str_exp(node):
    # Vintage basic prebuilt function
    # Returns the output of the passed in expression as a string

    (STR,exp) = node
    assert_match(STR,'str')

    # Determine the value of the expression by walking its node
    exp = walk(exp)

    return str(exp)
#########################################################################TAN_EXP
def tan_exp(node):
    # Vintage basic prebuilt function
    # Returns the tangent of the passed in expression

    (TAN,exp) = node
    assert_match(TAN,'tan')

    # Determine the value of the expression by walking its node
    exp = walk(exp)

    return math.tan(exp)
#########################################################################VAL_EXP
def val_exp(node):
    # Vintage basic prebuilt function
    # Returns the value of a string as a floating point number

    (VAL,exp) = node
    assert_match(VAL,'val')

    # If the expression is an ID, walk it to get the value
    if exp[0] == 'id':
        exp = walk(exp)

    # Check that input is a string
    if isinstance(exp,int) or isinstance(exp,float):
        raise StopExecution("VAL function input must be of type string")

    return float(exp)
#########################################################################RETURN_STMT
def return_stmt(node):
    # Return statement
    # returns

    (RETURN,) = node
    assert_match(RETURN,'return')

    raise ReturnStatement
        
#########################################################################
# walk
#########################################################################
def walk(node):
    node_type = node[0]
    
    if node_type in dispatch_dict:
        node_function = dispatch_dict[node_type]
        return node_function(node)
    
    else:
        raise ValueError("walk: unknown tree node type: " + node_type)

dispatch_dict = {
    'seq'     : seq,
    'line'    : line,
    'print'   : print_stmt,
    'let'     : let_stmt,
    'integer' : integer_exp,
    'real'    : real_exp,
    'id'      : id_exp,
    'goto'    : goto_stmt,
    'gosub'   : gosub_stmt,
    '+'       : add_exp,
    '-'       : sub_exp,
    '/'       : div_exp,
    '*'       : mul_exp,
    '^'       : expon_exp,
    '<='      : le_exp,
    '<'       : lt_exp,
    '>='      : ge_exp,
    '>'       : gt_exp,
    '<>'      : ineq_exp,
    '=='      : eq_exp,
    'uminus'  : uminus_exp,
    'if'      : if_stmt,
    'for'     : for_stmt,
    'fundecl' : func_decl_stmt,
    'callexp' : call_exp,
    'input'   : input_stmt,
    'data'    : data_stmt,
    'read'    : read_stmt,
    'dim'     : dim_stmt,
    'rem'     : rem_stmt,
    'on'      : on_stmt,
    'return'  : return_stmt,
    'restore' : rest_stmt,
    'not'     : not_stmt,
    'and'     : and_stmt,
    'or'      : or_stmt,
    'abs'     : abs_exp,
    'asc'     : asc_exp,
    'atn'     : atn_exp,
    'chr'     : chr_exp,
    'cos'     : cos_exp,
    'eExp'    : e_exp,
    'int'     : int_exp,
    'left'    : left_exp,
    'len'     : len_exp,
    'log'     : log_exp,
    'mid'     : mid_exp,
    'right'   : right_exp,
    'rnd'     : rnd_exp,
    'sgn'     : sgn_exp,
    'sin'     : sin_exp,
    'spc'     : spc_exp,
    'sqr'     : sqr_exp,
    'str'     : str_exp,
    'tan'     : tan_exp,
    'val'     : val_exp,
    'end'     : end_stmt,
    'arr'     : arr_exp

}
# StopExecution exception used to handle end and stop statements
# allows us to immediatly recurse up the tree
class StopExecution(Exception):
    def _render_traceback_(self):
        pass
# ReturnStatement exception used to handle return statements attached to GOSUB statements
class ReturnStatement(Exception):
    def _render_traceback_(self):
        pass
