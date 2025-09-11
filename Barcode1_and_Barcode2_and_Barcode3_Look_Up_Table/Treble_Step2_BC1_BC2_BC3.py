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


output_directory = 'output_TS2'#UPDATE output directory name
# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

#UPDATE names and fig format
# Global Variables
Lib_Name = 'Step2_TL4S2'
Fig_Format = 'jpeg'

def getmid(seq, pre, post):
    re_key = pre + "(.*)" + post
    poi_search = re.search(re_key, seq)
    return poi_search.group(1) if poi_search else "X" #X is added if pre and post seq flanking barcodes cannot be found 

#UPDATE barcode lengths and pre and post seq,
def tilebc_mapper(readfile, bc1_len=9, bc2_len=6, bc3_len=16, bc1_pre="GCTAGC", bc1_post="CTCGAG", bc2_pre="TGCTAT", bc2_post="GGCCGGCC", bc3_pre="AGGGCCCC", bc3_post="GCGGT"):
    sequences = []

    # Open file appropriately depending on compression
    open_func = gzip.open if readfile.endswith('.gz') else open
    mode = 'rt' if readfile.endswith('.gz') else 'r'

    with open_func(readfile, mode) as fin:
        for line in fin:
            if line.startswith('@'):
                seq = next(fin).strip()
                sequences.append(seq)

    barcode2_list, barcode2_lengths, bc2q_list = [], [], []
    bc1_list, barcode1_lengths, bc1q_list = [], [], []
    barcode3_list, bc3_lengths, barcode3q_list = [], [], []

    for read in sequences:
        
        barcode1 = getmid(read, bc1_pre, bc1_post)
        bc1_list.append(barcode1)
        barcode1_len = len(barcode1)
        barcode1_lengths.append(barcode1_len)
        bc1q_list.append(1 if barcode1_len == bc1_len else 0) #if wrong length = 0, if correct length = 1
        
        barcode2 = getmid(read, bc2_pre, bc2_post)
        barcode2_list.append(barcode2)
        barcode2_len = len(barcode2)
        barcode2_lengths.append(barcode2_len)
        bc2q_list.append(1 if barcode2_len == bc2_len else 0) #if wrong length = 0, if correct length = 1    
       
        barcode3 = getmid(read, bc3_pre, bc3_post)
        bc3_len_actual = len(barcode3)
        bc3_quality = 1 if bc3_len_actual == bc3_len else 0 #if wrong length = 0, if correct length = 1
        barcode3_list.append(barcode3)
        bc3_lengths.append(bc3_len_actual)
        barcode3q_list.append(bc3_quality)

#UPDATE names of the summary table if you don't like integration and tile related names
    tileBC_dict = {
        "Reads": sequences, 
        "BC1": bc1_list, 
        "BC1 Len": barcode1_lengths, 
        "BC1 Qual": bc1q_list,
        "BC2": barcode2_list, 
        "BC2 Len": barcode2_lengths, 
        "BC2 Qual": bc2q_list, 
        "BC3": barcode3_list,
        "BC3 Len": bc3_lengths,
        "BC3 Qual": barcode3q_list
    }
    tileBC_df = pd.DataFrame(tileBC_dict)
    tileBC_summary_dict = {
        'Category': [
            'Total Num of sequences',
            'Total Correct BC1 len',
            'Total Correct BC2 Len',
            'Total Correct BC3 len',
            'Total Correct BC1 and BC2 len'
            'Total Correct BC2 and BC3 len',
            'Total Correct BC1 and BC2 len',
            'Total Correct BC1, BC2, and BC3 len',
        ],
        'Read Count': [
            len(sequences),
            (tileBC_df["BC1 Qual"] == 1).sum(),
            (tileBC_df["BC2 Qual"] == 1).sum(),
            (tileBC_df["BC3 Qual"] == 1).sum(),
            ((tileBC_df["BC1 Qual"] == 1) & (tileBC_df["BC2 Qual"] == 1)).sum()
            ((tileBC_df["BC3 Qual"] == 1) & (tileBC_df["BC2 Qual"] == 1)).sum(),
            ((tileBC_df["BC3 Qual"] == 1) & (tileBC_df["BC1 Qual"] == 1)).sum(),
            ((tileBC_df["BC1 Qual"] == 1) & (tileBC_df["BC2 Qual"] == 1) & (tileBC_df["BC3 Qual"] == 1)).sum()
        ]
    }
    tileBC_summary_df = pd.DataFrame(tileBC_summary_dict)
    return tileBC_df, tileBC_summary_df

