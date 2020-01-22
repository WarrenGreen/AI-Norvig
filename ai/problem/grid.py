from collections import namedtuple
from typing import Tuple

from ai.search.exception import InputException
from ai.problem.problem import Problem


GridLocation = namedtuple(
    "GridLocation", ["row", "col", "value", "terminal", "navigable", "start"]
)
# Hacky default values for python 3.6
GridLocation.__new__.__defaults__ = (0, 0, 0.0, False, True, False)


class GridProblem(Problem):
    VISUALIZATION_STRING = "| {0:>10} "

    UP = (-1, 0)
    LEFT = (1, 0)
    RIGHT = (0, 1)
    DOWN = (0, -1)
    STAY = (0, 0)

    def __init__(self, grid):
        """

        Args:
            grid (List[List[GridLocation]): 2-dimensional grid with GridLocation
        """
        self.grid = grid
        self.row_size = len(grid)
        self.col_size = len(grid[0])
        self.start_location = None
        for row in range(self.row_size):
            for col in range(self.col_size):
                if self.grid[row][col].start:
                    self.start_location = (row, col)
                    break

        if self.start_location is None or len(self.start_location) < 2:
            raise InputException("Start location must be of format: (row, col).")

    def get_value(self, state):
        row, col = state
        return self.grid[row][col].value

    @classmethod
    def create_start(cls):
        # 4x3 world described in Chapter 21
        grid = []
        for row_index in range(3):
            row = []
            for col_index in range(4):
                row.append(GridLocation(row_index, col_index, -0.01))
            grid.append(row)

        grid[0][3] = grid[0][3]._replace(value=1.0, terminal=True)
        grid[1][3] = grid[1][3]._replace(value=-1.0, terminal=True)

        grid[1][1] = grid[1][1]._replace(value=0.0, navigable=False)
        grid[2][0] = grid[2][0]._replace(start=True)

        return cls(grid)

    def generate_successors(self, state: Tuple[int, int]):
        for action in self.generate_actions(state):
            yield self.apply_action(state, action)

    def valid_action(self, state, action):
        row_delta, col_delta = action
        row, col = state
        if self.row_size <= row + row_delta or row + row_delta < 0:
            return False
        if self.col_size <= col + col_delta or col + col_delta < 0:
            return False
        if not self.grid[row + row_delta][col + col_delta].navigable:
            return False

        return True

    def generate_actions(self, state):
        for row_delta, col_delta in [GridProblem.UP, GridProblem.LEFT,
                                     GridProblem.RIGHT, GridProblem.DOWN,
                                     GridProblem.STAY]:
            if self.valid_action(state, (row_delta, col_delta)):
                yield (row_delta, col_delta)

    def apply_action(self, state, action):
        if self.valid_action(state, action):
            row, col = state
            row_delta, col_delta = action
            return row + row_delta, col + col_delta
        else:
            return state

    def is_terminal(self, state):
        row, col = state
        return self.grid[row][col].terminal

    def visualize(self, path):
        """
        Visualize the grid with the given path
        Args:
            path List[Tuple[int, int]]: Lists of locations
        """
        print("Initial Grid")
        for row in range(self.row_size):
            col_str = ""
            for col in range(self.col_size):
                if row == self.start_location[0] and col == self.start_location[1]:
                    col_str += GridProblem.VISUALIZATION_STRING.format("start")
                elif not self.grid[row][col].navigable:
                    col_str += GridProblem.VISUALIZATION_STRING.format("==========")
                else:
                    col_str += GridProblem.VISUALIZATION_STRING.format(
                        str(self.grid[row][col].value)
                    )
            col_str += " |"
            print(col_str)

        print()
        print("Path Followed")
        for row in range(self.row_size):
            col_str = ""
            for col in range(self.col_size):
                if (row, col) in path:
                    col_str += GridProblem.VISUALIZATION_STRING.format("X")
                elif not self.grid[row][col].navigable:
                    col_str += GridProblem.VISUALIZATION_STRING.format("==========")
                else:
                    col_str += GridProblem.VISUALIZATION_STRING.format(
                        str(self.grid[row][col].value)
                    )
            col_str += " |"
            print(col_str)
