# Timothy Colaneri
# CSC 402 Project/ Fall 2019
# Vintage Basic state object

import queue                           #Queue used to hold data for DATA/READ
from VintageBASIC_symtab import SymTab #Scoable symbol table

class State:
    
    def __init__(self):
        self.initialize()

    def initialize(self):
        # symbol table to hold variable-value associations
        self.symbol_table = SymTab()

        
        
        # List used to hold input program
        self.instr_list = []   # List hold tuples of each lines instructions
                               # List parallel to instr_labels
        self.instr_labels = [] # List holds labels for each line in program
                               # List parallel to instr_list

        # Queues used to hold data for DATA/READ statements
        self.value_list = queue.Queue()         #Holds data input by READ statement
        self.backup_value_list = queue.Queue()  #Holds data backup for RESTORE statement
        self.instr_index = 0                    #Holds current line Index in program list


        # when done parsing this variable will hold our AST
        self.AST = None # Hold on to this because it may become useful

state = State()



