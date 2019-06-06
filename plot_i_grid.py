import seaborn as sns
from labelLine import labelLines
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors as colors
from matplotlib import ticker
from latex_exp import latex_exp
import re

import sys
import grid_plot_aleksey
import argparse
from scipy.interpolate import InterpolatedUnivariateSpline as IUS
##Defining grid
#--------------------------------------------------------------------------------------------------_#
ang_test=np.arange(5., 91, 5)
ang_idx=list(range(len(ang_test)))
a_test=np.arange(0.1, 0.91,0.1)
a_idx=list(range(len(a_test)))
e_test=np.arange(0.5, 1.01,0.1)
e_test[-1]=0.99
e_test=np.around(e_test, 2)
e_idx=list(range(len(e_test)))
#--------------------------------------------------------------------------------------------------_#

##Will be replaced with argparse parameters
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fix", help="variable to hold fixed", default='a')
parser.add_argument("v", help="fixed value (must be in grid)")
parser.add_argument("--prec", help="Precession time-scale", action="store_true")
parser.add_argument("-l", "--loc",\
 default='/home/aleksey/Dropbox/projects/disk_torque/torque_data_2/old_grid/grid_disk_3/',\
 help='location of data')


args=parser.parse_args()
fix=args.fix
val=float(args.v)
loc=args.loc
prec=args.prec
print(prec)
lab=r'$t_j$'
tag='tau'
if prec:
	tag='i'
	lab=r'$t_i$'


x=ang_test
y=e_test
labx='omega'
laby='e'
if fix=='e':
	y=a_test
	laby='a'
	e_idx=np.where(e_test==val)[0]	
elif fix=='o':
	x=a_test
	labx='a'
	ang_idx=np.where(ang_test==val)[0]
else:
	a_idx=np.where(a_test==val)[0]

Ntrials=5
##Extracting data...
#--------------------------------------------------------------------------------------------------_#
deriv=np.zeros([len(a_test), len(ang_test), len(e_test), Ntrials])
derivb=np.zeros([len(a_test), len(ang_test), len(e_test), Ntrials])
ti_avg=np.zeros([len(a_test), len(ang_test), len(e_test)])
num=np.zeros([len(a_test), len(ang_test), len(e_test)])

norm=1.0
m=2.5e-7
for ii,a1 in enumerate(a_test):
	for jj,ang in enumerate(ang_test):
		for kk,e1 in enumerate(e_test):
			for idx in range(1,Ntrials+1):
				num[ii, jj, kk]=m*(a1*(1.-e1**2))**0.5
				if tag=='i':
					norm=1.0/m
					num[ii, jj]=ang*np.pi/180
				deriv[ii,jj,kk,idx-1]=np.genfromtxt(loc+'{2}_N1000_a_{4}_{0:.1f}_{1}_{3}'.format(a1, ang, tag, idx, e1))*norm
				derivb[ii,jj,kk,idx-1]=np.genfromtxt(loc+'{2}_N1000_b_{4}_{0:.1f}_{1}_{3}'.format(a1, ang, tag, idx, e1))*norm


ti_avg=num/np.mean(deriv, axis=3)
idx=np.meshgrid(a_idx, ang_idx, e_idx)
# ti_avg=ti_avg[a_idx, ang_idx, e_idx]
ti_avg=ti_avg[tuple(idx)]
ti_avg=np.squeeze(ti_avg)

deriv_avg=np.mean(deriv, axis=3)
deriv_avg=deriv_avg[tuple(idx)]
deriv_avg=np.squeeze(deriv_avg)
num=num[tuple(idx)]
num=np.squeeze(num)
#--------------------------------------------------------------------------------------------------_#
grid_plot_aleksey.grid_plot(x, y, ti_avg, labx=labx, laby=laby, lab=lab, name='{0}_'.format(tag)+labx+'_'+laby+'.pdf')
ords=num[1,:]
print(deriv_avg[1,:])
print(ords[::-1])
# print(IUS(ords[::-1], (deriv_avg[1,:]**-1.0)[::-1]).integral(ords[0], ords[-1]))
print(np.trapz((deriv_avg[1,:]**-1.0)[::-1], ords[::-1]))