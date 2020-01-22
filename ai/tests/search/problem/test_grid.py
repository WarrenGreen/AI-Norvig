import pytest

from ai.search.problem.grid import GridProblem


class TestEightQueens:
    def test_create_start(self):
        problem = GridProblem.create_start()
        assert problem.start_location == (2, 0)
        assert problem.get_value((0, 3)) == 1.0
        assert problem.get_value((1, 3)) == -1.0

    def test_generate_successor(self):
        problem = GridProblem.create_start()
        successors = []
        for successor in problem.generate_successors((1, 0)):
            successors.append(successor)

        assert len(successors) == len(set(successors))
        assert set(successors) == {problem.grid[2][0], problem.grid[0][0]}
