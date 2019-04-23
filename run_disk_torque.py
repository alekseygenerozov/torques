from bash_command import bash_command as bc
import numpy as np
import sys
import argparse

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
# offset=sys.argv[5]

args=parser.parse_args()

dd=1.0
i=0
No=1001
while (dd>0.05) and (i<4):
	Nd=min(len(np.genfromtxt('a_{0}.txt'.format(args.dtag))), 1000)
	bc.bash_command('/projects/alge9397/code/c/torques/rebound_disk --etest {0} --atest {1} -o {2} -n {3} -f {4}  -q {5} --ein {6} --dtag {7}'\
		.format(args.etest, args.atest, args.pomega, No, 0, args.q, args.ein, args.dtag))
	sys.stdout.flush()
	bc.bash_command('/projects/alge9397/code/c/torques/rebound_disk --etest {0} --atest {1} -o {2} -n {3} -f {4}  -q {5} --ein {6} --dtag {7}'\
		.format(args.etest, args.atest, args.pomega, No, 1, args.q, args.ein, args.dtag))
	# bc.bash_command('~/code/c/torques/rebound_disk --etest {0} --atest {1} -o {2} -n {3} -f {4}  -q {5} --ein {6} --dtag {7}'.format(args.etest, args.atest, args.pomega, No, 0, args.q, args.ein, args.dtag))
	# sys.stdout.flush()
	# bc.bash_command('~/code/c/torques/rebound_disk --etest {0} --atest {1} -o {2} -n {3} -f {4}  -q {5} --ein {6} --dtag {7}'.format(args.etest, args.atest, args.pomega, No, 1, args.q, args.ein, args.dtag))

	tdot1=np.genfromtxt('tau_N{6}_a_e{0}_a{1}_o{2}_q{3}_ein{4}_dt{5}'.format(args.etest, args.atest, args.pomega, args.q, args.ein, args.dtag, Nd))
	tdot2=np.genfromtxt('tau_N{6}_b_e{0}_a{1}_o{2}_q{3}_ein{4}_dt{5}'.format(args.etest, args.atest, args.pomega, args.q, args.ein, args.dtag, Nd))
	dd=np.max(np.abs((tdot1-tdot2)/tdot1))
	# idot1=np.genfromtxt('i_N1000_a_e{0}_a{1}_o{2}_q{3}_ein{4}_dt{5}'.format(args.etest, args.atest, args.pomega, args.q, args.ein, args.dtag))
	# idot2=np.genfromtxt('i_N1000_b_e{0}_a{1}_o{2}_q{3}_ein{4}_dt{5}'.format(args.etest, args.atest, args.pomega, args.q, args.ein, args.dtag))
	# dd=max(dd, abs((idot1-idot2)/idot1))
	No=No*2
	i+=1
	print args.etest, args.atest, args.pomega, i-1,No/2, abs((tdot1-tdot2)/tdot1)#, abs((idot1-idot2)/idot1)
