#!/usr/bin/env bash

#SBATCH --job-name=CCS7_Final_LUT
#SBATCH --account=
#SBATCH --partition=savio3_bigmem
#SBATCH --time=04:00:00
#SBATCH --output=%x-%j.out   # Save output to jobname-jobid.out file
#SBATCH --error=%x-%j.err    # Save error to jobname-jobid.err file

# Load necessary modules
module load python
pip install --user numpy pandas matplotlib seaborn

# Check if the necessary arguments are provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

# Get the input directory from the command line arguments
INPUT_DIR=$1

# Call your Python script with the necessary parameters
python3 /pathway/to/CCS7_BC1_Final_LUT_Read_Threshold.py --input_dir "$INPUT_DIR"

echo "Processing complete for $INPUT_DIR."
