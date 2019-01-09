from bash_command import bash_command as bc
import numpy as np
import sys

e1=sys.argv[1]
a1=sys.argv[2]
ang=sys.argv[3]
idx=sys.argv[4]
# offset=sys.argv[5]
dd=1.0
i=0

No=100
while (dd>0.05) and (i<6):
	bc.bash_command('/home/aleksey/code/c/torques/rebound_disk {0} {1} {2} {3} {4} {5}'.format(e1, a1, ang, idx, 0,  No))
	bc.bash_command('/home/aleksey/code/c/torques/rebound_disk {0} {1} {2} {3} {4} {5}'.format(e1, a1, ang, idx, 1,  No))

	# bc.bash_command('/projects/alge9397/code/c/torques/rebound_disk {0} {1} {2} {3} {4} {5}'.format(e1, a1, ang, idx, 0,  No))
	# bc.bash_command('/projects/alge9397/code/c/torques/rebound_disk {0} {1} {2} {3} {4} {5}'.format(e1, a1, ang, idx, 1,  No))

	tdot1=np.genfromtxt('tau_N1000_a_{0}_{1}_{2}_{3}'.format(e1, a1, ang, idx))
	tdot2=np.genfromtxt('tau_N1000_b_{0}_{1}_{2}_{3}'.format(e1, a1, ang, idx))
	dd=abs((tdot1-tdot2)/tdot1)
	idot1=np.genfromtxt('i_N1000_a_{0}_{1}_{2}_{3}'.format(e1, a1, ang, idx))
	idot2=np.genfromtxt('i_N1000_b_{0}_{1}_{2}_{3}'.format(e1, a1, ang, idx))
	dd=max(dd, abs((idot1-idot2)/idot1))
	No=No*2
	i+=1
	print e1, a1, ang, i-1,No/2, abs((tdot1-tdot2)/tdot1), abs((idot1-idot2)/idot1)
	sys.stdout.flush()
