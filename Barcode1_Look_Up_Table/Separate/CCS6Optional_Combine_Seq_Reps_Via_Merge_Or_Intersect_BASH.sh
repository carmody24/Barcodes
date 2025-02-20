#!/usr/bin/env bash
#Author: your_email@berkeley.edu

#SBATCH --job-name=CCS6_M_and_I
# Account:
#SBATCH --account=
# Partition:
#SBATCH --partition=savio3_bigmem
# Wall Clock Limit:
#SBATCH --time=05:00:00
# Output and Error files
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

## Commands to run:

module load python

# Install Seaborn if it's not already available
pip install --user seaborn

python3 /pathway/to/CCS6Optional_Combine_Seq_Reps_Via_Merge_Or_Intersect.py -r1 /pathway/to/Seq_Rep1_Map3_Final.csv -r2 /pathway/to/Seq_Rep1_Map3_Final.csv --intersect --merge
