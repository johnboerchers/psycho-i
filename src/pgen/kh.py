# Initial conditions for Kelvin-Helmholtz

import sys

sys.path.append("../..")

import src.mesh
import src.input
from src.eos import e_EOS, p_EOS
import numpy as np

import matplotlib.pyplot as plt


def ProblemGenerator(pin: src.input.PsychoInput, pmesh: src.mesh.PsychoArray) -> None:
    """Generates the problem in by inputting the information to the problem mesh

    This function is called in `main.py` and sets the initial conditions
    specified in the problem input (pin) onto the problem mesh (pmesh).

    Needs to exist for each problem type in order for everything to work.

    Parameters
    ----------
    pin : PsychoInput
        Contains the problem information stored in the PsychoInput
        object
    
    pmesh : PsychoArray
        PsychoArray mesh which contains all of the current mesh information
        and the conserved variables Un

    """

    # Get x values and y values
    x = np.linspace(
        pin.value_dict["x1min"], pin.value_dict["x1max"], pin.value_dict["nx1"] + 2 * pin.value_dict["ng"]
    )
    y = np.linspace(
        pin.value_dict["x2min"], pin.value_dict["x2max"], pin.value_dict["nx2"] + 2 * pin.value_dict["ng"]
    )

    # make empty pressure array for storage
    pressures = np.zeros_like(pmesh.Un[0, :, :])

    rho0 = pin.value_dict["rho0"]
    rho1 = pin.value_dict["rho1"]

    p0 = pin.value_dict["p0"]
    p1 = pin.value_dict["p1"]

    u0 = pin.value_dict["u0"]
    u1 = pin.value_dict["u1"]

    # Y velocity needs to be tripped by random velocity perturbations to start instability
    v1 = pin.value_dict["pert_amp"] * np.random.random(size=pmesh.Un[0, :, 0].size)
    v2 = pin.value_dict["pert_amp"] * np.random.random(size=pmesh.Un[0, :, 0].size)
    # print(f"V1 : {v1}")

    # Filling array values
    # Densitys
    pmesh.Un[0, :, :] = rho0
    pmesh.Un[0, :, np.abs(y) >= 0.25] = rho1

    # Density times x velocity
    pmesh.Un[1, :, :] = rho0 * u0
    pmesh.Un[1, :, np.abs(y) >= 0.25] = rho1 * u1

    # Density times y velocity
    pmesh.Un[2, :, :] = rho0 * 0.0
    pmesh.Un[2, :, int(pin.value_dict["nx2"] * 0.25)] = rho1 * v1
    pmesh.Un[2, :, int(pin.value_dict["nx2"] * -0.25)] = -rho1 * v2

    # Pressures for calculating total energy
    pressures[:, :] = p0

    # need to fill total energy
    pmesh.Un[3, :, :] = (
        0.5 * (pmesh.Un[0, :, :]) * (pmesh.Un[1, :, :] / pmesh.Un[0, :, :]) ** 2
        + 0.5 * (pmesh.Un[0, :, :]) * (pmesh.Un[2, :, :] / pmesh.Un[0, :, :]) ** 2
        + (pmesh.Un[0, :, :])
        * e_EOS(pmesh.Un[0, :, :], pressures, pin.value_dict["gamma"])
    )

    return
