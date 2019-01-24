import numpy as np

# a1s=np.arange(0., 1.01, 0.1)
# a1s[0]=0.01
a1s=np.array([0.1])
angs=np.arange(0.0, 91., 5.)
#e1s=[1.0-1.0e-6]
e1s=np.arange(0.0, 1.01, 0.02)
# e1s[-1]=0.99
# e1s[0]=0.01
# offsets=[0,1]
# e1s=[0.7]
# angs=[0.2, 0.4, 1.0, 2.0, 4.0, 8.0, 16.0]

for e1 in e1s:
	for a1 in a1s:
		for ang in angs:
			temp=open('template.sh').read()
			temp=temp.replace('xx', '{0:.2f}'.format(e1))
			temp=temp.replace('yy', str(a1))
			temp=temp.replace('zz', str(ang))
			f=open('e{0}_a{1}_ang{2}.sh'.format(e1, a1, ang), 'w')
			f.write(temp)
			f.close()