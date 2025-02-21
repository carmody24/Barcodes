#!/usr/bin/env bash
#Author: carmodyc@berkeley.edu

#SBATCH --job-name=Sort1_M1
#SBATCH --account=
#SBATCH --partition=savio3_bigmem
#SBATCH --time=24:00:00
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

# Create an output directory within the current directory
OUTPUT_DIR="$(pwd)/output_files"
mkdir -p "$OUTPUT_DIR"

# Loop through each .fastq.gz file in the input directory
for file in "$INPUT_DIR"/*.fastq.gz; 
do 
  # Check if no fastq files found
  if [ ! -e "$file" ]; then
    echo "No .fastq files found in the directory."
    exit 1
  fi

  # Extract the base name without extension
  base_name=$(basename "$file" .fastq.gz)

  # Define the decompressed file path
  decompressed_file="$OUTPUT_DIR/${base_name}.fastq"

  # Decompress the file
  gzip -cd "$file" > "$decompressed_file"

  # Define the output CSV file name with Map1
  output_csv="$OUTPUT_DIR/${base_name}_Map1.csv"

  # Call your Python script with the necessary parameters
  python3 /pathway/to/CC_Sort1_M1.py --input "$decompressed_file" --output "$output_csv"

  # Optionally remove the decompressed file to save space
  rm "$decompressed_file"

done

echo "Processing complete for all .fastq files in $INPUT_DIR."
