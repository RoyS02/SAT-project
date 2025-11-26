from __future__ import annotations
from typing import List, Tuple, Optional, Set
import random
import math

N_DEFAULT = 9

####################
# Helper functions #
####################

def sudoku_valid_check(grid: List[List[int]], r: int, c: int, v: int) -> bool:
    """
    Check if generated values in sudoku's are valid by checking consecutive sudoku rules
    and non-consecutive orthogonal rule.
    """
    # Check row validity 
    if any(grid[r][cc] == v for cc in range(9)):
        return False
    # Check column validity 
    if any(grid[rr][c] == v for rr in range(9)):
        return False
    # Check box validity 
    box_row = (r // 3) * 3
    box_column = (c // 3) * 3
    for rr in range(box_row, box_row + 3):
        for cc in range(box_column, box_column + 3):
            if grid[rr][cc] == v:
                return False
            
    # Check orthogonal validity
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        rr, cc = r + dr, c + dc
        if 0 <= rr < 9 and 0 <= cc < 9:
            neighbor_val = grid[rr][cc]
            if neighbor_val != 0 and abs(neighbor_val - v) == 1:
                return False
        
    return True


def solve_nonconsecutive(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                vals = list(range(1, 10))
                random.shuffle(vals)
                for v in vals:
                    if sudoku_valid_check(grid, r, c, v):
                        grid[r][c] = v
                        if solve_nonconsecutive(grid):
                            return True
                        grid[r][c] = 0
                return False
    return True

def generate_full_nonconsecutive_solution():
    grid = [[0]*9 for _ in range(9)]
    solve_nonconsecutive(grid)
    return grid

def puzzle_from_solution(solution, filled_percentage):
    puzzle = [row[:] for row in solution]
    total = 81
    keep = int(total * filled_percentage)

    cells = [(r,c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    to_remove = total - keep
    for (r,c) in cells:
        if to_remove == 0:
            break
        puzzle[r][c] = 0
        to_remove -= 1

    return puzzle

def varnumber(row: int, column: int, value: int, N: int = N_DEFAULT) -> int:
    """
    Zelfde conventie als in je comment:
        unit = row * N*N + column * N + value
    row, column: 0-based, value: 1..N
    """
    return row * N * N + column * N + value


def get_rcv(unit: int, N: int = N_DEFAULT) -> Optional[Tuple[int, int, int]]:
    """
    Inverse van varnumber:
        unit = row * N*N + column * N + value
    Geeft (row, column, value) 0-based r/c, value 1..N.
    """
    if unit <= 0:
        return None

    u = unit - 1  # intern 0-based
    value = u % N + 1
    u //= N
    column = u % N
    row = u // N
    return row, column, value


#####################
# TwoDoku functions #
#####################

def move_that_box(new_box: List[int], varnum: int, N: int = N_DEFAULT) -> int:
    rcv = get_rcv(varnum, N)

    r_old, c_old, value = rcv

    B_size = int(math.sqrt(N))  # bij Sudoku: 3

    # Find coordinate within old box
    r_in_old_box = r_old % B_size
    c_in_old_box = c_old % B_size

    # Find new value_number
    r_new = (new_box[0] - 1) * B_size + r_in_old_box
    c_new = (new_box[1] - 1) * B_size + c_in_old_box

    return varnumber(r_new, c_new, value, N)


def move_those_values(ready2move: List[List[int]], k: int, N: int = N_DEFAULT) -> List[int]:
    # This function is a tad hardcoded, but does make it easier to read what is going on
    moved_list: List[int] = []
    if k == 0:
        return moved_list

    if k == 9:    # k = 9:        3x3 -> 1x1
        for item in ready2move[0]:
            moved_list.append(move_that_box([1, 1], item, N))

    elif k == 18:   # k = 18:       3x2 -> 1x1, 3x3 -> 1x2
        for item in ready2move[0]:
            moved_list.append(move_that_box([1, 1], item, N))  # 3x2 -> 1x1
        for item in ready2move[1]:
            moved_list.append(move_that_box([1, 2], item, N))  # 3x3 -> 1x2

    elif k == 27:   # k = 27:       3x1 -> 1x1, 3x2 -> 1x2, 3x3 -> 1x3
        for item in ready2move[0]:
            moved_list.append(move_that_box([1, 1], item, N))
        for item in ready2move[1]:
            moved_list.append(move_that_box([1, 2], item, N))
        for item in ready2move[2]:
            moved_list.append(move_that_box([1, 3], item, N))

    elif k == 36:   # k = 36:       2x2 -> 1x1, 2x3 -> 1x2, 3x2 -> 2x1, 3x3 -> 2x2
        for item in ready2move[0]:
            moved_list.append(move_that_box([1, 1], item, N))
        for item in ready2move[1]:
            moved_list.append(move_that_box([1, 2], item, N))
        for item in ready2move[2]:
            moved_list.append(move_that_box([2, 1], item, N))
        for item in ready2move[3]:
            moved_list.append(move_that_box([2, 2], item, N))

    return moved_list


def apply_truths_to_grid(grid: List[List[int]], varnums: List[int]) -> None:
    """Zet (rcv) waarden in een grid."""
    for vn in varnums:
        rcv = get_rcv(vn)
        if rcv is None:
            continue
        r, c, v = rcv
        grid[r][c] = v


def generate_random_sudoku_puzzle(filled_percentage: float) -> List[List[int]]:
    """
    Make sudoku of 9 by 9 that takes sudoku rules into account
    """
    filled_percentage = max(0.0, min(1.0, filled_percentage))
    grid = [[0] * 9 for _ in range(9)]

    total_cells = 81
    target_filled = int(round(total_cells * filled_percentage))

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    filled = 0
    for (r, c) in cells:
        if filled >= target_filled:
            break
        # Try random value
        values = list(range(1, 10))
        random.shuffle(values)
        for v in values:
            if sudoku_valid_check(grid, r, c, v):
                grid[r][c] = v
                filled += 1
                # Go to next cell
                break  

    return grid


def extract_overlap_varnums_from_puzzle(grid_A: List[List[int]], k: int) -> List[List[int]]:
    """
    Check how big the overlap is based on K, and see which values/ Clues of sudoku A need to be 
    put in sudoku B. (does not copy them to sudoku B yet)
    """
    N = 9
    groups_count = {0: 0, 9: 1, 18: 2, 27: 3, 36: 4}[k]
    overlapping_values: List[List[int]] = [[] for _ in range(groups_count)]

    if k == 0:
        return overlapping_values

    if k == 9:    # 3x3 -> groep 0 (r=6..8, c=6..8)
        for i in range(6, 9):
            for j in range(6, 9):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[0].append(varnumber(i, j, v, N))

    elif k == 18:   # 3x2 -> g0, 3x3 -> g1
        for i in range(6, 9):      # 3x2 (r=6..8, c=3..5)
            for j in range(3, 6):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[0].append(varnumber(i, j, v, N))
        for i in range(6, 9):      # 3x3 (r=6..8, c=6..8)
            for j in range(6, 9):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[1].append(varnumber(i, j, v, N))

    elif k == 27:   # 3x1 -> g0, 3x2 -> g1, 3x3 -> g2
        for i in range(6, 9):      # 3x1 (c=0..2)
            for j in range(0, 3):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[0].append(varnumber(i, j, v, N))
        for i in range(6, 9):      # 3x2 (c=3..5)
            for j in range(3, 6):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[1].append(varnumber(i, j, v, N))
        for i in range(6, 9):      # 3x3 (c=6..8)
            for j in range(6, 9):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[2].append(varnumber(i, j, v, N))

    elif k == 36:   # 2x2 -> g0, 2x3 -> g1, 3x2 -> g2, 3x3 -> g3
        for i in range(3, 6):      # 2x2 (r=3..5, c=3..5)
            for j in range(3, 6):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[0].append(varnumber(i, j, v, N))
        for i in range(3, 6):      # 2x3 (r=3..5, c=6..8)
            for j in range(6, 9):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[1].append(varnumber(i, j, v, N))
        for i in range(6, 9):      # 3x2 (r=6..8, c=3..5)
            for j in range(3, 6):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[2].append(varnumber(i, j, v, N))
        for i in range(6, 9):      # 3x3 (r=6..8, c=6..8)
            for j in range(6, 9):
                v = grid_A[i][j]
                if v >= 0:
                    overlapping_values[3].append(varnumber(i, j, v, N))

    return overlapping_values

# ============================================================
# Extra clues toevoegen in B (buiten de overlap)
# ============================================================

def generate_clues_in_B(
    grid_B: List[List[int]],
    filled_percentage_B: float,
    overlap_coords_B: Set[Tuple[int, int]]
) -> None:
    """
    Generate sudoku B. First, take the overlapping cells from sudoku A and place them in sudoku B
    Fill the remaining cells based on filled percentage while taking sudoku rules into account
    """
    filled_percentage_B = max(0.0, min(1.0, filled_percentage_B))
    total_cells = 81
    target_filled = int(round(total_cells * filled_percentage_B))

    current_filled = sum(1 for r in range(9) for c in range(9) if grid_B[r][c] != 0)

    # Return if sudoku is filled enough
    if current_filled >= target_filled:
        return  

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    for (r, c) in cells:
        if current_filled >= target_filled:
            break
        if (r, c) in overlap_coords_B:
            continue
        if grid_B[r][c] != 0:
            continue

        # Try random value
        values = list(range(1, 10))
        random.shuffle(values)
        for v in values:
            if sudoku_valid_check(grid_B, r, c, v):
                grid_B[r][c] = v
                current_filled += 1
                # Go to next cell
                break


####################
# Generate TwoDoku #
####################

def generate_twodoku_puzzles_from_scratch(
    filled_A: float,
    filled_B: float,
    k: int
) -> Tuple[List[List[int]], List[List[int]], List[List[int]],
           Set[Tuple[int, int]], Set[Tuple[int, int]]]:
    """
    New version:

    1. Generate a full nonconsecutive solution for Sudoku A.
    2. Take the overlap region from A's *solution* (based on k).
    3. Map that region into Sudoku B (same digits, same cell positions in the box).
    4. Solve B with those overlap cells fixed.
       - If no solution, restart with a new solution_A.
    5. Generate puzzles from both solutions.
    6. Force the puzzles so that the overlap region of A and B has:
       - the same pattern of clues/zeros
       - the same digits where clues are present.

    Returns:
      - puzzle_A (9x9)
      - puzzle_B (9x9)
      - B_after_overlap (B grid right after copying overlap from A, before solving)
      - overlap_coords_A: set of (r,c) in A's overlap region
      - overlap_coords_B: set of (r,c) in B's overlap region
    """

    N = 9
    B_size = 3  # standard Sudoku

    filled_A = max(0.0, min(1.0, filled_A))
    filled_B = max(0.0, min(1.0, filled_B))


    # We loop until we find a pair (solution_A, solution_B) that is compatible
    # under the requested overlap.
    while True:
        # 1) Full solution for A
        solution_A = generate_full_nonconsecutive_solution()

        # 2) Build overlap from A's solution (reuse your extraction function)
        groups_A = extract_overlap_varnums_from_puzzle(solution_A, k)

        # Flatten groups_A keeping order (this order must match move_those_values)
        flat_varnums_A: List[int] = []
        for g in groups_A:
            flat_varnums_A.extend(g)

        # 3) Map that overlap into B
        overlap_varnums_B = move_those_values(groups_A, k)

        # B grid with only the overlap cells set
        solution_B = [[0] * N for _ in range(N)]
        apply_truths_to_grid(solution_B, overlap_varnums_B)

        # Keep a copy for debug / returning
        B_after_overlap = [row[:] for row in solution_B]

        # 4) Solve B with overlap fixed
        if not solve_nonconsecutive(solution_B):
            # This overlap is incompatible with any completion of B → try again
            continue

        # If we get here, we have consistent solutions A and B with correct overlap
        # 5) Build coordinate sets and mapping A -> B
        overlap_coords_A: Set[Tuple[int, int]] = set()
        overlap_coords_B: Set[Tuple[int, int]] = set()
        mapping_A_to_B: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

        # Reconstruct the mapping by pairing flat_varnums_A with overlap_varnums_B
        if len(flat_varnums_A) != len(overlap_varnums_B):
            # This should not happen if move_those_values is consistent
            raise RuntimeError("Mismatch between A and B overlap varnums length")

        for vnA, vnB in zip(flat_varnums_A, overlap_varnums_B):
            ra, ca, va = get_rcv(vnA)
            rb, cb, vb = get_rcv(vnB)
            overlap_coords_A.add((ra, ca))
            overlap_coords_B.add((rb, cb))
            mapping_A_to_B.append(((ra, ca), (rb, cb)))

            # Sanity check: solutions must agree on the digit
            if solution_A[ra][ca] != solution_B[rb][cb]:
                raise RuntimeError("Overlap solutions A/B disagree on digit; check mapping logic")

        # 6) Generate puzzles from both solutions
        puzzle_A = puzzle_from_solution(solution_A, filled_A)
        puzzle_B = puzzle_from_solution(solution_B, filled_B)

        # 7) Enforce identical overlap pattern between puzzle_A and puzzle_B:
        #    - If A has 0 at (ra, ca) → B must also be 0 at mapped (rb, cb)
        #    - If A has a digit → B must show the corresponding digit.
        for (ra, ca), (rb, cb) in mapping_A_to_B:
            if puzzle_A[ra][ca] == 0:
                # Both show empty
                puzzle_B[rb][cb] = 0
            else:
                # A shows a clue → set both to the correct solution digit
                digit_A = solution_A[ra][ca]
                digit_B = solution_B[rb][cb]
                # They should be equal by construction
                assert digit_A == digit_B
                puzzle_A[ra][ca] = digit_A
                puzzle_B[rb][cb] = digit_B

        # We have a consistent pair, break the loop
        break

    return puzzle_A, puzzle_B, B_after_overlap, overlap_coords_A, overlap_coords_B


# def main():
    # filled_A = 0.4   # 40% clues in A
    # filled_B = 0.4   # 40% clues in B (incl. overlap)
    # k        = 9    # grootte overlapvorm

    # puzzle_A, puzzle_B, B_after_overlap, overlap_A, overlap_B = \
    #     generate_twodoku_puzzles_from_scratch(filled_A, filled_B, k)
    # print("Puzzle A", puzzle_A)
#     # print("Puzzle B", puzzle_B)

# if __name__== "__main__":
#     main()