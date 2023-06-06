def find_high_values(counts, avg):
    '''
    Finds high-value elements in the histogram counts based on the given average.

    Args:
        counts (dict): Histogram counts representing the measurement results.
        avg (float): Average frequency (the counts that would be found per basic state if all of them were equal)

    Returns:
        high_values (list): List of high-value elements (more frequent than average).

    '''
    high_values = []
    for value in counts:
        if counts[value]/sum(counts.values()) > avg:
            high_values.append(value)
    return high_values

def verify(dict, clauses):
    '''
    Verifies if a dictionary of variable assignments satisfies the given clauses in a 3-SAT problem.

    Args:
        dict (dict): Dictionary of variable assignments.
        clauses (list): List of clauses in the 3-SAT problem.

    Returns:
        bool: True if the variable assignments satisfy all clauses, False otherwise.

    '''
    for clause in clauses:
        or_input = []
        for c in clause:
            if "¬" in c:
                val = bool(int(dict[c[1:]]))
                or_input.append(not val)
            else:
                val = bool(int(dict[c]))
                or_input.append(val)
        flag = 0
        for i in or_input:
            if i:
                flag = 1
        if not flag:
            return False
    return True
   
def read_data(counts, clauses, variables):    
    '''
    Analyzes the histogram counts of a quantum job and checks satisfiability of a 3-SAT problem.

    Args:
        counts (dict): Histogram counts representing the measurement results.
        clauses (list): List of clauses in the 3-SAT problem.
        variables (list): List of variables in the 3-SAT problem.

    Returns:
        high_values (list): List of the combinations of variables that were enhanced by Grover and therefore are satisfying the 3-SAT 
        problem. Returns empty list if there are no solutions or all states if the 3-SAT problem is always satisfiable.

    '''
    sample_space_size = 2**(len(variables))
    avg = 1/sample_space_size
    equal_flag = 0
    
    if max(counts.values()) - min(counts.values()) < sum(counts.values())/sample_space_size and len(counts.values()) == sample_space_size:
        equal_flag = 1
        print ("All values in histogram are about equal")

    high_values = find_high_values(counts, avg)
    if equal_flag:
        value_per_var = {}
        for i in range(0,len(high_values[0])):
            value_per_var[variables[i]] = high_values[0][i]
        if not verify(value_per_var, clauses):
            print("***This 3-SAT input is not satisfiable.***")
            print("***Satiability: False***")
            return []
        else: 
            print("***This 3-SAT input is always satisfiable.***")
            print("***Satiability: True***")
            return counts.keys()
    else:
        print("Frequent values in histogram:", high_values)

        flag = 0
        for value in high_values:
            value_per_var = {}
            for i in range(0,len(value)):
                value_per_var[variables[i]] = value[i]
            if not (verify(value_per_var, clauses)):
                flag = value
                break
        if flag:
            print("One of the frequent values is not an acceptable solution.")
            print("The value is:", value)

        else:
            print("***This 3-SAT input is satisfiable.***")
            print("***Satiability: True***")
            print("Values that satisfy it are:", variables, "=", high_values)
    return high_values