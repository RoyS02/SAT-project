# Hallo wereld
import math
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
    clauses = list()
    for r in range(N):
        for c in range(N):
            # Check first for only cell 0,0
            for v1 in range(1, N):
                for v2 in range(v1 + 1, N + 1):
                    clause_single = [varnumber(r,c,v1,N) * -1, varnumber(r,c,v2,N) * -1]
                    clauses.append(clause_single)
    return clauses

def exactly_one_v_per_cel(N):
    # Both at most one AND at least one are true
    clauses = at_least_one(N)
    clauses.extend(at_most_one(N))
    return clauses

def row_constraint(N):
    # Works
    clauses = list()
    for r in range(N):
        for v in range(1, N + 1):
            for c1 in range(N - 1):
                for c2 in range(c1 + 1, N):
                    clause_single = [varnumber(r,c1,v,N) * -1,
                                     varnumber(r,c2,v,N) * -1]
                    clauses.append(clause_single)

    return clauses



def box_constraint(N):
    B = int(math.sqrt(N))
    clauses = list()
    # Loop over boxes
    for b_r in range(B):
        for b_c in range(B):
           #clauses.extend(inside_box(N,B,b_r,b_c))
           for v in range(1, N + 1):
               # Loop over exact coordinates
               for r_1 in range(b_r * B, (b_r + 1) * B):
                   for c_1 in range(b_c * B, (b_c + 1) * B):
                       # For each coordinate loop for a second coordinate we can compare to
                       for r_2 in range(b_r * B, (b_r + 1) * B):
                           for c_2 in range(b_c * B, (b_c + 1) * B):
                               # We will save the literal if c_2 is bigger than c_1
                               # or r_2 is bigger than r_1
                               var_1, var_2 = varnumber(r_1,c_1,v,N), varnumber(r_2,c_2,v,N)
                               if var_1 < var_2:
                                   clause = [var_1 * -1,
                                             var_2 * -1]
                                   clauses.append(clause)

    return clauses





if __name__== "__main__":
    #print(exactly_one_v_per_cel(9))
    #print(exactly_one_v_per_cel(9))
    print(range(1,25))
    for i in range(1,25): print(i)
    #clauses = exactly_one_v_per_cel(4)

    #clauses = (row_constraint(4))
    clauses = box_constraint(4)
    for i in clauses:
        print(i)