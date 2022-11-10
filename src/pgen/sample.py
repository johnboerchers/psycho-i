###################################################################
#                                                                 #
#         Contains sample problem generator for sample.in         #
#                                                                 #
###################################################################

import sys
sys.path.append("../..")

import src.mesh
import src.input

class SamplePgen:

    def __init__(self, pin: src.input.PsychoInput):

        self.pin   = pin

    def ProblemGenerator(self, pmesh: src.mesh.PsychoArray):
        """
        This function is called in `main.py` and sets the initial conditions
        specified in the problem input (pin) onto the problem mesh (pmesh).

        Needs to exist for each problem type in order for everything to work.
        """
        pass
