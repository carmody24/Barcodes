#!/usr/bin/env bash

#SBATCH --job-name=Merge_Map3_Norm_and_Control
#SBATCH --account=
#SBATCH --partition=savio3_bigmem
#SBATCH --time=04:00:00
#SBATCH --output=%x-%j.out   # Save output to jobname-jobid.out file
#SBATCH --error=%x-%j.err    # Save error to jobname-jobid.err file

# Load necessary modules
module load python

# Install pandas if it's not already available
pip install --user pandas

# Check if the necessary arguments are provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

# Get the input directory from the command line arguments
INPUT_DIR=$1

# Call your Python script with the necessary parameters
python3 /pathway/to/CCS4Optional_Merge_Normal_and_Control_Map3.py --input_dir "$INPUT_DIR"

echo "Merging complete for files in $INPUT_DIR."
