from bash_command import bash_command as bc
import shlex
import numpy as np


eccs=[0.5, 0.6, 0.8, 0.9, 0.99]

for ecc in eccs:
	job=shlex.split(bc.bash_command('squeue -u alge9397 -t running|grep -i end_torq'))
	while (len(job)>0):
		job=shlex.split(bc.bash_command('squeue -u alge9397 -t running|grep -i end_torq'))
	bc.bash_command('for i in `echo e{0}_*sh`; do sbatch --array=1-5 $i ; done')


		

