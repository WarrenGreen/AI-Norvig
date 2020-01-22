from ai.search.adversarial.alpha_beta import search
from ai.problem.tictactoe import TicTacToe


def test_alpha_beta():
    problem_o = TicTacToe(player="O")
    problem_x = TicTacToe(player="X")
    state = problem_x.create_start()
    x_turn = True
    while not problem_x.is_terminal(state):
        if x_turn:
            problem = problem_x
        else:
            problem = problem_o

        x_turn = not x_turn
        new_state, new_value = search(problem, state)
        state = new_state

    assert new_value == 0
