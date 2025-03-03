# On turbulent magnetic reconnection: fast and slow mean steady-states

This repository contains all the files required to reproduce the data and figures within the paper, *On turbulent magnetic reconnection: fast and slow mean steady-states*

 - [preprint](https://arxiv.org/abs/2409.07346)

## Installation and Required Software

All the data-analysis and image generation is done via python scripts for which the following packages are required:

 - [Matplotlib](https://matplotlib.org/) &mdash; v3.9.2 
 - [NumPy](https://numpy.org/) &mdash; v1.26.4
 - [Xarray](https://docs.xarray.dev/en/stable/index.html) &mdash; v2023.6.0

The [Dask](https://docs.dask.org/en/stable/index.html) library is highly recommended to enable parallelized read/write operations via Xarray.  All version numbers are the versions used in this project.  It is likely that most modern versions of these packages will suffice.

We use the fluid simulation framework [BOUT++](https://github.com/boutproject/BOUT-dev) v5.1.1.  To install, follow the instructions on the [Getting Started](https://bout-dev.readthedocs.io/en/latest/user_docs/installing.html) page of their [documentation](https://bout-dev.readthedocs.io/en/latest/index.html).  The minimal installation (without SUNDIALS, PETSC, etc.) will be enough to run the code in this repository.  

## Code Structure

The repository is laid out as follows:

 - **simulation_files**

Contains all of the required input files to run the BOUT++ code that generates the results used in the Turbulent Reconnection Model.  Command line arguments can be used to change the values of $C_\tau$ and $C_\beta$ as in the paper.  The *parameter_scan_in_C_tau* subdirectory contains the BOUT.setting, BOUT.inp, and a BOUT.log file that was used to generate the original data. 

 - **analysis_files**

Contains the python scripts that calculate the various quantities ($U_{\rm a,in}$, $R_m$, etc) from the simulations.  

- **figure_files**

Contains all of the code used to generate each figure in the paper. All code contains an initial commented block as documentation. These scripts will not work 'out of the box'.  Some modification is required to point them to the correct data files on your local machine.  

## Questions and Contact Details

I am available via email (see email address for correspondence in the [paper](https://arxiv.org/abs/2409.07346) for any questions or issues regarding the code used in this repository.
