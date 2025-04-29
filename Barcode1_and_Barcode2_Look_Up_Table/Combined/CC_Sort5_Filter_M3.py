import pandas as pd
import os
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Filter CSV files based on lookup table.')
parser.add_argument('--lookup', type=str, required=True, help='Path to the lookup table CSV file.')
parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file.')
parser.add_argument('--output', type=str, required=True, help='Directory to save the filtered CSV file.')
args = parser.parse_args()

# Load the lookup table
lookup_df = pd.read_csv(args.lookup)

# Load the input CSV file
input_df = pd.read_csv(args.input)

# Filter rows based on the 'Cat' column
filtered_df = input_df[input_df['Cat'].isin(lookup_df['Cat'])]

# Save the filtered DataFrame to a new CSV file
output_filename = os.path.basename(args.input)
output_path = os.path.join(args.output, output_filename)
filtered_df.to_csv(output_path, index=False)

# Summary dictionary to store the original and filtered row counts
summary_dict = {
    'Filename': [output_filename],
    'Original_Row_Count': [input_df.shape[0]],
    'Filtered_Row_Count': [filtered_df.shape[0]]
}

# Convert the dictionary to a DataFrame
summary_df = pd.DataFrame(summary_dict)

# Define the summary output path
summary_output_path = os.path.join(args.output, 'summary.csv')

# Check if summary file already exists
if os.path.exists(summary_output_path):
    # If the summary file exists, append the new summary data
    existing_summary_df = pd.read_csv(summary_output_path)
    summary_df = pd.concat([existing_summary_df, summary_df], ignore_index=True)

# Save the summary DataFrame to the summary CSV file
summary_df.to_csv(summary_output_path, index=False)

