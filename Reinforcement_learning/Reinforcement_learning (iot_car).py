import numpy as np
import random
import time

# --- 환경 설정 ---
move_directions = ['up', 'down', 'left', 'right']
num_actions = len(move_directions)

grid = np.array([
    [-0.1, -1, -0.1, -0.1],
    [-0.1, -0.1, -0.1, -0.1],
    [-0.1, -0.1, -1, -0.1],
    [-0.1, -0.1, -1, 1.0]
])

GRID_ROWS, GRID_COLS = grid.shape

goal_position = tuple(np.argwhere(grid == 1.0)[0])
penalty_position = tuple(np.argwhere(grid == -1.0)[0])

# --- Q-러닝 파라미터 ---
learning_rate = 0.8
discount_factor = 0.95
epsilon = 1.0
min_epsilon = 0.1
epsilon_decay_rate = 0.001

q_table = np.zeros((GRID_ROWS, GRID_COLS, num_actions))

action_to_int = {action: i for i, action in enumerate(move_directions)}
int_to_action = {i: action for i, action in enumerate(move_directions)}

# --- 에이전트 클래스 ---
class Agent:
    def __init__(self, initial_position=(0, 0)):
        self.current_position = initial_position
        self.grid = grid

    def _get_reward_at_position(self, position):
        row, col = position
        return self.grid[row, col]

    def _get_next_position(self, action):
        row, col = self.current_position
        
        if action == 'up':
            next_row, next_col = max(0, row - 1), col
        elif action == 'down':
            next_row, next_col = min(GRID_ROWS - 1, row + 1), col
        elif action == 'left':
            next_row, next_col = row, max(0, col - 1)
        elif action == 'right':
            next_row, next_col = row, min(GRID_COLS - 1, col + 1)
        else:
            raise ValueError("Invalid action.")
            
        return (next_row, next_col)

# --- 학습 시뮬레이션 ---
num_episodes = 5000
max_steps_per_episode = 100

print("--- Q-러닝 시뮬레이션 시작 ---")
print("그리드:\n", grid)
print(f"목표: {goal_position}, 패널티: {penalty_position}")

for episode in range(num_episodes):
    agent = Agent(initial_position=(0, 0)) 
    current_state = agent.current_position
    
    epsilon = max(min_epsilon, epsilon - epsilon_decay_rate)

    if (episode + 1) % 500 == 0:
        print(f"\n--- 에피소드 {episode + 1}/{num_episodes} (Epsilon: {epsilon:.4f}) ---")
        
    for step in range(max_steps_per_episode):
        row, col = current_state
        
        if random.uniform(0, 1) < epsilon:
            action_index = random.randint(0, num_actions - 1)
            action = int_to_action[action_index]
        else:
            action_index = np.argmax(q_table[row, col, :])
            action = int_to_action[action_index]
            
        next_state = agent._get_next_position(action)
        reward = agent._get_reward_at_position(next_state)
        
        current_q_value = q_table[row, col, action_index]
        next_row, next_col = next_state
        max_next_q_value = np.max(q_table[next_row, next_col, :])
        
        new_q_value = current_q_value + learning_rate * (reward + discount_factor * max_next_q_value - current_q_value)
        q_table[row, col, action_index] = new_q_value
        
        agent.current_position = next_state
        current_state = next_state

        if current_state == goal_position:
            break
            
print("\n--- Q-러닝 시뮬레이션 완료 ---")
print(f"총 {num_episodes} 에피소드 학습 완료.")

# --- 학습된 Q-테이블 확인 ---
print("\n--- 학습된 Q-테이블 ---")
for r in range(GRID_ROWS):
    for c in range(GRID_COLS):
        q_values = q_table[r, c, :]
        print(f"위치 ({r},{c}): {', '.join([f'{int_to_action[i]}:{q_values[i]:.2f}' for i in range(num_actions)])}")

# --- 최적 경로 시뮬레이션 ---
print("\n--- 최적 경로 시뮬레이션 (탐험 없음) ---")
test_agent = Agent(initial_position=(0, 0))
test_current_state = test_agent.current_position
test_score = 0.0
path = [test_current_state]

for step in range(max_steps_per_episode):
    row, col = test_current_state
    
    best_action_index = np.argmax(q_table[row, col, :])
    action = int_to_action[best_action_index]
    
    next_state = test_agent._get_next_position(action)
    reward = test_agent._get_reward_at_position(next_state)
    
    test_score += reward
    test_agent.current_position = next_state
    test_current_state = next_state
    path.append(action)

    print(f"스텝 {step+1}: 현재 위치 {test_current_state}, 선택 행동 '{action}', 보상 {reward:.2f}, 총 점수 {test_score:.2f}")

    if test_current_state == goal_position:
        print(f"*** 목표 도달! 최종 경로: {path} ***")
        print(f"*** 최종 점수: {test_score:.2f} ***")
        break
    
    if test_current_state == penalty_position:
        print(f"*** 패널티 지점 도달! 최종 경로: {path} ***")
        print(f"*** 최종 점수: {test_score:.2f} ***")
        break

else:
    print(f"*** 최대 스텝 도달. 최종 경로: {path} ***")
    print(f"*** 최종 점수: {test_score:.2f} ***")