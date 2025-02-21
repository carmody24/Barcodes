import pandas as pd
import gc
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import os
import re
import argparse

#################
#code to talk with comand line docs you input 
#create are parser
parser = argparse.ArgumentParser(description='Process input CSV')

#add arguments to the parser
parser.add_argument('-i', '--input', type=str, required=True, help='fastq file') 

parser.add_argument('-o', '--output', type=str, required=True, help='Raw data output file path')
    # Add an argument for the output file path. -o or --output specifies the argument name.
    # It's required (required=True), of type string (type=str), and has a help message.

#Parse the command-line arguments 
args = parser.parse_args()

#use the parsed arguments 

#UPDATE names 
#Global Variables
Lib_Name = 'Lib_1_'
Output_Directory = f'Map1_SSL1' #currently makes a folder in the directory you are already in 
os.makedirs(Output_Directory, exist_ok=True) #makes sure no problems if the dir already exists
# x = os.path.join(Output_Directory,f'L1SS_i{Lib_Name}_Map1.csv')



Map2_Summary_Dict = {
        'Category': [
            ],
            'Read Count':[
            ]
    }
# print(f'(Location of graphs for {Lib_Name} is: {Output_Directory})')
def getmid(seq, pre, post):
    # seq = the sequence to parse
    # pre = substring that precedes piece of interest
    # post = substring that follows piece of interest
    # returns piece of interest
    
    re_key = pre + "(.*)"+ post
    poi_search = re.search(re_key, seq)
#     print(poi_search)
    if poi_search is None:
        poi = "X"
    else:
        poi = poi_search.group(1)
    
    return poi

#UPDATE lengths and pre and post seq 
def tilebc_mapper(readfile, bc2_len = 6, bc1_len = 11, bc2_pre = "CTTCTGA", bc2_post = "GCTAGC", 
                  bc1_pre ="GCTAGC", bc1_post = "CTCGAGA"): 
    
    #readfile = file of SEQUENCES ONLY
    # *_pre or *_post = the consensus sequences before or after each feature

    # make lists of reads
    readlist = readfile

    sequences = []
    #fastq_file_path2 = map
    with open (readlist, 'r') as fin:
        print("opened file")

        for line in fin:
            if line.startswith('@'):
                seq = next(fin) #looks at the next line to get thee read seq
                seq = seq.strip() #clean read
                sequences.append(seq) #add cleaned seq to list 
    print(sequences[:5])
    print(f"Total number of sequences: {len(sequences)}")
   
            
    #make lists of tiles/BCs from list of reads
    int_list = []
    int_lengths= []
    intq_list = [] #tile quality list: 1 is good, 0 is bad
    
  
    adBC_list = []
    adBC_lengths = []
    aq_list = []
    rpBC_list = []
    rpBC_lengths = []
    rq_list = []
    
    for read in sequences:
        int = getmid(read, bc2_pre, bc2_post) #use consensus seq to find tile
        int_list.append(int) #add tile to list
        int_len = len(int) #find length of tile
        int_lengths.append(int_len) #add length to list
        if int_len == bc2_len: #check if the length matches expected length
            intq_list.append(1) # if yes
        else:
            intq_list.append(0) # if no
            
        
        adBC = getmid(read, bc1_pre, bc1_post)
        adBC_list.append(adBC)
        adBC_len = len(adBC)
        adBC_lengths.append(adBC_len)
        if adBC_len == bc1_len:
            aq_list.append(1)
        else:
            aq_list.append(0)
#        
            
    # make the df
    tileBC_dict = {"Reads":sequences, "Int_BC":int_list, "Int_BC Len" : int_lengths, "Int_BC Qual":intq_list, 
                   "AD BCs":adBC_list, "Tile_BC Len": adBC_lengths,"Tile_BC Qual": aq_list}
    tileBC_df = pd.DataFrame.from_dict(tileBC_dict)
    print(f'Total number of sequences Int_BC Qual =1: {(tileBC_df["Int_BC Qual"]==1).sum()}')
    print(f'Total number of sequences Tile_BC Qual =1: {(tileBC_df["Tile_BC Qual"]==1).sum()}')
    
    tileBC_summary_dict = {
        'Category': [
            'Total Num of sequences',
            'Total Correct Int BC Len',
            'Total Correct AD BC len',
            'Total Correct Int and AD BC len',
            ],
            'Read Count':[
                len(sequences),
                (tileBC_df["Int_BC Qual"] == 1).sum(),
                (tileBC_df["Tile_BC Qual"] == 1).sum(),
                ((tileBC_df["Tile_BC Qual"] == 1) & (tileBC_df["Int_BC Qual"] == 1)).sum(),
            ]
    }
    tileBC_summary_df = pd.DataFrame.from_dict(tileBC_summary_dict)

    return tileBC_df, tileBC_summary_df

# set up main code to be run

def main(input_file, output_csv):

    # process input file into raw df
    rawmap, summary = tilebc_mapper(input_file)

    # write the output file
    f_path = os.path.join(Output_Directory, output_csv)
    rawmap.to_csv(f_path, index=False)

    summary_dir = os.path.join(Output_Directory, 'summary')
    os.makedirs(summary_dir, exist_ok=True)
    summary_path = os.path.join(summary_dir, 'summary_' + output_csv)
    summary.to_csv( summary_path, index=False)

main(args.input, args.output)



