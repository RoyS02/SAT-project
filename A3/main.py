import argparse
import sys
import os
from encoder import to_cnf  
# from generator import generate_twodoku_sudoku, grid_to_string
from box_gen import generate_twodoku_puzzles_from_scratch, solve_nonconsecutive, generate_full_nonconsecutive_solution, puzzle_from_solution

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
def parse_tuple(tuple):
    try:
        a, b = tuple.split(",")
        return int(a), int(b)
    except:
        raise argparse.ArgumentTypeError("Tuples must be in format: x,y")

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--filled_percentage", "-f",
                    type=float,
                    default=0.5)
    p.add_argument("--rows", "-r",
                    type=int,
                    default=15)
    p.add_argument("--columns", "-c",
                    type=int,
                    default=15)
    p.add_argument("--sudoku_one", "-s1",
                    type=parse_tuple,
                    default=(0, 0))
    p.add_argument("--sudoku_two", "-s2",
                    type=parse_tuple,
                    default=(6, 6))
    p.add_argument("--out", 
                   dest="out", 
                   default=None, 
                   help="Path to write DIMACS CNF (stdout if omitted)")
    return p.parse_args()
"""
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True, help="Path to puzzle .txt")
    p.add_argument("--out", dest="out", default=None, help="Path to write DIMACS CNF (stdout if omitted)")
    return p.parse_args()"""

from typing import List

Grid = List[List[int]]


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
    # Generate a TwoDoku puzzle based on command line arguments
    args = parse_args()
    puzzles = []
    
    # Generate 20 files
    """
    for i in range(1, 21):
        grid = generate_twodoku_sudoku(
            filled_percentage=args.filled_percentage,
            rows=args.rows,
            columns=args.columns,
            sudoku_one=args.sudoku_one,
            sudoku_two=args.sudoku_two)

        output_str = grid_to_string(grid)

        filename = f"{"TwoDoku"}_{i}{".txt"}"
        with open(filename, "w") as f:
            f.write(output_str + "\n")
        
        puzzles.append(filename)
        """
    filled_A = 0.4   # 40% clues in A
    filled_B = 0.4   # 40% clues in B (incl. overlap)
    k        = 9    # grootte overlapvorm

    puzzle_A, puzzle_B, B_after_overlap, overlap_A, overlap_B = \
         generate_twodoku_puzzles_from_scratch(filled_A, filled_B, k)
    
    
    solution_A = generate_full_nonconsecutive_solution()
    puzzle_A = puzzle_from_solution(solution_A, filled_A)

    solution_B = [row[:] for row in B_after_overlap]
    solve_nonconsecutive(solution_B)     # vult hem verder in
    puzzle_B = puzzle_from_solution(solution_B, filled_B)




    print("Puzzle A", grid_to_string(puzzle_A))
    print("Puzzle B", grid_to_string(puzzle_A))
    str_a = grid_to_string(puzzle_A)
    str_b = grid_to_string(puzzle_B)
  

    filename_A = f"grid_a"
    with open(filename_A, "w") as f:
        f.write(str_a + "\n")
    filename_B = f"grid_b"
    with open(filename_B, "w") as f:
        f.write(str_b + "\n")
    
    # Encode clauses to CNF and write to DIMACS format

    clauses_A, num_vars_A = to_cnf(filename_A)
    clauses_B, num_vars_B = to_cnf(filename_B)


    # Same base name as puzzle, but .cnf extension
    cnf_path_A = "D:\School\M Artificial Intelligence\KR\A3" + ".grida"
    cnf_path_B = "D:\School\M Artificial Intelligence\KR\A3" + ".gridb"
    
    write_dimacs(cnf_path_A, num_vars_A, clauses_A)
    write_dimacs(cnf_path_B, num_vars_B, clauses_B)
    # # Solve the TwoDoku puzzl

if __name__ == "__main__":
    main()