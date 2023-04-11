import random
import items
import matplotlib.pyplot as plt

rec_prob = 0.8  # given
mut_prob = 0.1  # given

# Ordinal number / Weight / Value
file_name = "items"

weight_limit = 71

population_size = 10  # kinda obvious given the data
generation_size = 20  # given

item_list = []
with open(file_name, "r") as file:
    for line in file:
        new_line = line.strip()
        new_line = new_line.split(" ")
        id, weight, value = new_line[0], new_line[1], new_line[2]
        new_item = items.Item(int(id), int(weight), int(value))
        item_list.append(new_item)


# item_list -> original item list
# i_list -> item list
# s_list -> solutions as list

def create_random_solution(i_list):
    solution = []
    for i in range(0, len(i_list)):
        solution.append(random.randint(0, 1))
    return solution


# check if sum of weight is lower than the limit
def check_if_valid_solution(i_list, s_list, limit):
    total_weight = 0
    for i in range(0, len(s_list)):
        if s_list[i] == 1:
            total_weight += i_list[i].weight
        if total_weight > limit:
            return False
    return True


# calculate value of picked items
def calculate_value(i_list, s_list):
    total_value = 0
    for i in range(0, len(s_list)):
        if s_list[i] == 1:
            total_value += i_list[i].value
    return total_value


def calculate_weight(i_list, s_list):
    total_weight = 0
    for i in range(0, len(s_list)):
        if s_list[i] == 1:
            total_weight += i_list[i].weight
    return total_weight


def check_for_duplicate_solution(solution1, solution2):
    for i in range(0, len(solution1)):
        if solution1[i] != solution2[i]:
            return False
    return True


def create_initial_population(pop_size, i_list, w_limit):
    population = []
    i = 0
    while i < pop_size:
        new_solution = create_random_solution(i_list)
        if check_if_valid_solution(i_list, new_solution, w_limit):
            if len(population) == 0:  # if population list is empty
                population.append(new_solution)
                i += 1
            else:
                skip_flag = False
                for j in range(0, len(population)):
                    if check_for_duplicate_solution(new_solution, population[j]):
                        skip_flag = True
                        continue
                if not skip_flag:
                    population.append(new_solution)
                    i += 1
    return population


def tournament_selection(pop):
    specimen_id_1 = random.randint(0, len(pop) - 1)
    specimen_id_2 = random.randint(0, len(pop) - 1)
    if calculate_value(item_list, pop[specimen_id_1]) > calculate_value(item_list, pop[specimen_id_2]):
        winner = pop[specimen_id_1]
    else:
        winner = pop[specimen_id_2]

    return winner


# simplest crossover aaaaa / bbbbb -> aabbb or abbbb or aaaab etc.
def crossover(parent1, parent2):
    breakoff_point = random.randint(0, len(parent1))
    first_part = parent1[:breakoff_point]
    second_part = parent2[breakoff_point:]
    child = first_part + second_part
    if check_if_valid_solution(item_list, child, weight_limit):
        return child
    else:
        # loopy-de loop
        return crossover(parent1, parent2)


# WhyTF last line in this block
def mutation(chromosome):  # GIVE ME CHROMOSOMES!!! YEAH, BUT LIKE, I HAVE LIKE 2 ATM...
    temp = chromosome
    mutation_id_1, mutation_id_2 = random.sample(range(0, len(chromosome)), 2)
    temp[mutation_id_1], temp[mutation_id_2] = temp[mutation_id_2], temp[mutation_id_1]

    if check_if_valid_solution(item_list, temp, weight_limit):
        return temp
    else:
        return mutation(chromosome)


# Not exactly following the task here
def create_generation(pop, mutation_rate, recombination_rate):
    new_gen = []
    for i in range(0, len(pop)):
        parent1 = tournament_selection(pop)
        parent2 = tournament_selection(pop)
        child = crossover(parent1, parent2)

        if random.random() < mutation_rate:
            child = mutation(child)

        new_gen.append(child)
    return new_gen


def best_solution(generation, i_list):
    best_value = 0
    best_weight = 0
    for i in range(0, len(generation)):
        temp_value = calculate_value(i_list, generation[i])
        temp_weight = calculate_weight(i_list, generation[i])

        if temp_value > best_value:
            best_value = temp_value
            best_weight = temp_weight

        return best_value, best_weight


value_list = []
weight_list = []


def genetic_algorithm(w_limit, p_size, gen_size, mut_prob, i_list):
    pop = create_initial_population(p_size, i_list, w_limit)
    for i in range(0, gen_size):
        pop = create_generation(pop, mut_prob, rec_prob)
        print(pop[0])

        print("VALUE:   ", calculate_value(i_list, pop[0]))
        print("WEIGHT:  ", calculate_weight(i_list, pop[0]))

        best_value, best_weight = best_solution(pop, i_list)
        value_list.append(best_value)
        weight_list.append(best_weight)

    return pop, value_list, weight_list


latest_pop, v_list, w_list = genetic_algorithm(w_limit=weight_limit,
                                               p_size=population_size,
                                               gen_size=generation_size,
                                               mut_prob=mut_prob,
                                               i_list=item_list)

plt.plot(v_list)
plt.xlabel('generations')
plt.ylabel('values')
plt.title("Values of the solutions during the generations")
plt.show()

plt.plot(w_list)
plt.xlabel('generations')
plt.ylabel('weight')
plt.title("Weight of the solutions during the generations")
plt.show()
