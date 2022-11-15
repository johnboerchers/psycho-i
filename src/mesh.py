###################################################################
#                                                                 #
#   Contains functions for mesh objects to be used in simulation  #
#                                                                 #
###################################################################

import numpy as np
import abc
import sys
sys.path.append("..")
from src.input import PsychoInput

class PsychoArray:

    def __init__(self, pin: PsychoInput, dtype: np.dtype) -> None:

        self.nvar  = pin.value_dict["nvar"]
        self.nx1   = pin.value_dict["nx1"]
        self.nx2   = pin.value_dict["nx2"]
        self.ng    = pin.value_dict["ng"]

        self.x1min = pin.value_dict["x1min"]
        self.x1max = pin.value_dict["x1max"]
        self.x2min = pin.value_dict["x2min"]
        self.x2max = pin.value_dict["x2max"]

        self.dx1 = (self.x1max - self.x1min) / self.nx1
        self.dx2 = (self.x2max - self.x2min) / self.nx2

        self.Un = np.zeros((self.nvar, self.nx1 + 2 * self.ng, self.nx2 + 2 * self.ng), dtype=dtype)

    def print_value(self, indvar: int, indx1: int, indx2: int) -> None:
        print(self.arr[indvar, indx1, indx2])



def get_interm_array(nvar: int, nx1: int, nx2: int, dtype: np.dtype) -> np.ndarray:
    """
    Generates empty scratch array for intermediate calculations
    """
    if nvar == 1:
        return np.zeros((nx1, nx2), dtype=dtype)
    else:
        return np.zeros((nvar, nx1, nx2), dtype=dtype)