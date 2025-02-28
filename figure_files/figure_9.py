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

ux =    ds.psi.differentiate('z')
uz = -1*ds.psi.differentiate('x')

S = xr.DataArray(np.zeros( (2,2) + ds.phi.shape), dims=['i','j','x','z'], coords=ds.psi.coords)

for i, dim in enumerate(['x','z']):
	for j, var in enumerate((ux,uz)):
		S[i,j,:,:] = var.differentiate(dim)

S = S + S.transpose('j','i','x','z')
S[:,:] = S[:,:] * 7/5 * np.sqrt(0.3) / np.pi * ds.K

bx =    ds.phi.differentiate('z')
bz = -1*ds.phi.differentiate('x')

M = xr.DataArray(np.zeros( (2,2) + ds.phi.shape), dims=['i','j','x','z'], coords=ds.phi.coords)

for i, dim in enumerate(['x','z']):
	for j, var in enumerate((bx,bz)):
		M[i,j,:,:] = var.differentiate(dim)

M = M + M.transpose('j','i','x','z')
M[:,:] = M[:,:] * 7/5 * np.sqrt(0.3) / np.pi * ds.W


vort = uz.differentiate('x') - ux.differentiate('z')


Em = 0.3 * (1/ (np.sqrt(0.3) * np.pi) ) * ds.W * vort - 0.3 * (1/ (np.sqrt(0.3) * np.pi) ) * ds.K * ds.j_par 
Reynolds = M-S

em_prod = -Em*ds.j_par
rm_prod = 0*ds.j_par

for i, u in enumerate((ux,uz)):
    for j, dim in enumerate(('x','z')):
        rm_prod += Reynolds[i,j] * u.differentiate(dim)

fig, ax = plt.subplots(figsize=(fig_width,fig_width/golden))

np.abs(em_prod).sel(z=0,method='nearest').sel(x=slice(-0.16,0.16)).plot(ax=ax,color='tab:red', linestyle='-',  label='$|\\mathbf{E}_M \\cdot \\mathbf{J}|$')
np.abs(rm_prod).sel(z=0,method='nearest').sel(x=slice(-0.16,0.16)).plot(ax=ax,color='tab:blue' , linestyle='-',  label='$|\\mathbf{R}:\\nabla \\mathbf{U}|$')

ax.legend()
ax.set_title('Production Across the Current Sheet')
ax.set_ylabel(' ')
plt.savefig('turbulent_production_across_sheet.png',bbox_inches='tight',dpi=400)


fig, ax = plt.subplots(figsize=(fig_width,fig_width/golden))

np.abs(em_prod).sel(x=0,method='nearest').sel(z=slice(-1,1)).plot(ax=ax,color='tab:red', linestyle='-',  label='$|\\mathbf{E}_M \\cdot \\mathbf{J}|$')
np.abs(rm_prod).sel(x=0,method='nearest').sel(z=slice(-1,1)).plot(ax=ax,color='tab:blue' , linestyle='-',  label='$|\\mathbf{R}:\\nabla \\mathbf{U}|$')

ax.legend()
ax.set_title('Production Along the Current Sheet')
ax.set_ylabel(' ')
plt.savefig('turbulent_production_along_sheet.png',bbox_inches='tight',dpi=400)
