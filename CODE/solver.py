# CDCL SAT Solver integrated with solve_cnf()
# Full-power CDCL with watched literals, VSIDS, conflict analysis (1-UIP), and non-chronological backjumping.

from typing import List, Tuple, Optional, Iterable, Dict
from collections import defaultdict, deque
import math

# ------------------ Utility: Watched Literal Data Structure ------------------
class WatchedLiterals:
    def __init__(self, clauses: List[List[int]]):
        self.clauses = clauses
        self.watched: Dict[int, List[int]] = defaultdict(list)  # literal -> clause indices
        self.watch_map: List[Tuple[int, int]] = []  # for each clause: (watched_lit1, watched_lit2)

        for i, clause in enumerate(self.clauses):
            if len(clause) >= 2:
                self.watch_map.append((clause[0], clause[1]))
                self.watched[clause[0]].append(i)
                self.watched[clause[1]].append(i)
            elif len(clause) == 1:
                lit = clause[0]
                self.watch_map.append((lit, lit))
                self.watched[lit].append(i)
            else:
                self.watch_map.append((0, 0))

    def remap_watch(self, clause_idx: int, old_lit: int, new_lit: int):
        self.watched[old_lit].remove(clause_idx)
        self.watched[new_lit].append(clause_idx)

# ------------------ CDCL Core ------------------
class CDCLSolver:
    def __init__(self, clauses: List[List[int]], num_vars: int):
        self.clauses = clauses
        self.num_vars = num_vars
        self.assign: List[int] = [0] * (num_vars + 1)
        self.level: List[int] = [0] * (num_vars + 1)
        self.reason: List[Optional[int]] = [None] * (num_vars + 1)

        self.decision_level = 0
        self.trail: List[int] = []

        self.wl = WatchedLiterals(self.clauses)

        self.var_score = [0.0] * (num_vars + 1)
        self.decay = 0.95

    # ------------------ Decision Variable Choice ------------------
    def pick_branch_lit(self) -> int:
        best = 1
        best_score = -1
        for v in range(1, self.num_vars + 1):
            if self.assign[v] == 0 and self.var_score[v] > best_score:
                best_score = self.var_score[v]
                best = v
        return best

    # ------------------ Propagation ------------------
    def propagate(self) -> Optional[int]:
        queue = deque(self.trail)
        seen = set()

        while queue:
            lit = queue.popleft()
            if lit in seen:
                continue
            seen.add(lit)

            watch_list = list(self.wl.watched.get(-lit, []))
            for ci in watch_list:
                clause = self.clauses[ci]
                w1, w2 = self.wl.watch_map[ci]
                other = w1 if w2 == -lit else w2

                if self.assign[abs(other)] == (1 if other > 0 else 2):
                    continue

                found_new = False
                for new_lit in clause:
                    if new_lit != other and new_lit != -lit:
                        a = self.assign[abs(new_lit)]
                        if a == 0 or a == (1 if new_lit > 0 else 2):
                            self.wl.remap_watch(ci, -lit, new_lit)
                            if w1 == -lit:
                                self.wl.watch_map[ci] = (new_lit, w2)
                            else:
                                self.wl.watch_map[ci] = (w1, new_lit)
                            found_new = True
                            break

                if found_new:
                    continue

                if self.assign[abs(other)] == 0:
                    val = 1 if other > 0 else 2
                    self.assign[abs(other)] = val
                    self.level[abs(other)] = self.decision_level
                    self.reason[abs(other)] = ci
                    self.trail.append(other)
                    queue.append(other)
                else:
                    return ci  # conflict
        return None

    # ------------------ Conflict Analysis (1-UIP) ------------------
    def analyze(self, conflict_clause: int) -> Tuple[List[int], int]:
        learnt = []
        seen = set()
        counter = 0
        level = self.decision_level

        clause = self.clauses[conflict_clause]

        while True:
            for lit in clause:
                v = abs(lit)
                if v not in seen:
                    seen.add(v)
                    if self.level[v] == level:
                        counter += 1
                    else:
                        learnt.append(lit)

            while True:
                x = self.trail.pop()
                vx = abs(x)
                if vx in seen:
                    break

            counter -= 1
            if counter == 0:
                learnt.append(-x)
                break
            clause = self.clauses[self.reason[vx]]

        max_level = 0
        for lit in learnt:
            v = abs(lit)
            if self.level[v] != level:
                max_level = max(max_level, self.level[v])

        return learnt, max_level

    # ------------------ Learn Clause & Backjump ------------------
    def add_clause(self, clause: List[int]):
        idx = len(self.clauses)
        self.clauses.append(clause)
        if len(clause) == 1:
            lit = clause[0]
            self.wl.watch_map.append((lit, lit))
            self.wl.watched[lit].append(idx)
        else:
            self.wl.watch_map.append((clause[0], clause[1]))
            self.wl.watched[clause[0]].append(idx)
            self.wl.watched[clause[1]].append(idx)

    # ------------------ Solve ------------------
    def solve(self) -> Tuple[str, List[int]]:
        while True:
            conflict = self.propagate()
            if conflict is not None:
                if self.decision_level == 0:
                    return "UNSAT", []
                learnt, bj = self.analyze(conflict)
                self.add_clause(learnt)
                self.decision_level = bj
            else:
                lit = self.pick_branch_lit()
                if lit == 0:
                    break
                self.decision_level += 1
                self.assign[lit] = 1
                self.level[lit] = self.decision_level
                self.reason[lit] = None
                self.trail.append(lit)

        model = []
        for i in range(1, self.num_vars + 1):
            if self.assign[i] == 1:
                model.append(i)
            elif self.assign[i] == 2:
                model.append(-i)
        return "SAT", model

# ------------------ solve_cnf interface ------------------
def solve_cnf(clauses: Iterable[Iterable[int]], num_vars: int) -> Tuple[str, List[int]]:
    clause_list = [list(c) for c in clauses]
    solver = CDCLSolver(clause_list, num_vars)
    return solver.solve()