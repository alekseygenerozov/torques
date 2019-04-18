import seaborn as sns
from labelLine import labelLines
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors as colors
from matplotlib import ticker
from latex_exp import latex_exp
import re

import sys
import json

def j(aa, ee):
	'''Specific angular momentum'''
	return (aa*(1.0-ee**2.0))**0.5

ang_test=np.arange(0., 91, 5)
e_test=np.arange(0.1, 1.01,0.1)
e_test[-1]=0.99
m=2.5e-7
mdisk=1000*m
tsec=2.0*np.pi*(1.0/mdisk)


tag=sys.argv[1]
a1=float(sys.argv[2])
loc='//home/aleksey/Dropbox/projects/disk_torque/torque_data_2/dat_q-1.6/reg/'
f=open(loc+"prec_rate.json", "rb")
prec_rate=json.loads(json.load(f))

deriv=np.zeros([len(e_test), len(ang_test)])
derivb=np.zeros([len(e_test), len(ang_test)])
# ti_avg=np.zeros([len(e_test), len(ang_test)])
# tib_avg=np.zeros([len(e_test), len(ang_test)])
deriv_norm=np.zeros([len(e_test), len(ang_test)])

norm=1.0/m
for ii,e1 in enumerate(e_test):
	for jj,ang in enumerate(ang_test):
		# for idx in range(1,Ntrials+1):
		deriv_norm[ii,jj]=(j(a1, e1)/tsec)
		lab=r'$\tau/(j/t_{sec})$'
		if tag=='i':
			# num[ii, jj]=ang*np.pi/180
			deriv_norm[ii,jj]=(2.0*np.pi/tsec)
			lab=r"$i_e'/(2 \pi/t_{sec})$"

		deriv[ii,jj]=np.mean(prec_rate['{3}_N1000_a_e{0}_a{1}_o{2}_q-1.6_ein0.9_dt1.8'.format(e1, a1, ang, tag)])*norm
		derivb[ii,jj]=np.mean(prec_rate['{3}_N1000_b_e{0}_a{1}_o{2}_q-1.6_ein0.9_dt1.8'.format(e1, a1, ang, tag)])*norm
		# if np.isnan(deriv[ii, jj]):
		# 	deriv[ii,jj]=derivb[ii, jj]

deriv_avg=deriv
#--------------------------------------------------------------------------------------------------_#
fig,ax=plt.subplots(figsize=(15,8))
ax.set_xlim(-2.5,92.5)
ax.set_ylim(0.05, 1.05)
ax.set_xlabel(r'$\bar{\omega}$')
ax.set_ylabel(r'$a$')

for ii,e1 in enumerate(e_test):
	for jj,ang in enumerate(ang_test):
		tmp=abs(deriv_avg[ii,jj]/deriv_norm[ii,jj])
		if tmp>=0.01:
			plt.text(ang, e1, '{0:.2f}'.format(abs(deriv_avg[ii,jj]/deriv_norm[ii,jj])), fontsize=12, horizontalalignment='center')
		else:
			plt.text(ang, e1, '{0:.0e}'.format(abs(deriv_avg[ii,jj]/deriv_norm[ii,jj])), fontsize=12, horizontalalignment='center')



tlist=[-10, -1, -0.1, -0.01, 0.01, 0.1, 1.0, 10.]
tlist_tex=map(latex_exp.latex_exp, tlist)
tlist_tex=[re.sub('1.0 \\\\times\s', '', tt) for tt in tlist_tex] 

ang_ords=np.append(ang_test-2.5, ang_test[-1]+2.5)
e_ords=np.append(e_test-0.05, e_test[-1]+0.05)
p1=ax.pcolormesh(ang_ords, e_ords, deriv_avg/deriv_norm, cmap='RdBu_r', norm=colors.SymLogNorm(linthresh=1.0e-3, vmin=-10.0, vmax=10.0))

# plt.colorbar(p1, label=r'$log(t_i)$')
cbar=fig.colorbar(p1, ax=ax, ticks=tlist, label=r'$\tau$')
cbar.ax.set_yticklabels(tlist_tex) 
fig.savefig('{0}_a{1}_grid_disk_2d.pdf'.format(tag, a1))