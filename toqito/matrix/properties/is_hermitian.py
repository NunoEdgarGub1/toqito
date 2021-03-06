"""Determines whether or not a matrix is Hermitian."""
import numpy as np


def is_hermitian(mat: np.ndarray) -> bool:
    """
    Check if matrix is Hermitian.

    A Hermitian matrix is a complex square matrix that is equal to its own
    conjugate transpose.

    References:
        [1] Wikipedia: Hermitian matrix.
        https://en.wikipedia.org/wiki/Hermitian_matrix

    :param mat: Matrix to check.
    :return: Return True if matrix is Hermitian, and False otherwise.
    """
    return np.allclose(mat, mat.conj().T)
