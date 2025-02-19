#!/usr/bin/env bash
#Author: carmodyc@berkeley.edu

#SBATCH --job-name=CCS1_M1_BC1
#
# Account:
#SBATCH --account=
# Partition:
#SBATCH --partition=savio3_bigmem
#
# Wall Clock Limit:




#SBATCH --time=12:00:00
## Commands to run:

module load python

python3 CCS1_BC1_M1_Identify_Quality_Reads.py -i Step1_BC1_Paired_Seq_Reads.fastq.gz.assembled.fastq -d Tiles_Design_File.txt
