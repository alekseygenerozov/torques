import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import LogFormatter 


poms=np.linspace(0, 180.0, 20)
poms=poms[1:-1]
print poms
eccs=np.arange(0, 1.01, 0.1)
eccs[0]=0.01
eccs[-1]=0.99

# di=0.01
m=2.5e-7

tag='dt0.1'
a1=0.99
dat=np.zeros([len(poms), len(eccs)])
dat2=np.zeros([len(poms), len(eccs)])
for i,pp in enumerate(poms):
	for j,ecc in enumerate(eccs):
		po=pp*np.pi/180.0

		taus=np.genfromtxt('tau_N1_a_e{0}_a{1}_o{2:.1f}_q0.0_ein{0}_{3}_a'.format(ecc, a1, pp, tag))
		taux=taus[0]
		tauy=taus[1]
		taua=np.cos(po)*taux+np.sin(po)*tauy

		alpha=2.0*np.pi*taua/m/(1.0-ecc**2.0)**0.5

		taus=np.genfromtxt('tau_N1_a_e{0}_a{1}_o{2:.1f}_q0.0_ein{0}_{3}_b'.format(ecc, a1, pp, tag))
		taux=taus[0]
		tauy=taus[1]
		taub=-np.sin(po)*taux+np.cos(po)*tauy

		beta=2.0*np.pi*taub/m/(1.0-ecc**2.0)**0.5
		dat[i,j]=-alpha*beta

for i,pp in enumerate(poms):
	for j,ecc in enumerate(eccs):
		po=pp*np.pi/180.0

		taus=np.genfromtxt('tau_N1_b_e{0}_a{1}_o{2:.1f}_q0.0_ein{0}_{3}_a'.format(ecc, a1, pp, tag))
		taux=taus[0]
		tauy=taus[1]
		taua=np.cos(po)*taux+np.sin(po)*tauy

		alpha=2.0*np.pi*taua/m/(1.0-ecc**2.0)**0.5

		taus=np.genfromtxt('tau_N1_b_e{0}_a{1}_o{2:.1f}_q0.0_ein{0}_{3}_b'.format(ecc, a1, pp, tag))
		taux=taus[0]
		tauy=taus[1]
		taub=-np.sin(po)*taux+np.cos(po)*tauy

		beta=2.0*np.pi*taub/m/(1.0-ecc**2.0)**0.5
		dat2[i,j]=-alpha*beta

x=poms*np.pi/180.0
y=eccs
delta_x=np.diff(x)[0]
delta_y=np.diff(y)[0]
##Label each grid point with appropriate value
fig,ax=plt.subplots(figsize=(12,9))
ax.set_xlabel(r'$\overline{\omega}$')
ax.set_ylabel(r'$e$')
ax.set_yticks(np.arange(0,1.01,0.05), minor=True)
ax.set_xticks(np.arange(0,np.pi*1.01,np.pi*0.25))
ax.set_xticks(np.arange(0,np.pi*1.01,np.pi*0.125),minor=True)
ax.set_xticklabels(['0', r'$\pi/4$', r'$\pi/2$', r'$3 \pi/4$', r'$\pi$'])
ax.set_ylim(0,1.0)
ax.set_xlim(0,1.01*np.pi)
# for ii,xx in enumerate(x):
# 	for jj,yy in enumerate(y):
# 		if (abs(dat[ii, jj]/np.max(dat)))<1.0e-3:
# 			plt.text(xx, yy, '{0:.0e}'.format(dat[ii, jj]/np.max(dat)), fontsize=10, horizontalalignment='center')
# 		else:
# 			plt.text(xx, yy, '{0:.0g}'.format(dat[ii, jj]/np.max(dat)), fontsize=10, horizontalalignment='center')


x_ords=np.append(x-delta_x/2.0,x[-1]+delta_x/2.0)
y_ords=np.append(y-delta_y/2.0,y[-1]+delta_y/2.0)
##Colormap to use. See https://matplotlib.org/gallery/color/colormap_reference.html for a list of possible color-maps
##Divide xy plane into colored boxes. x_ords and y_ords are the edge of each grid box (see above).
##pcolormesh is has weird indexing so we have to transpose the data array. 
##The norm argument defines a mapping from values to colors. See https://matplotlib.org/users/colormapnorms.html
levs=np.linspace(-6, 0, 25)
levs=10**levs
formatter = LogFormatter(10, labelOnlyBase=False) 
p1=ax.contourf(x, y, np.transpose(dat/np.max(dat)), cmap='RdBu_r',norm=colors.LogNorm(), levels=levs)
cbar=fig.colorbar(p1, ax=ax, ticks=np.logspace(-6,0,7), label=r'$\gamma^2$', extend='both')
levs=np.logspace(-5, 0, 6)
p2=ax.contour(x, y, np.transpose(dat/np.max(dat)), colors=['k'], levels=levs)

##Overplotting line -- replace y with  the actual x and y coordinates of your curve.
fig.savefig("gamma2_contour_{0}.png".format(tag))