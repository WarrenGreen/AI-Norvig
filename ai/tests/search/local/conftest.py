import math

import pytest

from ai.search.problem.problem import Problem


@pytest.fixture
def convex():
    class Convex(Problem):
        def generate_successors(self, state):
            yield state - 0.1
            yield state + 0.1

        def get_value(self, state):
            return math.sin(state)

        def is_terminal(self, state):
            return state >= 0.999

        def create_start(self):
            return 0.0

    return Convex()


@pytest.fixture
def convex_flat_negative():
    class Convex(Problem):
        def generate_successors(self, state):
            yield state - 0.1
            yield state + 0.1

        def get_value(self, state):
            if state < 0:
                return 0
            else:
                return math.sin(state)

        def is_terminal(self, state):
            return state >= 0.999

        def create_start(self):
            return -1.0

    return Convex()
