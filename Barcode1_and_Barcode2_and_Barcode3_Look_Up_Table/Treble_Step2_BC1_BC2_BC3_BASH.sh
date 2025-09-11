#!/usr/bin/env bash
#Author: carmodyc@berkeley.edu

#SBATCH --job-name=Treble_Step2
#SBATCH --account=
#SBATCH --partition=savio2_bigmem
#SBATCH --time=04:00:00
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
for file in "$INPUT_DIR"/*.fastq.gz; #UPDATE if your file is named differently need to change this so it matches what your file is
do 
  # Check if no fastq files found
  if [ ! -e "$file" ]; then
    echo "No .fastq.gz files found in the directory."
    exit 1
  fi

  # Call yython script with the necessary parameters
  python3 /pathway/to/Treble_Step2_BC1_BC2_BC3.py --input "$file" 

done
