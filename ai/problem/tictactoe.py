import math
from collections import defaultdict
from copy import copy

from ai.search.exception import InputException
from ai.problem import Problem


class TicTacToe(Problem):
    SIZE = 3
    PLAYER_VALUES = ["X", "O"]

    def __init__(self, player="X"):
        self.player = player

    def get_value(self, state):
        for winning_indices in [
            (0, 1, 2),  # rows
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),  # cols
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),  # diagonals
            (6, 4, 2),
        ]:
            if (
                state[winning_indices[0]]
                == state[winning_indices[1]]
                == state[winning_indices[2]]
                is not None
            ):
                if state[winning_indices[0]] == self.player:
                    return 1
                else:
                    return -1

        if None in state:
            raise InputException("Not a valid terminal state.")

        return 0

    def is_terminal(self, state):
        try:
            self.get_value(state)
        except InputException:
            return False
        else:
            return True

    def generate_successors(self, state):
        placement_count = defaultdict(lambda: 0)
        for value in state:
            placement_count[value] += 1

        if (
            placement_count[TicTacToe.PLAYER_VALUES[0]]
            <= placement_count[TicTacToe.PLAYER_VALUES[1]]
        ):
            current_turn = TicTacToe.PLAYER_VALUES[0]
        else:
            current_turn = TicTacToe.PLAYER_VALUES[1]
        for index, value in enumerate(state):
            if value is None:
                new_state = copy(state)
                new_state[index] = current_turn
                yield new_state

    def create_start(self):
        return [None] * int(math.pow(TicTacToe.SIZE, 2))

    def format_str(self, state):
        out_str = ""
        for rows in range(TicTacToe.SIZE):
            formatted_row = [
                x if x is not None else " "
                for x in state[rows * TicTacToe.SIZE : (rows + 1) * TicTacToe.SIZE]
            ]
            out_str += str(formatted_row) + "\n"

        return out_str
