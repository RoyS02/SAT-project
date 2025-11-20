from typing import Tuple
from typing import Set, List

def simplify(clauses: List[Set[int]]) -> Tuple[List[Set[int]], Set[int]]:
    # CNF moet gesolved worden:
    truth_list = set()
    # Step 1: simplify
    terminate = 0

    while not terminate: # Terminate when clauses is simplified
        taut_tot = 0
        pure_tot = 0
        unit_tot = 0

        clauses = [set(clause) for clause in clauses]
        # maybe a clauses copy?
        for clause in clauses[:]:

            # We are deleting from the clauses list so skipp a clause that has already been delete
            if not clause in clauses: continue

            # Tautology check
            taut = delete_tautologies(clause)
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


def delete_tautologies(clause: Set[int]) -> int:
    taut_count = 0
    for literal in clause:
        opposite_literal = literal * -1
        if opposite_literal in clause:
            taut_count += 1
            return taut_count
    return taut_count
