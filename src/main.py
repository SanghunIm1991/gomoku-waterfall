# エントリポイント（NFR-02: Windows GUIアプリとして起動可能）
# `py src\main.py` で直接実行する際、プロジェクトルートを sys.path に追加し、
# 他モジュールと同じ `from src.xxx import ...` 形式のimportを成立させる。
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk

from src.app_controller import AppController
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from src.game_state import GameState
from src.main_window import MainWindow


def main():
    root = tk.Tk()
    root.title("五目並べ")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)

    game_state = GameState()
    main_window = MainWindow(root)
    controller = AppController(game_state, main_window, main_window.board_canvas)
    controller.initialize()

    root.mainloop()


if __name__ == "__main__":
    main()
