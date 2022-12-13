import numpy as np
import sys

sys.path.append("..")
from src.mesh import PsychoArray
from src.eos import p_EOS
from numba import njit


@njit()
def get_primitive_variables_1d(Un: np.ndarray, gamma: float):
    """Returns the primitive variables at a point provided Un.

    This function returns the primitive variables at a single point
    provided the conserved variables Un are provided at the same point.

    Parameters
    ----------
    Un : ndarray[float]
        Conserved variables
    gamma : float
        Specific heat ratio

    Returns
    -------
    rho : float
        Density
    u : float
        Horizontal velocity
    v : float
        Vertical velocity
    p : float
        Pressure

    """
    rho = Un[0]
    u = Un[1] / rho
    v = Un[2] / rho
    e = Un[3] / rho - 1 / 2 * rho * (u * u + v * v)

    p = p_EOS(rho, e, gamma)

    return rho, u, v, p


@njit()
def get_primitive_variables_2d(Un: np.ndarray, gamma: float):
    """Returns the primitive variables for all points provided Un.

    This function returns the primitive variables for all points
    provided the conserved variables Un are provided.

    Parameters
    ----------
    Un : ndarray[float]
        Conserved variables
    gamma : float
        Specific heat ratio

    Returns
    -------
    rho : ndarray[float]
        Density
    u : ndarray[float]
        Horizontal velocity
    v : ndarray[float]
        Vertical velocity
    p : ndarray[float]
        Pressure

    """

    rho = Un[0, :, :]
    u = Un[1, :, :] / rho
    v = Un[2, :, :] / rho
    e = Un[3, :, :] / rho - 1 / 2 * rho * (u * u + v * v)

    p = p_EOS(rho, e, gamma)

    return rho, u, v, p


@njit()
def get_fluxes_1d(Un: np.ndarray, gamma: float, direction: str) -> np.ndarray:
    """Returns fluxes provided the conserved variables, Un, at a point

    This function returns the fluxes in the x or y direction at one specified
    cell provided the conserved variables, Un, at the specified cell

    Parameters
    ----------
    Un : ndarray[float]
        Conserved variables
    gamma : float
        Specific heat ratio
    direction : str
        Specify the 'x' or 'y' direction

    Returns
    -------
    F : ndarray[float]
        The computed flux vector at one cell in the specified direction

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
    """Returns fluxes provided the conserved variables, Un, for all cells

    This function returns the fluxes in the x or y direction for all cells
    provided the conserved variables, Un.

    Parameters
    ----------
    Un : ndarray[float]
        Conserved variables
    gamma : float
        Specific heat ratio
    direction : str
        Specify the 'x' or 'y' direction

    Returns
    -------
    F : ndarray[float]
        The computed flux vector at all cells in the specified direction

    """

    F = np.zeros_like(Un)
    rho, u, v, p = get_primitive_variables_2d(Un, gamma)

    if direction == "x":

        F[0, :, :] = rho * u
        F[1, :, :] = rho * u * u + p
        F[2, :, :] = rho * u * v
        F[3, :, :] = u * (Un[3, :, :] + p)

    elif direction == "y":

        F[0, :, :] = rho * v
        F[1, :, :] = rho * u * v
        F[2, :, :] = rho * v * v + p
        F[3, :, :] = v * (Un[3, :, :] + p)

    return F


def calculate_timestep(pmesh: PsychoArray, cfl: float, gamma: float) -> float:
    """Calculates the maximum timestep allowed for a given CFL to remain stable


    Parameters
    ----------
    pmesh : PsychoArray
        PsychoArray mesh which contains all of the current mesh information
        and the conserved variables Un
    cfl : float
        Courant-Freidrichs-Lewy condition necessary for stability when
        choosing the timestep
    gamma: float
        Specific heat ratio


    Returns
    -------
    float
        The calculated timestep for the provided conditions

    """
    # print(type(cfl), type(gamma))
    rho, u, v, p = get_primitive_variables_2d(pmesh.Un, gamma)

    a = np.sqrt(gamma * p / rho)
    # print(np.abs(u) + a)

    max_vel = max(np.amax(np.abs(u) + a), np.amax(np.abs(v) + a))

    return cfl * pmesh.dx1 / max_vel
