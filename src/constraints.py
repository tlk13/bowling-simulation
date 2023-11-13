from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np

from utils import Triangle


@dataclass
class PDConstraint(ABC):
    """This abstract class represents a general constraint for projective dynamics.
    The constraint is encoded using the mangling matrix A and the selection matrix S.

    Note that B from the paper is assumed to be the identity matrix."""

    weight: float
    A: np.ndarray
    S: np.ndarray

    @abstractmethod
    def _get_auxiliary_variable(self, current_positions: np.ndarray) -> np.ndarray:
        """Computes the auxiliary variable p for the constraint for the given
        current positions. This corresponds to the local step."""
        raise NotImplementedError

    def get_global_system_matrix_contribution(self) -> np.ndarray:
        """Returns the contribution of the constraint to the global system matrix (the
        LHS)."""
        return self.weight * self.S.T @ self.A.T @ self.A @ self.S

    def get_global_system_rhs_contribution(
        self, current_positions: np.ndarray
    ) -> np.ndarray:
        """Returns the contribution of the RHS constribution of the global system."""
        p = self._get_auxiliary_variable(current_positions)
        return self.weight * self.S.T @ self.A.T @ p


@dataclass
class Simplicial2DConstraint(PDConstraint):
    """This class represents a 2D simplicial constraint as described in the
    paper.

    The calculation of the projection T is taken from Appendix A of the paper.
    """

    triangle: Triangle
    intial_positions: np.ndarray

    sigma_min: float = 0.95
    sigma_max: float = 1.05

    A: np.ndarray = field(init=False)
    S: np.ndarray = field(init=False)

    def __post_init__(self):
        n = len(self.intial_positions)

        self.A = np.array(
            [
                [1, 0, -1],
                [0, 1, -1],
                [0, 0, 0],
            ]
        )

        self.S = np.zeros((3, n))
        self.S[0, self.triangle.v0] = 1
        self.S[1, self.triangle.v1] = 1
        self.S[2, self.triangle.v2] = 1

    def _get_auxiliary_variable(self, current_positions: np.ndarray) -> np.ndarray:
        X_g = self.A @ self.S @ self.intial_positions
        X_f = self.A @ self.S @ current_positions

        U, s, V_t = np.linalg.svd(X_f @ np.linalg.pinv(X_g))

        s = np.clip(s, self.sigma_min, self.sigma_max)
        s = np.diag(s)

        T = U @ s @ V_t

        auxiliar_variable = T @ X_g

        return auxiliar_variable
