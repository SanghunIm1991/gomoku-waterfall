# COMP-07 Constants（定数一覧）
# 対応要件: NFR-05, CON-02
# 他の全モジュールはここで定義される定数を参照し、値をハードコーディングしない。

BOARD_SIZE = 15
WIN_LENGTH = 5

EMPTY = "EMPTY"
BLACK = "BLACK"
WHITE = "WHITE"

CELL_SIZE = 32
MARGIN = 32

WINDOW_WIDTH = CELL_SIZE * (BOARD_SIZE - 1) + MARGIN * 2
WINDOW_HEIGHT = WINDOW_WIDTH + 60

STONE_COLORS = {
    BLACK: "black",
    WHITE: "white",
}

HIGHLIGHT_COLOR = "red"
