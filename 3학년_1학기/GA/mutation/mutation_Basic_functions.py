import random
import copy
import math as mt 

#무작위 편차 돌연변이
def mutation_random_deviation(ind, mu, sigma, p):
    mut = copy.deepcopy(ind)
    for i in range(len(mut)):
        if random.random() < p:  #확률 계산
            mut[i] = mut[i] + random.gauss(mu, sigma)
    return mut

#교차 돌연변이
def mutation_exchange(ind):
    mut = copy.deepcopy(ind)
    pos = random.sample(range(0, len(mut)), 2) #돌연변이 지점 선택
    g1 = mut[pos[0]]
    g2 = mut[pos[1]]
    mut[pos[1]] = g1
    mut[pos[0]] = g2
    return mut

#mutation_shift
def mutation_shift(ind):
    mut = copy.deepcopy(ind)
    pos = random.sample(range(0, len(mut)), 2)
    g1 = mut[pos[0]]
    dir = int(mt.copysign(1, pos[1] - pos[0]))
    for i in range(pos[0], pos[1], dir):
        mut[i] = mut[i + dir]
        mut[pos[1]] = g1
    return mut

#dit flip mutation
def mutation_bit_flip(ind):
    mut = copy.deepcopy(ind)
    pos = random.randint(0, len(ind) - 1)
    print(pos)
    g1 = mut[pos]
    print(g1)
    print((g1 + 1) % 2)
    mut[pos] = (g1 + 1) % 2
    return mut