"""Tests for tensor function."""
import unittest
import numpy as np

from toqito.base.ket import ket
from toqito.matrix.operations.tensor import tensor, tensor_n, tensor_list


class TestTensor(unittest.TestCase):
    """Unit test for tensor."""

    def test_tensor(self):
        """Test standard tensor on vectors."""
        e_0 = ket(2, 0)
        expected_res = np.kron(e_0, e_0)

        res = tensor(e_0, e_0)

        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_tensor_n_0(self):
        """Test tensor n=0 times."""
        e_0 = ket(2, 0)
        expected_res = None

        res = tensor_n(e_0, 0)
        self.assertEqual(res, expected_res)

    def test_tensor_n_1(self):
        """Test tensor n=1 times."""
        e_0 = ket(2, 0)
        expected_res = e_0

        res = tensor_n(e_0, 1)
        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_tensor_n_2(self):
        """Test tensor n=2 times."""
        e_0 = ket(2, 0)
        expected_res = np.kron(e_0, e_0)

        res = tensor_n(e_0, 2)
        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_tensor_n_3(self):
        """Test tensor n=3 times."""
        e_0 = ket(2, 0)
        expected_res = np.kron(np.kron(e_0, e_0), e_0)

        res = tensor_n(e_0, 3)
        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_tensor_list_0(self):
        """Test tensor empty list."""
        expected_res = None

        res = tensor_list([])
        self.assertEqual(res, expected_res)

    def test_tensor_list_1(self):
        """Test tensor list with one item."""
        e_0 = ket(2, 0)
        expected_res = e_0

        res = tensor_list([e_0])

        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_tensor_list_2(self):
        """Test tensor list with two items."""
        e_0, e_1 = ket(2, 0), ket(2, 1)
        expected_res = np.kron(e_0, e_1)

        res = tensor_list([e_0, e_1])

        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_tensor_list_3(self):
        """Test tensor list with three items."""
        e_0, e_1 = ket(2, 0), ket(2, 1)
        expected_res = np.kron(np.kron(e_0, e_1), e_0)

        res = tensor_list([e_0, e_1, e_0])

        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)


if __name__ == "__main__":
    unittest.main()
