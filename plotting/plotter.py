import matplotlib.pyplot as plt
import numpy as np

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> cefd7c3 (Added architecture for plotting)
=======

>>>>>>> 9d988f1 (Formatting changes)
class Plotter:
    """Extends Matplotlib for plotting the output
    from the solver"""

    def __init__(self, datafiles: dict[str, str], grid_info: dict):
<<<<<<< HEAD
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
        
=======

>>>>>>> 9d988f1 (Formatting changes)
        # Get and store the data and info
        self.datafiles = datafiles
        self.grid_info = grid_info
        print(self.datafiles.keys())

        # Extract information needed for plotting
<<<<<<< HEAD
        self.dx = grid_info['dx']
        self.dy = grid_info['dy']
        self.Nx = grid_info['Nx']
        self.Ny = grid_info['Ny']
>>>>>>> cefd7c3 (Added architecture for plotting)
=======
        self.dx = grid_info["dx"]
        self.dy = grid_info["dy"]
        self.Nx = grid_info["Nx"]
        self.Ny = grid_info["Ny"]
>>>>>>> 9d988f1 (Formatting changes)

        self.x = [self.dx * self.Nx for self.Nx in range(self.Nx)]
        self.y = [self.dy * self.Ny for self.Ny in range(self.Ny)]
        self.xp, self.yp = np.meshgrid(self.x, self.y)

<<<<<<< HEAD
<<<<<<< HEAD
    def create_plot(self, *args) -> None:

=======

    def create_plot(self, *args) -> None:
        
>>>>>>> cefd7c3 (Added architecture for plotting)
=======
    def create_plot(self, *args) -> None:

>>>>>>> 9d988f1 (Formatting changes)
        # Load in data to be plotted
        if not set(args).issubset(self.datafiles):
            raise Exception("The output you wish to plot was not in the data file")

        data = np.zeros((len(args), self.Nx + 1, self.Ny + 1))
        for iter, each_var in enumerate(args):
<<<<<<< HEAD
<<<<<<< HEAD
            data[iter] = np.loadtxt("./plotting/" + f"{self.datafiles[each_var]}")
=======
            data[iter] = np.loadtxt('./plotting/' + f'{self.datafiles[each_var]}')
>>>>>>> cefd7c3 (Added architecture for plotting)
=======
            data[iter] = np.loadtxt("./plotting/" + f"{self.datafiles[each_var]}")
>>>>>>> 9d988f1 (Formatting changes)

        # Create plots for variable supplied in
        # args
        fig, axs = plt.subplots(1, len(args))

        for count, ax in enumerate(axs.flat):
            ax.set_xlim((self.x[0], self.x[-1]))
            ax.set_ylim((self.y[0], self.y[-1]))
<<<<<<< HEAD
<<<<<<< HEAD
            cf = ax.contourf(self.xp, self.yp, data[count], 100, cmap="jet")
            fig.colorbar(cf, label=f"{args[count]}")

        plt.show()
=======
            cf = ax.contourf(self.xp, self.yp, data[count], 100, cmap ='jet')
            cbar = fig.colorbar(cf, label = f'{args[count]}')
=======
            cf = ax.contourf(self.xp, self.yp, data[count], 100, cmap="jet")
            fig.colorbar(cf, label=f"{args[count]}")
>>>>>>> 9d988f1 (Formatting changes)

        plt.show()


<<<<<<< HEAD
if __name__ == '__main__':
    grid_sizing = {'dx': 0.2, 'dy': 0.2, 'Nx': 5, 'Ny': 5}
    plotter = Plotter({'u': 'sample_u.txt', 'v': 'sample_v.txt'}, grid_sizing)
    plotter.create_plot('u', 'v')
>>>>>>> cefd7c3 (Added architecture for plotting)
=======
if __name__ == "__main__":
    grid_sizing = {"dx": 0.2, "dy": 0.2, "Nx": 5, "Ny": 5}
    plotter = Plotter({"u": "sample_u.txt", "v": "sample_v.txt"}, grid_sizing)
    plotter.create_plot("u", "v")
>>>>>>> 9d988f1 (Formatting changes)
