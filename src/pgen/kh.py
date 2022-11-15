
# Initial conditions for Kelvin-Helmholtz

import sys
sys.path.append("../..")

import src.mesh
import src.input
import numpy as np


def ProblemGenerator(pin: src.input.PsychoInput, pmesh: src.mesh.PsychoArray) -> None:
    """
    This function is called in `main.py` and sets the initial conditions
    specified in the problem input (pin) onto the problem mesh (pmesh).

    Needs to exist for each problem type in order for everything to work.
    """

    x = np.linspace(pin.value_dict["x1min"], pin.value_dict["x1max"], pin.value_dict["nx1"])
    y = np.linspace(pin.value_dict["x2min"], pin.value_dict["x2max"], pin.value_dict["nx2"])

    rho0 = pin.value_dict["rho0"]
    rho1 = pin.value_dict["rho1"]

    p0 = pin.value_dict["p0"]
    p1 = pin.value_dict["p1"]

    u0 = pin.value_dict["u0"]
    u1 = pin.value_dict["u1"]

    # Y velocity needs to be tripped by random perturbations to start instability
    v1 = pin.value_dict["pert_amp"] * np.random.random(size=pmesh.arr[0,:,0].size)

    # Filling array values
    pmesh.arr[0,:,:] = rho0
    pmesh.arr[0,:,np.where(np.abs(y) >= 0.25)] = rho1

    pmesh.arr[1,:,:] = rho0 * u0
    pmesh.arr[1,:,np.where(np.abs(y) >= 0.25)] = rho1 * u1

    pmesh.arr[2,:,:] = rho0 * 0.0
    pmesh.arr[2,:,np.where(np.abs(y) == 0.25)] = rho1 * v1
    

    return