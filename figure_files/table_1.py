import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8,4))

taus = [0.5, 1.0, 1.5, 2.0]
rate = np.zeros( (len(taus),5) )
Rm = np.zeros( (len(taus),5) )
scalings = np.zeros( (len(taus),5) )
for i,tau in enumerate(taus):

    for s in range(5):

        rate[i,s] = np.nanmean(np.abs(np.loadtxt('../Ma_in_tau_' + str(tau) + '_safety_' + str(s) + '.txt')[-40:-1]))
        Rm[i,s] = np.nanmean(np.loadtxt('../Rm_eff_tau_' + str(tau) + '_safety_' + str(s) + '.txt')[-40:-1])
        scalings[i,s] = 1/np.sqrt(Rm[i,s])


print('$C_\\tau$' + ' '.join([f"& ${tau}$ " for tau in taus]) + '\\\\')
print('$M_{a,in}$' + 
      ' '.join([f"& ${M:.3f} \\pm {Merr:.3f}$ " for M,Merr in zip(rate.mean(axis=1),rate.std(axis=1))]) + '\\\\')
print('$R_{m,eff}$' + 
      ' '.join([f"& ${R:.3f} \\pm {Rerr:.3f}$ " for R,Rerr in zip(Rm.mean(axis=1),Rm.std(axis=1))]) + '\\\\')
print('$R_{m,eff}^{-1/2}$' + 
      ' '.join([f"& ${S:.3f} \\pm {Serr:.3f}$ " for S,Serr in zip(scalings.mean(axis=1),scalings.std(axis=1))]) + '\\\\')
