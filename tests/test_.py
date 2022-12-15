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
        if len(os.listdir("./output/plots")):
            for file in os.scandir("./output/plots"):
                os.remove(file.path)
        os.removedirs("./output/plots")

    assert not os.path.exists("./output/plots")

    pin = PsychoInput(f"inputs/sample.in")

    pin.parse_input_file()

    pmesh = PsychoArray(pin, np.float64)

    sampleProblemGenerator(pin=pin, pmesh=pmesh)

    test_plotter = Plotter(pmesh)
    test_plotter.check_path_exists()

    assert os.path.exists("./output/plots")


def test_plotter_init():

    # Initialize plotter with sample data and
    # verify it loads the correct data in
    pin = PsychoInput(f"inputs/sample.in")

    pin.parse_input_file()

    pmesh = PsychoArray(pin, np.float64)

    sampleProblemGenerator(pin=pin, pmesh=pmesh)

    test_plotter = Plotter(pmesh)

    assert np.ceil(test_plotter.x1[-1]) == pmesh.x1max
    assert np.ceil(test_plotter.x2[-1]) == pmesh.x2max

    # Pick a random point to test
    randint_x1 = np.random.randint(0, len(test_plotter.x1))
    randint_x2 = np.random.randint(0, len(test_plotter.x2))

    assert test_plotter.ng == pmesh.ng
    assert (
        test_plotter.rho[randint_x1, randint_x2] == pmesh.Un[0, randint_x1, randint_x2]
    )
    assert (
        test_plotter.rho[randint_x1, randint_x2]
        * test_plotter.u[randint_x1, randint_x2]
        == pmesh.Un[1, randint_x1, randint_x2]
    )
    assert (
        test_plotter.rho[randint_x1, randint_x2]
        * test_plotter.v[randint_x1, randint_x2]
        == pmesh.Un[2, randint_x1, randint_x2]
    )
    assert (
        test_plotter.rho[randint_x1, randint_x2]
        * test_plotter.et[randint_x1, randint_x2]
        == pmesh.Un[3, randint_x1, randint_x2]
    )


def test_plotter_figure():

    # Initialize plotter with sample data and
    # verify it generates a figure
    pin = PsychoInput(f"inputs/sample.in")

    pin.parse_input_file()

    pmesh = PsychoArray(pin, np.float64)

    sampleProblemGenerator(pin=pin, pmesh=pmesh)

    test_plotter = Plotter(pmesh)

    test_plotter.create_plot(
        ["rho"],
        ["test"],
        ["magma"],  # the coolest cmap by the way
        stability_name="test",
        style_mode=True,
        iter=1,
        time=0,
    )

    assert os.path.exists("./output/plots/0001.png")

    os.remove("./output/plots/0001.png")
