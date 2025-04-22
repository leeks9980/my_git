import random
from typing import List
import multiprocessing
from numpy import arange
import matplotlib.pyplot as plt
from pylab import meshgrid, cm
from toolbox import *

#프로세스 작동 방식 변경 (하지 않을 경우 다른 함수들을 찾지 못함)
multiprocessing.set_start_method("spawn", force=True)

#적합도 함수
def func(x, y):
    return - 10 * pow(x * y, 2) * x / (3 * pow(x * x * x / 4 + 1, 2)+ pow(y, 4) + 1)

#Structure of individual
class Individual:
    def __init__(self, gene_list: List[float]) -> None:
        self.gene_list = [constraints(g) for g in gene_list] #유전자 값이 특정 범위를 넘지 못하게 지정
        self.fitness = func(self.gene_list[0], self.gene_list[1])
    def __str__(self):
        return f'x: {self.gene_list[0]}, y: {self.gene_list[0]}, fitness:{self.fitness}'

#basic GA operations
#교차 방법 지정
def crossover(parent1, parent2):
    child1_genes, child2_genes = crossover_blend(parent1.gene_list,parent2.gene_list, 0.5)
    return Individual(child1_genes), Individual(child2_genes)

#돌연변이 방법 지정
def mutate(ind):
    mutated_gene = mutation_random_deviation(ind.gene_list, 0, 1, 0.5)
    return Individual(mutated_gene)

#선택방법 지정
def select(population):
    return selection_rank_with_elite(population, elite_size = 4)

#모집단 생성
def create_random():
    return Individual([round(random.uniform(-10, 10), 2),round(random.uniform(-10, 10), 2)])

#메인 코드 
if __name__ == "__main__": 
    #Parameter set
    POPULATION_SIZE_LIST = [6, 10, 20, 50] #모집단 크기  모집단 크기에 따라 달라지는 결과값 확인하기 위함
    CROSSOVER_PROBABILITY = .8 #교차 확률
    MUTATION_PROBABILITY = .2 #돌연변이 확룰
    MAX_GENERATIONS = 10 #알고리즘 반복 횟수

    X_range = arange(-10, 10, 0.2)        # x축 범위 생성
    Y_range = arange(-10, 10, 0.2)        # y축 범위 생성
    #영역내 모든 적합도 값 계산
    X, Y = meshgrid(X_range, Y_range)     # 2차원 격자 좌표 생성
    Z = func(X, Y)                        # 목적 함수의 함수값 계산 (히트맵용)


    for POPULATION_SIZE in POPULATION_SIZE_LIST:
        first_population = [create_random() for _ in range(POPULATION_SIZE)]
        best_ind = random.choice(first_population)
        generation_number = 0           #반복횟수 최기화
        population = first_population.copy()

        while generation_number < MAX_GENERATIONS:
            generation_number += 1          #반복 횟수 탐지
            offspring = select(population)          #선택 단계
            crossed_offspring = crossover_operation(offspring, crossover, CROSSOVER_PROBABILITY)            #교차 단계
            mutated_offspring = mutation_operation(crossed_offspring, mutate, MUTATION_PROBABILITY)         #돌연변이 단계
            population = mutated_offspring.copy() # 다음 세대 생성

            #적합고 계산
            best_of_generation = max(population, key=lambda ind: ind.fitness)  
            if best_ind.fitness < best_of_generation.fitness:
                best_ind = best_of_generation

            #시각화
            im = plt.imshow(Z, cmap=cm.bwr, extent=[-10, 10, -10, 10]) #적합도에 따리 영역표시
            plt.colorbar(im)
            plt.xticks([])
            plt.yticks([])
            plt.title(f"Population size: {POPULATION_SIZE}, Generation: {generation_number} \n"
                      f"Best Individual: {round(best_ind.fitness, 2)}")
            plt.scatter([ind.gene_list[0] for ind in population], 
                        [ind.gene_list[1] for ind in population], 
                        color='black')
            plt.show()