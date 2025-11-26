import os
import csv
import time
import solver
from solver import solve_cnf
from main_a2 import parse_dimacs   # reuse the parser from main.py


def solve_one_cnf(path: str):
    """Read a DIMACS CNF, solve it, return statistics."""
    clauses, num_vars = parse_dimacs(path)
    num_clauses = len(clauses)

    start = time.perf_counter()
    status, _ = solve_cnf(clauses, num_vars)
    elapsed = time.perf_counter() - start

    return {
        "status": status,
        "num_vars": num_vars,
        "num_clauses": num_clauses,
        "dpll_calls": solver.DPLL_CALLS,
        "time_sec": elapsed,
    }


def main():
    base_dir = os.path.dirname(__file__)
    cnf_dir = os.path.join(base_dir, "CNF encoding")
    output_csv = os.path.join(cnf_dir, "experiment_results.csv")

    NUM_PAIRS = 20

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "pair_index",
            "puzzle",
            "status",
            "dpll_calls",
            "num_vars",
            "num_clauses",
            "time_sec",
        ])

        for i in range(1, NUM_PAIRS + 1):
            path_A = os.path.join(cnf_dir, f"DIMACS_{i}.grid_A")
            path_B = os.path.join(cnf_dir, f"DIMACS_{i}.grid_B")

            if not os.path.exists(path_A):
                print(f"WARNING: {path_A} not found — skipping.")
                continue
            if not os.path.exists(path_B):
                print(f"WARNING: {path_B} not found — skipping.")
                continue

            # Solve A
            stats_A = solve_one_cnf(path_A)
            writer.writerow([
                i, "A",
                stats_A["status"],
                stats_A["dpll_calls"],
                stats_A["num_vars"],
                stats_A["num_clauses"],
                f"{stats_A['time_sec']:.6f}",
            ])

            # Solve B
            stats_B = solve_one_cnf(path_B)
            writer.writerow([
                i, "B",
                stats_B["status"],
                stats_B["dpll_calls"],
                stats_B["num_vars"],
                stats_B["num_clauses"],
                f"{stats_B['time_sec']:.6f}",
            ])

    print(f"Experiment results saved to {output_csv}")


if __name__ == "__main__":
    main()
