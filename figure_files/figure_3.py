#
# Generates figure 3 in Turbulent Magnetic Reconnection: fast and slow 
# mean steady states
# 
# Images of the plasma current.
#
import sys
import os
import xarray as xr
import matplotlib.pyplot as plt
import dask
from glob import glob

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica",
    "font.size" : 24
})


taus = [0.1, 0.1, 1.0, 1.0, 2.5, 2.5]
times = [10, 91, 10, 63, 10, 146]

for tau, time in zip(taus,times):

    ds = xr.open_dataarray('$SIMULATION_DIR' + f'/j_par_tau_{tau}_t_{time}.nc')

    fig, ax = plt.subplots(figsize=(8,4),layout='tight')

    ds.plot(ax=ax,add_labels=False)
    ax.set_xlabel('$z$')
    ax.set_ylabel('$x$')
    ax.set_title(f'$t={time}$')
    plt.savefig(f'./j_par_tau_{tau}_t_{time}.png')
    plt.close()
