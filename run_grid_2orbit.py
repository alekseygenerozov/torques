import numpy as np
from bash_command import bash_command as bc

poms=np.linspace(0, 180.0, 20)
poms=poms[1:-1]
eccs=np.arange(0, 1.01, 0.1)
eccs[0]=0.01
eccs[-1]=0.9
taga='a'
tagb='b'

for idx,pp in enumerate(poms):
	for ecc in eccs:
		bc.bash_command('python run_disk_torque.py --ein {0} --etest {0} -d {1} --pomega {2:.2f}'.format(ecc, taga, pp))
		bc.bash_command('python run_disk_torque.py --ein {0} --etest {0} -d {1} --pomega {2:.2f}'.format(ecc, tagb, pp))

