import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
import gc

############################
# Create parser for command-line arguments
#input is a directory incase you want to subject multiple Map3 files to the same thresholding (sometimes I do merge and intersect Map3 at same time)
parser = argparse.ArgumentParser(description='Process input CSV files and perform filtering and analysis.')
parser.add_argument('-i', '--input_dir', type=str, required=True, help='Input directory containing Map3 CSV files')

# Parse the command-line arguments 
args = parser.parse_args()

# Use the parsed arguments 
input_directory = args.input_dir

# Extract the base name of the input directory
base_name = os.path.basename(input_directory.rstrip('/'))

#UPDATE names if you want 
# Global Variables
Lib_Name = 'L1I_ge10'
Fig_Format = 'jpeg'
Thres_TBcov = 30 #UPDATE to the read min threshold you want = critical 

# Define the output directory within the current directory
output_directory = os.path.join(os.getcwd(), f'{Lib_Name}_{base_name}_CCS7_output_files')
os.makedirs(output_directory, exist_ok=True)

# Define the summary directory within the output directory
summary_dir = os.path.join(output_directory, f'{Lib_Name}_CCS7_summary')
os.makedirs(summary_dir, exist_ok=True)

def process_map3_file(file_path):
    Map4_Summary_Dict = {
        'Category': [],
        'Read Count': []
    }

    base_name = os.path.splitext(os.path.basename(file_path))[0] #naming of output file based on input file name
    
    # Load Map3 file
    map3 = pd.read_csv(file_path)

    #fM_path = os.path.join(output_directory, f'{Lib_Name}_{base_name}_Map3.csv')
    #map3.to_csv(fM_path, index=False)

    # Add info to summary dict
    Map4_Summary_Dict['Category'].append('Map3 Starting Read Count')
    Map4_Summary_Dict['Read Count'].append(map3.shape[0])
    
    # Count unique Tiles initially
    initial_unique_tiles = map3['Tiles'].nunique()
    Map4_Summary_Dict['Category'].append('Initial Unique Tiles')
    Map4_Summary_Dict['Read Count'].append(initial_unique_tiles)

    # Filter out rows where one ADBC maps to multiple tiles but will keep if 90% of the times the BC appears it is with 1 tile
    grouped = map3.groupby('AD BCs')['Tiles'].value_counts().reset_index(name='count')
    total_counts = grouped.groupby('AD BCs')['count'].sum().reset_index(name='total_count')
    grouped = grouped.merge(total_counts, on='AD BCs')
    grouped['percentage'] = grouped['count'] / grouped['total_count']
    to_keep = grouped[grouped['percentage'] >= 0.9] #you can modify this to be more strigent but wouldn't make more permisive 
    filtered_df = map3.merge(to_keep[['AD BCs', 'Tiles']], on=['AD BCs', 'Tiles'], how='inner')
    
    # Count unique Tiles after filtering
    final_unique_tiles = filtered_df['Tiles'].nunique()
    Map4_Summary_Dict['Category'].append('Final Unique Tiles (after initial filtering)')
    Map4_Summary_Dict['Read Count'].append(final_unique_tiles)

    # Add info to summary dict
    Map4_Summary_Dict['Category'].append('Section: Filtering to Remove reads where one ADBC maps to multiple tiles and most frequent occurancace is <90%')
    Map4_Summary_Dict['Read Count'].append('')
    Map4_Summary_Dict['Category'].append('Starting number of unique tile + bc combos')
    Map4_Summary_Dict['Read Count'].append(grouped.shape[0])
    Map4_Summary_Dict['Category'].append('Ending number of unique tile + bc combos')
    Map4_Summary_Dict['Read Count'].append(to_keep.shape[0])
    Map4_Summary_Dict['Category'].append('Starting number of unique BCs')
    Map4_Summary_Dict['Read Count'].append(total_counts.shape[0])
    Map4_Summary_Dict['Category'].append('Ending number of unique BCs')
    Map4_Summary_Dict['Read Count'].append(filtered_df['AD BCs'].nunique())
    Map4_Summary_Dict['Category'].append('Ending number of reads')
    Map4_Summary_Dict['Read Count'].append(filtered_df.shape[0])

    #you can uncomment out this to produce a file of the FULL df after initial filtering but I found it unnessicary 
    #dffp = os.path.join(output_directory, f'{Lib_Name}_{base_name}_Map3_initial_filtered_df.csv')
    #filtered_df.to_csv(dffp, index=False)

    # Generate tbcov
    Map4_Summary_Dict['Category'].append(f'Section: Filtering Out Low Coverage Tile+BC combos <{Thres_TBcov} reads each')
    Map4_Summary_Dict['Read Count'].append('')
    tbcov = filtered_df['Cat'].value_counts().to_frame().reset_index()
    Map4_Summary_Dict['Category'].append('Starting Unique Tile + BC')
    Map4_Summary_Dict['Read Count'].append(tbcov.shape[0])
    
    #you can uncomment this to produce a file of the LUT (unique Tile+ BC1 combos) after initial filtering but I found it unnessicary 
    #tffp = os.path.join(output_directory, f'{Lib_Name}_{base_name}_initial_tbcov_filter.csv')
    #tbcov.to_csv(tffp, index=False)

    # Export summary table into csv file after initial filtering uncomment if you want 
    #Map4_Summary_Dict_df = pd.DataFrame.from_dict(Map4_Summary_Dict)
    #sum_f_p = os.path.join(summary_dir, f'{Lib_Name}_{base_name}_Summary_CCS_firsthalf_Map3filter.csv')
    #Map4_Summary_Dict_df.to_csv(sum_f_p, index=False)

    # Filter by coverage threshold
    map3_ge100 = filtered_df[filtered_df['Cat'].isin(tbcov[tbcov['count'] >= Thres_TBcov]['Cat'])]
    #you can uncomment to create csv file of FULL df filtered for both filters but creates a very large file so I only make the LUT 
    #map3_ge5_fp = os.path.join(output_directory, f'{Lib_Name}_{base_name}_ge{Thres_TBcov}.csv')
    #map3_ge100.to_csv(map3_ge5_fp, index=False)

    Map4_Summary_Dict['Category'].append(f'Map3 >= {Thres_TBcov} reads per Cat')
    Map4_Summary_Dict['Read Count'].append(map3_ge100.shape[0])
    
    # Count unique Tiles after filtering
    final_unique_tilesx = map3_ge100['Tiles'].nunique()
    Map4_Summary_Dict['Category'].append('Final Unique Tiles (after Final filtering)')
    Map4_Summary_Dict['Read Count'].append(final_unique_tilesx)

    map3_ge5_unique = map3_ge100.drop_duplicates(subset='Cat')
    
    #add counts of each Cat 
    map3_ge5_unique['Cat_Count'] = map3_ge100.groupby('Cat')['Cat'].transform('count')

    #create LUT of df filtered for ADBC mapping to multiple BC1 <90% of time and > read threshold, LUT are the unique Cat (Tile+BC1) combinations 
    map3_ge5_unique_fp = os.path.join(output_directory, f'{Lib_Name}_{base_name}_ge{Thres_TBcov}_LUT.csv')
    map3_ge5_unique.to_csv(map3_ge5_unique_fp, index=False)

    Map4_Summary_Dict['Category'].append(f'Map3 >= {Thres_TBcov} Unique Cat')
    Map4_Summary_Dict['Read Count'].append(map3_ge5_unique.shape[0])

    #create summary csv
    Map3_Summary_Dict_df = pd.DataFrame.from_dict(Map4_Summary_Dict)
    sum3_f_p = os.path.join(summary_dir, f'{Lib_Name}_{base_name}_ge{Thres_TBcov}_Summary_CCS7.csv')
    Map3_Summary_Dict_df.to_csv(sum3_f_p, index=False)

# Loop through each .csv file in the input directory
for file in os.listdir(input_directory):
    if file.endswith('.csv'):
        file_path = os.path.join(input_directory, file)
        process_map3_file(file_path)

print('Finished with Everything')
