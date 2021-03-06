"""Applies a superoperator to an operator."""
from typing import List, Union
import numpy as np
from toqito.matrix.operations.vec import vec
from toqito.perms.swap import swap


def apply_map(
    mat: np.ndarray, phi_op: Union[np.ndarray, List[List[np.ndarray]]]
) -> np.ndarray:
    """
    Apply a superoperator to an operator.

    :param mat: A matrix.
    :param phi_op: A superoperator.
    :return: The result of applying the superoperator `phi_op` to the operator
             `mat`.

    `phi_op` should be provided either as a Choi matrix, or as a list of numpy
    arrays with either 1 or 2 columns whose entries are its Kraus operators.
    """
    # Both of the following methods of applying the superoperator are much
    # faster than naively looping through the Kraus operators or constructing
    # eigenvectors of a Choi matrix.

    # The superoperator was given as a list of Kraus operators:
    if isinstance(phi_op, list):
        s_phi_op = [len(phi_op), len(phi_op[0])]

        # Map is completely positive.
        if s_phi_op[1] == 1 or (s_phi_op[0] == 1 and s_phi_op[1] > 2):
            for i in range(s_phi_op[0]):
                phi_op[i][1] = phi_op[i][0].conj().T
        else:
            for i in range(s_phi_op[0]):
                phi_op[i][1] = phi_op[i][1].conj().T
        phi_0_list = []
        phi_1_list = []
        for i in range(s_phi_op[0]):
            phi_0_list.append(phi_op[i][0])
            phi_1_list.append(phi_op[i][1])

        k_1 = np.concatenate(phi_0_list, axis=1)
        k_2 = np.concatenate(phi_1_list, axis=0)

        a_mat = np.kron(np.identity(len(phi_op)), mat)
        return np.matmul(np.matmul(k_1, a_mat), k_2)

    # The superoperator was given as a Choi matrix:
    if isinstance(phi_op, np.ndarray):
        mat_size = np.array(list(mat.shape))
        phi_size = np.array(list(phi_op.shape)) / mat_size

        a_mat = np.kron(vec(mat).T[0], np.identity(int(phi_size[0])))
        b_mat = np.reshape(
            swap(
                phi_op.T,
                [1, 2],
                [[mat_size[1], phi_size[1]], [mat_size[0], phi_size[0]]],
                True,
            ).T,
            (int(phi_size[0] * np.prod(mat_size)), int(phi_size[1])),
        )
        return np.matmul(a_mat, b_mat)
    raise ValueError(
        "Invalid: The variable `phi_op` must either be a list of "
        "Kraus operators or as a Choi matrix."
    )
