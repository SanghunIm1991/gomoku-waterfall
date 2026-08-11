# COMP-02 WinChecker（勝敗判定ロジック）
# 対応する関数設計: FUNC-05
# 対応要件: REQ-08, REQ-09, REQ-12, NFR-05, CON-02

from dataclasses import dataclass, field

from src.constants import BOARD_SIZE, WIN_LENGTH

# 縦・横・右上がり斜め・右下がり斜めの4方向（片方向のみ。逆方向は符号反転で数える）
_DIRECTIONS = [(0, 1), (1, 0), (1, -1), (1, 1)]


@dataclass
class WinResult:
    is_win: bool
    cells: list = field(default_factory=list)


class WinChecker:
    def check_win(self, board, row, col, color):
        all_cells = []
        is_win = False

        for d_row, d_col in _DIRECTIONS:
            line_cells = [(row, col)]

            r, c = row + d_row, col + d_col
            while 0 <= r <= BOARD_SIZE - 1 and 0 <= c <= BOARD_SIZE - 1 and board.get_stone(r, c) == color:
                line_cells.append((r, c))
                r, c = r + d_row, c + d_col

            r, c = row - d_row, col - d_col
            while 0 <= r <= BOARD_SIZE - 1 and 0 <= c <= BOARD_SIZE - 1 and board.get_stone(r, c) == color:
                line_cells.append((r, c))
                r, c = r - d_row, c - d_col

            if len(line_cells) >= WIN_LENGTH:
                is_win = True
                for cell in line_cells:
                    if cell not in all_cells:
                        all_cells.append(cell)

        if not is_win:
            return WinResult(is_win=False, cells=[])
        return WinResult(is_win=True, cells=all_cells)
