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
Output_Directory = os.path.join(os.getcwd(), 'output_files_Map3_analysisf')
os.makedirs(Output_Directory, exist_ok=True)

# Global Variables 
Fig_Format = 'jpeg'  # file format you want all the graphs to be saved
Lib_Name = 'Sort_Lib_2_R2'  # name you want to be at the start of the files 

Map3_Summary_Dict = {
    'Category': [],
    'Read Count': []
}

# Read and merge the CSV files in the input directory
all_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]
map3 = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)

#Graphs of coverage of Unique combinations of Tile + BC1 and of Unique Tile coverage based on Map3 (Map1 filtered to only keep rows with correct length of tile and BC1 and tile must be in design file)
def analyze_tcov_nom(map3_data):
    sns.histplot(x='count', data=map3_data, bins=100)
    plt.title(f'{Lib_Name} Unique Tile Coverage All Bins Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_Tcov_uf_Map3.{Fig_Format}')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_tcov_exp(map3_data):
    sns.histplot(x='count', data=map3_data, log_scale=(True, True), bins=100)
    plt.title(f'{Lib_Name} Unique Tile Coverage All Bins Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_Tcov_uf_exp_Map3.{Fig_Format}')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_tbcov_exp(map3_data):
    sns.histplot(data=map3_data, x='count', log_scale=(True, True), bins=100)
    plt.title(f'{Lib_Name} Unique Tile + BC Coverage All Bins Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_TBcov_exp_uf_Map3.{Fig_Format}')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()
    
def analyze_tbcov_nom(map3_data):
    sns.histplot(data=map3_data, x='count', bins=100)
    plt.title(f'{Lib_Name} Unique Tile + BC Coverage All Bins Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_TBcov_nom_uf_Map3.{Fig_Format}')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

# Tile + BC coverage
tbcov = map3['Cat'].value_counts().to_frame().reset_index()
#analyze_tbcov_nom(tbcov)
analyze_tbcov_exp(tbcov)

tbcov.columns = ['Cat', 'count']
tbcov['count'] = tbcov['count'].astype(int)

tcov = map3['AD BCs'].value_counts().to_frame().reset_index()
analyze_tcov_exp(tcov)
analyze_tcov_nom(tcov)

tcov.columns = ['AD BCs', 'count']
tcov['count'] = tcov['count'].astype(int)

# Calculate the number of Cat with counts above thresholds
above_2 = tbcov[tbcov['count'] > 2].shape[0]
above_3 = tbcov[tbcov['count'] > 3].shape[0]
above_5 = tbcov[tbcov['count'] > 5].shape[0]
above_10 = tbcov[tbcov['count'] > 10].shape[0]
above_100 = tbcov[tbcov['count'] > 100].shape[0]
above_1000 = tbcov[tbcov['count'] > 1000].shape[0]
above_10000 = tbcov[tbcov['count'] > 10000].shape[0]


# Calculate the number of Tiles with counts above thresholds
tabove_2 = tcov[tcov['count'] > 2].shape[0]
tabove_3 = tcov[tcov['count'] > 3].shape[0]
tabove_5 = tcov[tcov['count'] > 5].shape[0]
tabove_10 = tcov[tcov['count'] > 10].shape[0]
tabove_100 = tcov[tcov['count'] > 100].shape[0]
tabove_1000 = tcov[tcov['count'] > 1000].shape[0]
tabove_10000 = tcov[tcov['count'] > 10000].shape[0]


# Add info to summary dict
Map3_Summary_Dict['Category'].append('Map3 shape')
Map3_Summary_Dict['Read Count'].append(map3.shape[0])

Map3_Summary_Dict['Category'].append('Unique Tile + BC Count')
Map3_Summary_Dict['Read Count'].append(tbcov.shape[0])

Map3_Summary_Dict['Category'].append('Number of Cat with counts above  2')
Map3_Summary_Dict['Read Count'].append(above_2)

Map3_Summary_Dict['Category'].append('Number of Cat with counts above 3')
Map3_Summary_Dict['Read Count'].append(above_3)

Map3_Summary_Dict['Category'].append('Number of Cat with counts above 5')
Map3_Summary_Dict['Read Count'].append(above_5)

Map3_Summary_Dict['Category'].append('Number of Cat with counts above 10')
Map3_Summary_Dict['Read Count'].append(above_10)

Map3_Summary_Dict['Category'].append('Number of Cat with counts above 100')
Map3_Summary_Dict['Read Count'].append(above_100)

Map3_Summary_Dict['Category'].append('Number of Cat with counts above 1,000')
Map3_Summary_Dict['Read Count'].append(above_1000)

Map3_Summary_Dict['Category'].append('Number of Cat with counts above 10,000')
Map3_Summary_Dict['Read Count'].append(above_10000)

Map3_Summary_Dict['Category'].append('Unique Tile  Count')
Map3_Summary_Dict['Read Count'].append(tcov.shape[0])

Map3_Summary_Dict['Category'].append('Number of Tiles with counts above  2')
Map3_Summary_Dict['Read Count'].append(tabove_2)

Map3_Summary_Dict['Category'].append('Number of Tiles with counts above 3')
Map3_Summary_Dict['Read Count'].append(tabove_3)

Map3_Summary_Dict['Category'].append('Number of Tiles with counts above 5')
Map3_Summary_Dict['Read Count'].append(tabove_5)

Map3_Summary_Dict['Category'].append('Number of Tiles with counts above 10')
Map3_Summary_Dict['Read Count'].append(tabove_10)

Map3_Summary_Dict['Category'].append('Number of Tiles with counts above 100')
Map3_Summary_Dict['Read Count'].append(tabove_100)

Map3_Summary_Dict['Category'].append('Number of Tiles with counts above 1,000')
Map3_Summary_Dict['Read Count'].append(tabove_1000)

Map3_Summary_Dict['Category'].append('Number of Tiles with counts above 10,000')
Map3_Summary_Dict['Read Count'].append(tabove_10000)

# Export summary
Map3_Summary_Dict_df = pd.DataFrame.from_dict(Map3_Summary_Dict)
sum3_f_p = os.path.join(Output_Directory, f'{Lib_Name}_{base_name}_Summary_Map3.csv')
Map3_Summary_Dict_df.to_csv(sum3_f_p, index=False)


