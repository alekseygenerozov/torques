import seaborn as sns
from labelLine import labelLines
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors as colors
from matplotlib import ticker
from latex_exp import latex_exp
import re

import sys

ang_test=np.array([0.2, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0])

m=2.5e-7
e=0.7
Ntrials=5
tag=sys.argv[1]
loc='//home/aleksey/Dropbox/projects/disk_binaries/torque_data_2/grid_inc/'


ti=np.zeros([len(ang_test), Ntrials])
ti_avg=np.zeros(len(ang_test))
ti_err=np.zeros(len(ang_test))

# tib=np.zeros([len(a_test), len(ang_test)])

a1=1
for jj,ang in enumerate(ang_test):
	for idx in range(1,Ntrials+1):
		tmp=np.genfromtxt(loc+'{2}_N1000_a_0.7_{0}_{1}_{3}'.format(a1, ang, tag, idx))
		jo=m*(a1*(1.-e**2))**0.5

		if tag=='i':
			tmp=tmp/m
			ti[jj,idx-1]=(ang*np.pi/180/tmp)
		else:
			ti[jj,idx-1]=jo/tmp

ti_avg=np.mean(ti, axis=1)
# ti_err=np.std(ti, axis=2)



fig,ax=plt.subplots(figsize=(15,8))
ax.set_xlim(0., 20.)
ax.set_xlabel(r'$i$')
ax.set_ylabel(r'$t$')
ax.semilogy(ang_test, abs(ti_avg))
ax.semilogy(ang_test[ti_avg<0], abs(ti_avg[ti_avg<0]), 's')
ax.semilogy(ang_test[ti_avg>0], abs(ti_avg[ti_avg>0]), 'D')


fig.savefig('{0}_grid_disk_inc.pdf'.format(tag))