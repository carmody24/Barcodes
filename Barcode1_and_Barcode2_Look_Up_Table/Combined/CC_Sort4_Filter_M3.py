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

# Extract the base name of the input directory
base_name = os.path.basename(input_dir.rstrip('/'))

# Define and create the output directory within the current directory
Output_Directory = os.path.join(os.getcwd(), 'output_files_sort_CC4') #UPDATE to where you want your files to go 
os.makedirs(Output_Directory, exist_ok=True)

# Global Variables
Fig_Format = 'jpeg'  # file format you want all the graphs to be saved
Lib_Name = 'S2_Lib3_R1'  # name you want to be at the start of the files
Thres_TBcov = 5  # UPDATE to the read min threshold you want

Map4_Summary_Dict = {
    'Category': [],
    'Read Count': []
}

# Read and merge the CSV files in the input directory
all_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]
map3 = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)

# Add initial info to the summary dict
Map4_Summary_Dict['Category'].append('Map3 Starting Read Count')
Map4_Summary_Dict['Read Count'].append(map3.shape[0])

# Count unique AD BCs initially
initial_unique_tiles = map3['AD BCs'].nunique()
Map4_Summary_Dict['Category'].append('Initial Unique AD BCs')
Map4_Summary_Dict['Read Count'].append(initial_unique_tiles)

# Generate value counts for 'Cat' and filter by the threshold
tbcov = map3['Cat'].value_counts().to_frame().reset_index()
tbcov.columns = ['Cat', 'count']

Map4_Summary_Dict['Category'].append('Starting Unique Tile + BC Count')
Map4_Summary_Dict['Read Count'].append(tbcov.shape[0])

# Filter 'Cat' by coverage threshold > Thres_TBcov
filtered_cats = tbcov[tbcov['count'] >= Thres_TBcov]
filtered_map3 = map3[map3['Cat'].isin(filtered_cats['Cat'])]

Map4_Summary_Dict['Category'].append(f'Map3 >= {Thres_TBcov} reads per Cat (Tile + BC)')
Map4_Summary_Dict['Read Count'].append(filtered_map3.shape[0])

# Count unique AD BCs after filtering
final_unique_tiles = filtered_map3['AD BCs'].nunique()
Map4_Summary_Dict['Category'].append('Final Unique AD BCs (after filtering)')
Map4_Summary_Dict['Read Count'].append(final_unique_tiles)

# Generate unique 'Cat' LUT and export as CSV
unique_cats = filtered_map3.drop_duplicates(subset='Cat')
unique_cats['Cat_Count'] = filtered_map3.groupby('Cat')['Cat'].transform('count')

lut_fp = os.path.join(Output_Directory, f'{Lib_Name}_{base_name}_ge{Thres_TBcov}_SORT_LUT.csv')
unique_cats.to_csv(lut_fp, index=False)

Map4_Summary_Dict['Category'].append(f'Map3 >= {Thres_TBcov} Unique Cat')
Map4_Summary_Dict['Read Count'].append(unique_cats.shape[0])

# Export the summary dictionary as a CSV
summary_fp = os.path.join(Output_Directory, f'{Lib_Name}_{base_name}_ge{Thres_TBcov}_Summary_CCS4.csv')
pd.DataFrame(Map4_Summary_Dict).to_csv(summary_fp, index=False)

