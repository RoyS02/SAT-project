import math

def read_grid(path: str) -> list[list[int]]:
    with open(path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    grid: list[list[int]] = []
    for line in lines:
        grid.append([int(x) for x in line.split()])
    return grid

def to_cnf(input_path: str):
    grid = read_grid(input_path)
    R = len(grid)
    C = len(grid[0])
    # Sudoku digits 1..9 (you can parameterize if you want)
    N = 9

    # active[r][c] = True iff this cell is part of (some) Sudoku
    active = [[grid[r][c] != -1 for c in range(C)] for r in range(R)]

    clauses = []
    clauses.extend(exactly_one_v_per_cell(R, C, N, active))
    clauses.extend(row_constraint(R, C, N, active))
    clauses.extend(column_constraint(R, C, N, active))
    clauses.extend(box_constraint(R, C, N, active))
    clauses.extend(orthogonal_constraint(R, C, N, active))
    clauses.extend(clues_constraint(grid, R, C, N, active))
    
    num_vars = R * C * N
    clauses = check_for_duplicates(clauses)
    return clauses, num_vars

def check_for_duplicates(clauses):
    """
    Check for duplicate clauses and remove to save space
    """
    duplicate_clauses = set()
    unique_clauses = []
    for c in clauses:
        clause = tuple(sorted(c))
        if clause not in duplicate_clauses:
            duplicate_clauses.add(clause)
            unique_clauses.append(list(clause))
    return unique_clauses

def var_mapping(r: int, c: int, v: int, N: int, C: int) -> int:
    return r * C * N + c * N + v

def exactly_one_v_per_cell(R, C, N, active):
    clauses = []

    # at least one
    for r in range(R):
        for c in range(C):
            if not active[r][c]:
                continue
            clause = [var_mapping(r, c, v, N, C) for v in range(1, N+1)]
            clauses.append(clause)

    # at most one
    for r in range(R):
        for c in range(C):
            if not active[r][c]:
                continue
            for v1 in range(1, N):
                for v2 in range(v1+1, N+1):
                    v1_id = var_mapping(r, c, v1, N, C)
                    v2_id = var_mapping(r, c, v2, N, C)
                    clauses.append([-v1_id, -v2_id])

    return clauses

def row_constraint(R, C, N, active):
    clauses = []
    for r in range(R):
        for v in range(1, N+1):
            cells = [c for c in range(C) if active[r][c]]
            if not cells:
                continue
            # at least one
            clauses.append([var_mapping(r, c, v, N, C) for c in cells])
            # at most one
            for i in range(len(cells) - 1):
                for j in range(i+1, len(cells)):
                    c1, c2 = cells[i], cells[j]
                    x = var_mapping(r, c1, v, N, C)
                    y = var_mapping(r, c2, v, N, C)
                    clauses.append([-x, -y])
    return clauses

def column_constraint(R, C, N, active):
    clauses = []
    for c in range(C):
        for v in range(1, N+1):
            cells = [r for r in range(R) if active[r][c]]
            if not cells:
                continue
            # at least one
            clauses.append([var_mapping(r, c, v, N, C) for r in cells])
            # at most one
            for i in range(len(cells) - 1):
                for j in range(i+1, len(cells)):
                    r1, r2 = cells[i], cells[j]
                    x = var_mapping(r1, c, v, N, C)
                    y = var_mapping(r2, c, v, N, C)
                    clauses.append([-x, -y])
    return clauses

def row_constraint(R, C, N, active):
    clauses = []
    for r in range(R):
        for v in range(1, N+1):
            cells = [c for c in range(C) if active[r][c]]
            if not cells:
                continue
            # at least one
            clauses.append([var_mapping(r, c, v, N, C) for c in cells])
            # at most one
            for i in range(len(cells) - 1):
                for j in range(i+1, len(cells)):
                    c1, c2 = cells[i], cells[j]
                    x = var_mapping(r, c1, v, N, C)
                    y = var_mapping(r, c2, v, N, C)
                    clauses.append([-x, -y])
    return clauses

def column_constraint(R, C, N, active):
    clauses = []
    for c in range(C):
        for v in range(1, N+1):
            cells = [r for r in range(R) if active[r][c]]
            if not cells:
                continue
            # at least one
            clauses.append([var_mapping(r, c, v, N, C) for r in cells])
            # at most one
            for i in range(len(cells) - 1):
                for j in range(i+1, len(cells)):
                    r1, r2 = cells[i], cells[j]
                    x = var_mapping(r1, c, v, N, C)
                    y = var_mapping(r2, c, v, N, C)
                    clauses.append([-x, -y])
    return clauses

def box_constraint(R, C, N, active, boards=None):
    if boards is None:
        boards = [(0, 0)]  # default: single 9x9 at top-left

    B = int(math.sqrt(N))  # 3 for standard Sudoku
    clauses = []

    for (top, left) in boards:
        # iterate 3x3 boxes inside this 9x9
        for br in range(0, N, B):
            for bc in range(0, N, B):
                # collect cells inside this box that are active
                cells = []
                for dr in range(B):
                    for dc in range(B):
                        r = top + br + dr
                        c = left + bc + dc
                        if 0 <= r < R and 0 <= c < C and active[r][c]:
                            cells.append((r, c))
                if not cells:
                    continue
                # Sudoku "exactly one v per box"
                for v in range(1, N+1):
                    # at least one
                    clauses.append([var_mapping(r, c, v, N, C) for (r, c) in cells])
                    # at most one
                    for i in range(len(cells)-1):
                        for j in range(i+1, len(cells)):
                            r1, c1 = cells[i]
                            r2, c2 = cells[j]
                            x = var_mapping(r1, c1, v, N, C)
                            y = var_mapping(r2, c2, v, N, C)
                            clauses.append([-x, -y])
    return clauses

def orthogonal_constraint(R, C, N, active):
    clauses = []
    directions = [(0, 1), (1, 0)]  # right, down
    for r in range(R):
        for c in range(C):
            if not active[r][c]:
                continue
            for dr, dc in directions:
                r2, c2 = r + dr, c + dc
                if 0 <= r2 < R and 0 <= c2 < C and active[r2][c2]:
                    for v in range(1, N):
                        x1 = var_mapping(r, c, v, N, C)
                        x2 = var_mapping(r2, c2, v+1, N, C)
                        y1 = var_mapping(r, c, v+1, N, C)
                        y2 = var_mapping(r2, c2, v, N, C)
                        clauses.append([-x1, -x2])
                        clauses.append([-y1, -y2])
    return clauses

def clues_constraint(grid, R, C, N, active):
    clauses = []
    for r in range(R):
        for c in range(C):
            if not active[r][c]:
                continue
            v = grid[r][c]
            if 1 <= v <= N:  # ignore 0 and -1
                var = var_mapping(r, c, v, N, C)
                clauses.append([var])
    return clauses