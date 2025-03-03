#
# Generates figure 4 in Turbulent Magnetic Reconnection: fast and slow 
# mean steady states
# 
# Current and Turbulent energy at the center of the current sheet vs time.
#
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica",
    "font.size" : 25
})


for tau in [0.1, 0.5, 1.0, 1.5]:
    J_0 = np.pi

    fig, ax1 = plt.subplots(figsize=(8,4))
    ax2 = ax1.twinx()

    J = np.abs(np.loadtxt('../J0_tau_' + str(tau) + '.txt'))
    DK = np.loadtxt('../K_tau_' + str(tau) + '.txt')

    time = [j for j in range(len(J))]
    eq = J_0/tau

    ax1.plot(time,J,color='tab:red')
    ax1.plot(time,[eq for i in range(len(time))],color='grey',linestyle='--')
    ax1.set_xlabel('$t$')
    ax1.set_ylabel('$J_{c}$',color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    time = [j for j in range(len(DK))]
    ax2.plot(time,DK,color='tab:blue')
    ax2.set_ylabel('$K_c$',color='tab:blue')
    ax2.tick_params(axis='y',labelcolor='tab:blue')

    ax2.set_yscale('log')

    fig.tight_layout()
    plt.savefig(f'J_K_pic_{tau}.png')
