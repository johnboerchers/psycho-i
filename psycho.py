from src.input import PsychoInput
from src.pgen import kh
from src.mesh import PsychoArray, get_interm_array
from src.reconstruct import get_limited_slopes
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-p", "--problem", 
    help="Problem name as specified in the problem generation file and input file",
    type=str
)

args = parser.parse_args()

if __name__ == "__main__":

    problem_name = args.problem

    input_fname = f"inputs/{problem_name}"

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

    # Initialize the simulation
    problem_generator(pin, pmesh)

    # Initialize time to start loop
    t    = 0.0
    tmax = pin.value_dict["tmax"]
    cfl  = pin.value_dict["CFL"]

    # Initialize scratch arrays for intermediate calculations
    nx1 = pin.value_dict["nx1"]
    nx2 = pin.value_dict["nx2"]
    ng  = pin.value_dict["ng"]

    Unp1 = get_interm_array(4, nx1+2*ng, nx2+2*ng, np.float64)

    U_i_j  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)
    U_ip1_j  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)
    U_im1_j  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)
    U_i_jp1  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)
    U_i_jm1  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)

    U_i_L  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)
    U_i_R  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)

    U_j_L  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)
    U_j_R  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)

    U_i_L_bar  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)
    U_i_R_bar  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)

    U_j_L_bar  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)
    U_j_R_bar  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-2), np.float64)

    U_l_i_riemann = get_interm_array(4, nx1+(2*ng-3), nx2+(2*ng-2), np.float64)
    U_r_i_riemann = get_interm_array(4, nx1+(2*ng-3), nx2+(2*ng-2), np.float64)

    U_l_j_riemann  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-3), np.float64)
    U_r_j_riemann  = get_interm_array(4, nx1+(2*ng-2), nx2+(2*ng-3), np.float64)


    # Main simulation loop for MUSCL-Hancock Scheme
    while t < tmax:

        # Calculate timestep

        # Enforce BCs

        # Data Reconstruction
        delta_i, delta_j = get_limited_slopes(U_i_j, U_ip1_j, U_im1_j, U_i_jp1, U_i_jm1, beta=1.0)

        # Evolution step

        # Riemann Problem

        # Conservative update
        
        pass

