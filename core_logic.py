# core_logic.py
import random
import copy
from config import GRID_SIZE

# --- 辅助操作：转置和反转 ---

def transpose(matrix):
    """转置矩阵 (行列互换)。"""
    return [list(row) for row in zip(*matrix)]

def reverse(matrix):
    """反转矩阵的每一行。"""
    new_matrix = []
    for row in matrix:
        new_matrix.append(row[::-1])
    return new_matrix

# --- 游戏逻辑类 ---

class GameLogic:
    def __init__(self):
        # 存储历史状态 (矩阵, 分数)。只保留最近的一个状态实现单步撤销。
        self.history_states = []
        self.current_matrix = None
        self.current_score = 0
        
    def initialize_game(self):
        """初始化 4x4 矩阵并启动新游戏。"""
        matrix = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self._add_new_tile(matrix)
        self._add_new_tile(matrix)
        
        self.current_matrix = matrix
        self.current_score = 0
        self.history_states = [] # 重置历史记录
        self._save_state() # 保存初始状态
        return matrix, 0

    def _add_new_tile(self, matrix):
        """在随机空位添加一个 2 (90% 概率) 或 4 (10% 概率)。"""
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if matrix[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            matrix[r][c] = 2 if random.random() < 0.9 else 4
            return True
        return False

    def _move_row_left(self, row):
        """辅助函数：将一行进行左移和合并操作。"""
        new_row = [i for i in row if i != 0]
        score_added = 0
        i = 0
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                score_added += new_row[i]
                new_row.pop(i+1) 
            i += 1
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row, score_added

    def move_and_update(self, direction):
        """根据方向移动整个矩阵，并更新游戏状态。"""
        original_matrix = copy.deepcopy(self.current_matrix) 
        matrix = copy.deepcopy(self.current_matrix)
        total_score_added = 0
        
        # --- 核心移动逻辑 ---
        if direction == 'left':
            for r in range(GRID_SIZE):
                new_row, score = self._move_row_left(matrix[r])
                matrix[r] = new_row
                total_score_added += score
                
        elif direction == 'right':
            matrix = reverse(matrix)
            for r in range(GRID_SIZE):
                new_row, score = self._move_row_left(matrix[r])
                matrix[r] = new_row
                total_score_added += score
            matrix = reverse(matrix)
            
        elif direction == 'up':
            matrix = transpose(matrix)
            for r in range(GRID_SIZE):
                new_row, score = self._move_row_left(matrix[r])
                matrix[r] = new_row
                total_score_added += score
            matrix = transpose(matrix)
            
        elif direction == 'down':
            matrix = transpose(matrix)
            matrix = reverse(matrix)
            for r in range(GRID_SIZE):
                new_row, score = self._move_row_left(matrix[r])
                matrix[r] = new_row
                total_score_added += score
            matrix = reverse(matrix)
            matrix = transpose(matrix)

        moved_or_merged = (original_matrix != matrix)

        if moved_or_merged:
            self._save_state() # 发生移动前先保存旧状态
            self.current_matrix = matrix
            self.current_score += total_score_added
            self._add_new_tile(self.current_matrix) # 添加新数字

        return moved_or_merged, total_score_added

    # --- 撤销功能相关 ---
    
    def _save_state(self):
        """保存当前的游戏状态到历史记录。"""
        # 只保留最近的一个状态
        self.history_states = [(copy.deepcopy(self.current_matrix), self.current_score)]

    def undo_move(self):
        """撤销一步操作，恢复到上一个状态。"""
        if not self.history_states:
            return False, self.current_matrix, self.current_score

        # 恢复状态
        prev_matrix, prev_score = self.history_states.pop()
        self.current_matrix = prev_matrix
        self.current_score = prev_score
        
        return True, self.current_matrix, self.current_score

    # --- 游戏状态判定 ---

    def check_win(self):
        """检查是否有 2048 出现。"""
        return any(2048 in row for row in self.current_matrix)

    def is_game_over(self):
        """检查游戏是否结束。"""
        if any(0 in row for row in self.current_matrix):
            return False
        
        # 检查相邻是否可合并
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if c < GRID_SIZE - 1 and self.current_matrix[r][c] == self.current_matrix[r][c+1]:
                    return False
                if r < GRID_SIZE - 1 and self.current_matrix[r][c] == self.current_matrix[r+1][c]:
                    return False
                    
        return True