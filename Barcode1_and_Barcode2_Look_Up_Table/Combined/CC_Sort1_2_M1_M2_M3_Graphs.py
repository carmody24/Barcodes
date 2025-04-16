import pandas as pd
import gc
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import argparse
import gzip

#####################
# Define parser for command-line arguments
parser = argparse.ArgumentParser(description='Process input fastq files and generate Map1, Map2, and Map3.')
parser.add_argument('-i', '--input', type=str, required=True, help='Input directory containing fastq.gz files')

# Parse the command-line arguments
args = parser.parse_args()


output_directory = 'output_sort'
# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

#UPDATE names and fig format
# Global Variables
Lib_Name = 'Sort_Lib_1'
Fig_Format = 'jpeg'

def getmid(seq, pre, post):
    re_key = pre + "(.*)" + post
    poi_search = re.search(re_key, seq)
    return poi_search.group(1) if poi_search else "X" #X is added if pre and post seq flanking barcodes cannot be found 

#UPDATE barcode lengths and pre and post seq,
def tilebc_mapper(readfile, bc2_len=6, bc1_len=11, bc2_pre="CTTCTGA", bc2_post="GCTAGC", bc1_pre="GCTAGC", bc1_post="CTCGAGA"):
    sequences = []

    # Open file appropriately depending on compression
    open_func = gzip.open if readfile.endswith('.gz') else open
    mode = 'rt' if readfile.endswith('.gz') else 'r'

    with open_func(readfile, mode) as fin:
        for line in fin:
            if line.startswith('@'):
                seq = next(fin).strip()
                sequences.append(seq)

    int_bc_list, int_lengths, int_q_list = [], [], []
    adBC_list, adBC_lengths, aq_list = [], [], []

    for read in sequences:
        int_bc = getmid(read, bc2_pre, bc2_post)
        int_bc_list.append(int_bc)
        int_len = len(int_bc)
        int_lengths.append(int_len)
        int_q_list.append(1 if int_len == bc2_len else 0) #if wrong length = 0, if correct length = 1
        
        adBC = getmid(read, bc1_pre, bc1_post)
        adBC_list.append(adBC)
        adBC_len = len(adBC)
        adBC_lengths.append(adBC_len)
        aq_list.append(1 if adBC_len == bc1_len else 0) #if wrong length = 0, if correct length = 1

#UPDATE names of the summary table if you don't like integration and tile related names
    tileBC_dict = {
        "Reads": sequences, 
        "Int_BC": int_bc_list, 
        "Int_BC Len": int_lengths, 
        "Int_BC Qual": int_q_list, 
        "AD BCs": adBC_list, 
        "Tile_BC Len": adBC_lengths, 
        "Tile_BC Qual": aq_list
    }
    tileBC_df = pd.DataFrame(tileBC_dict)
    tileBC_summary_dict = {
        'Category': [
            'Total Num of sequences',
            'Total Correct Int BC Len',
            'Total Correct AD BC len',
            'Total Correct Int and AD BC len',
        ],
        'Read Count': [
            len(sequences),
            (tileBC_df["Int_BC Qual"] == 1).sum(),
            (tileBC_df["Tile_BC Qual"] == 1).sum(),
            ((tileBC_df["Tile_BC Qual"] == 1) & (tileBC_df["Int_BC Qual"] == 1)).sum(),
        ]
    }
    tileBC_summary_df = pd.DataFrame(tileBC_summary_dict)
    return tileBC_df, tileBC_summary_df

def analyze_map1_Int_BC_len(map1_data, base_name):
    plt.hist(map1_data['Int_BC Len'], bins=50)
    plt.title(f'{base_name} Int_BC Len Map1')
    plt.xlim([0, 150])
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Int_BC_Len_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_Tile_BC_len(map1_data, base_name):
    plt.hist(map1_data['Tile_BC Len'], bins=50)
    plt.title(f'{base_name} Tile_BC Len Map1')
    plt.xlim([0, 15])
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Tile_BC_Len_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_Int_BC_qual(map1_data, base_name):
    plt.hist(map1_data['Int_BC Qual'], bins=50)
    plt.title(f'{base_name} Int_BC Qual')
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Int_BC_Qual_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_Tile_BC_qual(map1_data, base_name):
    plt.hist(map1_data['Tile_BC Qual'], bins=50)
    plt.title(f'{base_name} Tile_BC Qual Map1')
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Tile_BC_Qual_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def process_input_file(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    rawmap, summary = tilebc_mapper(input_file)
    
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Map1.csv')
    rawmap.to_csv(f_path, index=False)
    
    analyze_map1_Int_BC_len(rawmap, base_name)
    analyze_map1_Tile_BC_len(rawmap, base_name)
    analyze_map1_Int_BC_qual(rawmap, base_name)
    analyze_map1_Tile_BC_qual(rawmap, base_name)
    
    summary_dir = os.path.join(output_directory, 'summary')
    os.makedirs(summary_dir, exist_ok=True)
    summary_path = os.path.join(summary_dir, f'{base_name}_{Lib_Name}_summary_Map1.csv')
    summary.to_csv(summary_path, index=False)

    #map1_nans = rawmap.replace(0, np.nan)
    map1_nans = rawmap[(rawmap["Int_BC Qual"] == 1) & (rawmap["Tile_BC Qual"] == 1)]
    map2 = map1_nans.dropna().reset_index().drop(columns=['index', 'Reads', 'Int_BC Len', 'Int_BC Qual', 'Tile_BC Len', 'Tile_BC Qual'])
    #m2fp = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Map2.csv')
    #map2.to_csv(m2fp, index=False) #UPDATE can uncomment if you want map2 created but you dont use it for anything
    
    map3 = map2.copy()
    # Convert the columns to strings if necessary
    map3['Int_BC'] = map3['Int_BC'].astype(str)
    map3['AD BCs'] = map3['AD BCs'].astype(str)
    
    map3['Cat'] = map3['Int_BC'] + '-' + map3['AD BCs']
    m3fp = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Map3.csv')
    map3.to_csv(m3fp, index=False)

    del rawmap, map2, map3
    gc.collect()
    
process_input_file(args.input)



