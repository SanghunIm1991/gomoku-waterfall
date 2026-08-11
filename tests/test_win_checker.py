# TEST-WINCHECKER: docs/04_test/test_specification.md 4.2
# 対象: COMP-02 WinChecker（FUNC-05）

import unittest

from src.board import Board
from src.constants import BLACK, BOARD_SIZE, WHITE
from src.win_checker import WinChecker


def _place(board, cells, color):
    for row, col in cells:
        board.place_stone(row, col, color)


class TestWinChecker(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.checker = WinChecker()

    def test_TC_WIN_01_horizontal_five_wins(self):
        cells = [(7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
        _place(self.board, cells, BLACK)

        result = self.checker.check_win(self.board, 7, 5, BLACK)

        self.assertTrue(result.is_win)
        self.assertEqual(set(result.cells), set(cells))

    def test_TC_WIN_02_vertical_five_wins(self):
        cells = [(2, 10), (3, 10), (4, 10), (5, 10), (6, 10)]
        _place(self.board, cells, BLACK)

        result = self.checker.check_win(self.board, 4, 10, BLACK)

        self.assertTrue(result.is_win)
        self.assertEqual(set(result.cells), set(cells))

    def test_TC_WIN_03_diagonal_down_right_five_wins(self):
        cells = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        _place(self.board, cells, BLACK)

        result = self.checker.check_win(self.board, 2, 2, BLACK)

        self.assertTrue(result.is_win)
        self.assertEqual(set(result.cells), set(cells))

    def test_TC_WIN_04_diagonal_down_left_five_wins(self):
        cells = [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]
        _place(self.board, cells, BLACK)

        result = self.checker.check_win(self.board, 2, 2, BLACK)

        self.assertTrue(result.is_win)
        self.assertEqual(set(result.cells), set(cells))

    def test_TC_WIN_05_four_in_a_row_does_not_win(self):
        cells = [(7, 3), (7, 4), (7, 5), (7, 6)]
        _place(self.board, cells, BLACK)

        result = self.checker.check_win(self.board, 7, 4, BLACK)

        self.assertFalse(result.is_win)
        self.assertEqual(result.cells, [])

    def test_TC_WIN_06_overline_six_wins_with_all_cells_highlighted(self):
        cells = [(7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
        _place(self.board, cells, BLACK)

        result = self.checker.check_win(self.board, 7, 4, BLACK)

        self.assertTrue(result.is_win)
        self.assertEqual(set(result.cells), set(cells))
        self.assertEqual(len(result.cells), 6)

    def test_TC_WIN_07_opponent_stone_breaks_the_run(self):
        _place(self.board, [(7, 0), (7, 1), (7, 2)], BLACK)
        _place(self.board, [(7, 3)], WHITE)
        _place(self.board, [(7, 4), (7, 5)], BLACK)

        result = self.checker.check_win(self.board, 7, 1, BLACK)

        self.assertFalse(result.is_win)
        self.assertEqual(result.cells, [])

    def test_TC_WIN_08_boundary_origin_does_not_raise(self):
        self.board.place_stone(0, 0, BLACK)
        result_corner_min = self.checker.check_win(self.board, 0, 0, BLACK)
        self.assertFalse(result_corner_min.is_win)

        edge = BOARD_SIZE - 1
        self.board.place_stone(edge, edge, WHITE)
        result_corner_max = self.checker.check_win(self.board, edge, edge, WHITE)
        self.assertFalse(result_corner_max.is_win)

    def test_TC_WIN_09_multiple_directions_merge_without_duplicates(self):
        horizontal = [(7, 5), (7, 6), (7, 7), (7, 8), (7, 9)]
        vertical = [(5, 7), (6, 7), (7, 7), (8, 7), (9, 7)]
        _place(self.board, horizontal, BLACK)
        _place(self.board, vertical, BLACK)

        result = self.checker.check_win(self.board, 7, 7, BLACK)

        self.assertTrue(result.is_win)
        expected = set(horizontal) | set(vertical)
        self.assertEqual(set(result.cells), expected)
        self.assertEqual(len(result.cells), len(expected))


if __name__ == "__main__":
    unittest.main()
