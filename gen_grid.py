import numpy as np

a1s=np.arange([0., 1.01, 0.1])
a1s[0]=0.01
angs=np.arange(5., 91., 5.)

e1=0.7
for a1 in a1s:
	for ang in angs:
		temp=open('template.sh').read()
		temp=temp.replace('xx', e1)
		temp=temp.replace('yy', a1)
		temp=temp.repace('zz', ang)
		f=open('e{0}_a{1}_ang{2}'.format(e1, a1, ang), 'w')
		f.write(temp)
		f.close()