#!/usr/bin/env bash
# Author: carmodyc@berkeley.edu

#SBATCH --job-name=Sort2
#SBATCH --account=
#SBATCH --partition=savio3_bigmem
#SBATCH --time=12:00:00
#SBATCH --output=%x-%j.out   # Save output to jobname-jobid.out file
#SBATCH --error=%x-%j.err    # Save error to jobname-jobid.err file

# Load necessary modules
module load python
pip install --user seaborn

# Check if the necessary arguments are provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

# Get the input directory from the command line arguments
INPUT_DIR=$1

# Create the output directory within the current directory
OUTPUT_DIR="$(pwd)/output_files_Map3"
mkdir -p "$OUTPUT_DIR"

# Loop through each .csv file in the input directory
for file in "$INPUT_DIR"/*.csv; 
do 
  # Check if no csv files found
  if [ ! -e "$file" ]; then
    echo "No .csv files found in the directory."
    exit 1
  fi

  # Call your Python script with the necessary parameters
  python3 /pathway/to/CC_Sort2_M2_M3_Graphs.py --input "$file"

done

echo "Processing complete for all .csv files in $INPUT_DIR."
