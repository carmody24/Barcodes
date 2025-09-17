#!/usr/bin/env bash

#SBATCH --job-name=CCS7_Final_LUT
#SBATCH --account=ac_stallerlab
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
python3 /global/scratch/projects/fc_mvslab/OpenProjects/Caitlin/L4/S1_czb/TL4S1_czb_NEW_Maps_and_Graphs/TL4S1_czb_Min_Maps_and_Graphs_Minimal/Unique_Cat_Filtering_Map4.py --input_dir "$INPUT_DIR"

echo "Processing complete for $INPUT_DIR."
