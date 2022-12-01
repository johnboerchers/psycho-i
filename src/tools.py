import numpy as np
import sys
from mesh import PsychoArray
from eos import e_EOS, p_EOS

def get_primitive_variables(Un: np.ndarray, gamma: float):
    """
    NEED TO ADD DOCUMENTATION
    """

    if len(Un.shape) > 1:
        rho = np.zeros_like(Un[0,:,:])
        u   = np.zeros_like(Un[0,:,:])
        v   = np.zeros_like(Un[0,:,:])
        p   = np.zeros_like(Un[0,:,:])

        rho[:,:] = Un[0,:,:]
        u[:,:]   = Un[1,:,:] / rho
        v[:,:]   = Un[2,:,:] / rho
        e   = Un[4,:,:] - 1/2 * ( u * u + v * v )

        p = p_EOS(rho, e, gamma)

        return rho, u, v, p

    else:

        rho = Un[0]
        u   = Un[1] / rho
        v   = Un[2] / rho
        e   = Un[4] - 1/2 * ( u * u + v * v )

        p = p_EOS(rho, e, gamma)

        return rho, u, v, p


def get_fluxes(Un: np.ndarray, direction: str) -> np.ndarray:
    """
    Returns fluxes for input array... need to be more descriptive but
    this is what's on the right side of the board
    """

    return


def calculate_timestep(pmesh: PsychoArray, cfl: float, gamma: float) -> float:
    """
    NEED TO ADD DOCUMENTATION
    """

    rho, u, v, p = get_primitive_variables(pmesh.Un, gamma)

    a = np.sqrt(gamma * p / rho)

    max_vel = np.amax(np.abs(u) + a, np.abs(v) + a)

    return cfl * pmesh.dx1 / max_vel