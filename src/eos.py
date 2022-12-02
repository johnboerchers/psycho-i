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
    return rho * (gamma - 1.0) * e


@njit()
def e_EOS(
    rho: Union[float, np.ndarray], p: Union[float, np.ndarray], gamma: float
) -> Union[float, np.ndarray]:
    return p / (rho * (gamma - 1.0))
