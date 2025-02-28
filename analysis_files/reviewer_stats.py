import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def prefunc(ds):
    return ds.drop_isel(x=[0,1,-2,-1])

Lz = 80
Lx = 10

for C_tau in [0.5, 1.0, 1.5]:
    filenames = [f'../data/tau_{C_tau}/BOUT.dmp.{i}.nc' for i in range(32)]

    ds = xr.open_mfdataset(filenames,concat_dim="x", combine="nested",data_vars='minimal', coords='minimal', compat='override',preprocess=prefunc, chunks='auto', parallel=True, engine='h5netcdf').squeeze()

    ds.coords['z'] = ds.z * Lz/len(ds.z) - Lz/2
    ds.coords['x'] = ds.x * Lx/len(ds.x) - Lx/2

    eta_eff = 5e-4 + 0.3*C_tau*(1/(np.sqrt(0.3)*np.pi))*ds.K.sel(x=0,z=0,method='nearest')
    Diffusion = (5e-4 + 0.3*C_tau*(1/(np.sqrt(0.3)*np.pi))*ds.K)*np.abs(ds.j_par)

    length_mask = xr.where(Diffusion.sel(z=slice(-10,10))>2*Diffusion.sel(z=slice(-10,10)).sel(x=0,method='nearest').mean(dim=['z']),1,0)
    lengths = np.abs(2*ds.z.sel(z=slice(-10,10)).where(length_mask==1).sel(x=0,method='nearest').max(dim='z').values)

    vz = -1*ds.psi.differentiate('x')

    vout = []

    for i,l in enumerate(lengths):
        if np.isnan(l):
            vout.append(0)
        else:
            vout.append( float( vz.isel(t=t).sel(x=0,z=float(l/2)) ) )
        
    np.savetxt('./summary_statistics/outflow_tau_' + str(C_tau) + '.txt', vout)
