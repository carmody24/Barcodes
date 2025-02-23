#!/usr/bin/env bash
# Author: carmodyc@berkeley.edu

#SBATCH --job-name=Sort_Map3
#SBATCH --account=
#SBATCH --partition=savio2
#SBATCH --time=12:00:00
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
python3 /pathway/to/Sort_CC3_M3_Filter_Analysis.py --input_dir "$INPUT_DIR"

echo "Processing complete for all .csv files in $INPUT_DIR."

