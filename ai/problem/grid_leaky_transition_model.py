from random import random

from ai.problem.grid import GridProblem


class GridLeakyTransitionModelProblem(GridProblem):
    PERP = {
        GridProblem.UP: [GridProblem.LEFT, GridProblem.RIGHT],
        GridProblem.DOWN: [GridProblem.LEFT, GridProblem.RIGHT],
        GridProblem.LEFT: [GridProblem.UP, GridProblem.DOWN],
        GridProblem.RIGHT: [GridProblem.UP, GridProblem.DOWN],
        GridProblem.STAY: [GridProblem.UP, GridProblem.DOWN]
    }

    def apply_action(self, state, action):
        """ 0.8 success, 0.1 for either perpendicular direction """
        row, col = state
        r = random()
        if r <= 0.8:
            row_delta, col_delta = action
        elif r <= 0.9:
            row_delta, col_delta = GridLeakyTransitionModelProblem.PERP[action][0]
        else:
            row_delta, col_delta = GridLeakyTransitionModelProblem.PERP[action][1]

        if self.valid_action(state, (row_delta, col_delta)):
            return row + row_delta, col + col_delta
        else:
            return state