import numpy as np


def get_unlimited_slopes(
    U_i_j: np.ndarray,
    U_ip1_j: np.ndarray,
    U_im1_j: np.ndarray,
    U_i_jp1: np.ndarray,
    U_i_jm1: np.ndarray,
    w: float,
):
    """
    Find the slopes between grid cells without a limiter.
    Can potentially lead to oscillations if there are discontinuities
    present in flow.

    Parameters
    ----------
    U_i_j : ndarray[float]
        Values of U not shifted by any index

    U_ip1_j : ndarray[float]
        Values of U shifted by i+1

    U_im1_j : ndarray[float]
        Values of U shifted by i-1

    U_i_jp1 : ndarray[float]
        Values of U shifted by j+1

    U_i_jm1 : ndarray[float]
        Values of U shifted by j-1

    w : float
        Weight parameter determining whether slopes
        are centered or biased in a particular direction

    Returns
    -------
    delta_i : ndarray[float]
        Slope of the conserved variables in the x-direction

    delta_j : ndarray[float]
        Slope of the conserved variables in the y-direction

    References
    ----------
    [1] Toro, E. F. (2011). Riemann solvers and Numerical Methods for fluid dynamics:
    A practical introduction. Springer.

    """
    delta_imoh = U_i_j - U_im1_j
    delta_ipoh = U_ip1_j - U_i_j
    delta_jmoh = U_i_j - U_i_jm1
    delta_jpoh = U_i_jp1 - U_i_j

    delta_i = 0.5 * (1.0 + w) * delta_imoh + 0.5 * (1.0 - w) * delta_ipoh
    delta_j = 0.5 * (1.0 + w) * delta_jmoh + 0.5 * (1.0 - w) * delta_jpoh

    return delta_i, delta_j


def get_limited_slopes(
    U_i_j: np.ndarray,
    U_ip1_j: np.ndarray,
    U_im1_j: np.ndarray,
    U_i_jp1: np.ndarray,
    U_i_jm1: np.ndarray,
    beta: float,
):
    """Minmod slope limiter to handle discontinuities

    Minimod slope limiter based on page 508 in [1], necessary
    for handling discontinuities

    Parameters
    ----------
    U_i_j : ndarray[float]
        Values of U not shifted by any index

    U_ip1_j : ndarray[float]
        Values of U shifted by i+1

    U_im1_j : ndarray[float]
        Values of U shifted by i-1

    U_i_jp1 : ndarray[float]
        Values of U shifted by j+1

    U_i_jm1 : ndarray[float]
        Values of U shifted by j-1

    beta : float
        Weight value determining type of limiter.
        Default value is 1.0 which represents a
        minmod limiter

    Returns
    -------
    delta_i : ndarray[float]
        Slope of the conserved variables in the x-direction

    delta_j : ndarray[float]
        Slope of the conserved variables in the y-direction

    References
    ----------
    [1] Toro, E. F. (2011). Riemann solvers and Numerical Methods for fluid dynamics:
    A practical introduction. Springer.

    """
    delta_imoh = U_i_j - U_im1_j
    delta_ipoh = U_ip1_j - U_i_j
    delta_jmoh = U_i_j - U_i_jm1
    delta_jpoh = U_i_jp1 - U_i_j

    i_up = np.where(delta_ipoh > 0.0)
    i_dn = np.where(delta_ipoh <= 0.0)
    j_up = np.where(delta_jpoh > 0.0)
    j_dn = np.where(delta_jpoh <= 0.0)

    zero_arr = np.zeros_like(U_i_j)
    delta_i = np.zeros_like(U_i_j)
    delta_j = np.zeros_like(U_i_j)

    # Positive slope limits in x direction
    delta_i[i_up] = np.maximum(
        zero_arr[i_up],
        np.maximum(
            np.minimum(beta * delta_imoh[i_up], delta_ipoh[i_up]),
            np.minimum(delta_imoh[i_up], beta * delta_ipoh[i_up]),
        ),
    )

    # Negative slope limits in x direction
    delta_i[i_dn] = np.minimum(
        zero_arr[i_dn],
        np.minimum(
            np.maximum(beta * delta_imoh[i_dn], delta_ipoh[i_dn]),
            np.maximum(delta_imoh[i_dn], beta * delta_ipoh[i_dn]),
        ),
    )

    # Positive slope limits in y direction
    delta_j[j_up] = np.maximum(
        zero_arr[j_up],
        np.maximum(
            np.minimum(beta * delta_jmoh[j_up], delta_jpoh[j_up]),
            np.minimum(delta_jmoh[j_up], beta * delta_jpoh[j_up]),
        ),
    )

    # Negative slope limits in y direction
    delta_j[j_dn] = np.minimum(
        zero_arr[j_dn],
        np.minimum(
            np.maximum(beta * delta_jmoh[j_dn], delta_jpoh[j_dn]),
            np.maximum(delta_jmoh[j_dn], beta * delta_jpoh[j_dn]),
        ),
    )

    return delta_i, delta_j
