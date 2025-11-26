from typing import List, Tuple
import random
import argparse

Grid = List[List[int]]

####################
# Helper functions #
####################
def format_grid(grid: Grid) -> str:
    return "\n".join(" ".join(f"{v:2d}" for v in row) for row in grid)

def grid_to_string(grid):
    return "\n".join(
        " ".join(str(x) for x in row)
        for row in grid)

def write_grid_to_file(grid, path):
    with open(path, "w") as f:
        for row in grid:
            line = " ".join(str(x) for x in row)
            f.write(line + "\n")

#####################
# TwoDoku Generator #
######################

def generate_twodoku_sudoku(
    filled_percentage: float,
    rows: int,
    columns: int,
    sudoku_one: tuple[int,int],
    sudoku_two: tuple[int,int]) -> Grid:

    # Start with empty grid
    grid: Grid = [[0 for _ in range(columns)] for _ in range(rows)]

    # Determine which cells actually belong to at least one 9x9 block
    twodoku_cells = set()
    twodoku_blocks = [sudoku_one, sudoku_two]
    for top, left in twodoku_blocks:
        for r in range(9):
            for c in range(9):
                rr = top + r
                cc = left + c
                if 0 <= rr < rows and 0 <= cc < columns:
                    twodoku_cells.add((rr, cc))

    twodoku_cells = list(twodoku_cells)
    total_valid = len(twodoku_cells)
    cells_to_fill = int(total_valid * filled_percentage)

    # Fill random cells with clues
    random.shuffle(twodoku_cells)
    cells_to_fill_positions = twodoku_cells[:cells_to_fill]

    for (r, c) in cells_to_fill_positions:
        grid[r][c] = random.randint(1, 9)
    
    sudoku_set = set(twodoku_cells)
    for r in range(rows):
        for c in range(columns):
            if (r, c) not in sudoku_set:
                grid[r][c] = -1
    return grid

"""def main():
    args = parse_args()
    if args.out:
        if "." in args.out:
            base, ext = args.out.rsplit(".", 1)
            ext = "." + ext
        else:
            base, ext = args.out, ".txt"
    else:
        base, ext = "output", ".txt"
    # Generate 20 files
    for i in range(1, 21):
        grid = generate_twodoku_sudoku(
            filled_percentage=args.filled_percentage,
            rows=args.rows,
            columns=args.columns,
            sudoku_one=args.sudoku_one,
            sudoku_two=args.sudoku_two)

        output_str = grid_to_string(grid)

        filename = f"{base}_{i}{ext}"
        with open(filename, "w") as f:
            f.write(output_str + "\n")

if __name__ == "__main__":
    main()"""