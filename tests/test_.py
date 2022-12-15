import sys
import numpy as np

sys.path.append("..")

from src.input import PsychoInput
from src.mesh import PsychoArray, get_interm_array
from src.pgen.kh import ProblemGenerator
from src.eos import p_EOS,e_EOS
from src.reconstruct import get_limited_slopes
from src.tools import get_primitive_variables_1d, get_primitive_variables_2d, get_fluxes_1d, get_fluxes_2d, calculate_timestep
from src.data_saver import PsychoOutput
from plotting.plotter import Plotter



def test_psycho_input():

    # Test that the parameter input parsing works with kh

    pin = PsychoInput(f"inputs/kh.in")

    pin.parse_input_file()

    assert pin.value_dict["rho1"] > pin.value_dict["rho0"]
    assert pin.value_dict["rho0"] > 0.0
    assert pin.value_dict["rho1"] > 0.0
    assert pin.value_dict["p0"] == pin.value_dict["p1"]
    assert pin.value_dict["p0"] > 0.0
    assert pin.value_dict["u0"] >= 0.0
    assert pin.value_dict["u1"] < 0.0
    assert pin.value_dict["pert_amp"] < 1.0
    assert pin.value_dict["pert_amp"] > 0.0
    assert pin.value_dict["CFL"] < 1.0
    assert pin.value_dict["CFL"] > 0.0
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


    nx1 = pin.value_dict["nx1"]
    nx2 = pin.value_dict["nx2"]
    ng = pin.value_dict["ng"]
    assert pmesh.Un.ndim == (nx1,nx2)
    
    assert pmesh.Un[3, :, :] >= 0 # total energy is positive


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
    assert pstate[:][:] > 0.0

    estate = e_EOS(rho,p,gamma)
    assert estate[:][:] > 0.0

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
    
    assert pmesh.Un.ndim == (pmesh.nvar, pmesh.nx1 + 2 * pmesh.ng, pmesh.nx2 + 2 * pmesh.ng)
    
    interm = np.array()
    interm = pmesh.get_interm_array(pmesh.nvar, pmesh.nx1, pmesh.nx2)
    if (pmesh.nvar==1):
        assert interm.ndim == (pmesh.nx1, pmesh.nx2)
    else:
        assert interm.ndim == (pmesh.nvar, pmesh.nx1, pmesh.nx2)


def test_bc_enforced():
    """Check boundary condition enforcement

    """


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


def test_psycho_1d_variables():
    """Tests that array dimensions in get_primitive_variables_1d() in tools.py are correct. 

    """
    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)

    pin.parse_input_file()

    gamma = pin.value_dict["gamma"]

    rho, u, v, p = get_primitive_variables_1d(pmesh.Un, gamma)

    assert rho.ndim == (4)
    assert rho[:] > 0.0
    assert u.ndim == (4)
    assert v.ndim == (4)
    assert p.ndim == (4)
    assert p[:] > 0.0


def test_psycho_2d_variables():
    """Tests that array dimensions in get_primitive_variables_2d() in tools.py are correct. 

    """
    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)

    pin.parse_input_file()

    gamma = pin.value_dict["gamma"]

    rho, u, v, p = get_primitive_variables_2d(pmesh.Un, gamma)

    assert rho.ndim == (pmesh.nvar, pmesh.nx1 + 2 * pmesh.ng, pmesh.nx2 + 2 * pmesh.ng)
    assert rho[:,:] > 0.0
    assert u.ndim == (pmesh.nvar, pmesh.nx1 + 2 * pmesh.ng, pmesh.nx2 + 2 * pmesh.ng)
    assert v.ndim == (pmesh.nvar, pmesh.nx1 + 2 * pmesh.ng, pmesh.nx2 + 2 * pmesh.ng)
    assert p.ndim == (pmesh.nvar, pmesh.nx1 + 2 * pmesh.ng, pmesh.nx2 + 2 * pmesh.ng)
    assert p[:,:] > 0.0



def test_psycho_1d_fluxes():
    """Tests that array dimensions in get_fluxes_1d() in tools.py are correct. 

    """
    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)

    pin.parse_input_file()

    gamma = pin.value_dict["gamma"]

    Fx = get_fluxes_1d(pmesh.Un, gamma, 'x')
    assert Fx.ndim == (4)
    assert Fx[1] >= 0.0

    Fy = get_fluxes_1d(pmesh.Un, gamma, 'y')
    assert Fy.ndim == (4)
    assert Fy[2] >= 0.0



