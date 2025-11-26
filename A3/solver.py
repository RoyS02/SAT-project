from typing import List, Tuple, Optional, Iterable
from collections import defaultdict, deque
DPLL_CALLS = 0
MAX_DPLL_CALLS = 100_000 

def pure_literal(clauses: List[List[int]]) -> Tuple[List[List[int]], List[int]]:
    """
    As a pre-processing step, find all pure literals and assign them true.
    """
    assignment: List[int] = []
    changed = True

    # Changed flag to keep track of whether any pure literals were found
    while changed:
        changed = False

        # loop to count literals
        literal_count = defaultdict(int)
        for clause in clauses:
            for literal in clause:
                literal_count[literal] += 1

        # find pure literals
        pure_literal = [literal for literal in literal_count
                        if literal_count[literal] > 0 
                        and literal_count.get(-literal, 0) == 0]

        if not pure_literal:
            break

        changed = True

        # Set of pure literals for quick lookup
        pure_set = set(pure_literal)
        assignment.extend(pure_literal)

        new_clauses: List[List[int]] = []

        # Check for clauses satisfied by pure literals
        for c in clauses:
            if any(l in pure_set for l in c):
                continue
            new_clauses.append(c)
        clauses = new_clauses
    return clauses, assignment


def simplify(clauses: List[List[int]]) -> Tuple[List[List[int]], List[int]]:
    """
    Simplify clauses by using unit propagation.
    """
    implied: List[int] = []
    implied_set = set()

    # collect all initial unit clauses
    unit_clauses = deque(literal for clause in clauses
                        if len(clause) == 1
                        for literal in clause)

    while unit_clauses and clauses:
        literal = unit_clauses.popleft()

        # Check for conflicts
        if -literal in implied_set:
            return ([[]], implied)
        if literal in implied_set:
            continue

        implied_set.add(literal)
        implied.append(literal)

        new_clauses: List[List[int]] = []

        for clause in clauses:
            # clause already satisfied
            if literal in clause:
                continue
            # clause contains the negation of the literal
            if -literal in clause:
                reduced = [x for x in clause if x != -literal]
                # Catch empty clause
                if not reduced:
                    return ([[]], implied)
                # Append new unit clause to queue
                if len(reduced) == 1:
                    unit_clauses.append(reduced[0])
                new_clauses.append(reduced)
            else:
                # clause unaffected
                new_clauses.append(clause)
        clauses = new_clauses
    return clauses, implied


def DLIS_heuristic(clauses: List[List[int]]) -> int:
    """
    Find the literal that appears most frequently in the clauses.
    """
    counts = defaultdict(int)

    # Loop through all clauses and count literal occurrences
    for clause in clauses:
        for literal in clause:
            counts[literal] += 1
    
    return max(counts, key=counts.get)


def DPLL(clauses: List[List[int]], num_vars: int, assignment: Optional[List[int]] = None
         )-> Tuple[bool, List[int]]:
    """
    DPLL algorithm with unit propagation and DLIS heuristic.
    """
    global DPLL_CALLS, MAX_DPLL_CALLS

    if DPLL_CALLS >= MAX_DPLL_CALLS:
        return False, []

    DPLL_CALLS += 1
    print("number of dpll calls: ", DPLL_CALLS)
    # Check if assignment is empty, if so, initialize it
    if assignment is None:
        assignment = []

    # Run simplification (unit propagation)
    clauses, implied_truth = simplify(clauses)

    # Make copy of assignment for branching
    full_assignment = assignment.copy()
    assigned = set(full_assignment)

    # Check for conflicts in implied literals, and add to assignment
    for literal in implied_truth:
        if -literal in assigned:
            return False, []
        if literal not in assigned:
            assigned.add(literal)
            full_assignment.append(literal)

    # If there is an empty clause, return UNSAT
    if any(len(c) == 0 for c in clauses):
        return False, []

    # If all clauses are empty, return SAT
    if not clauses:
        return True, full_assignment

    # use DLIS heuristic to choose which literal to split on
    split_literal = DLIS_heuristic(clauses)

    # Try literal as True
    sat, model = DPLL(clauses + [[split_literal]], num_vars, full_assignment + [split_literal])

    # If satisfied, return true and model
    if sat:
        return True, model

    # Try literal as False
    return DPLL(clauses + [[-split_literal]], num_vars, full_assignment + [-split_literal])


def solve_cnf(clauses: Iterable[Iterable[int]], num_vars: int) -> Tuple[str, List[int]]:
    """
    Solve the CNF sudoku by DPLL algorithm with pure literal preprocessing.
    """
    clause_list: List[List[int]] = [list(c) for c in clauses]

    # Preprocessing: pure literal elimination
    clause_list, pre_assign = pure_literal(clause_list)

    # DPLL_CALLS variable to check how many calls were made
    global DPLL_CALLS
    DPLL_CALLS = 0

    # Run DPLL
    sat, model = DPLL(clause_list, num_vars, pre_assign)
    
    if sat:
        solution = "SAT"
    else:
        solution = "UNSAT"

    return solution, model