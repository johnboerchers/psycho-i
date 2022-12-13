###################################################################
#                                                                 #
#   Contains functions for mesh objects to be used in simulation  #
#                                                                 #
###################################################################

import numpy as np
import sys

sys.path.append("..")
from src.input import PsychoInput


class PsychoArray:
    """Class which contains the mesh and conserved variables

    Parameters
    ----------
    pin : PsychoInput
        Contains the problem information stored in the PsychoInput
        object

    dtype : dtype
        Specify the dtype for the conserved variables to be stored
        in the PyschoArray

    Attributes
    ----------
    nvar : int
        Number of variables to be stored

    nx1 : int
        Number of cells in the x1 direction

    nx2 : int
        Number of cells in the x2 direction

    ng : int
        Number of ghost cells

    x1min, x2min : float
        Min x1 and x2 values

    x1max, x2max : float
        Max x1 and x2 values

    dx1, dx2 : float
        Step size in the x1 and x2 directions

    Un : ndarray[dtype]
        Conserved variables

    """

    def __init__(self, pin: PsychoInput, dtype: np.dtype) -> None:

        self.nvar = pin.value_dict["nvar"]
        self.nx1 = pin.value_dict["nx1"]
        self.nx2 = pin.value_dict["nx2"]
        self.ng = pin.value_dict["ng"]

        self.x1min = pin.value_dict["x1min"]
        self.x1max = pin.value_dict["x1max"]
        self.x2min = pin.value_dict["x2min"]
        self.x2max = pin.value_dict["x2max"]

        self.dx1 = (self.x1max - self.x1min) / self.nx1
        self.dx2 = (self.x2max - self.x2min) / self.nx2

        self.Un = np.zeros(
            (self.nvar, self.nx1 + 2 * self.ng, self.nx2 + 2 * self.ng), dtype=dtype
        )

    def enforce_bcs(self, pin: PsychoInput) -> None:
        """Implements the desired boundary conditions

            Will enforce the boundary conditions set in the PsychoInput class
            on the conserved variables, Un.

        pin : PsychoInput
            Contains the problem information stored in the PsychoInput
            object

        """

        # Left boundary
        if pin.value_dict["left_bc"] == "transmissive":
            self.Un[:, : self.ng, :] = self.Un[:, self.ng : 2 * self.ng, :]

        elif pin.value_dict["left_bc"] == "periodic":
            self.Un[:, : self.ng, :] = self.Un[:, -2 * self.ng : -self.ng, :]

        elif pin.value_dict["left_bc"] == "wall":
            pass

        else:
            raise ValueError("Please use an implemented boundary condition type")

        # Right boundary
        if pin.value_dict["right_bc"] == "transmissive":
            self.Un[:, -self.ng :, :] = self.Un[:, -2 * self.ng : -self.ng, :]

        elif pin.value_dict["right_bc"] == "periodic":
            self.Un[:, -self.ng :, :] = self.Un[:, self.ng : 2 * self.ng, :]

        elif pin.value_dict["right_bc"] == "wall":
            pass

        else:
            raise ValueError("Please use an implemented boundary condition type")

        # Top boundary
        if pin.value_dict["top_bc"] == "transmissive":
            self.Un[:, :, : self.ng] = self.Un[:, :, self.ng : 2 * self.ng]

        elif pin.value_dict["top_bc"] == "periodic":
            self.Un[:, : self.ng] = self.Un[:, -2 * self.ng : -self.ng, :]

        elif pin.value_dict["top_bc"] == "wall":
            pass

        else:
            raise ValueError("Please use an implemented boundary condition type")

        # Bottom boundary
        if pin.value_dict["bottom_bc"] == "transmissive":
            self.Un[:, :, : self.ng] = self.Un[:, :, self.ng : 2 * self.ng]

        elif pin.value_dict["bottom_bc"] == "periodic":
            self.Un[:, :, : self.ng] = self.Un[:, :, -2 * self.ng : -self.ng]

        elif pin.value_dict["bottom_bc"] == "wall":
            pass

        else:
            raise ValueError("Please use an implemented boundary condition type")

    def print_value(self, indvar: int, indx1: int, indx2: int) -> None:
        print(self.arr[indvar, indx1, indx2])


def get_interm_array(nvar: int, nx1: int, nx2: int, dtype: np.dtype) -> np.ndarray:
    """Generates empty scratch array for intermediate calculations

    Parameters
    ----------
    nvar : int
        Number of variables

    nx1 : int
        Number of cells in the x1 direction

    nx2 : int
        Number of cells in the x2 direction

    dtype : dtype
        Type for the values to have in the scratch array

    Returns
    -------
    ndarray :
        Scratch array with provided dtype
    """
    if nvar == 1:
        return np.zeros((nx1, nx2), dtype=dtype)
    else:
        return np.zeros((nvar, nx1, nx2), dtype=dtype)
