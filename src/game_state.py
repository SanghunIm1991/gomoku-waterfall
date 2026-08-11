# COMP-03 GameState（対局状態管理）
# 対応する関数設計: FUNC-06〜11
# 対応要件: REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, CON-01

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

from src.board import Board
from src.constants import BLACK, WHITE
from src.win_checker import WinChecker


class GameStatus(Enum):
    ONGOING = "ONGOING"
    WIN = "WIN"
    DRAW = "DRAW"
    ALREADY_OVER = "ALREADY_OVER"
    INVALID_MOVE = "INVALID_MOVE"


@dataclass
class MoveResult:
    success: bool
    status: GameStatus
    winner: Optional[str]
    highlight_cells: list
    current_turn: str
    moved_color: Optional[str]


def _other_color(color):
    return WHITE if color == BLACK else BLACK


class GameState:
    def __init__(self):
        self._board = Board()
        self._win_checker = WinChecker()
        self._current_turn = BLACK
        self._is_over = False
        self._winner = None
        self._highlight_cells = []

    def play(self, row, col):
        if self.is_game_over():
            return MoveResult(
                success=False,
                status=GameStatus.ALREADY_OVER,
                winner=self._winner,
                highlight_cells=self._highlight_cells,
                current_turn=self._current_turn,
                moved_color=None,
            )

        placing_color = self._current_turn

        if not self._board.place_stone(row, col, placing_color):
            return MoveResult(
                success=False,
                status=GameStatus.INVALID_MOVE,
                winner=None,
                highlight_cells=[],
                current_turn=self._current_turn,
                moved_color=None,
            )

        win_result = self._win_checker.check_win(self._board, row, col, placing_color)

        if win_result.is_win:
            self._is_over = True
            self._winner = placing_color
            self._highlight_cells = win_result.cells
            return MoveResult(
                success=True,
                status=GameStatus.WIN,
                winner=placing_color,
                highlight_cells=self._highlight_cells,
                current_turn=placing_color,
                moved_color=placing_color,
            )

        if self._board.is_full():
            self._is_over = True
            self._winner = None
            return MoveResult(
                success=True,
                status=GameStatus.DRAW,
                winner=None,
                highlight_cells=[],
                current_turn=placing_color,
                moved_color=placing_color,
            )

        self._current_turn = _other_color(placing_color)
        return MoveResult(
            success=True,
            status=GameStatus.ONGOING,
            winner=None,
            highlight_cells=[],
            current_turn=self._current_turn,
            moved_color=placing_color,
        )

    def get_current_turn(self):
        return self._current_turn

    def is_game_over(self):
        return self._is_over

    def get_result(self):
        if not self._is_over:
            return None
        return self._winner if self._winner is not None else "DRAW"

    def get_highlight_cells(self):
        return self._highlight_cells

    def reset(self):
        self._board.reset()
        self._current_turn = BLACK
        self._is_over = False
        self._winner = None
        self._highlight_cells = []
