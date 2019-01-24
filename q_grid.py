import seaborn as sns
from labelLine import labelLines
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors as colors
from matplotlib import ticker
from latex_exp import latex_exp
import re

import sys

ang_test=np.arange(5., 91, 5)
a_test=np.arange(0.1, 1.01,0.1)

m=2.5e-7
##Rescale torques disk so that it is 0.01 times the central mass
m0=0.01
rescale=m0/(1000.0*m)

rt=1.0e-4
Ntrials=5
tag='tau'
loc='//home/aleksey/Dropbox/projects/disk_torque/torque_data_2/grid_disk_3/'

q=np.zeros([len(a_test), len(ang_test), Ntrials])
qb=np.zeros([len(a_test), len(ang_test), Ntrials])

num=np.zeros([len(a_test), len(ang_test)])
eccs=[0.5, 0.7, 0.9]
for ecc in eccs:
	for ii,a1 in enumerate(a_test):
		for jj,ang in enumerate(ang_test):
			for idx in range(1,Ntrials+1):
				jlc=m*(rt*(2.0-rt/a1))**0.5
				porb=2.0*np.pi*a1**1.5

				q[ii,jj,idx-1]=np.genfromtxt(loc+'{3}_N1000_a_{0}_{1}_{2}_{4}'.format(ecc, a1, ang, tag, idx))*rescale*porb/jlc
				qb[ii,jj,idx-1]=np.genfromtxt(loc+'{3}_N1000_b_{0}_{1}_{2}_{4}'.format(ecc, a1, ang, tag, idx))*rescale*porb/jlc

	qavg=np.mean(q, axis=2)

	fig,ax=plt.subplots(figsize=(15,8))
	ax.set_xlim(2.5,92.5)
	ax.set_ylim(0.05, 1.05)
	ax.set_xlabel(r'$\bar{\omega}$')
	ax.set_ylabel(r'$a$')

	v1=-1
	v2=1
	tlist=np.concatenate([-10.0**np.array(range(v1, v2+1)),10.0**np.array(range(v1, v2+1))])
	tlist_tex=map(latex_exp.latex_exp, tlist)
	tlist_tex=[re.sub('1.0 \\\\times\s', '', tt) for tt in tlist_tex] 

	ang_ords=np.append(ang_test-2.5, ang_test[-1]+2.5)
	a_ords=np.append(a_test-0.05, a_test[-1]+0.05)
	p1=ax.pcolormesh(ang_ords, a_ords, qavg, cmap='RdBu_r',norm=colors.SymLogNorm(linthresh=0.01, vmin=-10.0**v2, vmax=10.0**v2))

	for ii,a1 in enumerate(a_test):
		for jj,ang in enumerate(ang_test):
			tmp=abs(qavg[ii,jj])
			# print tmp
			if tmp>=0.01:
				ax.text(ang, a1, '{0:.2f}'.format(abs(tmp)), fontsize=12, horizontalalignment='center')
			else:
				ax.text(ang, a1, '{0:.0e}'.format(abs(tmp)), fontsize=12, horizontalalignment='center')

	cbar=fig.colorbar(p1, ax=ax, ticks=tlist, label=r'$q$')
	cbar.ax.set_yticklabels(tlist_tex) 
	fig.savefig('q_grid_{0}.pdf'.format(ecc))