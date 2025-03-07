#!/usr/bin/env bash

#SBATCH --job-name=No_Length
#SBATCH --account=
# Partition:
#SBATCH --partition=savio2
#SBATCH --time=04:00:00
#SBATCH --output=%x-%j.out   # Save output to jobname-jobid.out file
#SBATCH --error=%x-%j.err    # Save error to jobname-jobid.err file

# Load necessary modules
module load python

# Install pandas if not already available
pip install --user pandas seaborn

# Check if the necessary arguments are provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

# Get the input directory from the command line arguments
INPUT_DIR=$1

# Call your Python script with the necessary parameters
python3 /pathway/to/no_length/CC_M3_Including_Not_In_T_Length.py --input_dir "$INPUT_DIR"

echo "Processing complete for replicates in $INPUT_DIR."
