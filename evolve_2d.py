import numpy as np
from scipy.interpolate import griddata, interp2d, interpn
import sys

from scipy.integrate import ode

loc='//home/aleksey/Dropbox/projects/disk_torque/torque_data_2/grid_disk_a1/'

Ntrials=3
ang_test=np.arange(0., 91, 5)
ang_test_rad=ang_test*np.pi/180.0
# a_test=np.arange(0.1, 1.01,0.1)
a_test=[1.0]
e_test=np.arange(0., 1.01, 0.02)
e_test[-1]=0.99
e_test[0]=0.01

m=2.5e-7
mdisk=1000.0*m
t_sec=2.0*np.pi*(1.0/mdisk)
t_norm=t_sec/(2.0*np.pi)
a0=1.0



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

			jdot[ii, kk, idx-1]=np.genfromtxt(loc+'tau_N1000_a_{0:g}_{1}_{2}_{3}'.format(e1, a0, ang, idx))/m
			idot[ii, kk, idx-1]=np.genfromtxt(loc+'i_N1000_a_{0:g}_{1}_{2}_{3}'.format(e1, a0,  ang, idx))/m

idot_avg=np.mean(idot, axis=2)
jdot_avg=np.mean(jdot, axis=2)


def jdot_interp(e, omega):
	sign=1.0
	if omega<0:
		sign=-1.0
	# return sign*(interp2d(e_test, ang_test_rad, jdot_avg.T, kind='linear'))(e, np.abs(omega))
	return sign*interpn((e_test, ang_test_rad), jdot_avg, [e, abs(omega)], method='linear')


def idot_interp(e, omega):
	
	interpa=(interp2d(e_test, ang_test_rad, idot_avg.T, kind='linear'))
	# return interpa(e, abs(omega))-interpa(0.7, 0.0)
	idot0=interpn((e_test, ang_test_rad), idot_avg, [0.7, 0.0], method='linear')
	return interpn((e_test, ang_test_rad), idot_avg, [e, abs(omega)])-idot0

def rhs(t,y):
	j=y[0]
	omega=y[1]

	e=eccentricity(j)
	return [jdot_interp(e, omega), idot_interp(e, omega)]

##Initial conditions for test particle 
e_part=0.7
# a_part=1.0
j_part=j(e_part)
omega_part=sys.argv[1]
##Time step
t_tot=100.0*t_norm
delta_t=2.0*np.pi
# delta_t=t_norm/100.0
t=0.0

r=ode(rhs)
y0=[j_part,  omega_part]
r.set_initial_value(y0, t)

while r.successful() and r.t<t_tot:
	print r.t/(2.0*np.pi), eccentricity(r.y[0]), r.y[1]*180.0/np.pi
	r.integrate(r.t+delta_t)

# while (t<t_tot):
# 	# print j_part, jdot_interp(e_part, a_part, omega_part)
# 	jp=jdot_interp(e_part, a_part, omega_part)
# 	ip=idot_interp(e_part, a_part, omega_part)
# 	j_part=j_part+jp*delta_t
# 	e_part=eccentricity(j_part, a_part)
# 	omega_part=omega_part+ip*delta_t*180.0/np.pi
# 	t+=delta_t
# 	print t/(2.0*np.pi), e_part, a_part, omega_part
# 	sys.stdout.flush()