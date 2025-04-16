#!/usr/bin/env bash
# Author: carmodyc@berkeley.edu

#SBATCH --job-name=Downsample_FASTQ
#SBATCH --account=
#SBATCH --partition=savio3_bigmem
#SBATCH --time=12:00:00
#SBATCH --output=%x-%j.out   # Save output to jobname-jobid.out file
#SBATCH --error=%x-%j.err    # Save error to jobname-jobid.err file

# Load necessary modules
module load python

# Install Biopython if not already installed
pip install --user biopython

# Check if the input directory is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

# Set up variables
INPUT_DIR=$1 
DOWNSAMPLE_FRACTION=0.1  #UPDATE with the fraction you want downsampled (0.1 = 10%) 

# Format fraction for filenames (replace "." with "-")
SAFE_FRACTION="${DOWNSAMPLE_FRACTION//./-}"

# Create the output directory
OUTPUT_DIR="$INPUT_DIR/downsample_${SAFE_FRACTION}"
mkdir -p "$OUTPUT_DIR"

# Loop through all FASTQ files in the directory
for file in "$INPUT_DIR"/*.fastq; do
  # Check if files exist
  if [ ! -e "$file" ]; then
    echo "No FASTQ files found in the directory."
    exit 1
  fi

  # Generate output filename and place in the new directory
  OUTPUT_FASTQ="$OUTPUT_DIR/$(basename "${file%.fastq}_${SAFE_FRACTION}_downsampled.fastq")"

  # Run Python script to downsample the file
  python3 /pathway/to/downsample.py "$file" "$OUTPUT_FASTQ" "$DOWNSAMPLE_FRACTION"

  echo "Processed: $file -> $OUTPUT_FASTQ"
done
