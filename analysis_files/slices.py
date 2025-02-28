import xarray as xr
import numpy as np

def prefunc(ds):
    return ds.drop_isel(x=[0,1,-2,-1])

Lz = 80
Lx = 10

for C_tau in [0.5, 1.0, 1.5, 2.0]:
    filenames = [f'../data/tau_{C_tau}/BOUT.dmp.{i}.nc' for i in range(32)]

    ds = xr.open_mfdataset(filenames,concat_dim="x", combine="nested",data_vars='minimal', coords='minimal', compat='override',preprocess=prefunc, chunks='auto', parallel=True, engine='h5netcdf').squeeze()

    ds.coords['z'] = ds.z * Lz/len(ds.z) - Lz/2
    ds.coords['x'] = ds.x * Lx/len(ds.x) - Lx/2

    np.savetxt('./summary_statistics/K_across_tau' + str(C_tau) + '.txt', ds.K.sel(z=0,method="nearest").squeeze().values)
    np.savetxt('./summary_statistics/K_along_tau'  + str(C_tau) + '.txt', ds.K.sel(x=0,method="nearest").squeeze().values)
