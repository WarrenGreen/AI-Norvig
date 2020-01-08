from ai.search.adversarial.minimax import search
from ai.search.problem.chess import Chess


def main():
    problem = Chess()
    state = problem.create_start()
    while not problem.is_terminal(state):
        new_state, new_value = search(problem, state)
        state = new_state


if __name__ == "__main__":
    main()
