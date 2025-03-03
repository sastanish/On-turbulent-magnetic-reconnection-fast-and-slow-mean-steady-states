#
# Generates figure 6 in Turbulent Magnetic Reconnection: fast and slow 
# mean steady states
# 
# Plots the steady-state diffusion region width vs Mach-number
#
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

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



fig, ax = plt.subplots(figsize=(fig_width,fig_width/golden))

for i,tau in enumerate([0.5, 1.0, 1.5]):

    va = np.loadtxt('$SUMMARY_STATISTICS_DIR' + 'va_tau_' + str(tau) + '_safety_0.txt')[30:]
    width = np.loadtxt('$SUMMARY_STATISTICS_DIR' + 'width_tau_' + str(tau) + '_safety_0.txt')[30:]

    fit = Polynomial.fit(va,width,1).convert().coef
    x = np.linspace(0.38,0.7)

    ax.plot(va,width,label=f'$C_\\tau ={tau}$',linestyle='',marker='x')
    ax.plot(x,fit[1]*x+fit[0],label=f'$\\delta ={fit[1]:.1f} B_{{\\rm in}} + {fit[0]:.2f}$ ',linestyle='--',color='grey')

ax.set_xlabel('$B_{\\rm in}$')
ax.set_ylabel('$\\delta$')


plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=3)

plt.tight_layout()

plt.savefig('width_vs_va.svg',bbox_inches='tight',dpi=600)
