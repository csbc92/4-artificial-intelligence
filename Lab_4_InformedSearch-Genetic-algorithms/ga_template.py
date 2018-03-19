import random


p_mutation = 0.2
num_of_generations = 30


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

    random_bit_to_flip = random.randrange(0, len(mutation))

    value = mutation[random_bit_to_flip]

    if value == 1:
        value = 0
    elif value == 0:
        value = 1

    mutation[random_bit_to_flip] = value

    return tuple(mutation)


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.
    #ordered_population = list(population)

    list = []

    # Append the individual elements with highest fitness level to a list
    fitness_sum = 0
    for individual in population:
        fitness = fitness_fn(individual)

        for index in range(fitness_sum, len(list) + fitness):
            list.insert(index, individual)

        fitness_sum += fitness

    # Pick two random selected individuals and and them to the set
    selected = set()
    while len(selected) < 2:
        random_selected = random.randrange(0, fitness_sum)
        selected.add(list[random_selected])

    return selected


def fitness_function(individual):
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''
    pairs = enumerate(reversed(individual))

    fitness = 0

    for bit in pairs:
        if bit[1] == 1:
            fitness += pow(2, bit[0])

    return fitness


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }
    initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    pass
    main()