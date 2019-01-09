import numpy as np

a1s=np.arange(0., 1.01, 0.1)
a1s[0]=0.01
angs=np.arange(5., 91., 5.)
e1s=np.arange(0.5, 1.01, 0.1)
e1s[-1]=0.99
offsets=[0,1]

for e1 in e1s:
	for a1 in a1s:
		for ang in angs:
			temp=open('template.sh').read()
			temp=temp.replace('xx', str(e1))
			temp=temp.replace('yy', str(a1))
			temp=temp.replace('zz', str(ang))
			f=open('e{0}_a{1}_ang{2}.sh'.format(e1, a1, ang), 'w')
			f.write(temp)
			f.close()