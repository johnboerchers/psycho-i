import numpy as np
import sys

sys.path.append("..")
from src.mesh import PsychoArray
from src.eos import e_EOS, p_EOS
from numba import njit


@njit()
def get_primitive_variables_1d(Un: np.ndarray, gamma: float):
    """
    NEED TO ADD DOCUMENTATION
    """
    rho = Un[0]
    u = Un[1] / rho
    v = Un[2] / rho
    e = Un[3] - 1 / 2 * (u * u + v * v)

    p = p_EOS(rho, e, gamma)

    return rho, u, v, p


@njit()
def get_primitive_variables_2d(Un: np.ndarray, gamma: float):
    """
    NEED TO ADD DOCUMENTATION
    """

    rho = Un[0, :, :]
    u = Un[1, :, :] / rho
    v = Un[2, :, :] / rho
    e = Un[3, :, :] - 1 / 2 * (u * u + v * v)

    p = p_EOS(rho, e, gamma)

    return rho, u, v, p


@njit()
def get_fluxes_1d(Un: np.ndarray, gamma: float, direction: str) -> np.ndarray:
    """
    Returns fluxes for input array... need to be more descriptive but
    this is what's on the right side of the board
    """

    F = np.zeros_like(Un)
    rho, u, v, p = get_primitive_variables_1d(Un, gamma)

    if direction == "x":

        F[0] = rho * u
        F[1] = rho * u**2 + p
        F[2] = rho * u * v
        F[3] = u * (Un[3] + p)

    elif direction == "y":

        F[0] = rho * v
        F[1] = rho * u * v
        F[2] = rho * v * v + p
        F[3] = v * (Un[3] + p)

    return F


@njit()
def get_fluxes_2d(Un: np.ndarray, gamma: float, direction: str) -> np.ndarray:
    """
    Returns fluxes for input array... need to be more descriptive but
    this is what's on the right side of the board
    """

    F = np.zeros_like(Un)
    rho, u, v, p = get_primitive_variables_2d(Un, gamma)

    if direction == "x":

        F[0, :, :] = rho * u
        F[1, :, :] = rho * u**2 + p
        F[2, :, :] = rho * u * v
        F[3, :, :] = u * (Un[3, :, :] + p)

    elif direction == "y":

        F[0, :, :] = rho * v
        F[1, :, :] = rho * u * v
        F[2, :, :] = rho * v * v + p
        F[3, :, :] = v * (Un[3, :, :] + p)

    return F


def calculate_timestep(pmesh: PsychoArray, cfl: float, gamma: float) -> float:
    """
    NEED TO ADD DOCUMENTATION
    """
    # print(type(cfl), type(gamma))
    rho, u, v, p = get_primitive_variables_2d(pmesh.Un, gamma)

    a = np.sqrt(gamma * p / rho)
    # print(np.abs(u) + a)

    max_vel = max(np.amax(np.abs(u) + a), np.amax(np.abs(v) + a))

    return cfl * pmesh.dx1 / max_vel
