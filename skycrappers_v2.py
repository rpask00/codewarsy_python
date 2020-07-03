from ttictoc import TicToc
import timeit
import copy
import functools
import itertools
import json
import time
from itertools import permutations


class Solve:
    def __init__(self, size, clues):
        self.size = size
        self.clues = clues
        self.possible_cols = []
        self.possible_rows = []
        self.variants = {i: set() for i in range(size+1)}
        self.city = [[0 for i in range(size)] for j in range(size)]

        for row in permutations(range(1, size+1)):
            visible = sum(v >= max(row[:i+1]) for i, v in enumerate(row))
            self.variants[visible].add(row)
            self.variants[0].add(row)

        for i in range(size):
            clue_left, clue_right = clues[4*size-1-i], clues[size + i]
            var_left = self.variants[clue_left]
            var_right = set(map(lambda row: tuple(
                reversed(row)), self.variants[clue_right]))
            self.possible_rows.append(var_left.intersection(var_right))

            clue_top, clue_btm = clues[i], clues[3*size-1-i]
            var_top = self.variants[clue_top]
            var_btm = set(map(lambda row: tuple(
                reversed(row)), self.variants[clue_btm]))
            self.possible_cols.append(var_top.intersection(var_btm))

    def solve_puzzle(self):
        while True:
            state = []
            for i in range(self.size):
                for j in range(self.size):
                    row_set = set(row[j] for row in self.possible_rows[i])
                    col_set = set(col[i] for col in self.possible_cols[j])
                    union_set = row_set.intersection(col_set)

                    prev_rows_len = len(self.possible_rows[i])

                    self.possible_rows[i] = [
                        row for row in self.possible_rows[i] if row[j] in union_set]
                    new_rows_len = len(self.possible_rows[i])

                    prev_cols_len = len(self.possible_rows[i])
                    self.possible_cols[j] = [
                        col for col in self.possible_cols[j] if col[i] in union_set]
                    new_cols_len = len(self.possible_rows[i])



                    state.append(prev_rows_len is new_rows_len)
                    state.append(prev_cols_len is new_cols_len)

            if all(state):
                if any(len(var_row) > 1 for var_row in self.possible_rows):
                    return self.after_solve(self.city, 0)

                return list(list(row[0]) for row in self.possible_rows)

    def validate_city(self, city):
        for row in city:
            row = [r for r in row if r is not 0]
            if len(set(row)) is not len(row):
                return False

        return True

    def after_solve(self, city, id):
        if id == self.size * 2:
            return [list(row) for row in city]

        if id >= self.size:
            for row in self.possible_rows[id % self.size]:
                city[id % self.size] = row
                if not self.validate_city(city):
                    continue

                result = self.after_solve(copy.deepcopy(city), id+1)
                if result is False:
                    continue

                return result
            return False

        for col in self.possible_cols[id]:
            col_copy = list(col)
            for row in city:
                row[id] = col_copy.pop(0)

            if not self.validate_city(city):
                continue

            result = self.after_solve(copy.deepcopy(city), id+1)

            if result is False:
                continue

            return result
        return False


clues = [
    [3, 3, 2, 1, 2, 2, 3,   4, 3, 2, 4, 1, 4, 2,  2, 4, 1, 4, 5, 3, 2,   3, 1, 4, 2, 5, 2, 3],
    [0, 0, 5, 3, 0, 2, 0,   0, 0, 0, 4, 5, 0, 0,  0, 0, 0, 3, 2, 5, 4,   2, 2, 0, 0, 0, 0, 5],
    [7, 0, 0, 0, 2, 2, 3,   0, 0, 3, 0, 0, 0, 0,  3, 0, 3, 0, 0, 5, 0,   0, 0, 0, 0, 5, 0, 4],
    [6, 4, 0, 2, 0, 0, 3,   0, 3, 3, 3, 0, 0, 4,  0, 5, 0, 5, 0, 2, 0,   0, 0, 0, 4, 0, 0, 3],
    [0, 0, 0, 5, 0, 0, 3,   0, 6, 3, 4, 0, 0, 0,  3, 0, 0, 0, 2, 4, 0,   2, 6, 2, 2, 2, 0, 0],
    [0, 0, 5, 0, 0, 0, 6,   4, 0, 0, 2, 0, 2, 0,  0, 5, 2, 0, 0, 0, 5,   0, 3, 0, 5, 0, 0, 3],
    [0, 0, 5, 3, 0, 2, 0,   0, 0, 0, 4, 5, 0, 0,  0, 0, 0, 3, 2, 5, 4,   2, 2, 0, 0, 0, 0, 5],
    [0, 2, 3, 0, 2, 0, 0,   5, 0, 4, 5, 0, 4, 0,  0, 4, 2, 0, 0, 0, 6,   5, 2, 2, 2, 2, 4, 1],
    [0, 2, 3, 0, 2, 0, 0,   5, 0, 4, 5, 0, 4, 0,  0, 4, 2, 0, 0, 0, 6,   0, 0, 0, 0, 0, 0, 0],
    [3, 0, 3, 0, 0, 5, 0,   0, 0, 0, 0, 5, 0, 4,  7, 0, 0, 0, 2, 2, 3,   0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 4,   7, 0, 0, 0, 2, 2, 3,  0, 0, 3, 0, 0, 0, 0,   3, 0, 3, 0, 0, 5, 0],
    [0, 0, 3, 0, 0, 0, 0,   3, 0, 3, 0, 0, 5, 0,  0, 0, 0, 0, 5, 0, 4,   7, 0, 0, 0, 2, 2, 3],
]

t = TicToc('name')
for clue in clues:
    t.tic()
    s = Solve(len(clue)//4, clue)
    print(s.solve_puzzle())

    t.toc()  # Prints and returns the elapsed time
    print(t.elapsed)


