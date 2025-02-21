import re
import pandas as pd
import numpy as np
import os
import argparse
import gc
import matplotlib.pyplot as plt
import seaborn as sns

#UPDATE names based on you lib and preferences and what file type you want your figures to be saved
# Global Variables
Lib_Name = 'Lib_1_i'
Output_Directory = f'{Lib_Name}_CCS1_2_5_BC1_Maps_and_Graphs'
os.makedirs(Output_Directory, exist_ok=True)
Fig_Format = 'jpeg'

# Define needed functions for data processing

def find_designed(des):
    """Creates a lookup dictionary of all designed tiles from a file."""
    dt = []
    with open(des, 'r') as f_des:
        for line in f_des:
            leftReplace = line.replace("CCCAGCTTAAGCCACCATG", "") #UPDATE to match seq flanking your tiles in the design file, usually primer homology extensions
            rightReplace = leftReplace.replace("gGATCCGAGCTCGCTAGC\n", "") #UPDATE to match seq flanking your tiles in the design file, usually primer homology extensions
            dt.append(rightReplace.strip())
    return {tile: 1 for tile in dt}

def getmid(seq, pre, post):
    """Extracts the sequence between pre and post substrings."""
    match = re.search(f"{pre}(.*){post}", seq)
    return match.group(1) if match else "X" #puts and X if the pre and/or post seq cannot be found 

def tilebc_mapper(readfile, dtd, t_len=120, bc1_len=11, tile_pre="CACCATG", tile_post="GGATCCG",
                  adBC_pre="CGCTAGC", adBC_post="CTCGAGA"):  #UPDATE you need to change the correct tile length (t_len)and BC1 length (bc1_len) and the pre and post sequences flanking them
    """Processes input sequences to map tiles and barcodes."""  
    
    # Lists to store extracted data  
    tile_list, tile_lengths, tq_list, des_query = [], [], [], []  
    adBC_list, adBC_lengths, aq_list = [], [], []  
    total_sequences = 0  # Track the number of reads processed  

    with open(readfile, 'r') as fin:  # Reads paired fastq file and extracts the reads  
        for line in fin:  
            if line.startswith('@'):  # Identifies the sequence header  
                seq = next(fin).strip()  # Reads the actual sequence  
                total_sequences += 1  

                # Identify Tile and BC1 based on pre and post sequences and check length  
                tile = getmid(seq, tile_pre, tile_post)  
                tile_len = len(tile)  
                tile_quality = 1 if tile_len == t_len else 0  # Quality column given 1 if length matches expected length, otherwise 0  
                tile_is_designed = 1 if tile in dtd else 0  # Checks if the tile is in the design dictionary  

                adBC = getmid(seq, adBC_pre, adBC_post)  
                adBC_len = len(adBC)  
                adBC_quality = 1 if adBC_len == bc1_len else 0  # Quality column for BC1, 1 if length matches expected length otherwise 0  

                # Store extracted values  
                tile_list.append(tile)  
                tile_lengths.append(tile_len)  
                tq_list.append(tile_quality)  
                des_query.append(tile_is_designed)  

                adBC_list.append(adBC)  
                adBC_lengths.append(adBC_len)  
                aq_list.append(adBC_quality)  

    # Create DataFrame containing all extracted information  
    tileBC_df = pd.DataFrame({  
        "Tiles": tile_list,  
        "T Len": tile_lengths,  
        "T Qual": tq_list,  
        "Designed": des_query,  
        "AD BCs": adBC_list,  
        "A Len": adBC_lengths,  
        "A Qual": aq_list  
    })  

    # Summary table is initialized  
    tileBC_summary_df = pd.DataFrame({  
        'Category': [  
            'Total Num of sequences',  # Total number of reads processed  
            'Total Correct Tiles',  # Reads with tile length matching expected length  
            'Total Correct BC',  # Reads with BC1 length matching expected length  
            'Total Correct Designed',  # Reads with tile sequence found in design file  
            'Total Correct Tile & BC',  # Reads with both correct tile and BC1 length  
            'Total Correct Tile, BC, and Designed',  # Reads that match expected tile length, BC1 length, and are in the design file  
            'Total Num of Designed Tiles'  # Total unique tiles present in the design file  
        ],  
        'Read Count': [  
            total_sequences,  # Count of total sequences  
            (tileBC_df['T Qual'] == 1).sum(),  # Count of correctly sized tiles  
            (tileBC_df['A Qual'] == 1).sum(),  # Count of correctly sized BC1s  
            (tileBC_df['Designed'] == 1).sum(),  # Count of tiles found in design file  
            ((tileBC_df['T Qual'] == 1) & (tileBC_df['A Qual'] == 1)).sum(),  # Count of reads with correct tile & BC1  
            ((tileBC_df['T Qual'] == 1) & (tileBC_df['Designed'] == 1) & (tileBC_df['A Qual'] == 1)).sum(),  # Count of fully correct reads  
            len(dtd)  # Total number of designed tiles  
        ]  
    })  

    return tileBC_df, tileBC_summary_df  


