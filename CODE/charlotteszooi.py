# Hallo wereld

def varnumber(r, c, v, N) -> int:
    return N * N * r + N * c + v

def at_least_one(N):
    # Works
    clauses = list()
    clause = list()

    for r in range(N):
        for c in range(N):
            for v in range(1, N + 1):
                literal = varnumber(r, c, v, N)
                clause.append(literal)
            clauses.append(clause)
            clause = list()
    return clauses

def at_most_one(N):
    pass
    # Return is dnf

def exactly_one_v_per_cel(N):
    # Both at most one AND at least one are true
    clauses = at_least_one(N)
    return clauses

if __name__== "__main__":
    for i in range(1, 25 + 1): print(i)
    #print(exactly_one_v_per_cel(9))
    #print(exactly_one_v_per_cel(9))
    clauses = exactly_one_v_per_cel(9)
    for i in clauses:
        print(i)