# COMP-04 MainWindow（メインウィンドウ）
# 対応する関数設計: FUNC-12〜13
# 対応要件: REQ-07, REQ-09, REQ-10, REQ-13, NFR-01, NFR-05

import tkinter as tk

from src.board_canvas import BoardCanvas


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        self._status_label = tk.Label(self, text="", font=("", 14))
        self._status_label.pack(side=tk.TOP, pady=8)

        self._reset_button = tk.Button(self, text="リセット")
        self._reset_button.pack(side=tk.TOP, pady=4)

        self.board_canvas = BoardCanvas(self)
        self.board_canvas.pack(side=tk.TOP)

    def update_status_text(self, text):
        self._status_label.config(text=text)

    def set_reset_callback(self, callback):
        self._reset_button.config(command=callback)
