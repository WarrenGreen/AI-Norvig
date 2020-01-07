from ai.search.adversarial.minimax import search
from ai.search.problem.tictactoe import TicTacToe


def main():
    problem_o = TicTacToe(player="O")
    problem_x = TicTacToe(player="X")
    state = problem_x.create_start()
    print(problem_x.format_str(state))
    x_turn = True
    while not problem_x.is_terminal(state):
        if x_turn:
            problem = problem_x
        else:
            problem = problem_o

        x_turn = not x_turn
        new_state, new_value = search(problem, state,)
        state = new_state
        print(problem.format_str(new_state), f"value for player x: {new_value}\n")


if __name__ == "__main__":
    main()
