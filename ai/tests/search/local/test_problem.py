import pytest

from ai.search.local.problem import EightQueens


@pytest.fixture
def eight_queens():
    return EightQueens()


class TestEightQueens:
    def test_generate_successor(self):
        for size in range(4, 12):
            queens = EightQueens(size=size)
            state = queens.create_start()
            set_state_1 = set(enumerate(state))
            state_gen = queens.generate_successors(state)
            for _ in range(10):
                set_state_2 = set(enumerate(next(state_gen)))
                diff = set_state_1 - set_state_2
                assert len(diff) == 1

    def test_get_value(self, eight_queens):
        assert eight_queens.get_value([4, 5, 6, 3, 4, 5, 6, 5]) == -17
        assert eight_queens.get_value([7, 2, 6, 3, 1, 4, 0, 5]) == -1

        problem_2 = EightQueens(size=2)
        assert problem_2.get_value([0, 1]) == -1
