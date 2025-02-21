import pandas as pd
import gc
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

# Code to talk with command line docs you input
# Create parser
parser = argparse.ArgumentParser(description='Process input CSV file.')
parser.add_argument('-i', '--input', type=str, required=True, help='Input CSV file path of Map1 created from Step1')

# Parse the command-line arguments
args = parser.parse_args()

# Use the parsed arguments
Map1_File = args.input

# Extract the base name of the input file without extension
base_name = os.path.splitext(os.path.basename(Map1_File))[0]

# Define and create the output directory within the current directory
Output_Directory = os.path.join(os.getcwd(), 'output_files_Map3')
os.makedirs(Output_Directory, exist_ok=True)

# Define and create the summary directory within the output directory
summary_dir = os.path.join(Output_Directory, 'summary')
os.makedirs(summary_dir, exist_ok=True)

#UPDATE names
# Global Variables
Fig_Format = 'jpeg'  # File format for graphs
Lib_Name = 'Lib_1_Sort'  # Prefix for file names

Map2_Summary_Dict = {
    'Category': [],
    'Read Count': []
}

# Map1 Functions creates quality graphs of data from Map1
def analyze_map1_Int_BC_len(map1_data, base_name):
    plt.hist(map1_data['Int_BC Len'], bins=50)
    plt.title(f'{base_name} Int_BC Len Map1')
    plt.xlim([0, 150])
    f_path = os.path.join(Output_Directory, f'{base_name}_{Lib_Name}_Int_BC_Len_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_Tile_BC_len(map1_data1, base_name):
    plt.hist(map1_data1['Tile_BC Len'], bins=50)
    plt.title(f'{base_name} Tile_BC Len Map1')
    plt.xlim([0, 15])
    f_path1 = os.path.join(Output_Directory, f'{base_name}_{Lib_Name}_Tile_BC_Len_Map1.jpg')
    plt.savefig(f_path1, format=Fig_Format)
    plt.clf()

def analyze_map1_Int_BC_qual(map1_data2, base_name):
    plt.hist(map1_data2['Int_BC Qual'], bins=50)
    plt.title(f'{base_name} Int_BC Qual')
    f_path2 = os.path.join(Output_Directory, f'{base_name}_{Lib_Name}_Int_BC_Qual_Map1.jpg')
    plt.savefig(f_path2, format=Fig_Format)
    plt.clf()

def analyze_map1_Tile_BC_qual(map1_data3, base_name):
    plt.hist(map1_data3['Tile_BC Qual'], bins=50)
    plt.title(f'{base_name} Tile_BC Qual Map1')
    f_path3 = os.path.join(Output_Directory, f'{base_name}_{Lib_Name}_Tile_BC_Qual_Map1.jpg')
    plt.savefig(f_path3, format=Fig_Format)
    plt.clf()

# Read in raw df to Make Map1
map1 = pd.read_csv(Map1_File)

# Analyze map1 and make graphs
analyze_map1_Int_BC_len(map1, base_name)
analyze_map1_Tile_BC_len(map1, base_name)
analyze_map1_Int_BC_qual(map1, base_name)
analyze_map1_Tile_BC_qual(map1, base_name)

print('Map1 maps finished')

#######################
# Add things to summary for Map1
Map2_Summary_Dict['Category'].append('Map1 Total Num of sequences')
Map2_Summary_Dict['Read Count'].append(map1.shape[0])

Map2_Summary_Dict['Category'].append('Map1 Total Correct Int BC')
Map2_Summary_Dict['Read Count'].append((map1["Int_BC Qual"] == 1).sum())

Map2_Summary_Dict['Category'].append('Map1 Total Correct AD BC')
Map2_Summary_Dict['Read Count'].append((map1["Tile_BC Qual"] == 1).sum())

Map2_Summary_Dict['Category'].append('Map1 Total Correct Int and AD BC')
Map2_Summary_Dict['Read Count'].append(((map1["Tile_BC Qual"] == 1) & (map1["Int_BC Qual"] == 1)).sum())

# Create Map2 (only have Tiles and BC columns)
map1_nans = map1.replace(0, np.nan)
map2 = map1_nans.dropna().reset_index()
clabels = ['index', 'Reads', 'Int_BC Len', 'Int_BC Qual', 'Tile_BC Len', 'Tile_BC Qual']
map2 = map2.drop(clabels, axis=1)
m2fp = os.path.join(Output_Directory, f'{base_name}_{Lib_Name}_Map2.csv')
map2.to_csv(m2fp, index=False)
del map1, map2
gc.collect()

# Create Map3 (Tiles, BC, and Cat (tile - BC)
map3 = pd.read_csv(m2fp)
adcol = map3['AD BCs'].copy()
map3['Cat'] = map3['Int_BC'].str.cat(adcol, sep="-")
Map2_Summary_Dict['Category'].append('Map3 Shape (should be same as Total Correct Tile and Inc BC)')
Map2_Summary_Dict['Read Count'].append(map3.shape[0])
m3fp = os.path.join(Output_Directory, f'{base_name}_{Lib_Name}_Map3.csv')
map3.to_csv(m3fp, index=False)

# Save summary
Map2_Summary_Dict_df = pd.DataFrame.from_dict(Map2_Summary_Dict)
summary_path = os.path.join(summary_dir, f'{base_name}_{Lib_Name}_Sort2_summary.csv')
Map2_Summary_Dict_df.to_csv(summary_path, index=False)

print('Everything Finished')
