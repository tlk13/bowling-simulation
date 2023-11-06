from dataclasses import dataclass

import numpy as np


@dataclass
class Vertex:
    """This class represents a vertex in the mesh."""

    position: np.ndarray
    velocity: np.ndarray
    mass: float
    external_force: np.ndarray


@dataclass
class Triangle:
    """This class represents a triangle by the indices of its vertices."""

    v0: int
    v1: int
    v2: int


@dataclass
class Constraint:
    """This class represents a generic constraint by the A, S and B matrix."""

    w: float
    A: np.ndarray
    S: np.ndarray
    B: np.ndarray
