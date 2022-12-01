# Implementation of single timestep for MUSCL-Hancock

All of this can be seen on page 504 of the Toro pdf included in this directory

1. Enforce boundary conditions (two ghost cells are needed for this method)
    - Transmissive (ghost cells equal to adjacent interior points)
    - Periodic (ghost cells equal to real cells on opposite side of simulation volume)
    - Wall (velocities are set for no-slip on walls, density gradient is zero)

2. Data reconstruction
    - The current state of the variable $U_i^n$ is stored in `pmesh.arr` (I will probably change this to be labeled as `pmesh.Un` instead).
    - **Trevor** will implement code to calculate the slopes of the quantities at each of the spaces, denoted as $\Delta_i$ for the x-direction and $\Delta_j$ for the y-direction.
    - Then *boundary extrapolated values* are calculated as follows. This step is just like the interpolation in the finite difference method, except a slope limiter is used to help combat oscillations (**Trevor** is worrying about that part). Stay tuned for Trevor to update this to be in 2D.

    $$U_i^L = U_{i,j}^n - \frac{1}{2} \Delta_i, \,\, U_i^R = U_{i,j}^n + \frac{1}{2} \Delta_i$$
    $$U_j^L = U_{i,j}^n - \frac{1}{2} \Delta_j, \,\, U_j^R = U_{i,j}^n + \frac{1}{2} \Delta_j$$

3. Evolution
    - The boundary extrapolated values are then used to advance the left and right interpolated values of $U_i^n$ by half a timestep to get higher order solution.

    $$\bar U_i^L = U_i^L + \frac{1}{2} \frac{\Delta t}{\Delta x}\left[ F(U_i^L) - F(U_i^R) \right]$$
    $$\bar U_i^R = U_i^R + \frac{1}{2} \frac{\Delta t}{\Delta x}\left[ F(U_i^L) - F(U_i^R) \right]$$

    $$\bar U_j^L = U_j^L + \frac{1}{2} \frac{\Delta t}{\Delta y}\left[ G(U_j^L) - G(U_j^R) \right]$$
    $$\bar U_j^R = U_j^R + \frac{1}{2} \frac{\Delta t}{\Delta y}\left[ G(U_j^L) - G(U_j^R) \right]$$

    - $F(U)$ is the normal flux vector that was used with the finite difference formulation, except this time with no viscosity and no thermal conduction (we could add them if we really wanted to but I don't think it would be worth the extra effort). The flux vector is the same shape as the `pmesh.arr` array but each of the 4 first indices is just the flux associated with that index.

4. Riemann Problem
    - **Trevor** will take charge of this part.

5. Conservative update

    $$U_i^{n+1} = U_i^n + \frac{\Delta t}{\Delta x} \left[ F_{i-\frac{1}{2}} - F_{i+\frac{1}{2}} \right] + \frac{\Delta t}{\Delta y} \left[ G_{j-\frac{1}{2}} - G_{i+\frac{1}{2}} \right]$$
