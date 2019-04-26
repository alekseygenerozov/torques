# from rebound_runs_alro import end_aleksey_config_b as end
import numpy as np
import sys
import math

def rotate_vec(angle,axis,vec):    
	'''
	Rotate vector vec by angle around axis (couter-clockwise)
	'''
	vRot = vec*math.cos(angle) + np.cross(axis,vec)*math.sin(angle) + axis*np.dot(axis,vec)*(1 -math.cos(angle))
	return vRot	

def gen_disk(ang1, ang1_mean, ang2, ang2_mean, ang3, ang3_mean):
	'''
	This is from some old code that starts with perfectly aligned e and j vectors and then rotates them by a small amount
	'''
	ehat = np.array([1,0,0])
	jhat = np.array([0,0,1])
	bhat = np.cross(jhat,ehat)    # rotate jhat by angle1 over major axis and angle 2 minor axis
	# rotate ehat by angle2 over minor axis (for consistency) and angle3 about jhat
	angle1 = np.random.normal(ang1_mean, ang1, 1)
	angle2 = np.random.normal(ang2_mean, ang2, 1)
	angle3 = np.random.normal(ang3_mean, ang3, 1)    
	jhat = rotate_vec(angle1,ehat,jhat)
	jhat = rotate_vec(angle2,bhat,jhat)
	ehat = rotate_vec(angle2,bhat,ehat)
	ehat = rotate_vec(angle3,jhat,ehat)    
	n = np.cross(np.array([0,0,1]), jhat)
	n = n / np.linalg.norm(n)   
	Omega = math.atan2(n[1], n[0])
	omega = math.acos(np.dot(n, ehat))
	if ehat[2] < 0:
		omega = 2*np.pi - omega    
	inc=math.acos(jhat[2])    
	return inc, Omega, omega





pert=float(sys.argv[1])
apert=float(sys.argv[2])
base='./'
poms=np.linspace(0, 1, 20)
flist=['inc','Om','om']

elems= gen_disk(0,pert,0,0,0,0)
print elems
for ii,ee in enumerate(elems):
    f=open(base+flist[ii]+'_{0}_a.txt'.format(pert), 'w')
    f.write('{0}\n'.format(ee))
    f.close()
f=open('a_{0}_a.txt'.format(pert),'w')
f.write('{0}\n'.format(apert))
f.close()


elems=gen_disk(0,0,0,pert,0,0)
print elems
for ii,ee in enumerate(elems):
    f=open(base+flist[ii]+'_{0}_b.txt'.format(pert),'w')
    f.write('{0}\n'.format(ee))
    f.close()
f=open('a_{0}_b.txt'.format(pert),'w')
f.write('{0}\n'.format(apert))
f.close()
    