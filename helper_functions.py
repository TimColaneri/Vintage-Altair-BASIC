# Vintage BASIC interpreter helper functions
# Timothy Colaneri
# CSC402 / Fall 2019

import math

#asserts that two inputs are a match
##################################################################
def assert_match(input, expected):
    if input != expected:
        raise ValueError("Pattern match failed: expected {} but got {}".format(expected, input))
##################################################################
def partition(array,auxArray,lIndex,rIndex):
    # Quicksort partition
    # this quicksort partition handles two parallel arrays
    # using the first one to sort by
    
    index = ( lIndex - 1 )   
    pivot = array[rIndex]    
  
    for ctr in range(lIndex , rIndex):
  
        if   int(array[ctr]) <= int(pivot): 

            index = index + 1 
            array[index],array[ctr] = array[ctr],array[index]
            auxArray[index],auxArray[ctr] = auxArray[ctr],auxArray[index]
  
    array[index+1],array[rIndex] = array[rIndex],array[index+1]
    auxArray[index+1],auxArray[rIndex] = auxArray[rIndex],auxArray[index+1]
    return ( index+1 ) 
  
################################################################## 
def quicksort(array,auxArray,lIndex,rIndex):
    # Quicksort
    # this quicksort handles two parallel arrays
    # using the first one to sort by
    
    if lIndex < rIndex: 
  
        split = partition(array,auxArray,lIndex,rIndex) 
  
        quicksort(array,auxArray, lIndex, split - 1) 
        quicksort(array,auxArray, split +1, rIndex)
###################################################################
def splitProg(prog):
    # Split prog used by interpreter to split program into 2 lists:
    # 1 - labels
    # 2 - code
    # Quicksort then used to sort the two lists into execution order
    
    labels = []
    stmts = []
    label = ''
    code = ''
    foundLabel = False

    # For each line in the program
    for line in prog.split('\n'):

        # For each character in the line
        for char in line:

            # The first time we encounter a space, we are done taking
            # in the label
            if char == ' ':
                foundLabel = True
                
            if foundLabel:
                code+=char
            else:
                label += char

        # Add the label and code to the lists
        labels.append(label)
        stmts.append(code)
        code = ''
        label = ''
        foundLabel = False
    
    labels = labels[1:len(labels)-1]
    stmts = stmts[1:len(stmts)-1]

    # Sort
    quicksort(labels,stmts,0,len(labels)-1)
    
    output = ''
    ctr = 0
    
    # Assemble back together for the parser
    for entry in labels:
        output += labels[ctr]+stmts[ctr]+'\n'
        ctr += 1
        
        
    #print(output)
    
    return output
        
        
#######################TEST   


