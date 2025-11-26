import os
from typing import List
from encoder import to_cnf  
from generator import generate_twodoku_puzzles_from_scratch

Grid = List[List[int]]

def write_dimacs(target, num_vars: int, clauses) -> None:
    """Write DIMACS CNF to a file path or file-like (stdout)."""
    close = False
    if isinstance(target, str):
        f = open(target, "w")
        close = True
    else:
        f = target
    try:
        clauses = list(clauses)
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(str(l) for l in cl) + " 0\n")
    finally:
        if close:
            f.close()

def grid_to_string(grid):
    return "\n".join(
        " ".join(str(x) for x in row)
        for row in grid)

def write_grid_to_file(grid, path):
    with open(path, "w") as f:
        for row in grid:
            line = " ".join(str(x) for x in row)
            f.write(line + "\n")

def main():
    filled_A = 0.2
    filled_B = 0.2
    k        = 27    # or 9, 18, 27, 36 for overlaps

    # directory for CNF files
    cnf_dir = os.path.join(os.path.dirname(__file__), "CNF encoding")
    os.makedirs(cnf_dir, exist_ok=True)
    # directory for Sudoku files
    grid_dir = os.path.join(os.path.dirname(__file__), "Sudoku grids")
    os.makedirs(grid_dir, exist_ok=True)
    
    for i in range(1, 21):
        # 1) Generate one pair of Sudoku puzzles
        puzzle_A, puzzle_B, B_after_overlap, overlap_A, overlap_B = \
            generate_twodoku_puzzles_from_scratch(filled_A, filled_B, k)

        # 2) Write puzzle grids to text files
        gridA_txt = os.path.join(grid_dir, f"Sudoku_{i}.grid_A")
        gridB_txt = os.path.join(grid_dir, f"Sudoku_{i}.grid_B")

        with open(gridA_txt, "w") as f:
            f.write(grid_to_string(puzzle_A) + "\n")
        with open(gridB_txt, "w") as f:
            f.write(grid_to_string(puzzle_B) + "\n")

        # 3) Encode to CNF
        clauses_A, num_vars_A = to_cnf(gridA_txt)
        clauses_B, num_vars_B = to_cnf(gridB_txt)

        # 4) Write DIMACS CNF files (unique names per instance)
        cnfA_path = os.path.join(cnf_dir, f"DIMACS_{i}.grid_A")
        cnfB_path = os.path.join(cnf_dir, f"DIMACS_{i}.grid_B")

        write_dimacs(cnfA_path, num_vars_A, clauses_A)
        write_dimacs(cnfB_path, num_vars_B, clauses_B)

if __name__ == "__main__":
    main()