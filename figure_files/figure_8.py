import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# For LaTeX fonts
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'],'size': 16})
rc('text', usetex=True)


# For nice picture sizes
pt = 1./72.27 # 72.27 points to an inch.
jour_sizes = {"APJ": {"onecol": 246.*pt, "twocol": 510.*pt},
              "misc": {"onecol": 246.*pt, "twocol": 372.*pt},
              # Add more journals below or just edit the above numbers
             }

fig_width = jour_sizes["APJ"]["twocol"]
# Our figure's aspect ratio
golden = (1 + 5 ** 0.5) / 2
# In figsize - (my_width, my_width/golden)



def prefunc(ds):
    return ds.drop_isel(x=[0,1,-2,-1])

Lx = 10
Lz = 80

filenames = [f'../tau_1.0/BOUT.dmp.{i}.nc' for i in range(32)]
ds = xr.open_mfdataset(filenames,concat_dim="x", combine="nested",data_vars='minimal', coords='minimal', compat='override',preprocess=prefunc, chunks='auto', parallel=False).squeeze()

ds.coords['z'] = ds.z * Lz/len(ds.z) - Lz/2
ds.coords['x'] = ds.x * Lx/len(ds.x) - Lx/2

ds = ds.isel(t=-10).squeeze()
print(ds.t.values)

ux =    ds.psi.differentiate('z')
uz = -1*ds.psi.differentiate('x')

S = xr.DataArray(np.zeros( (2,2) + ds.phi.shape), dims=['i','j','x','z'], coords=ds.psi.coords)

for i, dim in enumerate(['x','z']):
	for j, var in enumerate((ux,uz)):
		S[i,j,:,:] = var.differentiate(dim)

S = S + S.transpose('j','i','x','z')
S[:,:] = S[:,:] * 7/5 * np.sqrt(0.3) / np.pi * ds.K

vel_strain_x = S[0,0].differentiate('x') + S[0,1].differentiate('z')
vel_strain_z = S[1,0].differentiate('x') + S[1,1].differentiate('z')


bx =    ds.phi.differentiate('z')
bz = -1*ds.phi.differentiate('x')

M = xr.DataArray(np.zeros( (2,2) + ds.phi.shape), dims=['i','j','x','z'], coords=ds.phi.coords)

for i, dim in enumerate(['x','z']):
	for j, var in enumerate((bx,bz)):
		M[i,j,:,:] = var.differentiate(dim)

M = M + M.transpose('j','i','x','z')
M[:,:] = M[:,:] * 7/5 * np.sqrt(0.3) / np.pi * ds.W

mag_strain_x = M[0,0].differentiate('x') + M[0,1].differentiate('z')
mag_strain_z = M[1,0].differentiate('x') + M[1,1].differentiate('z')

Reynolds_stress = np.sqrt(vel_strain_x**2+vel_strain_z**2) - np.sqrt(mag_strain_x**2+mag_strain_z**2)


Lorrenz = np.sqrt( np.power(ds.j_par * bz,2) + np.power( ds.j_par * bx,2))
advect = np.sqrt( np.power(ux * ux.differentiate('x') + uz * ux.differentiate('z'), 2) + np.power(ux * uz.differentiate('x') + uz * uz.differentiate('z'),2))

diffusion = 5e-4*np.sqrt( np.power(ux.differentiate('x').differentiate('x') + ux.differentiate('z').differentiate('z'), 2) + np.power( uz.differentiate('x').differentiate('x') + uz.differentiate('z').differentiate('z'), 2))


fig, ax = plt.subplots(figsize=(fig_width,fig_width/golden))

Reynolds_stress.sel(z=0,method='nearest').sel(x=slice(-0.16,0.16)).plot(ax=ax,color='black',label='$|\\nabla \\cdot \\mathbf{R}|$')
Lorrenz.sel(z=0,method='nearest').sel(x=slice(-0.16,0.16)).plot(ax=ax,color='tab:red',label='$|\\mathbf{J}\\times \\mathbf{B} |$')
advect.sel(z=0,method='nearest').sel(x=slice(-0.16,0.16)).plot(ax=ax,color='tab:blue',label='$|\\mathbf{U}\\cdot \\nabla \\mathbf{U} |$')
diffusion.sel(z=0,method='nearest').sel(x=slice(-0.16,0.16)).plot(ax=ax,color='tab:green',label='$| \\nabla^2 \\mathbf{U} |$')

ax.legend()
ax.set_title('Forces Across the Current Sheet')
ax.set_ylabel(' ')
ax.set_xlabel('$x$ ')

plt.savefig('momentum_across_sheet.png',bbox_inches='tight',dpi=400)


fig, ax = plt.subplots(figsize=(fig_width,fig_width/golden))

Reynolds_stress.sel(x=0,method='nearest').sel(z=slice(-1,1)).plot(ax=ax,color='black',label='$|\\nabla \\cdot \\mathbf{R}|$')
Lorrenz.sel(x=0,method='nearest').sel(z=slice(-1,1)).plot(ax=ax,color='tab:red',label='$|\\mathbf{J}\\times \\mathbf{B} |$')
advect.sel(x=0,method='nearest').sel(z=slice(-1,1)).plot(ax=ax,color='tab:blue',label='$|\\mathbf{U}\\cdot \\nabla \\mathbf{U} |$')
diffusion.sel(x=0,method='nearest').sel(z=slice(-1,1)).plot(ax=ax,color='tab:green',label='$| \\nabla^2 \\mathbf{U} |$')

ax.legend()
ax.set_title('Forces Along the Current Sheet')
ax.set_ylabel(' ')
ax.set_xlabel('$z$ ')

plt.savefig('momentum_along_sheet.png',bbox_inches='tight',dpi=400)
