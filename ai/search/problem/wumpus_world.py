import math
from collections import defaultdict
from copy import deepcopy
from random import randint

from ai.search.problem.problem import Problem


class WumpusWorld(Problem):
    PIT = "pit"
    BREEZE = "breeze"
    GOLD = "gold"
    WUMPUS = "wumpus"
    STENCH = "stench"

    def __init__(self, positions, size):
        self.positions = positions
        self.size = size
        self.num_pits = 0
        for _, labels in positions.items():
            if WumpusWorld.PIT in labels:
                self.num_pits += 1

        self.pit_probability = self.num_pits / math.pow(self.size, 2.0)
        self.wumpus_probability = 1.0 / math.pow(self.size, 2.0)

    @classmethod
    def random_world(cls, num_pits=1, size=3):
        positions = defaultdict(list)
        generated = 0
        while generated < num_pits:
            row = randint(0, size-1)
            col = randint(0, size-1)
            if row == 0 and col == 0:
                # Don't place pit in starting location
                continue
            positions[f"{row},{col}"].append(WumpusWorld.PIT)
            for successor in WumpusWorld._generate_successors(f"{row},{col}", size):
                if WumpusWorld.BREEZE not in positions[successor]:
                    positions[successor].append(WumpusWorld.BREEZE)

            generated += 1

        generated = 0
        while generated < 1:
            row = randint(0, size-1)
            col = randint(0, size-1)
            if row == 0 and col == 0:
                # Don't place wumpus in starting location
                continue
            positions[f"{row},{col}"].append(WumpusWorld.WUMPUS)
            generated += 1
            for successor in WumpusWorld._generate_successors(f"{row},{col}", size):
                if WumpusWorld.STENCH not in positions[successor]:
                    positions[successor].append(WumpusWorld.STENCH)

        generated = 0
        while generated < 1:
            row = randint(0, size-1)
            col = randint(0, size-1)
            if WumpusWorld.WUMPUS in positions[f"{row},{col}"] or WumpusWorld.PIT in positions[f"{row},{col}"]:
                # Don't place gold in pit or with wumpus
                continue
            positions[f"{row},{col}"].append(WumpusWorld.GOLD)
            generated += 1

        return cls(positions, size)

    @classmethod
    def default_world(cls):
        """
        | []                   | ['breeze', 'stench'] | ['wumpus']            |
        | ['breeze']           | ['pit']              | ['breeze', 'stench']  |
        | []                   | ['breeze']           | ['gold']              |

        """
        size = 3
        positions = defaultdict(list)
        positions["1,1"] = [WumpusWorld.PIT]
        positions["0,2"] = [WumpusWorld.WUMPUS]
        positions["2,2"] = [WumpusWorld.GOLD]
        for position, flags in deepcopy(positions).items():
            if WumpusWorld.PIT in flags:
                for successor in WumpusWorld._generate_successors(position, size):
                    positions[successor].append(WumpusWorld.BREEZE)

            if WumpusWorld.WUMPUS in flags:
                for successor in WumpusWorld._generate_successors(position, size):
                    positions[successor].append(WumpusWorld.STENCH)

        return cls(positions, size)

    def generate_successors(self, state):
        for successor in WumpusWorld._generate_successors(state, self.size):
            yield successor

    @staticmethod
    def _generate_successors(state, size):
        row, col = WumpusWorld.parse_state(state)
        for row_delta, col_delta in [(-1,0), (1,0), (0,1), (0,-1)]:
            if row_delta == 0 and col_delta == 0:
                continue
            if size <= row + row_delta or row + row_delta < 0:
                continue
            if size <= col + col_delta or col + col_delta < 0:
                continue
            yield f"{row + row_delta},{col + col_delta}"

    @staticmethod
    def parse_state(state):
        state_split = state.split(",")
        return int(state_split[0]), int(state_split[1])

    def get_value(self, state):
        return self.positions[state]

    def is_terminal(self, state):
        return WumpusWorld.GOLD in self.positions[state]

    def create_start(self):
        return WumpusWorld.random_world()

    def visualize(self, path):
        """
        Visualize the Wumpus World with the given path
        Args:
            path List[str]: Lists of node definitions
        """
        print("Initial Map")
        for row in range(self.size):
            col_str = ""
            for col in range(self.size):
                if row == 0 and col ==0:
                    col_str += "| {0:20} ".format(str(self.positions[f"{row},{col}"]+['start']))
                else:
                    col_str += "| {0:20} ".format(str(self.positions[f"{row},{col}"]))
            col_str += " |"
            print(col_str)

        print()
        print("Path Followed")
        for row in range(self.size):
            col_str = ""
            for col in range(self.size):
                loc = f"{row},{col}"
                if loc in path:
                    col_str += "| {0:20} ".format("X")
                else:
                    col_str += "| {0:20} ".format(str(self.positions[loc]))
            col_str += " |"
            print(col_str)
