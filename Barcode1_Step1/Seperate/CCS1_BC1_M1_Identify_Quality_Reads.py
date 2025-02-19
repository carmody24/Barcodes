# import packages

import re
import pandas as pd
import time
import argparse
import os
############################
#UPDATE the libray name sometimes I add the index number if processing multiple seq reps with diff indexes
#Global Variables 
Lib_Name = 'Lib_1_i30' #name you want to be at the start of the files 
Output_Directory = f'{Lib_Name}_Map1' #currently makes a folder in the directory you are already in 
os.makedirs(Output_Directory, exist_ok=True) #makes sure no problems if the dir already exists

# define needed functions for data processing
#UPDATE the left and right replace seq with the sequences that flank your designed tiles, ususally the primer added seq so they are properly extracted from the design file
def find_designed(des):
    """ takes a file where every line is a designed tile and creates a lookup dictionary of all designed tiles """
    dt = [] # initialize a list of designed tiles from design file
    with open(des, 'r') as f_des:
        # open the design file for reading
        for line in f_des:
            leftReplace = line.replace("CCCAGCTTAAGCCACCATG","")
            rightReplace = leftReplace.replace("gGATCCGAGCTCGCTAGC\n","")
            dt.append(rightReplace) #add tile to list without whitespace
    
    dt_dict = {} # initialize dictionary to lookup tiles in
    for i in dt:
        dt_dict[i] = 1 # add tiles into a diction ary
        
    print('Number of designed tiles:', len(dt_dict)) 

    return dt_dict

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

#UPDATE the below definition with the  correct Tile length (t_len), correct BC1 length (a_len), and sequences pre and post tile and BC1.
def tilebc_mapper(readfile,dtd, t_len = 120, a_len = 11, tile_pre = "CACCATG", tile_post = "GGATCCG", 
                  adBC_pre = "CGCTAGC", adBC_post = "CTCGAGA"): 
                  #rpBC_pre = "GCTCGAG", rpBC_post = "GGCC...CAT"):
    
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
    tile_list = []
    tile_lengths= []
    tq_list = [] #tile quality list: 1 is good, 0 is bad
    
    des_query = [] # tells us if tile matches design or not
    
    adBC_list = []
    adBC_lengths = []
    aq_list = []
    rpBC_list = []
    rpBC_lengths = []
    rq_list = []
    
    for read in sequences:
        tile = getmid(read, tile_pre, tile_post) #use consensus seq to find tile
        tile_list.append(tile) #add tile to list
        tile_len = len(tile) #find length of tile
        tile_lengths.append(tile_len) #add length to list
        if tile_len == t_len: #check if the length matches expected length
            tq_list.append(1) # if yes
        else:
            tq_list.append(0) # if no
            
        if tile in dtd:
            des_query.append(1)
        else:
            des_query.append(0)
#         print(tile)
        
        adBC = getmid(read, adBC_pre, adBC_post)
        adBC_list.append(adBC)
        adBC_len = len(adBC)
        adBC_lengths.append(adBC_len)
        if adBC_len == a_len:
            aq_list.append(1)
        else:
            aq_list.append(0)
#         print(adBC)

        #rpBC = getmid(read, rpBC_pre, rpBC_post)
        #rpBC_list.append(rpBC)
        #rpBC_len = len(rpBC)
        #rpBC_lengths.append(rpBC_len)
        #if rpBC_len == 14:
            #rq_list.append(1)
       #else:
            #rq_list.append(0)
            
    # make the df
    
    tileBC_dict = {"Reads":sequences, "Tiles":tile_list, "T Len" : tile_lengths, "T Qual":tq_list, "Designed": des_query, 
                  "AD BCs":adBC_list, "A Len": adBC_lengths,"A Qual": aq_list}
    tileBC_df = pd.DataFrame.from_dict(tileBC_dict)
    #print(f"Total number of sequences T Qual =1: {(tileBC_df['T Qual']==1).sum()}")
    #print(f"Total number of sequences A Qual =1: {(tileBC_df['A Qual']==1).sum()}")
    #print(f"Total number of sequences in Design file: {(tileBC_df['Designed']==1).sum()}")
    #print(f"Total number of sequences T Qual and A Qual =1: {((tileBC_df['T Qual']==1) & (tileBC_df['A Qual']==1)).sum()}")
    #print(f"Total number of sequences T Qual and A Qual =1 and in Design file: {((tileBC_df['T Qual']==1) & (tileBC_df['Designed']==1) & (tileBC_df['A Qual']==1)).sum()}")
    
    tileBC_summary_dict = {
        'Category': [
            'Total Num of sequences',
            'Total Correct Tiles',
            'Total Correct BC',
            'Total Correct Designed',
            'Total Correct Tile & BC',
            'Total Correct Tile, BC, and Designed',
            'Total Num of Designed Tiles'
            ],
            'Read Count':[
                len(sequences),
                (tileBC_df['T Qual'] == 1).sum(),
                (tileBC_df['A Qual'] == 1).sum(),
                (tileBC_df['Designed'] == 1).sum(),
                ((tileBC_df['T Qual'] == 1) & (tileBC_df['A Qual'] == 1)).sum(),
                ((tileBC_df['T Qual'] == 1) & (tileBC_df['Designed'] == 1) & (tileBC_df['A Qual'] == 1)).sum(),
                len(dtd)
            ]
    }
    tileBC_summary_df = pd.DataFrame.from_dict(tileBC_summary_dict)

    return tileBC_df, tileBC_summary_df

# set up main code to be run

def main(input_file, design_file):
    # get list of designed tiles
    designed_tile_dictionary = find_designed(design_file)

    # process input file into raw df
    rawmap, summary = tilebc_mapper(input_file,designed_tile_dictionary)

    # write the output file
    f_path = os.path.join(Output_Directory,f'{Lib_Name}_Map1.csv')
    rawmap.to_csv(f_path, index=False)

    summary_dir = os.path.join(Output_Directory, 'summary')
    os.makedirs(summary_dir, exist_ok=True)
    summary_path = os.path.join(summary_dir, f'{Lib_Name}_Summary.csv')
    summary.to_csv(summary_path, index=False)

if __name__ == "__main__":
    
    # Create ArgumentParser object with a description
    parser = argparse.ArgumentParser(description='Build Tile-BC map from step1 fastq file')

    # Add arguments to the parser
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path, fastq file of paired reads from BC1 Step1')

    parser.add_argument('-d', '--design', type=str, required=True, help='Design txt file (each line in file is a designed tile) path')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.input, args.design)

  
