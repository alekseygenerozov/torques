import seaborn as sns
from labelLine import labelLines
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors as colors
from matplotlib import ticker
from latex_exp import latex_exp
import re
import sys


ang_test=np.arange(5, 91, 5)
a_test=np.arange(0.1, 1.01,0.1)

m=2.5e-7
e=0.7
tag=sys.argv[1]
loc='/home/aleksey/Dropbox/projects/disk_torque/torque_data_2/grid_two_orbits/'


ti=np.zeros([len(a_test), len(ang_test)])
tib=np.zeros([len(a_test), len(ang_test)])

for ii,a1 in enumerate(a_test):
	for jj,ang in enumerate(ang_test):
#         tmp=np.genfromtxt(loc+'i__0.7_{0}_{1}'.format(a1, ang))[1]
		tmp=np.genfromtxt(loc+'{2}__0.7_{0}_{1}'.format(a1, ang, tag))
		jo=m*(a1*(1.-e**2))**0.5
		if tag=='i':
			tmp=tmp/m
			ti[ii,jj]=(ang*np.pi/180/tmp)
		else:
			ti[ii,jj]=jo/tmp





fig,ax=plt.subplots(figsize=(15,8))
ax.set_xlim(2.5,92.5)
ax.set_ylim(0.05, 1.05)
ax.set_xlabel(r'$\bar{\omega}$')
ax.set_ylabel(r'$a$')


tlist=[-1.0e6, -1.0e5, -1.0e4, -1.0e3,1.0e3, 1.0e4, 1.0e5, 1.0e6]
tlist_tex=map(latex_exp.latex_exp, tlist)
tlist_tex=[re.sub('1.0 \\\\times\s', '', tt) for tt in tlist_tex] 



ang_ords=np.append(ang_test-2.5, ang_test[-1]+2.5)
a_ords=np.append(a_test-0.05, a_test[-1]+0.05)
p1=ax.pcolormesh(ang_ords, a_ords, ti, cmap='RdBu_r',norm=colors.SymLogNorm(linthresh=100, vmin=-1.0e6, vmax=1.0e6))


# plt.colorbar(p1, label=r'$log(t_i)$')
cbar=fig.colorbar(p1, ax=ax, ticks=tlist, label=r'$\tau$')
cbar.ax.set_yticklabels(tlist_tex) 
fig.savefig('{0}_grid_orbit.pdf'.format(tag))