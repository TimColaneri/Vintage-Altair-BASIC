# Timothy Colaneri
# CSC402 Project
# Symbol table for Vintage basic
# Heavily modeled off of Cuppa 3 SymTab

CURR_SCOPE = 0

class SymTab:

    ##########################################################
    def __init__(self):
        
        self.scoped_symtab = [{}] # Global symbol table must be present
    ##########################################################
    def get_config(self):
        # Returns a copy of the symbol table in list format
        
        return list(self.scoped_symtab)
    ###########################################################
    def set_config(self, c):

        # Sets the current symbol table to the one passed into this
        # function
        self.scoped_symtab = c
    ##########################################################
    def push_scope(self):
        
        # pushes a new scope onto the scope stack
        self.scoped_symtab.insert(CURR_SCOPE,{})

    ##########################################################
    def pop_scope(self):
        
        # pops the current symbol table off the top
        # If its the global table, an error is raised
        if len(self.scoped_symtab) == 1:
            raise ValueError("cannot pop the global scope")
        else:
            self.scoped_symtab.pop(CURR_SCOPE)

    #-------
    def declare_sym(self, sym, init):
        # declare the scalar in the current scope: dict @ position 0
        
        # first we need to check whether the symbol was already declared
        # at this scope
        '''
        if sym in self.scoped_symtab[CURR_SCOPE]:
            raise ValueError("symbol {} already declared".format(sym))
            '''
        
        # enter the symbol in the current scope
        scope_dict = self.scoped_symtab[CURR_SCOPE]
        scope_dict[sym] = ( init)

    #-------
    def declare_fun(self, sym, init):
        # declare a function in the current scope: dict @ position 0
        
        # first we need to check whether the symbol was already declared
        # at this scope
        if sym in self.scoped_symtab[CURR_SCOPE]:
            raise ValueError("symbol {} already declared".format(sym))
        
        # enter the function in the current scope
        scope_dict = self.scoped_symtab[CURR_SCOPE]
        scope_dict[sym] = ('function', init)

    def declare_array(self, sym, array_type):
        '''
        declare an array in the current scope.
        '''
        # first we need to check whether the symbol was already declared
        # at this scope
        if sym in self.scoped_symtab[CURR_SCOPE]:
            raise ValueError("symbol {} already declared".format(sym))

        # unpack the array type
        size = array_type
        size = int(size[1])

        # declare symbol in current scope
        val = [0]
        while size:
            val.append(0)
            size -= 1
        self.scoped_symtab[CURR_SCOPE].update({sym:val})

    #-------
    def lookup_sym(self, sym):
        # find the first occurence of sym in the symtab stack
        # and return the associated value

        n_scopes = len(self.scoped_symtab)
        

        for scope in range(n_scopes):
            #print(self.scoped_symtab[scope])
            if sym in self.scoped_symtab[scope]:
                val = self.scoped_symtab[scope].get(sym)
                return val

        # not found
        raise ValueError("{} was not declared".format(sym))

    #-------
    def update_sym(self, sym, val):
        # find the first occurence of sym in the symtab stack
        # and update the associated value

        n_scopes = len(self.scoped_symtab)

        for scope in range(n_scopes):
            if sym in self.scoped_symtab[scope]:
                scope_dict = self.scoped_symtab[scope]
                scope_dict[sym] = val
                return

        # not found
        raise ValueError("{} was not declared".format(sym))
