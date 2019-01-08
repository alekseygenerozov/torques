from bash_command import bash_command as bc
import shlex
import numpy as np



job=shlex.split(bc.bash_command('squeue -u alge9397 -t running|grep -i end_torq'))
while (len(job)>0):
	job=shlex.split(bc.bash_command('squeue -u alge9397 -t running|grep -i end_torq'))
bc.bash_command('for i in `echo e0.5*sh`; do sbatch --array=1-5 $i ; done')


	

