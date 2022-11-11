import pytest
import sys
import numpy as np
sys.path.append("..")

from src.input import PsychoInput
from src.mesh  import PsychoArray
from src.pgen.sample import sampleProblemGenerator


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

    assert np.all(pmesh.arr[0,:,:] == 1.0)
    assert np.all(pmesh.arr[1,:,:] == 0.0)
    assert np.all(pmesh.arr[2,:,:] == 0.0)


