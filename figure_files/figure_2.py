import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

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

colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown'] 

for i,tau in enumerate([0.1, 0.5, 1.0, 1.5, 2.0, 2.5]):

    for s in range(5):
        rate = np.abs(np.loadtxt('../Ma_in_tau_' + str(tau) + '_safety_' + str(s) + '.txt')) #abs is from v_in being negative at the top of the sheet
        if s == 0:
            rates = np.zeros((5,len(rate)))
        rates[s,:] = rate
    time = [j for j in range(len(rate))]

    ax.plot(time,rate,label=f'$C_\\tau ={tau}$',color=colors[i])

ax.set_xlabel('$t$')
ax.set_ylabel('$M_{\\rm in}$')
xticks = ax.xaxis.get_major_ticks()
xticks[-1].set_visible(False)
#ax.set_ylim(0,0.12)

fig.subplots_adjust(top=0.8)
fig.legend(bbox_to_anchor=(0.1, 0.8, 0.82, 0.18), loc='lower left', mode='expand', ncols=3)

plt.savefig('reconnection_rate_vs_time.png',bbox_inches='tight',dpi=600)
