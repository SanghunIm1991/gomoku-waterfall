# TEST-GAMESTATE: docs/04_test/test_specification.md 4.3
# 対象: COMP-03 GameState（FUNC-06〜11）

import unittest

from src.constants import BLACK, BOARD_SIZE, EMPTY, WHITE
from src.game_state import GameState, GameStatus


def _draw_pattern_color(row, col):
    # 縦・横・斜めいずれの方向にも同色が2連続までしか発生しない安全なパターン。
    # 盤面を全て埋めても5連が発生しないことを保証するためのテスト専用パターン。
    return BLACK if (row + 2 * col) % 4 < 2 else WHITE


class TestGameState(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()

    def test_TC_GS_01_initial_turn_is_black(self):
        self.assertEqual(self.gs.get_current_turn(), BLACK)

    def test_TC_GS_02_successful_move_switches_turn(self):
        result = self.gs.play(0, 0)

        self.assertTrue(result.success)
        self.assertEqual(result.status, GameStatus.ONGOING)
        self.assertEqual(result.moved_color, BLACK)
        self.assertEqual(result.current_turn, WHITE)
        self.assertEqual(self.gs.get_current_turn(), WHITE)

    def test_TC_GS_03_move_on_occupied_cell_is_invalid_and_turn_unchanged(self):
        self.gs.play(0, 0)  # BLACKが着手、手番はWHITEに交代

        result = self.gs.play(0, 0)  # WHITEが同じマスへ着手を試みる

        self.assertFalse(result.success)
        self.assertEqual(result.status, GameStatus.INVALID_MOVE)
        self.assertIsNone(result.moved_color)
        self.assertEqual(result.current_turn, WHITE)
        self.assertEqual(self.gs.get_current_turn(), WHITE)

    def _play_black_horizontal_win(self, length):
        result = None
        for i in range(length):
            result = self.gs.play(7, i)  # BLACK
            if i < length - 1:
                self.gs.play(0, i)  # WHITE（無関係なマス）
        return result

    def test_TC_GS_04_five_in_a_row_wins_without_turn_switch(self):
        result = self._play_black_horizontal_win(5)

        self.assertTrue(result.success)
        self.assertEqual(result.status, GameStatus.WIN)
        self.assertEqual(result.winner, BLACK)
        self.assertEqual(result.current_turn, BLACK)
        self.assertEqual(result.moved_color, BLACK)
        self.assertEqual(set(result.highlight_cells), {(7, 0), (7, 1), (7, 2), (7, 3), (7, 4)})
        self.assertTrue(self.gs.is_game_over())

    def test_TC_GS_05_draw_when_board_full_without_win(self):
        last_cell = (0, 0)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row, col) == last_cell:
                    continue
                self.gs._board.place_stone(row, col, _draw_pattern_color(row, col))
        self.gs._current_turn = _draw_pattern_color(*last_cell)

        result = self.gs.play(*last_cell)

        self.assertTrue(result.success)
        self.assertEqual(result.status, GameStatus.DRAW)
        self.assertIsNone(result.winner)
        self.assertEqual(result.highlight_cells, [])
        self.assertTrue(self.gs.is_game_over())
        self.assertEqual(self.gs.get_result(), "DRAW")

    def test_TC_GS_06_move_after_game_over_is_rejected_and_board_unchanged(self):
        self._play_black_horizontal_win(5)

        result = self.gs.play(10, 10)

        self.assertFalse(result.success)
        self.assertEqual(result.status, GameStatus.ALREADY_OVER)
        self.assertIsNone(result.moved_color)
        self.assertEqual(self.gs._board.get_stone(10, 10), EMPTY)

    def test_TC_GS_07_result_after_win(self):
        self._play_black_horizontal_win(5)

        self.assertTrue(self.gs.is_game_over())
        self.assertEqual(self.gs.get_result(), BLACK)

    def test_TC_GS_08_result_after_draw(self):
        last_cell = (0, 0)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row, col) == last_cell:
                    continue
                self.gs._board.place_stone(row, col, _draw_pattern_color(row, col))
        self.gs._current_turn = _draw_pattern_color(*last_cell)
        self.gs.play(*last_cell)

        self.assertTrue(self.gs.is_game_over())
        self.assertEqual(self.gs.get_result(), "DRAW")

    def test_TC_GS_09_highlight_cells_before_and_after_win(self):
        self.assertEqual(self.gs.get_highlight_cells(), [])

        self.gs.play(1, 1)  # ONGOING（勝利なし）
        self.assertEqual(self.gs.get_highlight_cells(), [])

        self._reset_and_play_win()
        self.assertEqual(set(self.gs.get_highlight_cells()), {(7, 0), (7, 1), (7, 2), (7, 3), (7, 4)})

    def _reset_and_play_win(self):
        self.gs.reset()
        self._play_black_horizontal_win(5)

    def test_TC_GS_10_reset_restores_initial_state(self):
        self.gs.play(0, 0)
        self.gs.play(1, 1)

        self.gs.reset()

        self.assertEqual(self.gs.get_current_turn(), BLACK)
        self.assertFalse(self.gs.is_game_over())
        self.assertEqual(self.gs.get_highlight_cells(), [])
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.assertEqual(self.gs._board.get_stone(row, col), EMPTY)

    def test_TC_GS_11_overline_highlights_all_cells_via_game_state(self):
        # (7,0)〜(7,3)の4連と(7,5)の孤立石を先に置き、最後に隙間の(7,4)を
        # 埋めることで、1手で6連（長連）が成立する状況を作る
        # （5連の時点で対局が終了するため、単純に6手連続では長連を再現できない）。
        black_moves = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 5), (7, 4)]
        white_moves = [(0, 0), (0, 2), (0, 4), (0, 6), (0, 8)]

        result = None
        for i, black_move in enumerate(black_moves):
            result = self.gs.play(*black_move)
            if i < len(white_moves):
                self.gs.play(*white_moves[i])

        self.assertEqual(result.status, GameStatus.WIN)
        self.assertEqual(len(result.highlight_cells), 6)
        self.assertEqual(
            set(result.highlight_cells),
            {(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5)},
        )


if __name__ == "__main__":
    unittest.main()
