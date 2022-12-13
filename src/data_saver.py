# Reads data saving preferences; Saves requested variable data using requested file format and print frequency

import sys

sys.path.append("../..")

import src.mesh
import src.input
from src.tools import get_primitive_variables_2d
import numpy as np
import h5py


class PsychoOutput:
    """Class for producing the desired output

    Produces the desired output variables in the desired
    format - set in the problem input

    Attributes
    ----------
    input_fname : str
        File name for the output file

    """

    def __init__(self, input_fname: str):

        self.input_fname = input_fname

        # Dictionary containing all problem information
        self.value_dict = dict()

    def data_preferences(self, pin: src.input.PsychoInput) -> None:
        """
        This function is called in `psycho.py` and sets the data preferences
        specified in the problem input (pin).

        Parameters
        ----------
        pin : PsychoInput
            Contains the problem information stored in the PsychoInput
            object

        """

        self.Nx = pin.value_dict["nx1"]

        self.Ny = pin.value_dict["nx2"]

        self.shape = (self.Nx,self.Ny)

        # Get output variables as a list
        self.variables = pin.value_dict["output_variables"]

        # Get output frequency
        self.frequency = pin.value_dict["output_frequency"]

        # Get output file type
        self.file_type = pin.value_dict["data_file_type"]

        self.file_type_check = 0
        
        if "txt" in self.file_type:

            self.density_file = open("density.txt", "w").close()
            self.xvelocity_file = open("x-velocity.txt", "w").close()
            self.yvelocity_file = open("y-velocity.txt", "w").close()
            self.pressure_file = open("pressure.txt", "w").close()
            self.iter_time_file = open("iter_time.txt", "w").close()
            
            self.density_file = open("density.txt", "w")
            self.xvelocity_file = open("x-velocity.txt", "w")
            self.yvelocity_file = open("y-velocity.txt", "w")
            self.pressure_file = open("pressure.txt", "w")
            self.iter_time_file = open("iter_time.txt", "w")

            self.file_type_check = 1

        if "csv" in self.file_type:

            self.density_file = open("density.csv", "w").close()
            self.xvelocity_file = open("x-velocity.csv", "w").close()
            self.yvelocity_file = open("y-velocity.csv", "w").close()
            self.pressure_file = open("pressure.csv", "w").close()
            self.iter_time_file = open("iter_time.csv", "w").close()
            
            self.density_file = open("density.csv", "w")
            self.xvelocity_file = open("x-velocity.csv", "w")
            self.yvelocity_file = open("y-velocity.csv", "w")
            self.pressure_file = open("pressure.csv", "w")
            self.iter_time_file = open("iter_time.csv", "w")

            self.file_type_check = 2


        if "hdf5" in self.file_type:

            self.file_type_check = 3

        
        if self.file_type_check==0:

            raise ValueError("No correctly spelled output file type specified in input.")
    
    
    def save_data(
        self, pmesh: src.mesh.PsychoArray, t: float, tmax: float, gamma: float, iter: float
    ) -> None:
        """Saves the data to to the desired format

        Parameters
        ----------
        pmesh : PsychoArray
            PsychoArray mesh which contains all of the mesh information
            and the conserved variables, Un

        t : float
            The current time

        tmax : float
            The maximum time or the time the simulations runs until

        gamma : float
            Specific heat ratio

        """
        
        if (self.file_type_check==1): # writing to txt file

            self.iter_time_file.write(str(iter))
            self.iter_time_file.write(' ')
            self.iter_time_file.write(str(t))
            self.iter_time_file.write('\n')

        if (self.file_type_check==2): # writing to csv file

            self.iter_time_file.write(str(iter))
            self.iter_time_file.write(',')
            self.iter_time_file.write(str(t))
            self.iter_time_file.write('\n')
 
        if (self.file_type_check==3):

            file_name = str(iter)
            self.f = h5py.File(f'iter_{file_name}.hdf5', 'w')

            self.dset_time = self.f.create_dataset("time_dataset", data=t)


        rho, u, v, p = get_primitive_variables_2d(pmesh,gamma)
    
        var_check = 0           

        if "x-velocity" in self.variables:

            var_check = 1
            
            self.xvelocity = np.empty(self.shape,dtype=float)

            for j in reversed(range(u.shape[0]-4)):

                    for i in range(u.shape[1]-4):

                        self.xvelocity[i][j] = u[i+2][j+2]

            if (self.file_type_check==1): # writing to txt file
            
                for j in reversed(range(self.xvelocity.shape[0])):

                    for i in range(self.xvelocity.shape[1]):

                        self.xvelocity_file.write(str(self.xvelocity[i][j]))
                        self.xvelocity_file.write(' ')

                    self.xvelocity_file.write('\n')
            
            if (self.file_type_check==2): # writing to csv file
    
                for j in reversed(range(self.xvelocity.shape[0])):

                    for i in range(self.xvelocity.shape[1]):
                        
                        self.xvelocity_file.write(str(self.xvelocity[i][j]))
                        self.xvelocity_file.write(',')

                    self.xvelocity_file.write('\n')
                
                        
            if (self.file_type_check==3): # writing to hdf5 file

                self.dset_xvelocity = self.f.create_dataset("xvelocity_dataset", data=self.xvelocity)


        if "y-velocity" in self.variables:

            var_check = 1

            self.yvelocity = np.empty(self.shape,dtype=float)

            for j in reversed(range(v.shape[0]-4)):

                    for i in range(v.shape[1]-4):

                        self.yvelocity[i][j] = v[i+2][j+2]

            if (self.file_type_check==1): # write to txt

                for j in reversed(range(self.yvelocity.shape[0])):

                    for i in range(self.yvelocity.shape[1]):

                        self.yvelocity_file.write(str(self.yvelocity[i][j]))
                        self.yvelocity_file.write(' ')

                    self.yvelocity_file.write('\n')
            
            if (self.file_type_check==2): # write to csv file
                
                for j in reversed(range(self.yvelocity.shape[0])):

                    for i in range(self.yvelocity.shape[1]):
                        
                        self.yvelocity_file.write(str(self.yvelocity[i][j]))
                        self.yvelocity_file.write(',')

                    self.yvelocity_file.write('\n')

            if(self.file_type_check==3): # write to hdf5

                self.dset_yvelocity = self.f.create_dataset("yvelocity_dataset", data=self.yvelocity)
            
        if "density" in self.variables:

            var_check = 1

            self.density = np.empty(self.shape,dtype=float)

            for j in reversed(range(rho.shape[0]-4)):

                    for i in range(rho.shape[1]-4):

                        self.density[i][j] = rho[i+2][j+2]

            if (self.file_type_check==1): # write to txt

                for j in reversed(range(self.density.shape[0])):

                    for i in range(self.density.shape[1]):

                        self.density_file.write(str(self.density[i][j]))
                        self.density_file.write(' ')

                    self.density_file.write('\n')
            
            if (self.file_type_check==2): # write to csv file

                for j in reversed(range(self.density.shape[0])):

                    for i in range(self.density.shape[1]):
                        
                        self.density_file.write(str(self.density[i][j]))
                        self.density_file.write(',')

                    self.density_file.write('\n')

            if (self.file_type_check==3): # write to hdf5

                self.dset_density = self.f.create_dataset("density_dataset", data=self.density)

        if "pressure" in self.variables:

            var_check = 1

            self.pressure = np.empty(self.shape,dtype=float)

            for j in reversed(range(p.shape[0]-4)):

                    for i in range(p.shape[1]-4):

                        self.pressure[i][j] = p[i+2][j+2]

            if (self.file_type_check==1): # write to txt

                for j in reversed(range(self.pressure.shape[0])):

                    for i in range(self.pressure.shape[1]):

                        self.pressure_file.write(str(self.pressure[i][j]))
                        self.pressure_file.write(' ')

                    self.pressure_file.write('\n')

            if (self.file_type_check==2): # write to csv

                for j in reversed(range(self.pressure.shape[0])):

                    for i in range(self.pressure.shape[1]):
                        
                        self.pressure_file.write(str(self.pressure[i][j]))
                        self.pressure_file.write(',')

                    self.pressure_file.write('\n')

            if (self.file_type_check==3): # write to hdf5
                self.dset_pressure = self.f.create_dataset("pressure_dataset", data=self.pressure)


        if (var_check==0):

            raise ValueError("No correctly spelled output variables specified in input.")


        if (t>=tmax):

            if "hdf5" in self.file_type:

                self.f.close()

            else:

                self.density_file.close()
                self.xvelocity_file.close()
                self.yvelocity_file.close()
                self.pressure_file.close()
                self.iter_time_file.close()
