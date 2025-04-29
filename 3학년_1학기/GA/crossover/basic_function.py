import random
import copy
import math

class crossover:
    @classmethod #1개 지점 교차 (point crossover)
    def crossover_one_point(cls, p1, p2):
        point = random.randint(1, len(p1) - 1) #교차 지섬 선택
        c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)
        c1[point:], c2[point:] = p2[point:], p1[point:] #교차
        return [c1, c2]
    
    @classmethod #n개 지점 교차 (n-point crossover)
    def crossover_n_point(cls, p1, p2, n): #n개 지점 교차
        
        #n개 교차 지점 설정
        ps = random.sample(range(1, len(p1) - 1), n)

        #경재 지점 설정
        ps.append(0)
        ps.append(len(p1))
        ps = sorted(ps)
        
        c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)
        
        #교차
        for i in range(0, n + 1):
            if i % 2 == 0: #짝수 번쨰는 교차 하지 않음
                continue
            c1[ps[i]:ps[i + 1]] = p2[ps[i]:ps[i + 1]]
            c2[ps[i]:ps[i + 1]] = p1[ps[i]:ps[i + 1]]
        return [c1, c2]
    
    @classmethod #균일 교차 (uniform crossover)
    def crossover_uniform(cls, p1, p2, prop):
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        for i in range(len(p1)):
            if random.random() < prop: #교차 발생 확률
                c1[i], c2[i] = p2[i], p1[i]
        return [c1, c2]
    
    @classmethod
    def crossover_linear(cls, p1, p2, alpha): #선형 조합 교차(Linear combination crossover)
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        for i in range(len(p1)):
            c1[i] = round(p1[i] + alpha * (p2[i] - p1[i]), 2) #p1+a(p2-p1)
            c2[i] = round(p2[i] - alpha * (p2[i] - p1[i]), 2) #p2-a(p2-p1)
        return [c1, c2]

    @classmethod
    def crossover_blend(clr, p1, p2, alpha): # blend crossover
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        for i in range(len(p1)):
            l = min(c1[i], c2[i]) - alpha * abs(c2[i] - c1[i]) #p1-a(p2-p1)
            u = max(c1[i], c2[i]) + alpha * abs(c2[i] - c1[i]) #p2+a(p2-p1)
            c1[i] = round(l + random.random() * (u - l), 2)
            c2[i] = round(l + random.random() * (u - l), 2)
        return [c1, c2]
    
    @classmethod
    def crossover_order(clr, p1, p2):
        zero_shift = min(p1)
        length = len(p1)
        start, end = sorted([random.randrange(length) for _ in range(2)])
        
        c1, c2 = [math.nan] * length, [math.nan] * length  # nan 값 사용
        t1, t2 = [x - zero_shift for x in p1], [x - zero_shift for x in p2]

        spaces1, spaces2 = [True] * length, [True] * length

        # 교차 구간이 아닌 부분의 유무를 확인
        for i in range(length):
            if i < start or i > end:
                spaces1[t2[i]] = False
                spaces2[t1[i]] = False

        j1, j2 = end + 1, end + 1

        # 남은 값들 채우기
        for i in range(length):
            if not spaces1[t1[(end + i + 1) % length]]:
                c1[j1 % length] = t1[(end + i + 1) % length]
                j1 += 1
            if not spaces2[t2[(i + end + 1) % length]]:
                c2[j2 % length] = t2[(i + end + 1) % length]
                j2 += 1

        # 교차 구간 복사
        for i in range(start, end + 1):
            c1[i], c2[i] = t2[i], t1[i]

        return [[x + zero_shift for x in c1], [x + zero_shift for x in c2]]
