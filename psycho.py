from src.input import PsychoInput
from src.data_saver import PsychoOutput
from src.pgen import kh
from src.mesh import PsychoArray, get_interm_array
from src.reconstruct import get_limited_slopes
from src.tools import calculate_timestep, get_fluxes_2d
from src.riemann import solve_riemann
from plotting.plotter import Plotter
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-p",
    "--problem",
    help="Problem name as specified in the problem generation file and input file",
    type=str,
)

args = parser.parse_args()

if __name__ == "__main__":

    problem_name = args.problem

    input_fname = f"inputs/{problem_name}.in"

    # Load input file parameters to be used in simulation setup
    pin = PsychoInput(input_fname=input_fname)
    pin.parse_input_file()

    # Initialize empty problem mesh
    pmesh = PsychoArray(pin, np.float64)

    # Load the correct problem generator
    if problem_name == "kh":
        problem_generator = kh.ProblemGenerator
    else:
        raise ValueError("Please use an implemented problem type")

    # Initialize data saving preferences
    pout = PsychoOutput(input_fname=input_fname)
    pout.data_preferences(pin)

    # Initialize the simulation
    problem_generator(pin, pmesh)

    # Initialize time to start loop
    t = 0.0
    tmax = float(pin.value_dict["tmax"])
    cfl = float(pin.value_dict["CFL"])
    gamma = float(pin.value_dict["gamma"])

    print_freq = float(pin.value_dict["output_frequency"])

    # Initialize scratch arrays for intermediate calculations
    nx1 = pin.value_dict["nx1"]
    nx2 = pin.value_dict["nx2"]
    ng = pin.value_dict["ng"]

    Unp1 = get_interm_array(4, nx1 + 2 * ng, nx2 + 2 * ng, np.float64)

    U_i_j = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_ip1_j = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_im1_j = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_i_jp1 = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_i_jm1 = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)

    U_i_L = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_i_R = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)

    U_j_L = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_j_R = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)

    U_i_L_bar = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_i_R_bar = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)

    U_j_L_bar = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_j_R_bar = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)

    U_l_i_riemann = get_interm_array(
        4, nx1 + (2 * ng - 3), nx2 + (2 * ng - 2), np.float64
    )
    U_r_i_riemann = get_interm_array(
        4, nx1 + (2 * ng - 3), nx2 + (2 * ng - 2), np.float64
    )

    U_l_j_riemann = get_interm_array(
        4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 3), np.float64
    )
    U_r_j_riemann = get_interm_array(
        4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 3), np.float64
    )

    # Main simulation loop for MUSCL-Hancock Scheme
    iter = 0
    print(f"Iteration   |   Time   |   Timestep")
    while t < tmax:

        # Calculate timestep

        dt = calculate_timestep(pmesh, cfl, gamma)

        if t + dt > tmax:
            dt = tmax - t

        # Enforce BCs

        pmesh.enforce_bcs(pin)

        # Data Reconstruction

        # Getting arrays with shifted indices to calculate slopes
        U_i_j = pmesh.Un[:, 1:-1, 1:-1]
        U_ip1_j = pmesh.Un[:, 2:, 1:-1]
        U_im1_j = pmesh.Un[:, :-2, 1:-1]
        U_i_jp1 = pmesh.Un[:, 1:-1, 2:]
        U_i_jm1 = pmesh.Un[:, 1:-1, :-2]

        delta_i, delta_j = get_limited_slopes(
            U_i_j, U_ip1_j, U_im1_j, U_i_jp1, U_i_jm1, beta=1.0
        )

        # Evolution step
        # Boundary extrapolated values
        U_i_L = U_i_j - 1 / 2 * delta_i
        U_i_R = U_i_j + 1 / 2 * delta_i
        U_j_L = U_i_j - 1 / 2 * delta_j
        U_j_R = U_i_j + 1 / 2 * delta_j

        # Advance by half timestep
        F_i_L = get_fluxes_2d(U_i_L, gamma, "x")
        F_i_R = get_fluxes_2d(U_i_R, gamma, "x")
        G_j_L = get_fluxes_2d(U_j_L, gamma, "y")
        G_j_R = get_fluxes_2d(U_j_R, gamma, "y")

        int_flux = 1 / 2 * dt / pmesh.dx1 * (F_i_L - F_i_R) + 1 / 2 * dt / pmesh.dx2 * (
            G_j_L - G_j_R
        )

        U_i_L += int_flux
        U_i_R += int_flux
        U_j_L += int_flux
        U_j_R += int_flux

        # Riemann Problem
        # Set up Riemann states
        U_l_i_riemann = U_i_R[:, :-1, :]
        U_r_i_riemann = U_i_L[:, 1:, :]
        U_l_j_riemann = U_j_R[:, :, :-1]
        U_r_j_riemann = U_j_L[:, :, 1:]

        # Do the solve
        F = solve_riemann(U_l_i_riemann, U_r_i_riemann, gamma, "x")
        G = solve_riemann(U_l_j_riemann, U_r_j_riemann, gamma, "y")

        # Conservative update
        pmesh.Un[:, 2:-2, 2:-2] += dt / pmesh.dx1 * (
            F[:, :-1, 1:-1] - F[:, 1:, 1:-1]
        ) + dt / pmesh.dx2 * (G[:, 1:-1, :-1] - G[:, 1:-1, 1:])

        # Save Data
        if iter % print_freq == 0:
            pout.save_data(pmesh.Un, t, tmax, gamma, iter)

        if iter % print_freq == 0:
            #######################################
            # Plot during the run
            #######################################
            plotter = Plotter(pmesh)
            plotter.create_plot(
                pin.value_dict["variables_to_plot"],
                pin.value_dict["labels"],
                pin.value_dict["cmaps"],
                pin.value_dict["stability_name"],
                pin.value_dict["style_mode"],
                iter,
                t,
            )
            #######################################
            print(f"{iter}       {t}       {dt}")

        t += dt
        iter += 1
