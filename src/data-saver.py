# Reads data saving preferences; function is called in main.py to output desired quantities
# Or make a class where each of the inputs is a property and the instance of the class is the output and can be inherited for plotting

import sys

sys.path.append("../..")

import src.mesh
import src.input
import src.tools
import numpy as np

class PsychoOutput:
    
    def __init__(self):
        self.data = np.array()

    def data_preferences(self, pin: src.input.PsychoInput) -> None:
        """
        This function is called in `main.py` (or psycho.py) and sets
        the data preferences specified in the problem input (pin).

        """

        # Get output variables as a list
        self.variables = pin.value_dict["output_variables"]
    

        # Get output frequency
        self.frequency = pin.value_dict["output_frequency"]
    

        # Get output file type
        self.file_type = pin.value_dict["data_file_type"]

        for i in range(self.data_file_type):
            if (self.filetype(i) == "txt"):
                density_file = open("density.txt", "a")
                xvelocity_file = open("x-velocity.txt", "a")
                yvelocity_file = open("y-velocity.txt", "a")
                pressure_file = open("pressure.txt", "a")
                total_energy_file = open("total-energy.txt", "a")
            elif (self.file_type(i) == "csv"):
                density_file = open("density.csv", "a")
                xvelocity_file = open("x-velocity.csv", "a")
                yvelocity_file = open("y-velocity.csv", "a")
                pressure_file = open("pressure.csv", "a")
                total_energy_file = open("total-energy.csv", "a")
            elif (self.file_type(i) == "pickle"):
                density_file = open("density.pkl", "a")
                xvelocity_file = open("x-velocity.pkl", "a")
                yvelocity_file = open("y-velocity.pkl", "a")
                pressure_file = open("pressure.pkl", "a")
                total_energy_file = open("total-energy.pkl", "a")
            elif (self.file_type(i) == "hdf5"):
                density_file = open("density.hdf5", "a")
                xvelocity_file = open("x-velocity.hdf5", "a")
                yvelocity_file = open("y-velocity.hdf5", "a")
                pressure_file = open("pressure.hdf5", "a")
                total_energy_file = open("total-energy.hdf5", "a")
            elif (self.file_type(i) == "numpy.save"):
                density_file = open("density.npy", "a")
                xvelocity_file = open("x-velocity.npy", "a")
                yvelocity_file = open("y-velocity.npy", "a")
                pressure_file = open("pressure.npy", "a")
                total_energy_file = open("total-energy.npy", "a")
            else: 
                raise ValueError("No output file type specified in input.")
    
    def save_data(self, pout: src.tools, pmesh: src.mesh.PsychoArray):
        vars = get_primitive_variables_2d(pmesh.Un)
        for i in range(self.variables):
            if (self.variables(i) == "x-velocity"):

                self.data[i,:,:] = vars(2)
                xvelocity_file.write(self.data[i,:,:])
                
            elif (self.variables(i) == "y-velocity"):

                self.data[i,:,:] = vars(3)
                yvelocity_file.write(self.data[i,:,:])

            elif (self.variables(i) == "density"):

                self.data[i,:,:] = vars(1)
                density_file.write(self.data[i,:,:])

            elif (self.variables(i) == "pressure"):

                self.data[i,:,:] = vars(4)
                pressure_file.write(self.data[i,:,:])

            elif (self.variables(i) == "total-energy"):

                self.data[i,:,:] = vars() # need to add as output in get_primitive_variables_2d
                total_energy_file.write(self.data[i,:,:])
            else:
                raise ValueError("No output variables specified in input.")

            if (last_iteration): # need to implement last_iteration in solver
                density_file.close()
                xvelocity_file.close()
                yvelocity_file.close()
                pressure_file.close()
                total_energy_file.close()

  
