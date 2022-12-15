# PSYCHo-I - **P**ython **S**imulations **Y**ielding **H**ydr**o**dynamic **I**nstabilities
### A Python simulation code with finite volume compressible inviscid fluid solver



https://user-images.githubusercontent.com/54543048/207175783-6b93c8c6-138b-46ab-822a-b1eefbb44385.mov



## Implemented problems
- Kelvin-Helmholtz Instability
### Future problems
- Rayleigh-Taylor Instability
- Rayleigh-Benard Convection
- Richtmeyer-Meshkov Instability

## How to run

In order to run, activate the conda environment contained in `workflow/environment.yaml`. From there, the following command can be run from the main directory

```python psycho.py -p problem_name```

Where `problem_name` is the name of the problem being ran, corresponding to the name of the input file and problem generator file. For example, to run the Kelvin-Helmholtz instability problem, execute the command `python psycho.py -p kh`.

The outputs from the simulation for plotting can be found in `outputs/plots`.

Documentation for specifics about each of the functions present in the code can be found here: https://johnboerchers.github.io/psycho-i/index.html

## Implementing new problems

In order to implement new problems, it is as simple as adding a problem generator file in `src/pgen` with the corresponding problem name, and adding an input file to the `inputs` directory. There are template/sample files available in those directories to assist in implementing a new problem.

Next, in order for psycho to recognize the problem when set on the command line, in `psycho.py`, the new problem generator file needs to be imported, and a new conditional statement needs to be added underneath:

```
if problem_name == "kh":
        problem_generator = kh.ProblemGenerator
```

for the new file to be recognized and the correct problem generator to be used. From there, running the original run command with the new problem name should successfully execute the new problem.

## Solver information (and citation)

The solver implemented in `psycho-i` is a MUSCL-Hancock scheme as described in [1]. Specifically, it is a 2-dimensional finite volume solver for the inviscid Euler equations, with a minmod slope limiter and and HLLC Riemann solver (also explained extensively in [1]).

[1] Toro, E. F. (2011). Riemann solvers and Numerical Methods for fluid dynamics: A practical introduction. Springer.
