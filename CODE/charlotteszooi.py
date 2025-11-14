# Hallo wereld
import math
from typing import Tuple
from encoder import to_cnf

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

def delete_tautologies(clause: list[int], clauses: list[list[int]]) -> int:
    taut_count = 0
    for literal in clause:
        opposite_literal = literal * -1
        if opposite_literal in clause:
            # delete clause from clause list
            #clauses.remove(clause)
            taut_count += 1
            return taut_count
    return taut_count

def pure_literal(clause: list[int], clauses: list[list[int]]) -> Tuple[list[list[int]], list[int]]:
    # Nog veel werk aan de winkel
    truth_list = []

    for literal in clause:
        pure = True
        neg_lit = literal * -1
        # Check if only negative or positive in other clauses
        for loop_clause in clauses:
            # Finding prove of literal not being pure
            if neg_lit in loop_clause:
                pure = False
                break

        # Take literal out of all clauses if it is pure
        if pure:
            print(f"literal {literal} is seen as pure")
            if not literal in truth_list:
                truth_list.append(literal)
            for loop_clause in clauses[:]:
                if literal in loop_clause:
                    clauses.remove(loop_clause)
            break

    return clauses, truth_list



def unit_clause(clause: list[int], clauses: list[list[int]]) -> Tuple[list[list[int]], int, int]:
    """
    :param clause:
    :param clauses:
    :return:
    clauses
    truth: the number that is now deemed true -> 0 if none
    unit: if there was a unit -> might be redundend
    """

    if len(clause) == 1 and not clause[0] == 0:
        truth = clause[0]
        #clauses.remove(clause)
        """
        for clause_loop in clauses[:]:
            opposite = truth * -1
            if truth in clause_loop:
                clauses.remove(clause_loop)
            elif opposite in clause_loop:
                clause_loop.remove(opposite)        
        """
        new_clauses = []
        opposite = -truth

        for clause in clauses:
            if truth in clause:
                continue  # deze clause is voldaan, dus overslaan
            if opposite in clause:
                clause = [lit for lit in clause if lit != opposite]
            new_clauses.append(clause)

        clauses = new_clauses

        # Take clause out of all clauses
        """for clause_loop in clauses:
            if truth in clause_loop:
                clause_loop.remove(truth)
            elif truth * -1 in clause_loop:
                clause_loop.remove(truth * -1)
        """
        unit = 1
    else:
        unit = 0
        truth = 0
    return clauses, truth, unit



def simplify(clauses: list[list[int]]) -> list[list[int]]:
    # CNF moet gesolved worden:
    truth_list = list()
    # Step 1: simplify
    terminate = 0

    while not terminate: # Terminate when clauses is simplified
        taut_tot = 0
        pure_tot = 0
        unit_tot = 0

        # maybe a clauses copy?
        for clause in clauses[:]:

            # We are deleting from the clauses list so skipp a clause that has already been delete
            if not clause in clauses: continue

            # Tautology check
            taut = delete_tautologies(clause, clauses)
            taut_tot += taut
            if taut == 1:
                clauses.remove(clause)
                continue # skipp this clause if we have already determined it a tautology

            # Unit clause check
            clauses, truth, unit = unit_clause(clause, clauses)
            unit_tot += unit
            if not truth == 0: # Unit literal was found
                if not truth in truth_list:
                    truth_list.append(truth)
                    continue # Only pure literal check needed if no unit literal was found -> no double work

            # Pure Literal check
            clauses, truth = pure_literal(clause, clauses)
            pure_tot += len(truth)
            if not truth == list():
                for truth_item in truth:
                    if truth_item not in truth_list:
                        truth_list.append(truth_item)

        # Check if all are taken out of clauses
        print(f"taut_tot: {taut_tot}, pure_tot: {pure_tot}, unit_tot: {unit_tot}")
        print(f"truth_list: {truth_list} ")
        print(f"and clauses: {clauses}")

        if taut_tot == 0 and pure_tot == 0 and unit_tot == 0: # ... because then nothing more to simplify
            terminate = 1


    return clauses, truth_list


if __name__== "__main__":
    clauses, n = to_cnf("example_n9.txt")
    #print(clauses)
    # test 1
    #clauses = [[9, 3],[9],[4,2],[-9,4],[5,7],[1,-1],[1,3],[-2,-7],[-7,-5]] # Truth list is 9,4,3,5

    #print(n)
    print(f"lenght of clauses: {len(clauses)}")
    for clause in clauses: print(clause)
    print("hello?")
    clauses, truth_list = simplify(clauses)

    print("hey")
    for clause in clauses:
        if clause > 0: print(f"clause: {clause}")
    #print(f"truth_list: {truth_list}")

    check = 1
    # check if negative and positive in
    for item in truth_list:
        opposite = item * -1
        if opposite in truth_list:
            print("there is a contradiction in the truthlist")
            check = 0
            break

    if check == 1:
        print("Truth_list has no contradictions")

    sudoku_values = list()
    for item in truth_list:
        if item > 0:
            sudoku_values.append(item)
    print(f"sudoku_values: {sudoku_values}")
    print(f"the length of sudoku_values is: {len(sudoku_values)}")


