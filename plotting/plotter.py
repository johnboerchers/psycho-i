import matplotlib.pyplot as plt
import numpy as np

<<<<<<< HEAD

=======
>>>>>>> cefd7c3 (Added architecture for plotting)
class Plotter:
    """Extends Matplotlib for plotting the output
    from the solver"""

    def __init__(self, datafiles: dict[str, str], grid_info: dict):
<<<<<<< HEAD

        # Get and store the data and info
        self.datafiles = datafiles
        self.grid_info = grid_info

        # Extract information needed for plotting
        self.dx = grid_info["dx"]
        self.dy = grid_info["dy"]
        self.Nx = grid_info["Nx"]
        self.Ny = grid_info["Ny"]
=======
        
        # Get and store the data and info
        self.datafiles = datafiles
        self.grid_info = grid_info
        print(self.datafiles.keys())

        # Extract information needed for plotting
        self.dx = grid_info['dx']
        self.dy = grid_info['dy']
        self.Nx = grid_info['Nx']
        self.Ny = grid_info['Ny']
>>>>>>> cefd7c3 (Added architecture for plotting)

        self.x = [self.dx * self.Nx for self.Nx in range(self.Nx)]
        self.y = [self.dy * self.Ny for self.Ny in range(self.Ny)]
        self.xp, self.yp = np.meshgrid(self.x, self.y)

<<<<<<< HEAD
    def create_plot(self, *args) -> None:

=======

    def create_plot(self, *args) -> None:
        
>>>>>>> cefd7c3 (Added architecture for plotting)
        # Load in data to be plotted
        if not set(args).issubset(self.datafiles):
            raise Exception("The output you wish to plot was not in the data file")

        data = np.zeros((len(args), self.Nx + 1, self.Ny + 1))
        for iter, each_var in enumerate(args):
<<<<<<< HEAD
            data[iter] = np.loadtxt("./plotting/" + f"{self.datafiles[each_var]}")
=======
            data[iter] = np.loadtxt('./plotting/' + f'{self.datafiles[each_var]}')
>>>>>>> cefd7c3 (Added architecture for plotting)

        # Create plots for variable supplied in
        # args
        fig, axs = plt.subplots(1, len(args))

        for count, ax in enumerate(axs.flat):
            ax.set_xlim((self.x[0], self.x[-1]))
            ax.set_ylim((self.y[0], self.y[-1]))
<<<<<<< HEAD
            cf = ax.contourf(self.xp, self.yp, data[count], 100, cmap="jet")
            fig.colorbar(cf, label=f"{args[count]}")

        plt.show()
=======
            cf = ax.contourf(self.xp, self.yp, data[count], 100, cmap ='jet')
            cbar = fig.colorbar(cf, label = f'{args[count]}')

        plt.show()


if __name__ == '__main__':
    grid_sizing = {'dx': 0.2, 'dy': 0.2, 'Nx': 5, 'Ny': 5}
    plotter = Plotter({'u': 'sample_u.txt', 'v': 'sample_v.txt'}, grid_sizing)
    plotter.create_plot('u', 'v')
>>>>>>> cefd7c3 (Added architecture for plotting)