def test_psycho_2d_fluxes():
    """Tests that array dimensions in get_fluxes_2d() in tools.py are correct. 

    """

    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)

    pin.parse_input_file()

    gamma = pin.value_dict["gamma"]


    Fx = get_fluxes_2d(pmesh.Un, gamma, 'x')
    assert Fx.ndim ==(4, pmesh.nvar, pmesh.nx1 + 2 * pmesh.ng, pmesh.nx2 + 2 * pmesh.ng)
    assert Fx[1, :, :] >= 0.0

    Fy = get_fluxes_2d(pmesh.Un, gamma, 'y')
    assert Fy.ndim ==(4, pmesh.nvar, pmesh.nx1 + 2 * pmesh.ng, pmesh.nx2 + 2 * pmesh.ng)
    assert Fy[1, :, :] >= 0.0


def test_calculate_timestep():
    """Tests that array dimensions in calculate_timestep() in tools.py are correct. 

    """
    pin = PsychoInput(f"inputs/kh.in")
    pmesh = PsychoArray(pin, np.float64)

    pin.parse_input_file()

    cfl = float(pin.value_dict["CFL"])
    gamma = float(pin.value_dict["gamma"])

    assert calculate_timestep(pmesh, cfl, gamma) > 0.0




def test_psycho_data_file_existence():
    """Tests that correct data files exist.
    array dimensions in psycho_data_saver.py are correct. 

    """
    pin = PsychoInput(f"inputs/kh.in")
    pin.parse_input_file()

    pout = PsychoOutput(input_fname=input_fname)
    pout.data_preferences(pin)


    if "txt" in pout.file_type:
        if "x-velocity" in pout.variables:

            assert os.path.isfile('x-velocity.txt')

        if "y-velocity" in pout.variables:

            assert os.path.isfile('y-velocity.txt')

        if "density" in pout.variables:

            assert os.path.isfile('density.txt')

        if "pressure" in pout.variables:

            assert os.path.isfile('pressure.txt')


    if "csv" in pout.file_type:
        if "x-velocity" in pout.variables:

            assert os.path.isfile('x-velocity.csv')

        if "y-velocity" in pout.variables:

            assert os.path.isfile('y-velocity.csv')

        if "density" in pout.variables:

            assert os.path.isfile('density.csv')

        if "pressure" in pout.variables:

            assert os.path.isfile('pressure.csv')

    if "hdf5" in pout.file_type:
        
         assert os.path.isfile(f'iter_{file_name}.hdf5')

         if "x-velocity" in pout.variables:

            assert 

        if "y-velocity" in pout.variables:

            assert 

        if "density" in pout.variables:

            assert 

        if "pressure" in pout.variables:

            assert 


def test_psycho_data_saved_to_file():
    """Tests that array dimensions in psycho_data_saver.py are correct. 

    """
    pin = PsychoInput(f"inputs/kh.in")
    pin.parse_input_file()

    pmesh = PsychoArray(pin, np.float64)

    ProblemGenerator(pin=pin, pmesh=pmesh)

    pout = PsychoOutput(input_fname=input_fname)
    pout.data_preferences(pin)

    gamma = pin.value_dict["gamma"]

    rho, u, v, p = get_primitive_variables_2d(pmesh,gamma)

    
    if "txt" in pout.file_type:
        if "x-velocity" in pout.variables:

            assert 

        if "y-velocity" in pout.variables:

            assert 

        if "density" in pout.variables:

            assert 

        if "pressure" in pout.variables:

            assert 


    if "csv" in pout.file_type:
        if "x-velocity" in pout.variables:

            assert 

        if "y-velocity" in pout.variables:

            assert 

        if "density" in pout.variables:

            assert 

        if "pressure" in pout.variables:

            assert 

    if "hdf5" in pout.file_type:
        
         assert os.path.isfile(f'iter_{file_name}.hdf5')

         if "x-velocity" in pout.variables:

            assert 

        if "y-velocity" in pout.variables:

            assert 

        if "density" in pout.variables:

            assert 

        if "pressure" in pout.variables:

            assert 





#def test_psycho_plotting():
# check array dimensions
# not sure what other tests can be done for plotter...

