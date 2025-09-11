import pandas as pd
import gc
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

# Create parser
parser = argparse.ArgumentParser(description='Process input directory containing CSV files.')
parser.add_argument('-i', '--input_dir', type=str, required=True, help='Input directory containing CSV files')

# Parse the command-line arguments
args = parser.parse_args()
input_dir = args.input_dir

# Define and create the output directory within the current directory
Output_Directory = os.path.join(os.getcwd(), 'output_files') #UPDATE to where you want your files to go 
os.makedirs(Output_Directory, exist_ok=True)

# Global Variables
Fig_Format = 'jpeg'  #UPDATE file format you want all the graphs to be saved
Lib_Name = 'TS2'  # UPDATE name you want to be at the start of the files
Thres_TBcov = 50  # UPDATE to the read min threshold you want
Filter_Column = 'HAR'#UPDATE with the column you want to filter by usually the concatenation of all the barcodes 
summary_dict = {
    'Category': [],
    'Read Count': []
}

# Read the single CSV file in the input directory
csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
if len(csv_files) != 1:
    raise ValueError("Input directory must contain exactly one CSV file.")

csv_path = os.path.join(input_dir, csv_files[0])
map3 = pd.read_csv(csv_path)

# Add initial info to the summary dict
summary_dict['Category'].append('Map3 Starting Read Count')
summary_dict['Read Count'].append(map3.shape[0])

# Count unique BC1 initially
initial_unique_tiles = map3['BC1'].nunique()
summary_dict['Category'].append('Initial Unique BC1')
summary_dict['Read Count'].append(initial_unique_tiles)

# Count unique BC2 initially
initial_unique_tiles2 = map3['BC2'].nunique()
summary_dict['Category'].append('Initial Unique BC2')
summary_dict['Read Count'].append(initial_unique_tiles2)

# Count unique BC3 initially
initial_unique_tiles3 = map3['BC3'].nunique()
summary_dict['Category'].append('Initial Unique BC3')
summary_dict['Read Count'].append(initial_unique_tiles3)

# Generate value counts for Filter_Column and filter by the threshold
tbcov = map3[f'{Filter_Column}'].value_counts().to_frame().reset_index()
tbcov.columns = [f'{Filter_Column}', 'count']

summary_dict['Category'].append('Starting Unique BC1 + BC2 + BC3 Count')
summary_dict['Read Count'].append(tbcov.shape[0])

# Filter f'{Filter_Column}' by coverage threshold > Thres_TBcov
filtered_cats = tbcov[tbcov['count'] >= Thres_TBcov]
filtered_map3 = map3[map3[f'{Filter_Column}'].isin(filtered_cats[f'{Filter_Column}'])]

summary_dict['Category'].append(f'Map3 >= {Thres_TBcov} reads per HAR (BC1 + BC2 + BC3)')
summary_dict['Read Count'].append(filtered_map3.shape[0])

#summary file section divider
summary_dict['Category'].append('New Section')
summary_dict['Read Count'].append('Counts After Filtering')

# Count unique AD BCs after filtering
final_unique_tiles = filtered_map3['BC1'].nunique()
summary_dict['Category'].append('Final Unique BC1')
summary_dict['Read Count'].append(final_unique_tiles)

# Count unique BC2 after filtering
final_unique_tiles2 = filtered_map3['BC2'].nunique()
summary_dict['Category'].append('Final Unique BC2')
summary_dict['Read Count'].append(final_unique_tiles2)

# Count unique BC3 after filtering
final_unique_tiles3 = filtered_map3['BC3'].nunique()
summary_dict['Category'].append('Final Unique BC3')
summary_dict['Read Count'].append(final_unique_tiles3)

# Generate unique 'HA' LUT and export as CSV
unique_cats = filtered_map3.drop_duplicates(subset=f'{Filter_Column}')
unique_cats = unique_cats.copy()
unique_cats['Cat_Count'] = filtered_map3.groupby(f'{Filter_Column}')[f'{Filter_Column}'].transform('count')

file_path_csv = os.path.join(Output_Directory, f'{Lib_Name}_ge{Thres_TBcov}_{Filter_Column}_Step2_LUT.csv')
unique_cats.to_csv(file_path_csv, index=False)

summary_dict['Category'].append(f'Map3 >= {Thres_TBcov} Unique {Filter_Column}')
summary_dict['Read Count'].append(unique_cats.shape[0])

# Export the summary dictionary as a CSV
summary_fp = os.path.join(Output_Directory, f'{Lib_Name}_ge{Thres_TBcov}_{Filter_Column}_Summary.csv')
pd.DataFrame(summary_dict).to_csv(summary_fp, index=False)

