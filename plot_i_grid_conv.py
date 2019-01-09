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
e=0.7
Ntrials=5
tag=sys.argv[1]
loc='//home/aleksey/Dropbox/projects/disk_torque/torque_data_2/grid_disk_1/'


ti=np.zeros([len(a_test), len(ang_test)])
tib=np.zeros([len(a_test), len(ang_test)])
idx=1
# ti_avg=np.zeros([len(a_test), len(ang_test)])
# ti_err=np.zeros([len(a_test), len(ang_test)])

# tib=np.zeros([len(a_test), len(ang_test)])

for ii,a1 in enumerate(a_test):
	for jj,ang in enumerate(ang_test):
		tmp=np.genfromtxt(loc+'{2}_N1000_a_0.7_{0}_{1}_{3}'.format(a1, ang, tag, idx))
		jo=m*(a1*(1.-e**2))**0.5
		if tag=='i':
			tmp=tmp/m
			ti[ii,jj]=(ang*np.pi/180/tmp)
		else:
			ti[ii,jj]=jo/tmp

		tmp=np.genfromtxt(loc+'{2}_N1000_b_0.7_{0}_{1}_{3}'.format(a1, ang, tag, idx))
		jo=m*(a1*(1.-e**2))**0.5
		if tag=='i':
			tmp=tmp/m
			tib[ii,jj]=(ang*np.pi/180/tmp)
		else:
			tib[ii,jj]=jo/tmp


fig,ax=plt.subplots(figsize=(15,8))
ax.set_xlim(5,90)
ax.set_xlabel(r'$\bar{\omega}$')
ax.set_ylabel(r'$a$')

tlist=[0.0001, 0.01, 1.0e-1, 1, 10.0]
tlist_tex=map(latex_exp.latex_exp, tlist)
tlist_tex=[re.sub('1.0 \\\\times\s', '', tt) for tt in tlist_tex] 

# print np.min((ti_err/ti_avg)),np.max(np.abs(ti_err/ti_avg))
print np.min(abs((tib-ti)/ti))
p1=ax.pcolormesh(ang_test, a_test, abs((tib-ti)/ti), cmap='RdBu_r',norm=colors.LogNorm(vmin=0.001, vmax=2))
cbar=fig.colorbar(p1, ax=ax, ticks=tlist, label=r'$\tau$')
cbar.ax.set_yticklabels(tlist_tex) 
fig.savefig('{0}_grid_disk_conv.pdf'.format(tag))