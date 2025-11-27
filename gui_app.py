# gui_app.py
import tkinter as tk
from tkinter import messagebox
import json
import os
from core_logic import GameLogic 
from config import GRID_SIZE, COLORS, DIRECTION_MAP, CELL_WIDTH, CELL_HEIGHT, FONT_SIZE_GRID, FONT_SIZE_SCORE, BEST_SCORE_FILE 

class Game2048(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        
        self.logic = GameLogic()
        self.best_score = self.load_best_score() # 加载最高分
        self.game_running = True 
        
        self.setup_ui()     
        self.start_new_game() 
        self.master.bind('<Key>', self.key_handler)

    # --- 最高分持久化逻辑 ---
    
    def load_best_score(self):
        """从文件中加载历史最高分，如果文件不存在或出错则返回 0。"""
        if os.path.exists(BEST_SCORE_FILE):
            try:
                with open(BEST_SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    score = int(data.get('best_score', 0))
                    # print(f"DEBUG: Loaded best score: {score}")
                    return score
            except (IOError, json.JSONDecodeError):
                return 0
        return 0

    def save_best_score(self):
        """将当前的最高分保存到文件。"""
        data = {'best_score': self.best_score}
        try:
            with open(BEST_SCORE_FILE, 'w') as f:
                json.dump(data, f)
            # print(f"DEBUG: Saved new best score: {self.best_score}")
        except IOError:
            print("Error: Could not save the best score file.")
            
    # --- GUI 界面设置 ---
            
    def setup_ui(self):
        """设置游戏界面布局：分数区、重开按钮、撤销按钮和棋盘区。"""
        
        # 顶部控制区
        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=GRID_SIZE, pady=10)
        
        # 分数显示
        self.score_label = tk.Label(top_frame, text=f"Score: 0", font=("Helvetica", FONT_SIZE_SCORE))
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # 最高分显示
        self.best_score_label = tk.Label(top_frame, text=f"Best: {self.best_score}", font=("Helvetica", FONT_SIZE_SCORE))
        self.best_score_label.pack(side=tk.LEFT, padx=10)
        
        # 重开按钮
        self.restart_button = tk.Button(top_frame, text="New Game", command=self.start_new_game, font=("Helvetica", FONT_SIZE_SCORE - 4))
        self.restart_button.pack(side=tk.LEFT, padx=10)
        
        # 撤销按钮
        self.undo_button = tk.Button(top_frame, text="Undo", command=self.undo_action, font=("Helvetica", FONT_SIZE_SCORE - 4))
        self.undo_button.pack(side=tk.LEFT, padx=10)
        
        # 棋盘框架
        self.grid_frame = tk.Frame(self, bg='#bbada0', padx=5, pady=5)
        self.grid_frame.grid(row=1, column=0, columnspan=GRID_SIZE, padx=10, pady=10)
        
        # 存储方块 Label 的二维数组
        self.cell_labels = []
        for r in range(GRID_SIZE):
            row_labels = []
            for c in range(GRID_SIZE):
                cell = tk.Label(self.grid_frame,
                                text="",
                                font=("Helvetica", FONT_SIZE_GRID, "bold"),
                                width=CELL_WIDTH, 
                                height=CELL_HEIGHT,
                                bg=COLORS[0][0])
                cell.grid(row=r, column=c, padx=5, pady=5)
                row_labels.append(cell)
            self.cell_labels.append(row_labels)

    # --- 游戏控制和状态更新 ---

    def start_new_game(self):
        """重新开始一局新游戏。"""
        self.logic.initialize_game()
        self.game_running = True
        self.update_grid_cells()
        self.undo_button.config(state=tk.DISABLED) 
        
    def update_grid_cells(self):
        """根据当前的 logic 状态更新 GUI 上的所有方块和分数。"""
        
        # 更新棋盘
        matrix = self.logic.current_matrix
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = matrix[r][c]
                bg_color, fg_color = COLORS.get(value, ('#3c3a32', '#f9f6f2')) 
                
                self.cell_labels[r][c].configure(
                    text=str(value) if value != 0 else "",
                    bg=bg_color,
                    fg=fg_color
                )
        
        # 更新分数
        self.score_label.configure(text=f"Score: {self.logic.current_score}")
        self.best_score_label.configure(text=f"Best: {self.best_score}")

    def end_game(self, win=False):
        """处理游戏结束 (胜利或失败)。"""
        
        # 检查是否打破最高分
        if self.logic.current_score > self.best_score:
            self.best_score = self.logic.current_score
            self.update_grid_cells() 
            self.save_best_score() # 记录新的最高分
            
        self.game_running = False
        message = "You Won! 🎉" if win else "Game Over! 😭"
        messagebox.showinfo("2048 Game", message)

    def undo_action(self):
        """处理撤销按钮点击事件。"""
        success, matrix, score = self.logic.undo_move()
        
        if success:
            self.game_running = True 
            self.update_grid_cells()
            self.undo_button.config(state=tk.DISABLED) # 撤销一步后，禁止继续撤销
        else:
            messagebox.showinfo("Undo", "无法撤销：当前没有上一步操作记录。")

    def key_handler(self, event):
        """处理键盘事件，调用移动逻辑并更新界面。"""
        
        if not self.game_running:
            return 
            
        direction = DIRECTION_MAP.get(event.keysym)
        
        if direction:
            moved_or_merged, score_added = self.logic.move_and_update(direction)
            
            if moved_or_merged:
                self.undo_button.config(state=tk.NORMAL) 
                self.update_grid_cells()
                
                # 实时检查并更新当前最高分显示
                if self.logic.current_score > self.best_score:
                    self.best_score = self.logic.current_score
                    self.best_score_label.config(text=f"Best: {self.best_score}")

                if self.logic.check_win():
                    # 胜利后游戏继续，但弹出提示
                    self.end_game(win=True)
                    
                elif self.logic.is_game_over():
                    self.end_game(win=False)

# 主程序入口
if __name__ == '__main__':
    root = tk.Tk()
    root.title("2048 Game")
    root.resizable(False, False) 
    
    def on_closing():
        # 确保当前的 best_score 已经被设置（因为 key_handler 会更新 self.best_score）
        # 即使游戏未结束，如果最高分被打破，也会在这里被保存。
        game.save_best_score()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    game = Game2048(root)
    root.mainloop()