#
# Generates the sub-figure in figure 7 in Turbulent Magnetic Reconnection: fast and slow 
# mean steady states
#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# For LaTeX fonts
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'],'size': 14})
rc('text', usetex=True)


# For nice picture sizes
pt = 1./72.27 # 72.27 points to an inch.
jour_sizes = {"APJ":  {"onecol": 246.*pt, "twocol": 510.*pt},
              "misc": {"onecol": 246.*pt, "twocol": 372.*pt},
              # Add more journals below or just edit the above numbers
             }

fig_width = jour_sizes["APJ"]["onecol"]
# Our figure's aspect ratio
golden = (1 + 5 ** 0.5) / 2
# In figsize - (my_width, my_width/golden)

fig, ax = plt.subplots(figsize=(fig_width/golden,fig_width/golden))

Cbs = [0.03  , 0.08  , 0.1  , 0.28  , 0.32  , 0.35]
rate = []
for i,Cb in enumerate(Cbs):
    rate.append(np.abs(np.loadtxt('./summary_statistics/Ma_in_Cb' + str(Cb) + '_safety_' + str(1) + '.txt'))[-1])


x = np.linspace(0.03,0.35)
ax.plot(Cbs,rate,label=f'data',color='black',linestyle='',marker='x')
ax.plot(x,0.17*np.sqrt(x),label='$0.17 \\sqrt{C_\\beta}$',color='black',linestyle='--')

ax.set_xlabel('$C_\\beta$')
ax.set_ylabel('$M_{\\rm in}$')
xticks = ax.xaxis.get_major_ticks()
xticks[-1].set_visible(False)

ax.legend()

plt.savefig('reconnection_scaling.svg',bbox_inches='tight')
