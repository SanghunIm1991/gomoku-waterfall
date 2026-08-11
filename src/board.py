# COMP-01 Board（盤面モデル）
# 対応する関数設計: FUNC-01〜04
# 対応要件: REQ-04, REQ-05, REQ-10, REQ-13, NFR-05

from src.constants import BOARD_SIZE, EMPTY, Color, StoneValue


class Board:
    def __init__(self):
        self._cells = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    def _validate_coords(self, row: int, col: int) -> None:
        if not (0 <= row <= BOARD_SIZE - 1 and 0 <= col <= BOARD_SIZE - 1):
            raise ValueError(f"座標が範囲外です: ({row}, {col})")

    def place_stone(self, row: int, col: int, color: Color) -> bool:
        self._validate_coords(row, col)
        if self._cells[row][col] != EMPTY:
            return False
        self._cells[row][col] = color
        return True

    def get_stone(self, row: int, col: int) -> StoneValue:
        self._validate_coords(row, col)
        return self._cells[row][col]

    def is_full(self) -> bool:
        return all(cell != EMPTY for row in self._cells for cell in row)

    def reset(self) -> None:
        self._cells = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
