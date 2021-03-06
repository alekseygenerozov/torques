import subprocess
import os
import shlex
import sys

def bash_command(cmd):
	'''Run command from the bash shell'''
	process=subprocess.Popen(['/bin/bash', '-c',cmd],  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	return process.communicate()[0]

pre=os.path.join(os.path.dirname(__file__))
f=open(pre+'/Makefile','r')
rpath=((f.read().split('\n')[1]).split('='))[-1]
a=float(sys.argv[1])

bash_command('python {0}/elems_2orbit.py 0.05 {1}'.format(pre, a))
bash_command('python {0}/elems_2orbit.py 0.1 {1}'.format(pre, a))
bash_command('ln -s {0}/template_2orbit.sh'.format(pre))
bash_command('python {0}/gen_grid_2orbit.py {1}'.format(pre, 0.99*a))
bash_command('ln -s {0}/librebound.so'.format(rpath))
