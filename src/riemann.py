import sys

sys.path.append("..")

import numpy as np
from src.tools import get_fluxes_1d
from numba import njit


@njit()
def solve_riemann(
    U_l: np.ndarray, U_r: np.ndarray, gamma: float, direction: str
) -> np.ndarray:
    """Solve the Riemann problem

    Solves the Riemann problem using a HLLC Riemann solver - outlined in Toro
    adapted from page 322 (see [1])

    Parameters
    ----------
    U_l : ndarray[float]
        Conserved variables at the left cell face
    U_r : ndarray[float]
        Conserved variables at the right cell face
    gamma : float
        Specific heat ratio
    direction : str
        Specify the 'x' or 'y' direction

    Returns
    -------
    F : ndarray[float]
        The flux in the specified direction returned from the
        Riemann problem


    References
    -----------
    [1] Toro, E. F. (2011). Riemann solvers and Numerical Methods for fluid dynamics:
    A practical introduction. Springer.

    """

    U_state = np.zeros(4)
    F = np.zeros_like(U_l)

    for i in range(U_r.shape[1]):
        for j in range(U_r.shape[2]):

            rho_l = U_l[0, i, j]

            if direction == "x":
                un_l = U_l[1, i, j] / rho_l
                ut_l = U_l[2, i, j] / rho_l
            else:
                un_l = U_l[2, i, j] / rho_l
                ut_l = U_l[1, i, j] / rho_l

            E_l = U_l[3, i, j]
            rhoe_l = E_l - 0.5 * rho_l * (un_l**2 + ut_l**2)
            p_l = rhoe_l * (gamma - 1.0)
            p_l = max(p_l, 1e-5)

            rho_r = U_r[0, i, j]

            if direction == "x":
                un_r = U_r[1, i, j] / rho_r
                ut_r = U_r[2, i, j] / rho_r
            else:
                un_r = U_r[2, i, j] / rho_r
                ut_r = U_r[1, i, j] / rho_r

            E_r = U_r[3, i, j]
            rhoe_r = E_r - 0.5 * rho_r * (un_r**2 + ut_r**2)
            p_r = rhoe_r * (gamma - 1.0)
            p_r = max(p_r, 1e-5)

            # compute the sound speeds
            c_l = max(1e-5, np.sqrt(gamma * p_l / rho_l))
            c_r = max(1e-5, np.sqrt(gamma * p_r / rho_r))

            p_max = max(p_l, p_r)
            p_min = min(p_l, p_r)

            Q = p_max / p_min

            rho_avg = 0.5 * (rho_l + rho_r)
            c_avg = 0.5 * (c_l + c_r)

            # primitive variable Riemann solver (Toro, 9.3)
            factor = rho_avg * c_avg

            pstar = 0.5 * (p_l + p_r) + 0.5 * (un_l - un_r) * factor
            ustar = 0.5 * (un_l + un_r) + 0.5 * (p_l - p_r) / factor

            if Q > 2 and (pstar < p_min or pstar > p_max):

                # use a more accurate Riemann solver for the estimate here

                if pstar < p_min:

                    # 2-rarefaction Riemann solver
                    z = (gamma - 1.0) / (2.0 * gamma)
                    p_lr = (p_l / p_r) ** z

                    ustar = (
                        p_lr * un_l / c_l
                        + un_r / c_r
                        + 2.0 * (p_lr - 1.0) / (gamma - 1.0)
                    ) / (p_lr / c_l + 1.0 / c_r)

                    pstar = 0.5 * (
                        p_l
                        * (1.0 + (gamma - 1.0) * (un_l - ustar) / (2.0 * c_l))
                        ** (1.0 / z)
                        + p_r
                        * (1.0 + (gamma - 1.0) * (ustar - un_r) / (2.0 * c_r))
                        ** (1.0 / z)
                    )

                else:

                    # 2-shock Riemann solver
                    A_r = 2.0 / ((gamma + 1.0) * rho_r)
                    B_r = p_r * (gamma - 1.0) / (gamma + 1.0)

                    A_l = 2.0 / ((gamma + 1.0) * rho_l)
                    B_l = p_l * (gamma - 1.0) / (gamma + 1.0)

                    # guess of the pressure
                    p_guess = max(0.0, pstar)

                    g_l = np.sqrt(A_l / (p_guess + B_l))
                    g_r = np.sqrt(A_r / (p_guess + B_r))

                    pstar = (g_l * p_l + g_r * p_r - (un_r - un_l)) / (g_l + g_r)

                    ustar = 0.5 * (un_l + un_r) + 0.5 * (
                        (pstar - p_r) * g_r - (pstar - p_l) * g_l
                    )

            if pstar <= p_l:
                # rarefaction
                S_l = un_l - c_l
            else:
                # shock
                S_l = un_l - c_l * np.sqrt(
                    1.0 + ((gamma + 1.0) / (2.0 * gamma)) * (pstar / p_l - 1.0)
                )

            if pstar <= p_r:
                # rarefaction
                S_r = un_r + c_r
            else:
                # shock
                S_r = un_r + c_r * np.sqrt(
                    1.0 + ((gamma + 1.0) / (2.0 / gamma)) * (pstar / p_r - 1.0)
                )

            # This is from Toro
            S_c = (
                p_r - p_l + rho_l * un_l * (S_l - un_l) - rho_r * un_r * (S_r - un_r)
            ) / (rho_l * (S_l - un_l) - rho_r * (S_r - un_r))

            # Simpler assumption
            # S_c = ustar

            if S_r <= 0.0:
                # R region
                U_state[:] = U_r[:, i, j]

                if direction == "x":
                    F[:, i, j] = get_fluxes_1d(U_state, gamma, "x")
                else:
                    F[:, i, j] = get_fluxes_1d(U_state, gamma, "y")

            elif S_r > 0.0 and S_c <= 0:
                # R* region
                HLLCfactor = rho_r * (S_r - un_r) / (S_r - S_c)

                U_state[0] = HLLCfactor

                if direction == "x":
                    U_state[1] = HLLCfactor * S_c
                    U_state[2] = HLLCfactor * ut_r
                else:
                    U_state[1] = HLLCfactor * ut_r
                    U_state[2] = HLLCfactor * S_c

                U_state[3] = HLLCfactor * (
                    U_r[3, i, j] / rho_r
                    + (S_c - un_r) * (S_c + p_r / (rho_r * (S_r - un_r)))
                )

                if direction == "x":
                    # find the flux on the right interface
                    F[:, i, j] = get_fluxes_1d(U_r[:, i, j], gamma, "x")
                else:
                    F[:, i, j] = get_fluxes_1d(U_r[:, i, j], gamma, "y")
                # correct the flux
                F[:, i, j] = F[:, i, j] + S_r * (U_state[:] - U_r[:, i, j])

            elif S_c > 0.0 and S_l < 0.0:
                # L* region
                HLLCfactor = rho_l * (S_l - un_l) / (S_l - S_c)

                U_state[0] = HLLCfactor

                if direction == "x":
                    U_state[1] = HLLCfactor * S_c
                    U_state[2] = HLLCfactor * ut_l
                else:
                    U_state[1] = HLLCfactor * ut_l
                    U_state[2] = HLLCfactor * S_c

                U_state[3] = HLLCfactor * (
                    U_l[3, i, j] / rho_l
                    + (S_c - un_l) * (S_c + p_l / (rho_l * (S_l - un_l)))
                )

                if direction == "x":
                    # find the flux on the right interface
                    F[:, i, j] = get_fluxes_1d(U_l[:, i, j], gamma, "x")
                else:
                    F[:, i, j] = get_fluxes_1d(U_l[:, i, j], gamma, "y")

                # correct the flux
                F[:, i, j] = F[:, i, j] + S_l * (U_state[:] - U_l[:, i, j])

            else:

                U_state[:] = U_l[:, i, j]

                if direction == "x":
                    F[:, i, j] = get_fluxes_1d(U_state, gamma, "x")
                else:
                    F[:, i, j] = get_fluxes_1d(U_state, gamma, "y")

    return F
