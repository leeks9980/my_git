import random
import numpy as np

class Individual:
    def __init__(self, name: str, fitness: int) -> None:
        self.name = name
        self.fitness = fitness

    def __repr__(self):
        return f"{self.name}: {self.fitness}"

    @classmethod
    def create_random(cls, name: str) -> 'Individual':
        # 예시로 임의의 fitness 값을 설정 (1~10)
        fitness = random.randint(1, 10)
        return cls(name, fitness)

    @classmethod
    def create_random_population(cls, size: int) -> list['Individual']:
        # 개체군을 생성할 이름들 (A, B, C, D, E)
        # names = ['A', 'B', 'C', 'D', 'E']         # 얘 때문에 기존 코드로 실행시 개체군이 5개 밖에 나오지 않는 문제 발생
        names = [chr(65 + i) for i in range(size)]  # 얘로 바꾸니 해결 됨 65는 'A'의 ASCII 코드
        return [cls.create_random(name) for name in names[:size]]

def fitness_function(x):
    return np.sin(x) - 0.2 * abs(x)