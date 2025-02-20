import pandas as pd
import gc
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

#################
#code to talk with comand line docs you input 
#create are parser
parser = argparse.ArgumentParser(description='Process input CSV to remove low quality reads that don't have correct tile length, BC1 length, and/or design file match.')

#add arguments to the parser
parser.add_argument('-i', '--input', type=str, required=True, help='Input CSV file path of Map1 created from CCS1_BC1_M1_Identify_Quality_Reads') 

#Parse the command-line arguments 
args = parser.parse_args()

#use the parsed arguments 
File_From_Human_Step1_Map1 = args.input 

######################
#UPDATE variables based on your naming preferences
#Global Variables 
Fig_Format = 'jpeg' #file format you want all the graphs to be saved
Lib_Name = 'Lib_1_i30' #name you want to be at the start of the files 
Output_Directory = f'{Lib_Name}_Map3' #currently makes a folder in the directory you are already in 
os.makedirs(Output_Directory, exist_ok=True) #makes sure no problems if the dir already exists


Map2_Summary_Dict = {
        'Category': [
            ],
            'Read Count':[
            ]
    }

#############################################
#read in raw df to Make Map1 
map1 = pd.read_csv(File_From_Human_Step1_Map1)

#add info to summary dict
Map2_Summary_Dict['Category'].append('Map1 Shape (should be same as total seq)')
Map2_Summary_Dict['Read Count'].append(map1.shape[0])
# map1.head(5)

################################################################
#create Map2 (only have Tiles and BC columns)
#Replace all 0s in map1 with NaN to filter out any Qual=0 reads
map1_nans = map1.replace(0, np.nan)
# map1_nans.head()
map2 = map1_nans.dropna().reset_index()
#get rid of some now useless columns
clabels = ['index','Reads', 'T Len','T Qual', 'Designed', 'A Len','A Qual']
map2 = map2.drop(clabels, axis = 1)

#convert to csv and read in for the creation of map3 to save on memory 
m2fp = os.path.join(Output_Directory,f'{Lib_Name}_Map2.csv')
map2.to_csv( m2fp, index=False)

#delete maps to save mem
del map1, map2
gc.collect()

#########################################################
#Create Map3 (Tiles, BC, and Cat (tile - BC))
#read in map
map3 = pd.read_csv(m2fp)
# map3.head()

adcol = map3['AD BCs'].copy()

map3['Cat'] = map3['Tiles'].str.cat(adcol, sep="-")

#add info to summary dict
Map2_Summary_Dict['Category'].append('Map3 Shape (should be same as Total Correct T,BC,Des)')
Map2_Summary_Dict['Read Count'].append(map3.shape[0])

#save map3 as csv 
m3fp = os.path.join(Output_Directory,f'{Lib_Name}_Map3.csv')
map3.to_csv(m3fp,index=False)

#################################################

############################
#dictionary that will save quality checkpoint outputs and tbc count that you will need for loss table 
Map2_Summary_Dict_df = pd.DataFrame.from_dict(Map2_Summary_Dict)

#Summary Table creation 
sum_f_p = os.path.join(Output_Directory, f'{Lib_Name}_Summary_CCS2_BC1.csv')
Map2_Summary_Dict_df.to_csv(sum_f_p, index=False)


print('Everything Finished')


















