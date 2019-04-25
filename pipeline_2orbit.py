import subprocess
import os

def bash_command(cmd):
	'''Run command from the bash shell'''
	process=subprocess.Popen(['/bin/bash', '-c',cmd],  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	return process.communicate()[0]

pre=os.path.join(os.path.dirname(__file__))
print pre
bash_command('python {0}/elems_2orbit.py 0.05'.format(pre))
bash_command('python {0}/elems_2orbit.py 0.1'.format(pre))
bash_command('ln -s {0}/template_2orbit.sh'.format(pre))
bash_command('python {0}/gen_grid_2orbit.py'.format(pre))