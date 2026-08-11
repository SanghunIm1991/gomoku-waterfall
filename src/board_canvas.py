# COMP-05 BoardCanvas（盤面描画・入力）
# 対応する関数設計: FUNC-14〜19
# 対応要件: REQ-01, REQ-02, REQ-04, REQ-12, REQ-13, NFR-01, NFR-05

import tkinter as tk
from typing import Callable, Optional, Tuple

from src.constants import (
    BOARD_BG_COLOR,
    BOARD_SIZE,
    CELL_SIZE,
    HIGHLIGHT_COLOR,
    HIGHLIGHT_LINE_WIDTH,
    HIGHLIGHT_RADIUS_MARGIN,
    MARGIN,
    STONE_COLORS,
    STONE_OUTLINE_COLOR,
    STONE_RADIUS_MARGIN,
    WINDOW_WIDTH,
)

_STONE_RADIUS = CELL_SIZE // 2 - STONE_RADIUS_MARGIN
_HIGHLIGHT_RADIUS = CELL_SIZE // 2 - HIGHLIGHT_RADIUS_MARGIN
_BOARD_SPAN = (BOARD_SIZE - 1) * CELL_SIZE


def _to_pixel(row: int, col: int) -> Tuple[int, int]:
    return MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE


class BoardCanvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=WINDOW_WIDTH, height=WINDOW_WIDTH, bg=BOARD_BG_COLOR)
        self._click_callback: Optional[Callable[[int, int], None]] = None
        self.bind("<Button-1>", self._handle_click)

    def draw_grid(self) -> None:
        for i in range(BOARD_SIZE):
            x, y = _to_pixel(i, i)
            self.create_line(MARGIN, y, MARGIN + _BOARD_SPAN, y, tags="grid")
            self.create_line(x, MARGIN, x, MARGIN + _BOARD_SPAN, tags="grid")

    def draw_stone(self, row: int, col: int, color: str) -> None:
        x, y = _to_pixel(row, col)
        fill = STONE_COLORS[color]
        self.create_oval(
            x - _STONE_RADIUS,
            y - _STONE_RADIUS,
            x + _STONE_RADIUS,
            y + _STONE_RADIUS,
            fill=fill,
            outline=STONE_OUTLINE_COLOR,
            tags="stone",
        )

    def draw_highlight(self, cells: list) -> None:
        for row, col in cells:
            x, y = _to_pixel(row, col)
            self.create_oval(
                x - _HIGHLIGHT_RADIUS,
                y - _HIGHLIGHT_RADIUS,
                x + _HIGHLIGHT_RADIUS,
                y + _HIGHLIGHT_RADIUS,
                outline=HIGHLIGHT_COLOR,
                width=HIGHLIGHT_LINE_WIDTH,
                tags="highlight",
            )

    def clear(self) -> None:
        self.delete("stone")
        self.delete("highlight")

    def set_click_callback(self, callback: Callable[[int, int], None]) -> None:
        self._click_callback = callback

    def pixel_to_grid(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        if not (0 <= row <= BOARD_SIZE - 1 and 0 <= col <= BOARD_SIZE - 1):
            return None
        return row, col

    def _handle_click(self, event) -> None:
        result = self.pixel_to_grid(event.x, event.y)
        if result is None:
            return
        if self._click_callback is not None:
            row, col = result
            self._click_callback(row, col)
