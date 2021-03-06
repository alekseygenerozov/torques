from __future__ import print_function
import numpy as np
import sys
import argparse
import os

import subprocess

def bash_command(cmd):
	'''Run command from the bash shell'''
	process=subprocess.Popen(['/bin/bash', '-c',cmd],  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	return process.communicate()[0]

parser=argparse.ArgumentParser(description='Compute torque and precession rate on test orbit from END')
parser.add_argument('--etest',  default=0.7,
	help='eccentricity of test orbit', type=float)
parser.add_argument('--atest', default=0.99,
	help='sma of test orbit', type=float)
parser.add_argument('--ein', default=0.7,
	help='eccentricity at inner edge of END', type=float)
parser.add_argument('-q', default=0.0,
	help='specifies eccentricity gradient in disk', type=float)
parser.add_argument('-o','--pomega', default=0,
	help='specifies orientation ', type=float)
parser.add_argument('-d','--dtag', default='1',
	help='data file containing disk orbital elements ', type=str)
parser.add_argument('--iter', default=9, type=int,
	help='maximum number of iterations')
parser.add_argument('-n', '--nstart', default=1001, type=int,
	help='starting number of bins')
# offset=sys.argv[5]

args=parser.parse_args()

dd=1.0
i=0
No=args.nstart
iter_max=args.iter
pre=os.path.join(os.path.dirname(__file__))
while (dd>0.05) and (i<iter_max):
	Nd=min(len(np.array([np.genfromtxt('a_{0}.txt'.format(args.dtag))]).flatten()), 1000)
	bash_command(pre+'/rebound_disk --etest {0} --atest {1} -o {2} -n {3} -f {4}  -q {5} --ein {6} --dtag {7}'\
		.format(args.etest, args.atest, args.pomega, No, 0, args.q, args.ein, args.dtag))
	sys.stdout.flush()
	bash_command(pre+'/rebound_disk --etest {0} --atest {1} -o {2} -n {3} -f {4}  -q {5} --ein {6} --dtag {7}'\
		.format(args.etest, args.atest, args.pomega, No, 1, args.q, args.ein, args.dtag))
	tdot1=np.genfromtxt('tau_N{6}_a_e{0}_a{1}_o{2}_q{3}_ein{4}_dt{5}'.format(args.etest, args.atest, args.pomega, args.q, args.ein, args.dtag, Nd))
	tdot2=np.genfromtxt('tau_N{6}_b_e{0}_a{1}_o{2}_q{3}_ein{4}_dt{5}'.format(args.etest, args.atest, args.pomega, args.q, args.ein, args.dtag, Nd))
	dd=np.max(np.abs((tdot1-tdot2)/tdot1))
	# idot1=np.genfromtxt('i_N1000_a_e{0}_a{1}_o{2}_q{3}_ein{4}_dt{5}'.format(args.etest, args.atest, args.pomega, args.q, args.ein, args.dtag))
	# idot2=np.genfromtxt('i_N1000_b_e{0}_a{1}_o{2}_q{3}_ein{4}_dt{5}'.format(args.etest, args.atest, args.pomega, args.q, args.ein, args.dtag))
	# dd=max(dd, abs((idot1-idot2)/idot1))
	No=No*2
	i+=1
	print((args.etest, args.atest, args.pomega, i-1,No/2, abs((tdot1-tdot2)/tdot1)))#, abs((idot1-idot2)/idot1)
