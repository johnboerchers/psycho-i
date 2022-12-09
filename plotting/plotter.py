import matplotlib.pyplot as plt
import numpy as np
import sys
import itertools
sys.path.append("..")
from src.mesh import PsychoArray


class PlotterFromFile:
    """Extends Matplotlib for plotting the output
    from the solver"""

    def __init__(self, datafiles: dict[str, str], grid_info: dict):

        # Get and store the data and info
        self.datafiles = datafiles
        self.grid_info = grid_info

        # Extract information needed for plotting
        self.dx = grid_info['dx']
        self.dy = grid_info['dy']
        self.Nx = grid_info['Nx']
        self.Ny = grid_info['Ny']

        self.x = [self.dx * self.Nx for self.Nx in range(self.Nx)]
        self.y = [self.dy * self.Ny for self.Ny in range(self.Ny)]
        self.xp, self.yp = np.meshgrid(self.x, self.y)


    def create_plot(self, *args) -> None:

        # Load in data to be plotted
        if not set(args).issubset(self.datafiles):
            raise Exception("The output you wish to plot was not in the data file")

        data = np.zeros((len(args), self.Nx + 1, self.Ny + 1))
        for iter, each_var in enumerate(args):
            data[iter] = np.loadtxt("./plotting/" + f"{self.datafiles[each_var]}")


        # Create plots for variable supplied in
        # args
        fig, axs = plt.subplots(1, len(args))

        for count, ax in enumerate(axs.flat):
            ax.set_xlim((self.x[0], self.x[-1]))
            ax.set_ylim((self.y[0], self.y[-1]))

            cf = ax.contourf(self.xp, self.yp, data[count], 100, cmap ='jet')
            cbar = fig.colorbar(cf, label = f'{args[count]}')

        plt.show()


class PlotterDuringRun:
    """Extends Matplotlib for plotting output during the
    run"""

    def __init__(self, pmesh: PsychoArray):

        # Get information from the mesh needed
        # for plotting
        self.ng = pmesh.ng
        self.rho = pmesh.Un[0, self.ng:-self.ng, self.ng:-self.ng]
        self.u = pmesh.Un[1, self.ng:-self.ng, self.ng:-self.ng] / self.rho
        self.v = pmesh.Un[2, self.ng:-self.ng, self.ng:-self.ng] / self.rho
        self.et = pmesh.Un[3, self.ng:-self.ng, self.ng:-self.ng] / self.rho
        self.primitives = {"rho": self.rho, "u": self.u, "v": self.v, "et": self.et}

        # Create grid for plotting
        self.x1 = np.arange(pmesh.x1min, pmesh.x1max, pmesh.dx1)
        self.x2 = np.arange(pmesh.x2min, pmesh.x2max, pmesh.dx2)
        self.x1_plot, self.x2_plot = np.meshgrid(self.x1, self.x2)


    def create_plot(self, variables_to_plot: list[str], iter: int) -> None:

        # Check to make sure desired output is one that exists and
        # then pull the values which do exist
        if not any([True for check in variables_to_plot if check in self.primitives.keys()]):
            raise Exception("Please input only valid variables \n Valid variables are: rho, u, v, et")        

        # Create plots for each variable, if more than 2 plots
        # then create a new row
        mod = len(variables_to_plot) % 2
        if len(variables_to_plot) <= 2:
            fig, axs = plt.subplots(1, len(variables_to_plot))
        else:
            fig, axs = plt.subplots(2, len(variables_to_plot) - mod)

        for ax, var in zip(axs.flat, variables_to_plot): 
            ax.set_xlim((self.x1[0], self.x1[-1]))
            ax.set_ylim((self.x2[0], self.x2[-1]))

            cf = ax.contourf(self.x1_plot, self.x2_plot, np.rot90(self.primitives[var]), 100, cmap ='jet')
            ax.set_aspect('equal')
            fig.colorbar(cf, label = f'{var}')

        striter = str(iter).zfill(4)
        plt.savefig(f"{striter}.png")
        plt.close()

