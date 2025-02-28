import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def prefunc(ds):
    return ds.drop_isel(x=[0,1,-2,-1])

Lz = 80
Lx = 10
N_proc = 32

for C_tau in [...]: # Put all the values of C_tau you are interested in calculating here.
    filenames = ['$DATA_DIR' + /f'tau_{C_tau}/BOUT.dmp.{i}.nc' for i in range(N_proc)]

    ds = xr.open_mfdataset(filenames,concat_dim="x", combine="nested",data_vars='minimal', coords='minimal', compat='override',preprocess=prefunc, chunks='auto', parallel=True, engine='h5netcdf').squeeze()

    ds.coords['z'] = ds.z * Lz/len(ds.z) - Lz/2
    ds.coords['x'] = ds.x * Lx/len(ds.x) - Lx/2

    eta_eff = 5e-4 + 0.3*C_tau*(1/(np.sqrt(0.3)*np.pi))*ds.K.sel(x=0,z=0,method='nearest')
    Diffusion = (5e-4 + 0.3*C_tau*(1/(np.sqrt(0.3)*np.pi))*ds.K)*np.abs(ds.j_par)

    length_mask = xr.where(Diffusion.sel(z=slice(-10,10))>2*Diffusion.sel(z=slice(-10,10)).sel(x=0,method='nearest').mean(dim=['z']),1,0)
    lengths = np.abs(2*ds.z.sel(z=slice(-10,10)).where(length_mask==1).sel(x=0,method='nearest').max(dim='z').values)

    vx = ds.psi.differentiate('z')
    mag_B = np.sqrt(ds.phi.differentiate('x')**2 + ds.phi.differentiate('z')**2).sel(z=0,method='nearest')
    J_0 = ds.j_par.sel(z=0,x=0,method='nearest')
    K = ds.K.sel(z=0,x=0,method='nearest')

    np.savetxt('./summary_statistics/length_tau_' + str(C_tau) + '.txt', lengths)
    np.savetxt('./summary_statistics/J0_tau_' + str(C_tau) + '.txt', J_0)
    np.savetxt('./summary_statistics/K_tau_' + str(C_tau) + '.txt', K)
    np.savetxt('./summary_statistics/eta_eff_tau_' + str(C_tau) + '.txt', eta_eff)

    border = vx.sel(z=0,method='nearest').argmin(dim='x').values
    for safe_factor in range(5):

        ## Use a mask to efficiently find the indices we want in mag_B
        mask = xr.zeros_like(ds.t*ds.x,dtype=int)
        for t,x in enumerate(border + safe_factor):
            mask[t,x] = int(1)

        # Note, we use min here to find the non-NaN values.
        v_a = mag_B.where(mask==1,drop=True).min(dim='x')
        width = np.abs(2*ds.x[border+ safe_factor])
        recon_rate = (vx/mag_B).sel(z=0,method='nearest').where(mask==1,drop=True).min(dim='x')
        R_m = v_a*lengths/eta_eff

        np.savetxt('./summary_statistics/width_tau_' + str(C_tau) + '_safety_' + str(safe_factor) + '.txt', width)
        np.savetxt('./summary_statistics/Ma_in_tau_' + str(C_tau) + '_safety_' + str(safe_factor) + '.txt', recon_rate)
        np.savetxt('./summary_statistics/va_tau_' + str(C_tau) + '_safety_' + str(safe_factor) + '.txt', v_a)
        np.savetxt('./summary_statistics/Rm_eff_tau_' + str(C_tau) + '_safety_' + str(safe_factor) + '.txt', R_m)
