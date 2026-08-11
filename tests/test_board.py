# TEST-BOARD: docs/04_test/test_specification.md 4.1
# 対象: COMP-01 Board（FUNC-01〜04）

import unittest

from src.board import Board
from src.constants import BLACK, BOARD_SIZE, EMPTY, WHITE


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_TC_BOARD_01_place_stone_on_empty_cell_succeeds(self):
        result = self.board.place_stone(3, 4, BLACK)
        self.assertTrue(result)
        self.assertEqual(self.board.get_stone(3, 4), BLACK)

    def test_TC_BOARD_02_place_stone_on_occupied_cell_fails(self):
        self.board.place_stone(3, 4, BLACK)
        result = self.board.place_stone(3, 4, WHITE)
        self.assertFalse(result)
        self.assertEqual(self.board.get_stone(3, 4), BLACK)

    def test_TC_BOARD_03_place_stone_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            self.board.place_stone(-1, 0, BLACK)
        with self.assertRaises(ValueError):
            self.board.place_stone(0, BOARD_SIZE, BLACK)

    def test_TC_BOARD_04_get_stone_initial_is_empty(self):
        self.assertEqual(self.board.get_stone(0, 0), EMPTY)
        self.assertEqual(self.board.get_stone(BOARD_SIZE - 1, BOARD_SIZE - 1), EMPTY)

    def test_TC_BOARD_05_get_stone_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            self.board.get_stone(0, -1)
        with self.assertRaises(ValueError):
            self.board.get_stone(BOARD_SIZE, 0)

    def test_TC_BOARD_06_is_full_false_when_not_full(self):
        self.board.place_stone(0, 0, BLACK)
        self.assertFalse(self.board.is_full())

    def test_TC_BOARD_07_is_full_true_when_full(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.board.place_stone(row, col, BLACK if (row + col) % 2 == 0 else WHITE)
        self.assertTrue(self.board.is_full())

    def test_TC_BOARD_08_reset_clears_board(self):
        self.board.place_stone(1, 1, BLACK)
        self.board.place_stone(2, 2, WHITE)
        self.board.reset()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.assertEqual(self.board.get_stone(row, col), EMPTY)


if __name__ == "__main__":
    unittest.main()
