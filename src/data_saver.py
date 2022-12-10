# Reads data saving preferences; function is called in main.py to output desired quantities
# Or make a class where each of the inputs is a property and the instance of the class is the output and can be inherited for plotting

import sys

sys.path.append("../..")

import src.mesh
import src.input
from src.tools import get_primitive_variables_2d
import numpy as np

class PsychoOutput:
    
    def __init__(self, input_fname: str):

        self.input_fname = input_fname

        # Dictionary containing all problem information
        self.value_dict = dict()

    def data_preferences(self, pin: src.input.PsychoInput) -> None:
        """
        This function is called in `psycho.py` and sets the data preferences
        specified in the problem input (pin).
        """

        # Get output variables as a list
        self.variables = pin.value_dict["output_variables"]
    

        # Get output frequency
        self.frequency = pin.value_dict["output_frequency"]
    

        # Get output file type
        self.file_type = pin.value_dict["data_file_type"]


        file_type_check = 0
        
        if "txt" in self.file_type:
            self.density_file = open("density.txt", "w")
            self.xvelocity_file = open("x-velocity.txt", "w")
            self.yvelocity_file = open("y-velocity.txt", "w")
            self.pressure_file = open("pressure.txt", "w")
            file_type_check = 1

        if "csv" in self.file_type:
            self.density_file = open("density.csv", "w")
            self.xvelocity_file = open("x-velocity.csv", "w")
            self.yvelocity_file = open("y-velocity.csv", "w")
            self.pressure_file = open("pressure.csv", "w")
            file_type_check = 1

        if "pickle" in self.file_type:
            self.density_file = open("density.pkl", "w")
            self.xvelocity_file = open("x-velocity.pkl", "w")
            self.yvelocity_file = open("y-velocity.pkl", "w")
            self.pressure_file = open("pressure.pkl", "w")
            file_type_check = 1

        if "hdf5" in self.file_type:
            self.density_file = open("density.hdf5", "w")
            self.xvelocity_file = open("x-velocity.hdf5", "w")
            self.yvelocity_file = open("y-velocity.hdf5", "w")
            self.pressure_file = open("pressure.hdf5", "w")
            file_type_check = 1

        if "numpy.save" in self.file_type:
            self.density_file = open("density.npy", "w")
            self.xvelocity_file = open("x-velocity.npy", "w")
            self.yvelocity_file = open("y-velocity.npy", "w")   
            self.pressure_file = open("pressure.npy", "w")
            file_type_check = 1
        
        if file_type_check==0:
            raise ValueError("No output file type specified in input.")
    

    def save_data(self, pmesh: src.mesh.PsychoArray, t, tmax, gamma):
        rho, u, v, p = get_primitive_variables_2d(pmesh,gamma)
    
        var_check = 0
        if "x-velocity" in self.variables:
            
            for j in reversed(range(u.shape[0]-4)):
                print(j)
                for i in reversed(range(u.shape[1]-4)):
                    self.xvelocity_file.write(str(u[i+2][j+2]))
                    self.xvelocity_file.write(' ')
                self.xvelocity_file.write('\n')
            
            var_check = 1

        if "y-velocity" in self.variables:   

            for j in reversed(range(v.shape[0]-4)):
                for i in reversed(range(v.shape[1]-4)):
                    self.yvelocity_file.write(str(v[i+2][j+2]))
                    self.yvelocity_file.write(' ')
                self.yvelocity_file.write('\n')
            
            var_check = 1
            
        if "density" in self.variables:

            for j in reversed(range(rho.shape[0]-4)):
                for i in reversed(range(rho.shape[1]-4)):
                    self.density_file.write(str(rho[i+2][j+2]))
                    self.density_file.write(' ')
                self.density_file.write('\n')
            
            var_check = 1

        if "pressure" in self.variables:

            for j in reversed(range(p.shape[0]-4)):
                for i in reversed(range(p.shape[1]-4)):
                    self.pressure_file.write(str(p[i+2][j+2]))
                    self.pressure_file.write(' ')
                self.pressure_file.write('\n')

            var_check = 1

        
        if (var_check==0):
            raise ValueError("No output variables specified in input.")

        if (t>=tmax):
            self.density_file.close()
            self.xvelocity_file.close()
            self.yvelocity_file.close()
            self.pressure_file.close()

  
