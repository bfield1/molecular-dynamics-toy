# molecular-dynamics-toy
An interactive molecular dynamics simulation GUI.

This app lets you run a real molecular dynamics simulation on
your laptop or home computer. It includes interactive features like
clicking to add new atoms, changing the temperature and simulation cell size
live, and loading preset atomic configurations.

It uses a pre-trained universal machine learning interatomic potential 
([MatterSim](https://microsoft.github.io/mattersim/)) with a molecular
dynamics integrator from the
[Atomic Simulation Environment](https://ase-lib.org/) to do the physics, then
provides the graphical user interface using [pygame](https://www.pygame.org/).

Physical limitations of this simulation are those of the chosen interatomic
potential. Specifically, MatterSim is optimised for bulk materials (i.e. things
which fill the whole unit cell) and not for molecules or chemical reactivity.
While the physics engine is science-grade, this app is intended for
demonstration purposes, and no warranty is given for the accuracy
of any results.

## Installation

Set up a virtual Python environment, such as with
[Conda](https://docs.conda.io/projects/conda/en/stable/user-guide/getting-started.html).

After installing Conda, you can create a Conda environment in the command
line with
```
conda env create -n mdtoy "python=3.13"
conda activate mdtoy
```
(You can replace "mdtoy" with a name of your choice.)

Then, install the app with
```
pip install git+https://github.com/bfield1/molecular-dynamics-toy
```

Finally, run the app with
```
python -m molecular_dynamics_toy
```
It will automatically download the pre-trained Mattersim model the first time
you run it.

(You will need to have the virtual environment you created earlier active,
so if you open a new terminal run `conda activate mdtoy` again.)
