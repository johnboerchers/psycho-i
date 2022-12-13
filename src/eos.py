###################################################################
#                                                                 #
#            Contains the ideal gas equation of state             #
#                                                                 #
###################################################################

import numpy as np
from typing import Union
from numba import njit


@njit()
def p_EOS(
    rho: Union[float, np.ndarray], e: Union[float, np.ndarray], gamma: float
) -> Union[float, np.ndarray]:
    """Equation of state for pressure

    .. math:: p = \\rho * (\\gamma - 1) * e

    Parameters
    ----------
    rho : Union[float, ndarray]
        Density

    e : Union[float, ndarray]
        Internal energy

    gamma : float
        Specific heat ratio

    Returns
    -------
    Union[float, ndarray]
        Pressure

    """
    return rho * (gamma - 1.0) * e


@njit()
def e_EOS(
    rho: Union[float, np.ndarray], p: Union[float, np.ndarray], gamma: float
) -> Union[float, np.ndarray]:
    """Equation of state for internal energy

    .. math:: e = p / (\\rho * (\\gamma - 1))

    Parameters
    ----------
    rho : Union[float, ndarray]
        Density

    p : Union[float, ndarray]
        Pressure

    gamma : float
        Specific heat ratio

    Returns
    -------
    Union[float, ndarray]
        Internal Energy

    """
    return p / (rho * (gamma - 1.0))
