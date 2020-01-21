from random import randint, random

from numpy.random import choice


def search(population, fitness_fn, fitness_cutoff=1.0, mutation_rate=0.01):
    """

    Args:
        fitness_fn (Callable[List[int], float]): function to evaluate a state. Fitness should
            be a float in range [0, 1]
        population (List[List[int]]): Initial population
        fitness_cutoff (float): maximum acceptable error for a solution

    Returns:
        Tuple[List, int] solution state and solution value
    """
    if population is None:
        population = []

    fitness = None
    fittest_state = None
    while fitness is None or fitness < fitness_cutoff:
        new_population = []
        for _ in population:
            parent_1, parent_2 = random_proportional_choice(population, fitness_fn, 2)
            child = mate(parent_1, parent_2)
            if random() <= mutation_rate:
                child = mutate(child)
            new_population.append(child)
        population = new_population
        for state in population:
            new_fitness = fitness_fn(state)
            if fitness is None or new_fitness > fitness:
                fitness = new_fitness
                fittest_state = state

    return fittest_state


def mutate(state):
    index = randint(0, len(state)-1)
    if random() > 0.50:
        state[index] += 1
    else:
        state[index] -= 1

    return state


def mate(parent_1, parent_2):
    cut = randint(0, len(parent_1))
    return parent_1[:cut] + parent_2[cut:]


def random_proportional_choice(population, fitness_fn, number_of_choices):
    """
    Selects a item at random in proportion to that items fitness value without
    replacement

    Args:
        population (List(str):
        fitness_fn:
        number_of_choices: number of choices to return

    Returns:
        Tuple[str] - item from population
    """
    fitnesses = []
    total_fitness = 0.0
    for state in population:
        fitness = fitness_fn(state)
        fitnesses.append(fitness)
        total_fitness += fitness

    for index in range(len(fitnesses)):
        fitnesses[index] /= total_fitness

    picks = choice(list(range(len(population))), number_of_choices, p=fitnesses, replace=False)

    pop_picks = []
    for index in picks:
        pop_picks.append(population[index])
    return pop_picks