#Graphs of Tile and BC1 length and quality based on information collected above that is later convert to Map1 
def analyze_map1_T_len(map1_data):
    plt.hist(map1_data['T Len'], bins=50)
    plt.title(f'{Lib_Name} T Length Map1')
    plt.xlim([0, 150])
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_T_Length_Map1.{Fig_Format}')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_map1_bc1_len(map1_data1):
    plt.hist(map1_data1['A Len'], bins=50)
    plt.title(f'{Lib_Name} BC Length Map1')
    plt.xlim([0, 15])
    f_path1 = os.path.join(Output_Directory, f'{Lib_Name}_bc1_length_Map1.{Fig_Format}')
    plt.savefig(f_path1, format=Fig_Format)
    plt.clf()
    
def analyze_map1_T_qual(map1_data2):
    plt.hist(map1_data2['T Qual'], bins=50)
    plt.title(f'{Lib_Name} T Qual Map1')
    f_path2 = os.path.join(Output_Directory, f'{Lib_Name}_T_Qual_Map1.{Fig_Format}')
    plt.savefig(f_path2, format=Fig_Format)
    plt.clf()

def analyze_map1_A_qual(map1_data3):
    plt.hist(map1_data3['A Qual'], bins=50)
    plt.title(f'{Lib_Name} BC Qual Map1')
    f_path3 = os.path.join(Output_Directory, f'{Lib_Name}_A_Qual_Map1.{Fig_Format}')
    plt.savefig(f_path3, format=Fig_Format)
    plt.clf()

#Graphs of coverage of Unique combinations of Tile + BC1 and of Unique Tile coverage based on Map3 (Map1 filtered to only keep rows with correct length of tile and BC1 and tile must be in design file)
#uf or unfiltered is added to these graphs names becuase in later step these graphs will be made again but with filtered data
def analyze_tcov_nom(map3_data):
    sns.histplot(x='count', data=map3_data, bins=100)
    plt.title(f'{Lib_Name} Unique Tile Coverage Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_Tcov_uf_Map3.{Fig_Format}')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_tcov_exp(map3_data):
    sns.histplot(x='count', data=map3_data, log_scale=(True, True), bins=100)
    plt.title(f'{Lib_Name} Unique Tile Coverage Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_Tcov_uf_exp_Map3.{Fig_Format}')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_tbcov_exp(map3_data):
    sns.histplot(data=map3_data, x='count', log_scale=(True, True), bins=100)
    plt.title(f'{Lib_Name} Unique Tile + BC Coverage Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_TBcov_exp_uf_Map3.{Fig_Format}')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def process_maps(input_file, design_file):
    designed_tile_dict = find_designed(design_file)
    rawmap, tileBC_summary = tilebc_mapper(input_file, designed_tile_dict)

    rawmap.to_csv(os.path.join(Output_Directory, f'{Lib_Name}_Map1.csv'), index=False)

    # Create Map2
    map1 = rawmap.replace(0, np.nan).dropna().reset_index()
    map1.drop(columns=['index', 'Reads', 'T Len', 'T Qual', 'Designed', 'A Len', 'A Qual'], inplace=True) #drop rows that won't be used for anything
    #map1.to_csv(os.path.join(Output_Directory, f'{Lib_Name}_Map2.csv'), index=False) #UPDATE uncomment if you want map2 csv to be created. It isn't used for anything specifically and will be a large file.

    # Create Map3
    map3 = map1.copy()
    map3['Cat'] = map3['Tiles'] + '-' + map3['AD BCs'] #add row that links the tile with the BC1 directly
    map3.to_csv(os.path.join(Output_Directory, f'{Lib_Name}_Map3.csv'), index=False) #this is the map you will use in next steps 
    
    # Combine summaries
    combined_summary = pd.concat([tileBC_summary, pd.DataFrame({
        'Category': ['Map1 Shape', 'Map3 Shape'],
        'Read Count': [rawmap.shape[0], map3.shape[0]]
    })])

    # Analyze Map1
    analyze_map1_T_len(rawmap)
    analyze_map1_bc1_len(rawmap)
    analyze_map1_T_qual(rawmap)
    analyze_map1_A_qual(rawmap)
   

    # Delete Map1 to save memory
    del rawmap, map1
    gc.collect()

    # Tile coverage
    tcov = map3['Tiles'].value_counts().to_frame().reset_index()
    combined_summary = pd.concat([combined_summary, pd.DataFrame({
        'Category': ['Unique Tiles Count'],
        'Read Count': [tcov.shape[0]]
    })])
    
    # Tile + BC coverage
    tbcov = map3['Cat'].value_counts().to_frame().reset_index()
    combined_summary = pd.concat([combined_summary, pd.DataFrame({
        'Category': ['Unique Tile + BC Count'],
        'Read Count': [tbcov.shape[0]]
    })])
    
    # Save combined summary
    combined_summary.to_csv(os.path.join(Output_Directory, f'{Lib_Name}_CCS1_2_5_BC1_Summary.csv'), index=False)

    # Analyze Map3
    analyze_tbcov_exp(tbcov)
    analyze_tcov_exp(tcov)
    analyze_tcov_nom(tcov)

    print('Finished with everything')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine and optimize scripts.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input paired seq file path')
    parser.add_argument('-d', '--design', type=str, required=True, help ='Input design file')
    args = parser.parse_args()
    process_maps(args.input, args.design)
