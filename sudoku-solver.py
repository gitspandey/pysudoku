"""
A simple backtracking based Sudoku solver
"""

import argparse
import copy
import itertools
import time

class SudokuSolver:
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.solution = None
        self.counter = 0
        self.time = 0

    def __set(self, grid, x, y, value):
        self.counter += 1
        grid[x][y] = value

    def __is_valid(self, grid, coords):
        seen = []
        for x, y in coords:
            if grid[x][y] in seen:
                return False
            seen.append(grid[x][y])
        return True

    def __get_row_coordinates(self, row):
        return itertools.product([row], range(9))

    def __get_col_coordinates(self, col):
        return itertools.product(range(9), [col])

    def __get_box_coordinates(self, row, col):
        return itertools.product(range(3 * (row // 3), 3 * (row // 3) + 3), range(3 * (col // 3), 3 * (col // 3) + 3))

    def is_valid(self, grid):
        # check all rows
        if any(not self.__is_valid(grid, self.__get_row_coordinates(x)) for x in range(9)):
            return False

        # check all columns
        if any(not self.__is_valid(grid, self.__get_col_coordinates(y)) for y in range(9)):
            return False

        # check all boxes
        if any(not self.__is_valid(grid, self.__get_box_coordinates(x, y)) for x, y in itertools.product(range(3), range(3))):
            return False

        return True

    def succ(self, x, y):
        # loop back to front of next line at the end of each line
        return x + (y + 1) // 9, (y + 1) % 9

    def __find_candidates(self, grid, x, y):
        """Find candidates for grid[x][y] by examining all its neighbours"""

        def __safe_remove(list_, value):
            if value in list_:
                list_.remove(value)

        candidates = list(range(1, 10))
        for x1, y1 in self.__get_row_coordinates(x):
            __safe_remove(candidates, grid[x1][y1])

        for x1, y1 in self.__get_col_coordinates(y):
            __safe_remove(candidates, grid[x1][y1])

        for x1, y1 in self.__get_box_coordinates(x, y):
            __safe_remove(candidates, grid[x1][y1])

        return candidates

    def __solve(self, grid, x, y):
        if x == 9:
            if self.is_valid(grid):
                self.solution = grid
                return True
            return False

        x1, y1 = self.succ(x, y)

        # if this is a known value, just go the next one
        if grid[x][y] != 0:
            return self.__solve(grid, x1, y1)

        # examine the row, column and box to find suitable candidates
        # then go through that list one-by-one until the right one is found
        newGrid = copy.deepcopy(grid)
        candidates = list(self.__find_candidates(newGrid, x, y))
        for c in candidates:
            self.__set(newGrid, x, y, c)
            if self.__solve(newGrid, x1, y1):
                return True
        return False

    def solve(self):
        start = time.time()
        result = self.__solve(copy.deepcopy(self.grid), 0, 0)
        self.time = time.time() - start
        return result

    def to_str(self, grid):
        # join three numbers in a row together
        __join_cells = lambda g, x, y: ' '.join(str(g[x][y]) for y in range(y, y + 3))

        # ..separated by a | after every 3 number
        __row_to_str = lambda g, x: ' | '.join([__join_cells(g, x, 3 * y) for y in range(3)])

        # join three rows together
        __section_to_str = lambda g, s: '\n'.join(__row_to_str(g, x) for x in range(3 * s, 3 * s + 3))

        # ..separated by a line of hyphens every 3 rows
        separator = '\n{}\n'.format('-' * 21)

        return separator.join(__section_to_str(grid, s) for s in range(3))

    def print_solution(self):
        print('\n{}\n'.format(self.to_str(self.solution)))

    def print_stats(self):
        print('Values set: {}'.format(self.counter))
        print('Time taken: {:.2f}s'.format(self.time))

def main():
    parser = argparse.ArgumentParser(description='Solve a Sudoku grid.')
    parser.add_argument('-f', '--file', dest='filename', help='Input file containing the grid to solve')

    args = parser.parse_args()

    grid = []
    if args.filename:
        with open(args.filename) as fin:
            for line in fin:
                grid.append([int(c) for c in line.rstrip('\n')])
    else:
        print('Enter the Sudoku grid to solve:')
        for _ in range(9):
            line = input()
            grid.append([int(c) for c in line.rstrip('\n')])
        print()

    print('Crunching numbers...')
    solver = SudokuSolver(grid)
    solver.solve()
    solver.print_solution()
    solver.print_stats()

if __name__ == "__main__" :
    main()
