from __future__ import print_function
from bash_command import bash_command as bc
import numpy as np
import sys

# a_test =np.arange(0.1, 1.01, 0.1)
ang_test = np.arange(5, 91, 5)
a_test=[0.01]
# ang_test=[80]
for ii,a1 in enumerate(a_test):
	for jj,ang in enumerate(ang_test):
		dd=np.inf
		No=1002
		i=0
		while (dd>0.05) and (i<6):
			bc.bash_command('./rebounda 0.7 {0} {1} {2}'.format(a1, ang, No))
			bc.bash_command('./reboundb 0.7 {0} {1} {2}'.format(a1, ang, No))
			tdot1=np.genfromtxt('tau__0.7_{0}_{1}'.format(a1, ang))
			tdot2=np.genfromtxt('taub__0.7_{0}_{1}'.format(a1, ang))
			dd=abs((tdot1-tdot2)/tdot1)
			idot1=np.genfromtxt('i__0.7_{0}_{1}'.format(a1, ang))
			idot2=np.genfromtxt('ib__0.7_{0}_{1}'.format(a1, ang))
			dd=abs((idot1-idot2)/idot1)
			No=No*2
			i+=1
			print((a1, ang, i-1,No/2, abs((tdot1-tdot2)/tdot1), abs((idot1-idot2)/idot1)))
			sys.stdout.flush()
