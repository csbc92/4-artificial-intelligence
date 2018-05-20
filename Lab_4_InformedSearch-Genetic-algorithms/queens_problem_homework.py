import random
import queens_fitness


p_mutation = 0.3
num_of_generations = 9


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''

    if not (len(mother) == len(father)):
        raise ValueError("Mother and Father must be of equal length")

    random_max = len(mother)
    random_crossover_point = random.randrange(0, random_max)

    child = list()

    # Take properties from the mother and give it to the child
    for index in range(0, random_crossover_point):
        child.append(mother[index])

    # Take properties from the father and give it to the child
    for index in range(random_crossover_point, random_max):
        child.append(father[index])

    return tuple(child)


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''

    mutation = list(individual)

    random_index_to_mutate = random.randrange(0, len(mutation))

    value = mutation[random_index_to_mutate]

    mutation_value = random.randint(1, 8)  # Each position can have a value from 1 to 8 (inclusive)
    while mutation_value == value:  # Mutate as many times as needed in order to not be the same value again
        mutation_value = random.randint(1, 8)

    mutation[random_index_to_mutate] = mutation_value

    return tuple(mutation)


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # The following code is inspired from the Java sample WIKI page: https://en.wikipedia.org/wiki/Fitness_proportionate_selection
    # but with modifications to fit a negative fitness value.
    # The approach is called roulette selection
    fitness_sum = 0
    for individual in population:
        fitness = fitness_fn(individual)

        fitness_sum += fitness

    # Pick two random selected individuals and and them to the set
    selected = set()
    while len(selected) < 2:
        random_selected = random.randint(fitness_sum, 0)

        for individual in population:
            random_selected -= fitness_fn(individual)
            if random_selected > 0:
                selected.add(individual)
                break

    return selected


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    # Returns an set of lists with values between 1 to 8 (inclusive)
    return set([
        tuple(random.randint(1, 8) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 0

    # This initial population is a set of samples of how a queens board is represented. Start index is at A1 (A one)
    # Each index is corresponding to column letter A, B, C, .., Z
    # Each value is corresponding to the row on the board below
    """initial_population = {(2, 4, 7, 4, 8, 5, 5, 2),
                          (3, 2, 7, 5, 2, 4, 1, 1),
                          (2, 4, 4, 1, 5, 1, 2, 4),
                          (3, 2, 5, 4, 3, 2, 1, 3)
                          }
    """
    """
    Example of a sample in initial population
        8|  |  |  |  |q |  |  |  |
        7|  |  |q |  |  |  |  |  |
        6|  |  |  |  |  |  |  |  |
        5|  |  |  |  |  |q |q |  |
        4|  |q |  |q |  |  |  |  |
        3|  |  |  |  |  |  |  |  |
        2| q|  |  |  |  |  |  |q |
        1|  |  |  |  |  |  |  |  |
          A  B  C  D  E  F  G  H
    """
    initial_population = get_initial_population(8, 3)

    fittest = genetic_algorithm(initial_population, queens_fitness.fitness_fn_negative, minimal_fitness)
    print('Fittest Individual: ' + str(fittest) + " - fitness: " + str(queens_fitness.fitness_fn_negative(fittest)))


if __name__ == '__main__':
    pass
    main()