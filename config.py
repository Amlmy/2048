# config.py

# 棋盘尺寸
GRID_SIZE = 4

# 文件配置
BEST_SCORE_FILE = 'best_score.json'

# GUI 尺寸配置 (用于放大界面)
CELL_WIDTH = 5   
CELL_HEIGHT = 3  
FONT_SIZE_GRID = 34 
FONT_SIZE_SCORE = 18 

# 方块的颜色映射 (背景色, 数字颜色)
COLORS = {
    0: ('#cdc1b4', '#776e65'),  
    2: ('#eee4da', '#776e65'),  
    4: ('#ede0c8', '#776e65'),  
    8: ('#f2b179', '#f9f6f2'), 
    16: ('#f59563', '#f9f6f2'), 
    32: ('#f67c5f', '#f9f6f2'), 
    64: ('#f65e3b', '#f9f6f2'), 
    128: ('#edcf72', '#f9f6f2'),
    256: ('#edcc61', '#f9f6f2'),
    512: ('#edc850', '#f9f6f2'),
    1024: ('#edc53f', '#f9f6f2'),
    2048: ('#edc22e', '#f9f6f2'),
    4096: ('#60d394', '#f9f6f2'),
    8192: ('#39a089', '#f9f6f2'),
}

# 键盘映射
DIRECTION_MAP = {
    'Up': 'up', 'w': 'up',
    'Down': 'down', 's': 'down',
    'Left': 'left', 'a': 'left',
    'Right': 'right', 'd': 'right'
}