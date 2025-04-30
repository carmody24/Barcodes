#!/usr/bin/env bash
# Author: carmodyc@berkeley.edu

#SBATCH --job-name=Filter_M3
#SBATCH --account=
#SBATCH --partition=savio2
#SBATCH --time=03:00:00
#SBATCH --output=%x-%j.out   # Save output to jobname-jobid.out file
#SBATCH --error=%x-%j.err    # Save error to jobname-jobid.err file

# Load necessary modules
module load python
pip install --user pandas

# Check if the necessary arguments are provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <lookup_table.csv> <input_directory>"
  exit 1
fi

# Get the lookup table and input directory from the command line arguments
LOOKUP_TABLE=$1
INPUT_DIR=$2

# Create the output directory within the current directory
OUTPUT_DIR="$(pwd)/filtered_csv_files_ge50"
mkdir -p "$OUTPUT_DIR"

# Loop through each .csv file in the input directory
for file in "$INPUT_DIR"/*.csv; do
  # Check if no csv files found
  if [ ! -e "$file" ]; then
    echo "No .csv files found in the directory."
    exit 1
  fi

  # Call your Python script with the necessary parameters
  python3 /pathway/to/CC_Sort5_Filter_M3.py --lookup "$LOOKUP_TABLE" --input "$file" --output "$OUTPUT_DIR"

done

echo "Processing complete for all .csv files in $INPUT_DIR."
