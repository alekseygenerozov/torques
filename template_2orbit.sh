#!/bin/bash

#SBATCH --partition=shas
#SBATCH --qos=normal
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --job-name=end_torque
#SBATCH --output=end_torque_exx1_aww1_angyy1_tagzz1-%j.out

module load python/2.7.11
python ppp/run_disk_torque.py xx yy ww zz 
