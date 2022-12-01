import numpy as np


def get_limited_slopes(
    U_i_j: np.ndarray,
    U_ip1_j: np.ndarray,
    U_im1_j: np.ndarray,
    U_i_jp1: np.ndarray,
    U_i_jm1: np.ndarray,
    beta: float,
):
    """
    NEED TO ADD DOCUMENTATION HERE

    based on page 508 minmod slope limiter in Toro book
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
