import pandas as pd
import os
import argparse

# Create parser for command-line arguments
parser = argparse.ArgumentParser(description='Merge two CSV files with the same columns.')
parser.add_argument('-i', '--input_dir', type=str, required=True, help='Input directory containing the two CSV files you want to merge')

# Parse the command-line arguments
args = parser.parse_args()

# Get the list of CSV files in the input directory
csv_files = [f for f in os.listdir(args.input_dir) if f.endswith('.csv')]

# Ensure there are exactly two CSV files
if len(csv_files) != 2:
    raise ValueError('The input directory must contain exactly two CSV files.')

# Read the CSV files
df1 = pd.read_csv(os.path.join(args.input_dir, csv_files[0]))
df2 = pd.read_csv(os.path.join(args.input_dir, csv_files[1]))

# Merge the CSV files
merged_df = pd.concat([df1, df2], ignore_index=True)

# Set output file path
#UPDATE name if you want I like to include something more descriptive besides mjust Merge becuase there is another potential merge step in the future and you want to be able to differentiate them
output_file = os.path.join(args.input_dir, "Merged_Map3_with_Controls.csv") 

# Save the merged DataFrame to a new CSV file in the same directory
merged_df.to_csv(output_file, index=False)

