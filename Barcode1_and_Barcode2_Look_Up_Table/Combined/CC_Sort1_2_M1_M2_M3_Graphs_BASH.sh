#!/usr/bin/env bash
#Author: carmodyc@berkeley.edu

#SBATCH --job-name=Sort1_M1
#SBATCH --account=
#SBATCH --partition=savio3_bigmem
#SBATCH --time=10:00:00
#SBATCH --output=%x-%j.out   # Save output to jobname-jobid.out file
#SBATCH --error=%x-%j.err    # Save error to jobname-jobid.err file

# Load necessary modules
module load python

# Check if the directory name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

# Get the directory name from the command line argument
INPUT_DIR=$1

# Loop through each .fastq.gz.assembled.fastq file in the input directory
for file in "$INPUT_DIR"/*.fastq.gz.assembled.fastq; 
do 
  # Check if no fastq files found
  if [ ! -e "$file" ]; then
    echo "No .fastq.gz.assembled.fastq files found in the directory."
    exit 1
  fi

  # Call your Python script with the necessary parameters
  python3 /pathway/to/CC_Sort1_2_M1_M2_M3_Graphs.py --input "$file" 

done
