#!/usr/bin/env bash
# Author: carmodyc@berkeley.edu

#SBATCH --job-name=Filter_Step2
#SBATCH --account=
#SBATCH --partition=savio2
#SBATCH --time=01:00:00
#SBATCH --output=%x-%j.out   # Save output to jobname-jobid.out file
#SBATCH --error=%x-%j.err    # Save error to jobname-jobid.err file

# Load necessary modules
module load python

# Check if the necessary arguments are provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

# Get the input directory from the command line arguments
INPUT_DIR=$1

# Call your Python script with the necessary parameters
python3 /pathway/to/Filter_Treble_Step2_3_Barcodes.py --input_dir "$INPUT_DIR"



