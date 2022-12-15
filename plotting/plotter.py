import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append("..")
from src.mesh import PsychoArray


class Plotter:
    """Creates plots for the desired variables

    Parameters
    ----------
    pmesh : PsychoArray
        PsychoArray mesh which contains all of the current mesh information
        and the conserved variables Un

    Attributes
    ----------
    ng : int
        Number of ghost cells

    rho : ndarray[float]
        Array containing the rho (density) value at each point in space at
        a given time

    u : ndarray[float]
        Array containing the u (horizontal velocity) value at each
        point in space at a given time

    v : ndarray[float]
        Array continaing the v (vertical velocity) value at each point
        in space at a given time

    et : ndarray[float]
        Array containing the et (total energy) value at each point in space
        at a given time

    primitives: dict
        Dictionary containing each primitive (rho, u, v, et) with a corresponding
        key

    x1 : ndarray[float]
        Vector containing the x1 values

    x2 : ndarray[float]
        Vector containing the x2 values

    x1_plot : ndarray[float]
        Array of x1 values after using meshrid for plotting

    x2_plot : ndarray[float]
        Array of x2 values after using meshgrid for plotting

    """

    def __init__(self, pmesh: PsychoArray):

        # Get information from the mesh needed needed for plotting
        self.ng = pmesh.ng
        self.rho = pmesh.Un[0, self.ng : -self.ng, self.ng : -self.ng]
        self.u = pmesh.Un[1, self.ng : -self.ng, self.ng : -self.ng] / self.rho
        self.v = pmesh.Un[2, self.ng : -self.ng, self.ng : -self.ng] / self.rho
        self.et = pmesh.Un[3, self.ng : -self.ng, self.ng : -self.ng] / self.rho
        self.primitives = {"rho": self.rho, "u": self.u, "v": self.v, "et": self.et}

        # Create grid for plotting
        self.x1 = np.arange(pmesh.x1min, pmesh.x1max, pmesh.dx1)
        self.x2 = np.arange(pmesh.x2min, pmesh.x2max, pmesh.dx2)
        self.x1_plot, self.x2_plot = np.meshgrid(self.x1, self.x2)

    def check_path_exists(
        self,
    ) -> None:
        """Checks output path and creates it if necessary"""

        if not os.path.exists("./output/plots"):
            os.makedirs("./output/plots")

    def create_plot(
        self,
        variables_to_plot: list[str],
        labels: list[str],
        cmaps: list[str],
        stability_name: str,
        style_mode: bool,
        iter: int,
        time: float,
    ) -> None:
        """Creates desired plots for provided input variables at a given time

        Parameters
        ----------
        variables_to_plot : list[str]
            A list of strings containing the variables to be
            plotted
        labels : list[str]
            The corresponding labels for the variables (can be in LaTeX form)
        cmaps : list[str]
            The desired cmaps for each variable - entered in the corresponding
            order
        stability_name : str
            The name of the instability
        style_mode : bool
            Style_mode will turn off all extra text and display only the
            desired variable in full in the figure
        iter : int
            The current iteration
        time : float
            The current time
        """

        # Check to make sure desired output is one that exists
        if not any(
            [True for check in variables_to_plot if check in self.primitives.keys()]
        ):
            raise Exception(
                "Please input only valid variables \n Valid variables are: rho, u, v, et"
            )

        # Check if output directory exists
        self.check_path_exists()

        # Create plots for each variable, if more than 3 plots then add another row
        num_of_variables = len(variables_to_plot)

        if num_of_variables <= 3:
            fig, axs = plt.subplots(
                1,
                num_of_variables,
            )
        else:
            fig, axs = plt.subplots(2, 2, figsize=(10, 10))

        if num_of_variables == 1:

            var = variables_to_plot[0]
            cmaps = cmaps[0]
            labels = labels[0]

            axs.set_xlim((self.x1[0], self.x1[-1]))
            axs.set_ylim((self.x2[0], self.x2[-1]))

            cf = axs.contourf(
                self.x1_plot,
                self.x2_plot,
                np.rot90(self.primitives[var]),
                100,
                cmap=cmaps,
            )

            if not style_mode:
                axs.set_aspect("equal")

            axs.tick_params(
                axis="both",
                which="both",
                bottom=False,
                left=False,
                labelbottom=False,
                labelleft=False,
            )

            if not style_mode:
                cbar = fig.colorbar(
                    cf,
                    fraction=0.046,  # magic scaling I found to keep the
                    pad=0.04,  # colorbar the same size as the figure
                    orientation="horizontal",
                    label=rf"${labels}$",
                )

                ticks = np.linspace(
                    np.amin(self.primitives[var]), np.amax(self.primitives[var]), 5
                )
                cbar.set_ticks(ticks)

        else:
            count = 0
            for ax, var in zip(axs.flat, variables_to_plot):

                ax.set_xlim((self.x1[0], self.x1[-1]))
                ax.set_ylim((self.x2[0], self.x2[-1]))

                cf = ax.contourf(
                    self.x1_plot,
                    self.x2_plot,
                    np.rot90(self.primitives[var]),
                    100,
                    cmap=cmaps[count],
                )

                ax.set_aspect("equal")

                ax.tick_params(
                    axis="both",
                    which="both",
                    bottom=False,
                    left=False,
                    labelbottom=False,
                    labelleft=False,
                )

                if not style_mode:
                    cbar = fig.colorbar(
                        cf,
                        fraction=0.046,
                        pad=0.04,
                        orientation="horizontal",
                        label=rf"${labels[count]}$",
                    )

                    ticks = np.linspace(
                        np.amin(self.primitives[var]), np.amax(self.primitives[var]), 5
                    )
                    cbar.set_ticks(ticks)
                    count += 1

        # Save the output plot and adjust the figure settings
        striter = str(iter).zfill(4)

        if not style_mode:
            fig.tight_layout()
            fig.set_facecolor("lightgray")
            fig.subplots_adjust(top=0.87)
            fig.suptitle(
                stability_name + f"\n(t = {time:.3f} sec)",
                fontsize="xx-large",
                fontweight="bold",
                y=0.95,
            )
            if num_of_variables == 1:
                fig.suptitle(
                    stability_name + f"\n(t = {time:.3f} sec)",
                    fontsize="x-large",
                    fontweight="bold",
                    y=0.97,
                )

        if style_mode:
            fig.tight_layout(pad=0)
            fig.set_facecolor("dimgray")
            plt.savefig("output/plots/" + f"{striter}.png")
        plt.savefig("output/plots/" + f"{striter}.png")
        plt.close()

        return
