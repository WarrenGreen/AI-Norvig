import math
from collections import defaultdict, namedtuple
from copy import deepcopy
from random import randint
from typing import NamedTuple, List

from ai.search.exception import InputException
from ai.search.problem.grid import GridProblem, GridLocation
from ai.search.problem.problem import Problem


WumpusLocation = namedtuple(
    "WumpusLocation",
    [*GridLocation._fields, "pit", "breeze", "gold", "wumpus", "stench"],
)
# Hacky default values for python 3.6
WumpusLocation.__new__.__defaults__ = GridLocation.__new__.__defaults__ + (False,) * 5


class WumpusWorld(GridProblem):
    VISUALIZATION_STRING = "| {0:>20} "

    def __init__(self, grid):
        super().__init__(grid)
        self.num_pits = 0
        for row in range(self.row_size):
            for col in range(self.col_size):
                if self.grid[row][col].pit:
                    self.num_pits += 1

        self.pit_probability = self.num_pits / (self.row_size * self.col_size)
        self.wumpus_probability = 1.0 / (self.row_size * self.col_size)

    @classmethod
    def random_world(cls, starting_location=(0, 0), num_pits=1, row_size=3, col_size=3):
        grid: List[List[NamedTuple]] = []
        for row_index in range(3):
            row = []
            for col_index in range(4):
                row.append(WumpusLocation(row_index, col_index))
            grid.append(row)

        generated = 0
        pit_locations = set()
        while generated < num_pits:
            row = randint(0, row_size - 1)
            col = randint(0, col_size - 1)
            if (row, col) == starting_location:
                # Don't place pit in starting location
                continue
            grid[row][col] = grid[row][col]._replace(pit=True)
            pit_locations.add((row, col))
            for successor_row, successor_col in WumpusWorld._generate_successors(
                (row, col), row_size, col_size
            ):
                grid[successor_row][successor_col] = grid[successor_row][
                    successor_col
                ]._replace(breeze=True)
            generated += 1

        generated = 0
        wumpus_location = set()
        while generated < 1:
            row = randint(0, row_size - 1)
            col = randint(0, col_size - 1)
            if (row, col) == starting_location:
                # Don't place wumpus in starting location
                continue
            grid[row][col] = grid[row][col]._replace(wumpus=True)
            wumpus_location.add((row, col))
            generated += 1
            for successor_row, successor_col in WumpusWorld._generate_successors(
                (row, col), row_size, col_size
            ):
                grid[successor_row][successor_col] = grid[successor_row][
                    successor_col
                ]._replace(stench=True)

        generated = 0
        while generated < 1:
            row = randint(0, row_size - 1)
            col = randint(0, col_size - 1)
            if (row, col) in pit_locations or (row, col) in wumpus_location:
                # Don't place gold in pit or with wumpus
                continue
            grid[row][col] = grid[row][col]._replace(gold=True)
            generated += 1

        return cls(grid)

    @classmethod
    def default_world(cls):
        """
        | []                   | ['breeze', 'stench'] | ['wumpus']            |
        | ['breeze']           | ['pit']              | ['breeze', 'stench']  |
        | []                   | ['breeze']           | ['gold']              |

        """
        row_size = 3
        col_size = 3
        grid = []
        for row_index in range(row_size):
            row = []
            for col_index in range(col_size):
                row.append(WumpusLocation(row_index, col_index))
            grid.append(row)
        grid[0][0] = grid[0][0]._replace(start=True)
        grid[1][1] = grid[1][1]._replace(pit=True)
        grid[0][2] = grid[0][2]._replace(wumpus=True)
        grid[2][2] = grid[2][2]._replace(gold=True)
        for row in range(row_size):
            for col in range(col_size):
                if grid[row][col].pit:
                    for (
                        successor_row,
                        successor_col,
                    ) in WumpusWorld._generate_successors(
                        (row, col), row_size, col_size
                    ):
                        grid[successor_row][successor_col] = grid[successor_row][
                            successor_col
                        ]._replace(breeze=True)

                if grid[row][col].pit:
                    for (
                        successor_row,
                        successor_col,
                    ) in WumpusWorld._generate_successors(
                        (row, col), row_size, col_size
                    ):
                        grid[successor_row][successor_col] = grid[successor_row][
                            successor_col
                        ]._replace(stench=True)

        return cls(grid)

    @staticmethod
    def _generate_successors(state, row_size, col_size):
        row, col = state
        for row_delta, col_delta in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if row_delta == 0 and col_delta == 0:
                continue
            if row_size <= row + row_delta or row + row_delta < 0:
                continue
            if col_size <= col + col_delta or col + col_delta < 0:
                continue
            yield (row + row_delta, col + col_delta)

    def get_value(self, state):
        row, col = state
        return self.grid[row][col]

    def create_start(self):
        return WumpusWorld.random_world()

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
                if not self.grid[row][col].navigable:
                    col_str += WumpusWorld.VISUALIZATION_STRING.format("==========")
                else:
                    output_dict = [
                        key
                        for key, val in self.grid[row][col]._asdict().items()
                        if isinstance(val, bool) and val and key != "navigable"
                    ]
                    col_str += WumpusWorld.VISUALIZATION_STRING.format(str(output_dict))
            col_str += " |"
            print(col_str)

        print()
        print("Path Followed")
        for row in range(self.row_size):
            col_str = ""
            for col in range(self.col_size):
                if (row, col) in path:
                    col_str += WumpusWorld.VISUALIZATION_STRING.format("X")
                elif not self.grid[row][col].navigable:
                    col_str += WumpusWorld.VISUALIZATION_STRING.format("==========")
                else:
                    output_dict = [
                        key
                        for key, val in self.grid[row][col]._asdict().items()
                        if isinstance(val, bool) and val and key != "navigable"
                    ]
                    col_str += WumpusWorld.VISUALIZATION_STRING.format(str(output_dict))
            col_str += " |"
            print(col_str)
