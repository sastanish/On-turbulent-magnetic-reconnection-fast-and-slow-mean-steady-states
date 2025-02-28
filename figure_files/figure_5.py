import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
from matplotlib.lines import Line2D

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



fig, ax = plt.subplots(figsize=(fig_width,fig_width/golden))
ax2 = ax.twinx()

ax.set_xlabel('$t$')
ax.set_ylabel('$J_{c}$',color='tab:red')
ax.tick_params(axis='y', labelcolor='tab:red')

ax2.set_ylabel('$K_c$',color='tab:blue')
ax2.tick_params(axis='y',labelcolor='tab:blue')
ax2.set_yscale('log')


taus = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5]
J_avg = [0 for i in range(len(taus))]
J_err = [0 for i in range(len(taus))]
K_max = [0 for i in range(len(taus))]


for i,tau in enumerate(taus):

    J = np.loadtxt('../J0_tau_' + str(tau) + '.txt')
    K = np.loadtxt('../K_tau_' + str(tau) + '.txt')
    J_avg[i] = np.abs(np.mean(J[-30:]))
    K_max[i] = np.abs(np.max(K[-30:]))

ax2.plot(taus,K_max,marker='.',linestyle='',label='hres TRM: $K$',color='tab:blue',markersize=8)
ax.plot(taus,J_avg, marker='x',linestyle='',label='TRM: $|J|$',color='tab:red')

### For the tearing C_tau = 0.2
### case, here are the calculated
### values for mean and std at 
### the diff region center

#J = np.loadtxt('../J0_tau_' + str(0.2) + '.txt')
#K = np.loadtxt('../K_tau_' + str(0.2) + '.txt')

#ax.errorbar(0.2,np.abs(np.mean(J[110:151])),yerr=np.abs(np.std(J[110:151])),marker='x',linestyle='',label='TRM: $|J|$',color='tab:red')
#ax2.plot(0.2,np.abs(np.mean(K[110:151])),marker='.',linestyle='',label='hres TRM: $K$',color='tab:blue',markersize=8)

##############################

ax.set_xlabel('$C_\\tau$')
ax.set_ylabel('$J_c$')

x = np.linspace(0.147,2.5)
ax.plot(x,np.pi/x,label='$|J| =\\pi/x$ ',linestyle='-',color='grey')
ax.hlines(21.5,0,0.147,color='grey',linestyle='-',label='rmhd: $\\langle |J| \\rangle$')

taus = [0.05]
J_avg = [0 for i in range(len(taus))]
J_err = [0 for i in range(len(taus))]
K_max = [0 for i in range(len(taus))]
for i,tau in enumerate(taus):

    J = np.loadtxt('../hres_J0_tau_' + str(tau) + '.txt')
    K = np.loadtxt('../hres_K_tau_' + str(tau) + '.txt')
    J_avg[i] = np.abs(np.mean(J[-15:]))
    K_max[i] = np.abs(np.max(K[-15:]))

ax.plot(taus,J_avg,marker='x',linestyle='',label='hres TRM: $|J|$',color='tab:red')
ax2.plot(taus,K_max,marker='.',linestyle='',color='tab:blue',markersize=8)

custom_lines = [
                Line2D([0], [0], color='tab:red', marker='x', linestyle='', lw=4),
                Line2D([0], [0], color='tab:blue', marker='.',linestyle='', lw=4),
#                Line2D([0], [0], color='black', marker= '.',linestyle='', lw=2),
                Line2D([0], [0], color='grey', linestyle= '-', lw=2)
#                Line2D([0], [0], color='grey', linestyle= '--', lw=2),
#                Line2D([0], [0], color='black', linestyle= '-', lw=2)
               ]

custom_labels = [
                 '$J_c$',
                 '$K_c$',
                 '$\\min\\left( J_{\\tau}, J_{\\eta} \\right)$'
#                 'high res',
#                 '$|J|=J_0 / C_\\tau$',
#                 'rmhd: $\\langle |J| \\rangle$'
                ]
plt.legend(custom_lines,custom_labels,loc='center right')


plt.savefig('J0_vs_tau.png')
plt.savefig('J0_vs_tau.png',bbox_inches='tight',dpi=600)
