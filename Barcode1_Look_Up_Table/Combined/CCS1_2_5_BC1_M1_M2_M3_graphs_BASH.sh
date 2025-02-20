#!/usr/bin/env bash
#Author: carmodyc@berkeley.edu

#SBATCH --job-name=CCS1_2_5_BC1
# Account:
#SBATCH --account=
# Partition:
#SBATCH --partition=savio3_bigmem
# Wall Clock Limit:
#SBATCH --time=24:00:00
# Output and Error files
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

## Commands to run:

module load python

# Install Seaborn if it's not already available
pip install --user seaborn

python3 /pathway/to/CCS1_2_5_BC1_M1_M2_M3_graphs.py -i /pathway/to/Paired_Seq_Reads.fastq -d /pathway/to/Tiles_Design_File.txt
