import numpy as np

# a1s=np.arange(0., 1.01, 0.1)
# a1s[0]=0.01
a1=0.99
angs=np.linspace(0.0, 180.0, 20.)
angs=angs[1:-1]
e1s=np.arange(0, 1.01, 0.1)
e1s[0]=0.01
e1s[-1]=0.99

tags=['0.05_a', '0.05_b', '0.1_a', '0.1_b']

for e1 in e1s:
	for ang in angs:
		for tag in tags:
			temp=open('template.sh').read()
			temp=temp.replace('xx1', '{0}'.format(e1))
			temp=temp.replace('xx', '--etest {0}'.format(e1))
			temp=temp.replace('yy1', '{0}'.format(a1))
			temp=temp.replace('yy', '--atest {0:.1g}'.format(a1))
			temp=temp.replace('zz1', '{0}'.format(ang))
			temp=temp.replace('zz', '--pomega {0:.1f} --ein {1} --etest {1} --dtag {2}'.format(ang, e1, tag))
			f=open('e{0}_ang{1:.1f}_dt{2}.sh'.format(e1, ang, tag), 'w')
			f.write(temp)
			f.close()