def analyze_map1_barcode2_len(map1_data, base_name):
    plt.hist(map1_data['BC2 Len'], bins=50)
    plt.title(f'{base_name} BC2 Len Map1')
    plt.xlim([0, 150])
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_BC2_Len_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_bc1_len(map1_data, base_name):
    plt.hist(map1_data['BC1 Len'], bins=50)
    plt.title(f'{base_name} BC1 Len Map1')
    plt.xlim([0, 15])
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_BC1_Len_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_barcode2_qual(map1_data, base_name):
    plt.hist(map1_data['BC2 Qual'], bins=50)
    plt.title(f'{base_name} BC2 Qual')
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_BC2_Qual_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_bc1_qual(map1_data, base_name):
    plt.hist(map1_data['BC1 Qual'], bins=50)
    plt.title(f'{base_name} BC1 Qual Map1')
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_BC1_Qual_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_bc3_qual(map1_data, base_name):
    plt.hist(map1_data['BC3 Qual'], bins=50)
    plt.title(f'{base_name} BC3 Qual Map1')
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_BC3_Qual_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_bc3_len(map1_data, base_name):
    plt.hist(map1_data['BC3 Len'], bins=50)
    plt.title(f'{base_name} BC3 Len Map1')
    plt.xlim([0, 15])
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_BC3_len_Map1.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def process_input_file(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    rawmap, summary = tilebc_mapper(input_file)
    
    f_path = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Map1.csv')
    rawmap.to_csv(f_path, index=False)
    
    #comment out if you dont want it to make the graphs
    analyze_map1_barcode2_len(rawmap, base_name)
    analyze_map1_bc1_len(rawmap, base_name)
    analyze_map1_barcode2_qual(rawmap, base_name)
    analyze_map1_bc1_qual(rawmap, base_name)
    analyze_map1_bc3_qual(rawmap, base_name)
    analyze_map1_bc3_len(rawmap, base_name)
    
    summary_dir = os.path.join(output_directory, 'summary')
    os.makedirs(summary_dir, exist_ok=True)
    summary_path = os.path.join(summary_dir, f'{base_name}_{Lib_Name}_summary_Map1.csv')
    summary.to_csv(summary_path, index=False)

    map1_nans = rawmap.replace(0, np.nan)
    map1_nans = rawmap[(rawmap["BC2 Qual"] == 1) & (rawmap["BC1 Qual"] == 1) & (rawmap["BC3 Qual"] == 1)] 
    map2 = map1_nans.dropna().reset_index().drop(columns=['index', 'Reads', 'BC2 Len', 'BC2 Qual', 'BC1 Len', 'BC1 Qual','BC3 Qual', 'BC3 Len'])
    #m2fp = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Map2.csv')
    #map2.to_csv(m2fp, index=False) #UPDATE can uncomment if you want map2 created but you dont use it for anything
    
    map3 = map2.copy()
    # Convert the columns to strings if necessary
    map3['BC2'] = map3['BC2'].astype(str)
    map3['BC1'] = map3['BC1'].astype(str)
    map3['BC3'] = map3['BC3'].astype(str)
    
    #adds additional columns added that concatenate 2 or 3 columns 
    #UPDATE I have specific names i give my concatenations (HA) to go with other code I have, change to something more meaningful if you want 
    map3['Cat'] = map3['BC1'].str.cat([map3['BC2'], map3['BC3']], sep='-') 
    map3['HA'] = map3['BC1'].str.cat([map3['BC2']], sep='-')
    map3['HAR'] = map3['BC1'].str.cat([map3['BC2'], map3['BC3']], sep='-')
    m3fp = os.path.join(output_directory, f'{base_name}_{Lib_Name}_Map3.csv')
    map3.to_csv(m3fp, index=False)

    del rawmap, map2, map3
    gc.collect()
    
process_input_file(args.input)



