def save_variables(cnf):
    '''
    Saves the variables of the CNF expression, without the negation if there is one. Each variable is only added once.
    Output: 'variables' array
    '''
    variables=[]
    for clause in cnf:
        for c in clause:
            if c[0] == "¬":
                if c[1:] not in variables: #The index is used to not include negation symbol
                    variables.append(c[1:])
            else:
                if c not in variables:
                    variables.append(c)
    return variables


def simplify_clauses(cnf):
    '''
    Creates a 'clauses' array (duplicate clauses are ommited). x∨x or x∨¬x instances are simplified. 
    Output: 'clauses' array
    '''
    clauses = []
    for clause in cnf:    
        if clause not in clauses:    #For each clause that is not already in the "clauses" array
            i=0
            remove_flag = 0 #Flag for when clause is always satisfied
            while(i<len(clause) and not remove_flag):
                c = clause[i]
                #Search for x∨¬x instances
                #When variable 'c' is the negation of another, 
                #remove the clause (always satisfied)
                if "¬" in c:
                    temp_c = c[1:]
                    if clause.count(temp_c):
                        remove_flag = 1
                        break
                else:
                    temp_c = c
                    if clause.count("¬" + c):
                        remove_flag = 1
                        break
                        
                #Search for x∨x∨x instances
                if clause.count(c) == 3:
                    clause = [c]
                    
                #Search for x∨x instances
                elif clause.count(c) == 2:
                    j=i+1
                    while(j<len(clause)):
                        c2 = clause[j]
                        if c == c2: #When variable 'c' is duplicate in this clause, remove the one (c + c = c)
                            clause.pop(clause.index(c2))
                        j+=1
                i+=1

            #Save the clause after editing
            if len(clause)>0 and not remove_flag:
                clauses.append(clause)
    return clauses

def array_from_cnf(cnf):
    '''
    Creates two arrays from a cnf expression, named variables and clauses 
    e.g. Input: (x∨y∨z)∧(¬x∨¬y∨z)∧(x∨¬y∨¬z) 
         Output: variables = ['x', 'y', 'z'], clauses = ['x∨y∨z', '¬x∨¬y∨z', 'x∨¬y∨¬z']
    '''
    cnf = cnf.replace("+","∨")
    cnf = cnf.replace("~","¬")

    cnf = cnf.split("∧")
    if (len(cnf)==0):
        print("Not acceptable input")
    
    #Remove the outer '(',')' and split clauses on "∨" characters
    cnf_array = []
    for clause in cnf:
        clause = clause.replace('(', '')
        clause = clause.replace(')', '')
        cnf_array.append(clause.split("∨"))
    
    #Create arrays for variables and clauses
    variables = save_variables(cnf_array)
    clauses = simplify_clauses(cnf_array)                
    
    if (len(variables)==0):
        print("Not acceptable input")
    return variables, clauses