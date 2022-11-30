###################################################################
#                                                                 #
#         Contains sample problem generator for sample.in         #
#                                                                 #
###################################################################

import sys
sys.path.append("../..")

import src.mesh
import src.input


def sampleProblemGenerator(pin: src.input.PsychoInput, pmesh: src.mesh.PsychoArray) -> None:
    """
    This function is called in `main.py` and sets the initial conditions
    specified in the problem input (pin) onto the problem mesh (pmesh).

    Needs to exist for each problem type in order for everything to work.
    """

    rho0  = pin.value_dict["rho0"]
    p0    = pin.value_dict["p0"]
    u0    = pin.value_dict["u0"]
    v0    = pin.value_dict["v0"]

    pmesh.Un[0,:,:] = rho0
    pmesh.Un[1,:,:] = rho0 * u0
    pmesh.Un[2,:,:] = rho0 * v0
    # pmesh.arr[3,:,:] = rho0 * total energy

    return
