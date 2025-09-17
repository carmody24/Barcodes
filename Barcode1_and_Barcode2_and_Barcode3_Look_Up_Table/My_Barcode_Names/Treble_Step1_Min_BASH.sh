#!/usr/bin/env bash
#Author: carmodyc@berkeley.edu

#SBATCH --job-name=Treble_Step1
# Account:
#SBATCH --account=
# Partition:
#SBATCH --partition=savio3_bigmem
# Wall Clock Limit:
#SBATCH --time=03:00:00
# Output and Error files
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

## Commands to run:

module load python

# Install Seaborn if it's not already available
pip install --user seaborn

python3 /global/scratch/projects/fc_mvslab/OpenProjects/Caitlin/L4/S1_czb/Treble_Step1_minimal.py -i fastq_file.fastq -d design_file.txt
