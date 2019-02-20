import numpy as np
from scipy.interpolate import griddata, interp2d, interpn
import sys

from scipy.integrate import ode

loc='//home/aleksey/Dropbox/projects/disk_torque/torque_data_2/grid_disk_a0.5/'

Ntrials=3
ang_test=np.arange(0., 91, 5)
ang_test_rad=ang_test*np.pi/180.0
# a_test=np.arange(0.1, 1.01,0.1)
a_test=[1.0]
e_test=np.arange(0., 1.01, 0.1)
e_test[-1]=0.999999
e_test[0]=0.01

m=2.5e-7
mdisk=1000.0*m
t_sec=2.0*np.pi*(1.0/mdisk)
t_norm=t_sec/(2.0*np.pi)
a0=0.5
idot0=float(sys.argv[3])



def j(e):
	'''Specific angular momentum'''
	return (a0*(1-e**2.))**0.5

def eccentricity(j):
	'''Eccentricity'''
	return (1-j**2.0/a0)**0.5

jdot=np.zeros([len(e_test), len(ang_test), Ntrials])
idot=np.zeros([len(e_test),  len(ang_test), Ntrials])
idot_avg=np.zeros([len(e_test), len(ang_test)])
jdot_avg=np.zeros([len(e_test), len(ang_test)])

for ii,e1 in enumerate(e_test):
	for kk,ang in enumerate(ang_test):
		for idx in range(1,Ntrials+1):

			jdot[ii, kk, idx-1]=np.genfromtxt(loc+'tau_N1000_a_{0:.2f}_{1}_{2}_{3}'.format(e1, a0, ang, idx))/m
			idot[ii, kk, idx-1]=np.genfromtxt(loc+'i_N1000_a_{0:.2f}_{1}_{2}_{3}'.format(e1, a0,  ang, idx))/m

idot_avg=np.mean(idot, axis=2)
jdot_avg=np.mean(jdot, axis=2)
print interpn((e_test, ang_test_rad), idot_avg, [0.7, 0.0], method='linear')

def jdot_interp(e, omega):
	sign=1.0
	if omega<0:
		sign=-1.0
	# return sign*(interp2d(e_test, ang_test_rad, jdot_avg.T, kind='linear'))(e, np.abs(omega))
	return sign*interpn((e_test, ang_test_rad), jdot_avg, [e, abs(omega)], method='linear')


def idot_interp(e, omega):
	
	# interpa=(interp2d(e_test, ang_test_rad, idot_avg.T, kind='linear'))
	# return interpa(e, abs(omega))-interpa(0.7, 0.0)
	# idot0=interpn((e_test, ang_test_rad), idot_avg, [0.7, 0.0], method='linear')
	return interpn((e_test, ang_test_rad), idot_avg, [e, abs(omega)], method='linear')-idot0/m

def rhs(t,y):
	j=y[0]
	omega=y[1]

	e=eccentricity(j)
	return [jdot_interp(e, omega), idot_interp(e, omega)]

##Initial conditions for test particle 
e_part=float(sys.argv[1])
a_part=a0
j_part=j(e_part)
omega_part=float(sys.argv[2])
##Time step
t_tot=1000.0*t_norm
delta_t=2.0*np.pi
# delta_t=t_norm/100.0
t=0.0

r=ode(rhs)
y0=[j_part, omega_part]
r.set_initial_value(y0, t)

f=open('sol_pert_e{0}_om{1}_idot{2}'.format(e_part, omega_part, idot0), 'w')
while r.successful() and r.t<t_tot:
	f.write('{0} {1} {2}\n'.format(r.t/(2.0*np.pi), eccentricity(r.y[0]), r.y[1]*180.0/np.pi))
	r.integrate(r.t+delta_t)
f.close()
