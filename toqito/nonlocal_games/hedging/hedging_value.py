"""Semidefinite programs for obtaining values of quantum hedging scenarios."""
import cvxpy
import numpy as np

from toqito.perms.permutation_operator import permutation_operator
from toqito.super_operators.partial_trace import partial_trace_cvx


class HedgingValue:
    """
    Calculate optimal winning probabilities for hedging scenarios.

    Calculate the maximal and minimal winning probabilities for quantum
    hedging to occur in certain two-party scenarios.

    References:
        [1] Molina, Abel, and Watrous, John.
        "Hedging bets with correlated quantum strategies."
        Proceedings of the Royal Society A:
        Mathematical, Physical and Engineering Sciences
        468.2145 (2012): 2614-2629.
        https://arxiv.org/abs/1104.1140

        [2] Arunachalam, Srinivasan, Molina, Abel and Russo, Vincent.
        "Quantum hedging in two-round prover-verifier interactions."
        arXiv preprint arXiv:1310.7954 (2013).
        https://arxiv.org/pdf/1310.7954.pdf
    """

    def __init__(self, q_a: np.ndarray, num_reps: int) -> None:
        """
        Initialize the variables for semidefinite program.

        :param q_a: The fixed SDP variable.
        :param num_reps: The number of parallel repetitions.
        """
        self._q_a = q_a
        self._num_reps = num_reps

        self._sys = list(range(1, 2 * self._num_reps, 2))
        if len(self._sys) == 1:
            self._sys = self._sys[0]

        self._dim = 2 * np.ones((1, 2 * self._num_reps)).astype(int).flatten()
        self._dim = self._dim.tolist()

        # For the dual problem, the following unitary operator is used to
        # permute the subsystems of Alice and Bob which is defined by the
        # action:
        #   π(y1 ⊗ y2 ⊗ x1 ⊗ x2) = y1 ⊗ x1 ⊗ y2 ⊗ x2
        # for all y1 ∈ Y1, y2 ∈ Y2, x1 ∈ X1, x2 ∈ X2.).
        l_1 = list(range(1, self._num_reps + 1))
        l_2 = list(range(self._num_reps + 1, self._num_reps ** 2 + 1))
        if self._num_reps == 1:
            self._pperm = np.array([1])
        else:
            perm = [*sum(zip(l_1, l_2), ())]
            self._pperm = permutation_operator(2, perm)

    def max_prob_outcome_a_primal(self) -> float:
        r"""
        Compute the maximal probability for calculating outcome "a".

        The primal problem for the maximal probability of "a" is given as:

        .. math::

            \begin{equation}
                \begin{aligned}
                    \text{maximize:} \quad & \langle Q_{a_1} \otimes \ldots
                                             \otimes Q_{a_n}, X \rangle \\
                \text{subject to:} \quad & \text{Tr}_{\mathcal{Y}_1 \otimes
                                            \ldots \otimes \mathcal{Y}_n}(X) =
                                            I_{\mathcal{X}_1 \otimes \ldots
                                            \otimes \mathcal{X}_n},\\
                                            & X \in \text{Pos}(\mathcal{Y}_1
                                            \otimes \mathcal{X}_1 \otimes \ldots
                                            \otimes \mathcal{Y}_n \otimes
                                            \mathcal{X}_n)
                \end{aligned}
            \end{equation}

        :return: The optimal maximal probability for obtaining outcome "a".
        """
        x_var = cvxpy.Variable((4 ** self._num_reps, 4 ** self._num_reps), PSD=True)
        objective = cvxpy.Maximize(cvxpy.trace(self._q_a.conj().T @ x_var))
        constraints = [
            partial_trace_cvx(x_var, self._sys, self._dim)
            == np.identity(2 ** self._num_reps)
        ]
        problem = cvxpy.Problem(objective, constraints)

        return problem.solve()

    def max_prob_outcome_a_dual(self) -> float:
        r"""
        Compute the maximal probability for calculating outcome "a".

        The dual problem for the maximal probability of "a" is given as:

        .. math::

            \begin{equation}
                \begin{aligned}
                    \text{minimize:} \quad & \text{Tr}(Y) \\
                    \text{subject to:} \quad & \pi \left(I_{\mathcal{Y}_1
                    \otimes \ldots \otimes \mathcal{Y}_n} \otimes Y \right)
                    \pi^* \geq Q_{a_1} \otimes \ldots \otimes Q_{a_n}, \\
                    & Y \in \text{Herm} \left(\mathcal{X} \otimes \ldots \otimes
                    \mathcal{X}_n \right)
                \end{aligned}
            \end{equation}

        :return: The optimal maximal probability for obtaining outcome "a".
        """
        y_var = cvxpy.Variable(
            (2 ** self._num_reps, 2 ** self._num_reps), hermitian=True
        )
        objective = cvxpy.Minimize(cvxpy.trace(cvxpy.real(y_var)))

        kron_var = cvxpy.kron(np.eye(2 ** self._num_reps), y_var)
        if self._num_reps == 1:
            u_var = cvxpy.multiply(
                cvxpy.multiply(self._pperm, kron_var), self._pperm.conj().T
            )
            constraints = [cvxpy.real(u_var) >> self._q_a]
        else:
            constraints = [
                cvxpy.real(self._pperm @ kron_var @ self._pperm.conj().T) >> self._q_a
            ]
        problem = cvxpy.Problem(objective, constraints)

        return problem.solve()

    def min_prob_outcome_a_primal(self) -> float:
        r"""
        Compute the minimal probability for calculating outcome "a".

        The primal problem for the minimal probability of "a" is given as:

        .. math::

            \begin{equation}
                \begin{aligned}
                    \text{minimize:} \quad & \langle Q_{a_1} \otimes \ldots
                                             \otimes Q_{a_n}, X \rangle \\
                \text{subject to:} \quad & \text{Tr}_{\mathcal{Y}_1 \otimes
                                            \ldots \otimes \mathcal{Y}_n}(X) =
                                            I_{\mathcal{X}_1 \otimes \ldots
                                            \otimes \mathcal{X}_n},\\
                                            & X \in \text{Pos}(\mathcal{Y}_1
                                            \otimes \mathcal{X}_1 \otimes \ldots
                                            \otimes \mathcal{Y}_n \otimes
                                            \mathcal{X}_n)
                \end{aligned}
            \end{equation}

        :return: The optimal minimal probability for obtaining outcome "a".
        """
        x_var = cvxpy.Variable((4 ** self._num_reps, 4 ** self._num_reps), PSD=True)
        objective = cvxpy.Minimize(cvxpy.trace(self._q_a.conj().T @ x_var))
        constraints = [
            partial_trace_cvx(x_var, self._sys, self._dim)
            == np.identity(2 ** self._num_reps)
        ]
        problem = cvxpy.Problem(objective, constraints)

        return problem.solve()

    def min_prob_outcome_a_dual(self) -> float:
        r"""
        Compute the minimal probability for calculating outcome "a".

        The dual problem for the minimal probability of "a" is given as:

        .. math::

            \begin{equation}
                \begin{aligned}
                    \text{maximize:} \quad & \text{Tr}(Y) \\
                    \text{subject to:} \quad & \pi \left(I_{\mathcal{Y}_1
                    \otimes \ldots \otimes \mathcal{Y}_n} \otimes Y \right)
                    \pi^* \leq Q_{a_1} \otimes \ldots \otimes Q_{a_n}, \\
                    & Y \in \text{Herm} \left(\mathcal{X} \otimes \ldots \otimes
                    \mathcal{X}_n \right)
                \end{aligned}
            \end{equation}

        :return: The optimal minimal probability for obtaining outcome "a".
        """
        y_var = cvxpy.Variable(
            (2 ** self._num_reps, 2 ** self._num_reps), hermitian=True
        )
        objective = cvxpy.Maximize(cvxpy.trace(cvxpy.real(y_var)))

        kron_var = cvxpy.kron(np.eye(2 ** self._num_reps), y_var)

        if self._num_reps == 1:
            u_var = cvxpy.multiply(
                cvxpy.multiply(self._pperm, kron_var), self._pperm.conj().T
            )
            constraints = [cvxpy.real(u_var) << self._q_a]
        else:
            constraints = [
                cvxpy.real(self._pperm @ kron_var @ self._pperm.conj().T) << self._q_a
            ]
        problem = cvxpy.Problem(objective, constraints)

        return problem.solve()
