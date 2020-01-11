from collections import defaultdict
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

    @classmethod
    def random_world(cls, num_pits=3, size=4):
        positions = defaultdict(list)
        generated = 0
        while generated < num_pits:
            row = randint(size)
            col = randint(size)
            if row == 0 and col == 0:
                # Don't place pit in starting location
                continue
            positions[f"{row}{col}"].append(WumpusWorld.PIT)
            for successor in WumpusWorld._generate_successors(f"{row}{col}", size):
                positions[successor].append(WumpusWorld.BREEZE)

            generated += 1

        generated = 0
        while generated < 1:
            row = randint(size)
            col = randint(size)
            if row == 0 and col == 0:
                # Don't place wumpus in starting location
                continue
            positions[f"{row}{col}"] = WumpusWorld.WUMPUS
            generated += 1
            for successor in WumpusWorld._generate_successors(f"{row}{col}", size):
                positions[successor].append(WumpusWorld.STENCH)

        generated = 0
        while generated < 1:
            row = randint(size)
            col = randint(size)
            if WumpusWorld.WUMPUS in positions[f"{row}{col}"] or WumpusWorld.PIT in positions[f"{row}{col}"]:
                # Don't place gold in pit or with wumpus
                continue
            positions[f"{row}{col}"] = WumpusWorld.GOLD
            generated += 1

        return cls(positions, size)

    def generate_successors(self, state):
        for successor in WumpusWorld._generate_successors(state, self.size):
            yield successor

    @staticmethod
    def _generate_successors(state, size):
        row, col = int(state[0]), int(state[1])
        for row_delta in range(-1,2):
            for col_delta in range(-1, 2):
                if (row_delta == 0 and col_delta == 0) or size - 1 <= row + row_delta < 0 or size - 1 <= col + col_delta < 0:
                    continue
                yield f"{row + row_delta}{col + col_delta}"

    def get_value(self, state):
        return self.positions[state]

    def is_terminal(self, state):
        return WumpusWorld.GOLD in self.positions[state]

    def create_start(self):
        return WumpusWorld.random_world()
