# On turbulent magnetic reconnection: fast and slow mean steady-states

This repository contains all the files required to reproduce the data and figures within the paper [On turbulent magnetic reconnection: fast and slow mean steady-states](https://arxiv.org/abs/2409.07346)

## Installation and Required Software

All the data-analysis and image generation is done via python scripts for which the following packages are required:
    - [Matplotlib](https://matplotlib.org/) &mdash; version 
    - [NumPy](https://numpy.org/) &mdash; version 
    - [Xarray](https://docs.xarray.dev/en/stable/index.html) &mdash; version 
The [Dask](https://docs.dask.org/en/stable/index.html) library is highly recommended to enable parallelized read/write operations via Xarray.

We use the fluid simulation framework [BOUT++](https://github.com/boutproject/BOUT-dev).  To install, follow the instructions on the [Getting Started](https://bout-dev.readthedocs.io/en/latest/user_docs/installing.html) page of their [documentation](https://bout-dev.readthedocs.io/en/latest/index.html).  The minimal installation (without SUNDIALS, PETSC, etc.) will be enough to run the code in this repository.  

