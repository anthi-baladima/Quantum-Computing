def neg(sign):
    if sign:
        neg = ""
    else:
        neg = "¬"
    return neg

def graph_to_3sat(graph, n_colors):
    """
    Translates a graph coloring problem into 3SAT.
    The input graph is represented as a dictionary where the keys are the nodes and the values are the list of nodes
    that are connected to the key node by an edge.
    """
    n_nodes = len(graph)
    clauses = []
    
    # Each node needs at least one color
    for node in graph:
        clause = []
        for color in range(1, n_colors+1):
            clause.append(f"{node}_{color}")
        clauses.append(clause)

    # No node can have more than one color
    for node in graph:
        for color1 in range(1, n_colors+1):
            for color2 in range(color1+1, n_colors+1):
                clause = [f"¬{node}_{color1}", f"¬{node}_{color2}"]
                clauses.append(clause)
    
    # Nodes connected by an edge cannot have the same color
    for node1 in graph:
        for node2 in graph[node1]:
            for color in range(1, n_colors+1):
                clause = [f"¬{node1}_{color}", f"¬{node2}_{color}"]
                clauses.append(clause)
    
    # Convert each clause to a 3SAT clause
    sat_clauses = []
    for clause in clauses:
        clause_vars = []
        for var in clause:
            clause_vars.append(var)
            
        if len(clause_vars) <= 3:
            # Pad with false variables to make it a 3SAT clause
            for i in range(3-len(clause_vars)):
                clause_vars += [clause_vars[0]]
            sat_clauses.append(clause_vars)
        else:
            # Split into multiple 3SAT clauses
            sign = 1
            sat_clauses.append(clause_vars[0:2] + [neg(sign) + "anc" + str(clauses.index(clause)) + str(0)])
            i=0
            while i+4<len(clause_vars):
                sat_clauses.append([neg(1-sign) + "anc" + str(clauses.index(clause)) + str(i), clause_vars[i+2], neg(sign) + "anc" + str(clauses.index(clause)) + str(i+1)])
                i+=1
            sat_clauses.append([neg(1-sign) + "anc" + str(clauses.index(clause)) + str(i), clause_vars[-2], clause_vars[-1]])
    print("3-SAT of %d clauses" %len(sat_clauses))
        
    return sat_clauses
