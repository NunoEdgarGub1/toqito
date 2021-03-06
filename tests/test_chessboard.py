"""Tests for chessboard function."""
import unittest
import numpy as np

from toqito.state.states.chessboard import chessboard


class TestChessboard(unittest.TestCase):
    """Unit test for chessboard."""

    def test_chessboard(self):
        """The chessboard_state."""
        res = chessboard([1, 2, 3, 4, 5, 6], 7, 8)
        self.assertEqual(np.isclose(res[0][0], 0.22592592592592592), True)

    def test_chessboard_default_s(self):
        """The chessboard_state with default `s_param`."""
        res = chessboard([1, 2, 3, 4, 5, 6], 7)
        self.assertEqual(np.isclose(res[0][0], 0.29519938056523426), True)

    def test_chessboard_default_s_t(self):
        """The chessboard_state with default `s_param` and `t_param`."""
        res = chessboard([1, 2, 3, 4, 5, 6])
        self.assertEqual(np.isclose(res[0][0], 0.3863449236810438), True)


if __name__ == "__main__":
    unittest.main()
