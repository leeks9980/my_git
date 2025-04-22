import copy
import random
from multiprocessing import Pool
from typing import List

#교차 
def crossover_blend(p1, p2, alpha):     #(부모1, 부모2, 교차 범위)
    c1 = copy.deepcopy(p1)
    c2 = copy.deepcopy(p2)
    for i in range(len(p1)):
        l = min(c1[i], c2[i]) - alpha * abs(c2[i] - c1[i])
        u = max(c1[i], c2[i]) + alpha * abs(c2[i] - c1[i])
        c1[i] = round(l + random.random() * (u - l), 2)
        c2[i] = round(l + random.random() * (u - l), 2)
    return [c1, c2]

#돌연 변이
def mutation_random_deviation(ind, mu, sigma, p): 
    mut = copy.deepcopy(ind)
    for i in range(len(mut)):
        if random.random() < p:  #확률 계산
            mut[i] = mut[i] + random.gauss(mu, sigma)
    return mut

#선택
def selection_rank_with_elite(individuals, elite_size = 2):
    sorted_individuals = sorted(individuals, key = lambda ind:ind.fitness, reverse = True)
    rank_distance = 1 / len(individuals)
    ranks = [(1 - i * rank_distance) for i in range(len(individuals))]
    ranks_sum = sum(ranks)
    selected = sorted_individuals[0:elite_size]
    for i in range(len(sorted_individuals) - elite_size):
        shave = random.random() * ranks_sum
        rank_sum = 0
        for i in range(len(sorted_individuals)):
            rank_sum += ranks[i]
            if rank_sum > shave:
                selected.append(sorted_individuals[i])
                break
    return selected

#확률적 교차 실행      
def crossover_operation(population, method, prob):  #(집단, 교차방법, 확률)
    pool = Pool()
    crossed_offspring = []
    to_cross = []
    result = []
    
    for ind1, ind2 in zip(population[::2], population[1::2]):
        if random.random() < prob:
            to_cross.extend([ind1, ind2])
        else:
            crossed_offspring.extend([ind1, ind2])
    
    for i in range(0, len(to_cross), 2):
        result.append(
            pool.apply_async(method, args=(to_cross[i], to_cross[i + 1]))
        )
    for r in result:
        crossed_offspring.extend(r.get())
    
    pool.close()
    pool.join()

    return crossed_offspring

#확률적으로 돌연변이 실행  *돌연변이는 원래 확률 적으로 일어나지만 계산량이 많을 경우 대비
def mutation_operation(population, method, prob):  #(집단, 교차방법, 확률)
    pool = Pool()
    mutated_offspring = []
    to_mutate = []
    result = []
    
    for ind in population:
        if random.random() < prob:
            to_mutate.append(ind)
        else:
            mutated_offspring.append(ind)
    
    for ind in to_mutate:
        result.append(pool.apply_async(method, args=(ind,)))
    
    for r in result:
        mutated_offspring.append(r.get())
    
    pool.close()
    pool.join()
    return mutated_offspring

#영역 설정
def constraints(x): 
    if x > 10:
        return 10
    elif x < -10:
        return -10
    return x
