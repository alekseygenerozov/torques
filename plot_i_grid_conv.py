import seaborn as sns
from labelLine import labelLines
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors as colors
from matplotlib import ticker,cm
from latex_exp import latex_exp
import re

import sys

ang_test=np.arange(0., 91, 5)
a_test=np.arange(0.1, 1.01,0.1)


e=0.7
Ntrials=1
tag=sys.argv[1]
loc='//home/aleksey/Dropbox/projects/disk_torque/torque_data_2/grid_disk_3/'


deriv=np.zeros([len(a_test), len(ang_test), Ntrials])
derivb=np.zeros([len(a_test), len(ang_test), Ntrials])
deriv_avg=np.zeros([len(a_test), len(ang_test)])
derivb_avg=np.zeros([len(a_test), len(ang_test)])
num=np.zeros([len(a_test), len(ang_test)])
# ti_err=np.zeros([len(a_test), len(ang_test)])

norm=1.0
eccs=[0.5, 0.7, 0.9]
for ecc in eccs:
	for ii,a1 in enumerate(a_test):
		for jj,ang in enumerate(ang_test):
			for idx in range(1,Ntrials+1):
				deriv[ii,jj, idx-1]=np.genfromtxt(loc+'{3}_N1000_a_{0}_{1}_{2}_{4}'.format(ecc, a1, ang, tag, idx))*norm
				derivb[ii, jj, idx-1]=np.genfromtxt(loc+'{3}_N1000_b_{0}_{1}_{2}_{4}'.format(ecc, a1, ang, tag, idx))*norm


	deriv_avg=np.mean(deriv, axis=2)
	derivb_avg=np.mean(derivb, axis=2)

	fig,ax=plt.subplots(figsize=(15,8))
	ax.set_xlim(-2.5,92.5)
	ax.set_ylim(0.05, 1.05)
	ax.set_xlabel(r'$\bar{\omega}$')
	ax.set_ylabel(r'$a$')

	tlist=[0.0001, 0.01, 1.0e-1, 1, 10.0]
	tlist_tex=list(map(latex_exp.latex_exp, tlist))
	tlist_tex=[re.sub('1.0 \\\\times\s', '', tt) for tt in tlist_tex] 

	diffs=abs((derivb_avg-deriv_avg)/deriv_avg)
	print(ecc)
	# for ii,a1 in enumerate(a_test):
	# 	for jj,ang in enumerate(ang_test):
	# 		if diffs[ii, jj]>0.1:
	# 			print a1, ang, diffs[ii, jj], deriv_avg[ii, jj], derivb_avg[ii, jj]
	for ii,a1 in enumerate(a_test):
		for jj,ang in enumerate(ang_test):
			plt.text(ang, a1, '{0:.2f}'.format(diffs[ii, jj]), fontsize=10, horizontalalignment='center')

	cmap=cm.get_cmap('RdBu_r')
	##below line is not working...
	cmap.set_under('blue')

	ang_ords=np.append(ang_test-2.5, ang_test[-1]+2.5)
	a_ords=np.append(a_test-0.05, a_test[-1]+0.05)
	p1=ax.pcolormesh(ang_ords, a_ords, abs((derivb_avg-deriv_avg)/deriv_avg), cmap=cmap,norm=colors.LogNorm(vmin=0.001, vmax=2, clip=False))
	cbar=fig.colorbar(p1, ax=ax, ticks=tlist, label=r'$Error$', extend='both')
	cbar.ax.set_yticklabels(tlist_tex) 
	fig.savefig('{0}_grid_disk_conv_{1}.pdf'.format(tag, ecc))
