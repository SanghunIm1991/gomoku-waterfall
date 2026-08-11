# COMP-06 AppController（アプリケーション制御）
# 対応する関数設計: FUNC-20〜22
# 対応要件: REQ-04, REQ-05, REQ-06, REQ-07, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, NFR-03

from src.board_canvas import BoardCanvas
from src.constants import BLACK, WHITE, Color
from src.game_state import GameState, GameStatus
from src.main_window import MainWindow

_COLOR_NAMES = {BLACK: "黒", WHITE: "白"}


def _turn_text(color: Color) -> str:
    return f"{_COLOR_NAMES[color]}の番です"


def _win_text(color: Color) -> str:
    return f"{_COLOR_NAMES[color]}の勝ちです"


_DRAW_TEXT = "引き分けです"


class AppController:
    def __init__(self, game_state: GameState, main_window: MainWindow, board_canvas: BoardCanvas):
        self._game_state = game_state
        self._main_window = main_window
        self._board_canvas = board_canvas

    def on_board_click(self, row: int, col: int) -> None:
        result = self._game_state.play(row, col)

        if result.status in (GameStatus.INVALID_MOVE, GameStatus.ALREADY_OVER):
            return

        self._board_canvas.draw_stone(row, col, result.moved_color)

        if result.status == GameStatus.WIN:
            self._board_canvas.draw_highlight(result.highlight_cells)
            self._main_window.update_status_text(_win_text(result.winner))
        elif result.status == GameStatus.DRAW:
            self._main_window.update_status_text(_DRAW_TEXT)
        else:
            self._main_window.update_status_text(_turn_text(result.current_turn))

    def on_reset_click(self) -> None:
        self._game_state.reset()
        self._board_canvas.clear()
        self._main_window.update_status_text(_turn_text(self._game_state.get_current_turn()))

    def initialize(self) -> None:
        self._board_canvas.set_click_callback(self.on_board_click)
        self._main_window.set_reset_callback(self.on_reset_click)
        self._board_canvas.draw_grid()
        self._main_window.update_status_text(_turn_text(self._game_state.get_current_turn()))
