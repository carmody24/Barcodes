#!/usr/bin/env bash
#Author: carmodyc@berkeley.edu

#SBATCH --job-name=CCS2_BC1_M2_M3
#
# Account:
#SBATCH --account=
# Partition:
#SBATCH --partition=savio3_bigmem
#
# Wall Clock Limit:




#SBATCH --time=08:00:00
## Commands to run:

module load python

python3 /pathway/to/CCS2_BC1_M2_M3_Filter_for_Quality_Reads.py -i /pathway/to/CCS1_BC1_Map1.csv
