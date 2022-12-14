import sys
import numpy as np
import os

sys.path.append("..")

from src.input import PsychoInput
from src.mesh import PsychoArray
from src.pgen.sample import sampleProblemGenerator
from plotting.plotter import Plotter


def test_psycho_input():

    # Test that the parameter input parsing works with the sample set

    pin = PsychoInput(f"inputs/sample.in")

    pin.parse_input_file()

    assert pin.value_dict["rho0"] == 1.0
    assert pin.value_dict["p0"] == 1.0
    assert pin.value_dict["u0"] == 0.0
    assert pin.value_dict["v0"] == 0.0


def test_psycho_pgen():

    pin = PsychoInput(f"inputs/sample.in")

    pin.parse_input_file()

    pmesh = PsychoArray(pin, np.float64)

    sampleProblemGenerator(pin=pin, pmesh=pmesh)

    assert np.all(pmesh.Un[0, :, :] == 1.0)
    assert np.all(pmesh.Un[1, :, :] == 0.0)
    assert np.all(pmesh.Un[2, :, :] == 0.0)


def test_plotter_directory():

    # Remove directory if it exists to test the 
    # plotter's ability to create it
    if os.path.exists("./output/plots"):
        os.removedirs("./outputs/plots")

    assert not os.path.exists("./output/plots")

    pin = PsychoInput(f"inputs/sample.in")

    pin.parse_input_file()

    pmesh = PsychoArray(pin, np.float64)

    sampleProblemGenerator(pin=pin, pmesh=pmesh)

    test_plotter = Plotter(pmesh)
    test_plotter.check_path_exists()

    assert os.path.exists("./output/plots")

    