import sys
import numpy as np
import math

sys.path.append("..")

from src.input import PsychoInput
from src.mesh import PsychoArray, get_interm_array
from src.pgen.kh import ProblemGenerator
from src.eos import p_EOS,e_EOS
from src.reconstruct import get_limited_slopes,get_unlimited_slopes
from src.riemann import solve_riemann
from src.tools import get_primitive_variables_1d, get_primitive_variables_2d, get_fluxes_1d, get_fluxes_2d
from src.data_saver import PsychoOutput
from plotting.plotter import Plotter




def test_psycho_input():

    # Test that the parameter input parsing works with kh

    pin = PsychoInput(f"inputs/kh.in")

    pin.parse_input_file()

    assert pin.value_dict["rho0"] == 1.0
    assert pin.value_dict["rho1"] > pin.value_dict["rho0"]
    assert pin.value_dict["p0"] == pin.value_dict["p1"]
    assert pin.value_dict["u0"] >= 0
    assert pin.value_dict["u1"] < 0
    assert pin.value_dict["pert_amp"] < 1.0
    assert pin.value_dict["CFL"] < 1.0
    assert pin.value_dict["gamma"] == 1.4
    assert pin.value_dict["left_bc"] == "periodic"
    assert pin.value_dict["right_bc"] == "periodic"
    assert pin.value_dict["top_bc"] == "periodic"
    assert pin.value_dict["bottom_bc"] == "periodic"
    assert pin.value_dict["output_frequency"] >= 1



def test_psycho_pgen():
    """Tests values or signs of values from the problekm generator

    """

    pin = PsychoInput(f"inputs/kh.in")

    pin.parse_input_file()

    pmesh = PsychoArray(pin, np.float64)

    ProblemGenerator(pin=pin, pmesh=pmesh)
    # check that values are correct
    assert pmesh.Un[0, :, :] == 1.0 # rho0
    assert pmesh.Un[0, :, np.abs(y) >= 0.25] == 2.0 # rho1
    assert pmesh.Un[1, :, :] ==  0.3 # rho0*u0
    assert pmesh.Un[1, :, np.abs(y) >= 0.25] == -0.6 # rho1 * u1

    
    # not checking rho*v because v is random
    # not checking pressures array because it is just set to p0 which is checked in input test
    
    assert pmesh.Un[3, :, :] >= 0 # total energy is positive

#def test_psycho_output():
# check dimensions, whether files exist, etc

def test_psycho_eos():
    """Tests eos.py by generating random inputs and compares the output of eos.py with a direct application of the equation of state equation

    """

    pin = PsychoInput(f"inputs/kh.in")

    pin.parse_input_file()

    nx1 = pin.value_dict["nx1"]
    nx2 = pin.value_dict["nx2"]

    correct_pstate = np.empty((nx1,nx2),dtype=float)
    correct_estate = np.empty((nx1,nx2),dtype=float)
    pdiff = np.empty((nx1,nx2),dtype=float)
    ediff = np.empty((nx1,nx2),dtype=float)
    
    rho = 100.0*np.random.random_sample(size=(nx1,nx2))
    e = 100.0*np.random.random_sample(size=(nx1,nx2))
    p = 100.0*np.random.random_sample(size=(nx1,nx2))

    gamma = 1.4
    pstate = p_EOS(rho,e,gamma)

    estate = e_EOS(rho,p,gamma)

    tol = 0.001
    count = 0.0

    for j in nx2:
        for i in nx1:
            correct_pstate[i][j] = rho[i][j] * (gamma-1.0) * e[i][j]
            correct_estate[i][j] = p[i][j] / (rho[i][j] * (gamma - 1.0))

            pdiff[i][j] = abs(pstate[i][j] - correct_pstate[i][j])
            ediff[i][j] = abs(estate[i][j] - correct_estate[i][j])

            if (pdiff[i][j] <= tol) and (ediff[i][j] <= tol):
                count = count + 1

    assert count == (nx1*nx2)

def test_psycho_mesh():
    """Tests that array dimensions in mesh.py are correct. Should also check boundary condition enforcement

    """
    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)
    # check array dimensions
    # check that boundary conditions are enforced correctly

