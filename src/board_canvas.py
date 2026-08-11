# COMP-05 BoardCanvas（盤面描画・入力）
# 対応する関数設計: FUNC-14〜19
# 対応要件: REQ-01, REQ-02, REQ-04, REQ-12, REQ-13, NFR-01, NFR-05

import tkinter as tk

from src.constants import (
    BOARD_SIZE,
    CELL_SIZE,
    HIGHLIGHT_COLOR,
    MARGIN,
    STONE_COLORS,
    WINDOW_WIDTH,
)

_STONE_RADIUS = CELL_SIZE // 2 - 2
_HIGHLIGHT_RADIUS = CELL_SIZE // 2 - 6
_BOARD_SPAN = (BOARD_SIZE - 1) * CELL_SIZE


def _to_pixel(row, col):
    return MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE


class BoardCanvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=WINDOW_WIDTH, height=WINDOW_WIDTH, bg="#DEB887")
        self._click_callback = None
        self.bind("<Button-1>", self._handle_click)

    def draw_grid(self):
        for i in range(BOARD_SIZE):
            x, y = _to_pixel(i, i)
            self.create_line(MARGIN, y, MARGIN + _BOARD_SPAN, y, tags="grid")
            self.create_line(x, MARGIN, x, MARGIN + _BOARD_SPAN, tags="grid")

    def draw_stone(self, row, col, color):
        x, y = _to_pixel(row, col)
        fill = STONE_COLORS[color]
        self.create_oval(
            x - _STONE_RADIUS,
            y - _STONE_RADIUS,
            x + _STONE_RADIUS,
            y + _STONE_RADIUS,
            fill=fill,
            outline="black",
            tags="stone",
        )

    def draw_highlight(self, cells):
        for row, col in cells:
            x, y = _to_pixel(row, col)
            self.create_oval(
                x - _HIGHLIGHT_RADIUS,
                y - _HIGHLIGHT_RADIUS,
                x + _HIGHLIGHT_RADIUS,
                y + _HIGHLIGHT_RADIUS,
                outline=HIGHLIGHT_COLOR,
                width=3,
                tags="highlight",
            )

    def clear(self):
        self.delete("stone")
        self.delete("highlight")

    def set_click_callback(self, callback):
        self._click_callback = callback

    def pixel_to_grid(self, x, y):
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        if not (0 <= row <= BOARD_SIZE - 1 and 0 <= col <= BOARD_SIZE - 1):
            return None
        return row, col

    def _handle_click(self, event):
        result = self.pixel_to_grid(event.x, event.y)
        if result is None:
            return
        if self._click_callback is not None:
            row, col = result
            self._click_callback(row, col)
