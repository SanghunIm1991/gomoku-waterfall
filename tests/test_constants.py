# TEST-CONSTANTS: docs/04_test/test_specification.md 4.4
# 対象: COMP-07 Constants

import unittest

from src.constants import BOARD_SIZE, WIN_LENGTH


class TestConstants(unittest.TestCase):
    def test_TC_CONST_01_board_size_is_15(self):
        self.assertEqual(BOARD_SIZE, 15)

    def test_TC_CONST_02_win_length_is_5(self):
        self.assertEqual(WIN_LENGTH, 5)


if __name__ == "__main__":
    unittest.main()