def test_psycho_reconstruct():
    """Since reconstruct.py essentially finds a linear interpolation between values at the cell faces, the slope of the line that it finds should have a magnitude of 1 or smaller since our grid is made of squares. This test checks for that.

    """
    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)

    pin.parse_input_file()

    nx1 = pin.value_dict["nx1"]
    nx2 = pin.value_dict["nx2"]
    ng = pin.value_dict["ng"]

    U_i_j = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_ip1_j = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_im1_j = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_i_jp1 = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)
    U_i_jm1 = get_interm_array(4, nx1 + (2 * ng - 2), nx2 + (2 * ng - 2), np.float64)

    U_i_j = pmesh.Un[:, 1:-1, 1:-1]
    U_ip1_j = pmesh.Un[:, 2:, 1:-1]
    U_im1_j = pmesh.Un[:, :-2, 1:-1]
    U_i_jp1 = pmesh.Un[:, 1:-1, 2:]
    U_i_jm1 = pmesh.Un[:, 1:-1, :-2]

    delta_i, delta_j = get_limited_slopes(U_i_j, U_ip1_j, U_im1_j, U_i_jp1, U_i_jm1, beta=1.0)

    assert abs(delta_i) <= 1.0
    assert abs(delta_j) <= 1.0


def test_psycho_tools():
    """Tests that array dimensions in tools.py are correct. 

    """
    get_primitive_variables_1d()

    get_primitive_variables_2d()

    get_fluxes_1d()

    get_fluxes_2d()



#def test_psycho_plotting():
# check array dimensions
# not sure what other tests can be done for plotter...

#def test_psycho_primary_conservation():

    #get_primitive_variables_1d()

    #get_primitive_variables_2d()

    #get_fluxes_1d()

    #get_fluxes_2d()

    #assert 

#def test_psycho_secondary_conservation():


# BEFORE RUNNING CONVERGENCE TESTS, kh.in FILE OUTPUT NEEDS TO BE TXT
def test_psycho_temporal_convergence():
    """Tests for temporal convergence with error of order 1 or greater. It should execute psycho.py with different 512 cells in each direction. Then it should follow basically what we do in 557. This one and the next really need to be tested

    """

    os.system('python psycho.py -p temp_convergence')

    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)

    pin.parse_input_file()

    ng = pin.value_dict["ng"]
    
    u_reg_dx = np.loadtxt('x-velocity.txt', dtype=float)
    u_small_dx = pmesh.Un[1, ng : -ng, ng : -ng] / rho

    v_reg_dy = np.loadtxt('y-velocity.txt', dtype=float)
    v_small_dy = pmesh.Un[2, ng : -ng, ng : -ng] / rho

    x = np.linspace(pin.value_dict["x1min"],pin.value_dict["x1max"],pin.value_dict["nx1"] + 2 * pin.value_dict["ng"])
    dx = (abs(pin.value_dict["x1max"]) + abs(pin.value_dict["x1min"]))/range(x)
    dy = dx
    count = 0

    for j in range(ng):
        for i in range(ng):
            u_err[i][j] = abs(u_reg_dx[i][j] - u_small_dx[i][j])
            v_err[i][j] = abs(v_reg_dy[i][j] - v_small_dy[i][j])

            n_u[i][j] = math.log(u_err[i][j],10) / math.log(dx,10)
            n_v[i][j] = math.log(v_err[i][j],10) / math.log(dy,10)

            if (n_u[i][j]>=1) and (n_v[i][j>=1]):
                count = count +1

    assert count >= 0.95*ng*ng


def test_psycho_spatial_convergence():
    """Tests for spatial convergence with error of order 1 or greater. It should execute psycho.py with a CFL of 0.25 rather than 0.5. Then it should follow basically what we do in 557.

    """

    os.system('python psycho.py -p spatial_convergence') 

    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)

    pin.parse_input_file()

    ng = pin.value_dict["ng"]

    u_reg_dt = np.loadtxt('x-velocity.txt', dtype=float)
    u_small_dt = pmesh.Un[1, ng : -ng, ng : -ng] / rho

    v_reg_dt = np.loadtxt('y-velocity.txt', dtype=float)
    v_small_dt = pmesh.Un[2, ng : -ng, ng : -ng] / rho

    x = np.linspace(pin.value_dict["x1min"],pin.value_dict["x1max"],pin.value_dict["nx1"] + 2 * pin.value_dict["ng"])
    dx = (abs(pin.value_dict["x1max"]) + abs(pin.value_dict["x1min"]))/range(x)
    dy = dx
    count = 0

    for j in range(ng):
        for i in range(ng):
            u_err[i][j] = abs(u_reg_dt[i][j] - u_small_dt[i][j])
            v_err[i][j] = abs(v_reg_dt[i][j] - v_small_dt[i][j])

            n_u[i][j] = math.log(u_err[i][j],10) / math.log(dx,10)
            n_v[i][j] = math.log(v_err[i][j],10) / math.log(dy,10)

            if (n_u[i][j]>=1) and (n_v[i][j>=1]):
                count = count +1

    assert count >= 0.95*ng*ng




