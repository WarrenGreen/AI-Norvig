from collections import defaultdict
from copy import copy
from random import randint

from ai.problem import Problem


class EightQueens(Problem):
    def __init__(self, *, size=8):
        """

        Args:
             size (int): size of board square
        """
        self.size = size

    def create_start(self):
        state = []
        for _ in range(self.size):
            row = randint(0, self.size - 1)
            state.append(row)

        return state

    def generate_successors(self, state):
        successors = set()
        while len(successors) < 56:
            col = randint(0, self.size - 1)
            current_row = int(state[col])
            row = randint(0, self.size - 1)
            while row == current_row:
                row = randint(0, self.size - 1)

            new_state = copy(state)
            new_state[col] = row
            if str(new_state) in successors:
                continue

            successors.add(str(new_state))
            yield new_state

    def get_value(self, state):
        collisions = set()
        used_rows = defaultdict(list)
        for col, row in enumerate(state):
            # row collision
            for collision_col in used_rows[row]:
                collisions.add((col, collision_col))
                collisions.add((collision_col, col))

            used_rows[row].append(col)

            # diagonal collision
            for col_delta, row_delta in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                check_col = col + col_delta
                check_row = row + row_delta
                while 0 <= check_col < self.size and 0 <= check_row < self.size:
                    if state[check_col] == check_row:
                        collisions.add((col, check_col))
                        collisions.add((check_col, col))
                    check_col = check_col + col_delta
                    check_row = check_row + row_delta

        return -(len(collisions) // 2)
