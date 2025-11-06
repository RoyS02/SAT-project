"""
SAT Assignment Part 1 - Non-consecutive Sudoku Encoder (Puzzle -> CNF)

THIS is the file to edit.

Implement: to_cnf(input_path) -> (clauses, num_vars)

You're required to use a variable mapping as follows:
    var(r,c,v) = r*N*N + c*N + v
where r,c are in range (0...N-1) and v in (1...N).

You must encode:
  (1) Exactly one value per cell
  (2) For each value v and each row r: exactly one column c has v
  (3) For each value v and each column c: exactly one row r has v
  (4) For each value v and each sqrt(N)×sqrt(N) box: exactly one cell has v
  (5) Non-consecutive: orthogonal neighbors cannot differ by 1
  (6) Clues: unit clauses for the given puzzle
"""

from typing import Tuple, Iterable
import math

def to_cnf(input_path: str) -> Tuple[Iterable[Iterable[int]], int]:
    """
    Read puzzle from input_path and return (clauses, num_vars).

    - clauses: iterable of iterables of ints (each clause), no trailing 0s
    - num_vars: must be N^3 with N = grid size
    """

    # Exactly one value per cell
    f = open(input_path, 'r')
    sudoku = f.read()
    splitlines = sudoku.splitlines()
    N = len(splitlines)
    clauses = list()

    # Make list of all clauses
    clauses.extend(at_least_one(N))
    clauses.extend(at_most_one(N))
    clauses.extend(row_constraint(N))
    clauses.extend(box_constraint(N))
    clauses.extend(orthogonal_constraint(N))
    clauses.extend(clues_constraint(input_path))

    # Calculate number of variables
    num_vars = N * N * N

    f.close()
    return clauses, num_vars

def var_mapping(r: int, c: int, v: int, N: int) -> int:
    """
    Map (r: row, c: column, v: value) to variable number.

    - r and c range from 0 to N-1
    - v ranges from 1 to N 
    - N is the grid size of the sudoku
    - returns unique ID for each variable
    """
    return (r  * N * N) + (c  * N) + v 


def at_least_one(N):
    """
    Exactly one value per cell

    - For each cell (r, c), exactly one v ∈ {1, . . . , N } is true.
    """
    clauses = list()
    clause = list()

    for r in range(N):
        for c in range(N):
            for v in range(1, N + 1):
                literal = var_mapping(r, c, v, N)
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
                    clause_single = [var_mapping(r,c,v1,N) * -1, var_mapping(r,c,v2,N) * -1]
                    clauses.append(clause_single)
    return clauses

def row_constraint(N: int) -> Iterable[Iterable[int]]:
    """
    Generate clauses for row constraints.

    - For each value v and each row r, exactly one column c has v
    """
    clauses = []
    for r in range(0, N - 1):
        for v in range(1, N):
            clause = []
            for c in range(0, N - 1):
                for c2 in range(c + 1, N):
                    var1 = var_mapping(r, c, v, N)
                    var2 = var_mapping(r, c2, v, N)
                    clauses.append([-var1, -var2])
            clauses.append(clause)
    return clauses

def column_constraint(N: int) -> Iterable[Iterable[int]]:
    """
    Column constraint.

    - For each value v and each column c, exactly one row r has v
    """
    clauses = []
    for r in range(0, N-1):
        for v in range(1, N):
            clause = []
            for c in range(0, N-1):
                for c2 in range(c + 1, N):
                    var1 = var_mapping(r, c, v, N)
                    var2 = var_mapping(r, c2, v, N)
                    clauses.append([-var1, -var2])
            clauses.append(clause)
    return clauses

def box_constraint(N):
    """
    Box constraint.

    - For each value v and each B × B box, exactly one cell in that box has v.
    """

    B = int(math.sqrt(N))
    clauses = list()
    # Loop over boxes
    for b_r in range(B):
        for b_c in range(B):
            # Loop over values
            for v in range(1, N + 1):
                # Loop over exact coordinates
                for r_1 in range(b_r * B, (b_r + 1) * B - 1):
                    for c_1 in range(b_c * B, (b_c + 1) * B - 1):
                        # For each coordinate loop for a second coordinate we can compare to
                        for r_2 in range(b_r * B, (b_r + 1) * B - 1):
                            for c_2 in range(b_c * B, (b_c + 1) * B - 1):
                                # We will save the literal if c_2 is bigger than c_1
                                # or r_2 is bigger than r_1
                                if r_2 > r_1 or c_2 > c_1:
                                    clause = [var_mapping(r_1,c_1,v,N) * -1,
                                              var_mapping(r_2,c_2,v,N) * -1]
                                    clauses.append(clause)
    return clauses

def orthogonal_constraint(N: int) -> Iterable[Iterable[int]]:
    """
    Non-consecutive rule

    - For every cell (r, c) and each orthogonal neighbor (r′, c′):
      value(r, c) − value(r′, c′)̸ = 1.
    """
    clauses = []
    # orthogonal neighbors offsets compared to cell (r, c)
    orthogonal_cells = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
    for r in range(0, N - 1):
        for c in range(0, N - 1):
            for dr, dc in orthogonal_cells:
                r2, c2 = r + dr, c + dc 
                if 0 <= r2 < N and 0 <= c2 < N:
                    # IF ABSOLUTE DIFFERENCE IS 1
                    for v in range(1, N + 1):
                        var = var_mapping(r, c, v, N)
                        if v + 1 <= N: 
                            var_neighborPos = var_mapping(r2, c2, v + 1, N)
                            clauses.append([-var, -var_neighborPos])
                        if v - 1 >= 1:  
                            var_neighborNeg = var_mapping(r2, c2, v - 1, N)
                            clauses.append([-var, -var_neighborNeg])
                    """
                    # IF DIFFERENCE IS 1
                    for v in range (1, N):
                        var = var_mapping(r, c, v, N)
                        var_neighborPos = var_mapping(r2, c2, v + 1, N)
                        clauses.append([-var, -var_neighborPos])
                    """
    return clauses

def clues_constraint(sudoku: str) -> Iterable[Iterable[int]]:
    """
    Clues

    - Unit clauses corresponding to a given puzzle — for a given digit v > 0 at (r, c), add the unit
      clause Xr,c,v
    """
    clauses = []
    f = open(sudoku, 'r')
    sudoku = f.read()
    splitlines = sudoku.splitlines()
    N = len(splitlines)
    for r in range(N):
        line = splitlines[r]
        cleanLine = line.replace(" ", "")
        intCleanLine = [int(num) for num in cleanLine]
        # print(f"Integer Line {r}: {(intCleanLine)}")
        for num in range(N):
            v = intCleanLine[num]
            if v != 0:
                c = num
                var = var_mapping(r, c, v, N)
                clauses.append([var])
        print(clauses)
    return clauses