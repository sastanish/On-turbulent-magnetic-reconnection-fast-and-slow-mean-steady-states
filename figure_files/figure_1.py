import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as mpatches

# For LaTeX fonts
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'],'size': 14})
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

def plot_save(t,var,save_dir='.'):
    fig = ds[var].isel(t=t).plot()
    plt.savefig(save_dir + f'/{var}_{t:03d}.png')
    plt.close('all')
    return

Lz = 80
Lx = 10
C_tau = 1.0

time_index = -20

filenames = [f'../tau_1.0/BOUT.dmp.{i}.nc' for i in range(32)]

ds = xr.open_mfdataset(filenames,concat_dim="x", chunks=None, combine="nested",data_vars='minimal', coords='minimal', compat='override',preprocess=prefunc, parallel = False, engine='h5netcdf').squeeze()

ds.coords['z'] = ds.z * Lz/len(ds.z) - Lz/2
ds.coords['x'] = ds.x * Lx/len(ds.x) - Lx/2

Diffusion = 5e-4 + 0.3*C_tau*(1/(np.sqrt(0.3)*np.pi))*ds.K
vx = ds.psi.differentiate('z').sel(z=0,method='nearest').isel(t=time_index)
top_bc = ds.x[vx.argmax().values]
bottom_bc = ds.x[vx.argmin().values]
vx = vx.sel(x=slice(-1,1))

mask = xr.where(Diffusion>2*Diffusion.sel(x=0,method='nearest').mean(dim=['z']),1,0) #Slicing to eliminate the other perturbations that grow and generate K
right_bc = ds.z.where(mask==1).sel(x=0,method='nearest').isel(t=time_index).max().values
left_bc = ds.z.where(mask==1 ).sel(x=0,method='nearest').isel(t=time_index).min().values
print(right_bc)

#mask = xr.where(Diffusion.sel(z=slice(-10,10))>5e-3,1,0) #Slicing to eliminate the other perturbations that grow and generate K
#right_bc = ds.z.where(mask==1).sel(x=0,method='nearest').isel(t=time_index).max().values
#left_bc = ds.z.where(mask==1 ).sel(x=0,method='nearest').isel(t=time_index).min().values

#right_bc = Diffusion.isel(t=time_index).sel(x=0,method='nearest').sel(z=slice(0.05,10  )).differentiate('z').differentiate('z').idxmax(dim='z').values
#left_bc  = Diffusion.isel(t=time_index).sel(x=0,method='nearest').sel(z=slice(-10,-0.05)).differentiate('z').differentiate('z').idxmax(dim='z').values

fig, ax = plt.subplots(figsize=(fig_width,fig_width/golden))

#Diffusion.isel(t=time_index).sel(x=slice(-1,1),z=slice(-3,3)).plot(ax=ax,alpha=1.0,cmap='binary',add_colorbar=False,add_labels=False)
ds.j_par.isel(t=time_index ).sel(x=slice(-1,1),z=slice(-4,4)).plot(ax=ax,alpha=1.0,add_colorbar=False,add_labels=False)

divider = make_axes_locatable(ax)
ax_vx = divider.append_axes("left", 1.4, pad=0.2, sharey=ax)
ax_K  = divider.append_axes("bottom", 1.1, pad=0.2, sharex=ax)

ax.xaxis.set_tick_params(labelbottom=False)
ax.yaxis.set_tick_params(labelleft=False)

Diffusion.sel(x=0,method='nearest').isel(t=time_index).sel(z=slice(-4,4)).plot(ax=ax_K,label='$\\eta + C_\\beta \\tau K$')
vx.plot(ax=ax_vx,y='x',label='$U_{\\rm in}$')

ax_K.vlines([right_bc,left_bc],0,Diffusion.sel(x=0,z=0,method='nearest').isel(t=time_index).max(),linestyle='--',color='grey')
ax.vlines([right_bc,left_bc],-1,1,linestyle='--',color='grey')
ax_vx.hlines([top_bc,bottom_bc],vx.min(),vx.max(),linestyle='--',color='grey')
ax.hlines([top_bc,bottom_bc],-4,4,linestyle='--',color='grey')

ax_K.set_xlabel('$z$')
ax_K.set_ylabel('')
ax_vx.set_xlabel('')
ax_vx.set_ylabel('$x$')
ax_K.set_title('')
ax_vx.set_title('')

ax_K.legend()
ax_vx.legend()

#black_patch = mpatches.Patch(color='black', label="$\\eta \\mathbf{J} + \\langle u' \\times b' \\rangle$")
red_patch = mpatches.Patch(color='tab:blue', label='$|\\mathbf{J}|$')
ax.legend(handles=[red_patch])

plt.savefig('diffusion_region_boundaries.png',bbox_inches='tight',dpi=600)
