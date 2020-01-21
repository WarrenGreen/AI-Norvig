import argparse

from ai.search.local.genetic_algorithm import search
from ai.search.problem.eight_queens import EightQueens


def main(config):
    problem = EightQueens(size=config.size)
    def fitness(state):
        return problem.get_value(state)

    population = []
    for _ in range(config.pop_size):
        population.append(problem.create_start())
    print(search(population, fitness, fitness_cutoff=0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run hill climber solver on eight queens."
    )
    parser.add_argument(
        "--size", type=int, default=8, help="Size of queens board square",
    )
    parser.add_argument(
        "--pop_size", type=int, default=8, help="Size of population",
    )

    main(parser.parse_args())