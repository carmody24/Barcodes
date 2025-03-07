import pandas as pd
import os
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import gc

# Create parser for command-line arguments
parser = argparse.ArgumentParser(description='Process Map1 CSV files from different sequencing replicates or libraries individuually.')
parser.add_argument('-i', '--input_dir', type=str, required=True, help='Input directory containing Map1 CSV files that you want to check for BC1 that are the correct length and Tile length of 0 for No Tile Control')

# Parse the command-line arguments
args = parser.parse_args()
input_directory = args.input_dir

# Define the output directory within the current directory
output_directory = os.path.join(os.getcwd(), 'Map3_Including_Not_In_Design_File')
os.makedirs(output_directory, exist_ok=True)

# Initialize a dictionary for the summary
summary_dict = {'Category': [], 'Read Count': []}

def process_replicate(file_path):
    Lib_Name = 'Not_in_Design_File'#UPDATE if you want  a different name for all files in the folder to contain
    base_name = os.path.splitext(os.path.basename(file_path))[0] #remainder of the name for the output file is based on the input file's name
    df = pd.read_csv(file_path)
    
    summary_dict['Category'].append(f'{base_name} Map1 Shape')
    summary_dict['Read Count'].append(df.shape[0])

    # Remove rows that have an 'X' in any of their cells
    # an X was previously added to columns where the pre and post sequences that flank the tile and/or BC1 weren't found in the read
    df = df[~df.isin(['X']).any(axis=1)]

    # Filter rows
    #UPDATE if you want diff parameters can filter by specifc length if you want 
    map2 = df[(df['T Qual'] == 1) & (df['A Qual'] == 1)]

    # Check columns to ensure 'Tiles' is present
    print(f"Columns after filtering for {base_name}:", df.columns)

    # Save Map2, you can save if you want but Map2 doesn't get used for anything 
    # map2_path = os.path.join(output_directory, f'{base_name}_Not_In_Design_File_Map2.csv')
    # map2.to_csv(map2_path, index=False)

    # Append Map1 shape information to summary dictionary
    summary_dict['Category'].append(f'{base_name} Map1 Shape with X Removed')
    summary_dict['Read Count'].append(df.shape[0])
    # Append Map1 shape information to summary dictionary
    summary_dict['Category'].append(f'{base_name} Map2 Shape')
    summary_dict['Read Count'].append(map2.shape[0])
    
    #delete df to save mem
    del df
    gc.collect()

    # Create Map3
    map3 = map2.drop(columns=['Reads', 'T Qual', 'A Qual', 'T Len', 'A Len'])
    print(f"Columns in map3 for {base_name}:", map3.columns)

    # Ensure 'Tiles' column is in map3, even if it is empty
    if 'Tiles' not in map3.columns:
        map3['Tiles'] = ''

    # Create 'Cat' column
    map3['Cat'] = map3['Tiles'] + '-' + map3['AD BCs']

    # Save Map3 including Not in Design File Tiles
    #map3_path = os.path.join(output_directory, f'{base_name}_Map3_with_NOT_in_Design.csv') #UPDATE if you want a csv file with all of the normal map3 components (T Qual ==1, A Qual == 1, Designed ==1) AND including Designed ==0 aka not in design file tiles but that are the correct length and have a bc1
    #map3.to_csv(map3_path, index=False)

    #save Map3 of Only the Not in Design File Tiles
    map3_filteredx = map3[map3['Designed'] == 0]
    #map3_pathx = os.path.join(output_directory, f'{base_name}_Map3_ONLY_NOT_in_Design.csv') #UPDATE if you want a csv of all rows Designed ==0 (even multiple of the same tile+bc1 combinations)
    #map3_filteredx.to_csv(map3_pathx, index=False)
    
    #LUT of only Unique Cat
    map3_filtered_unique =  map3_filteredx.drop_duplicates(subset='Cat')
    #add counts of each Cat 
    map3_filtered_unique['Cat_Count'] = map3_filteredx.groupby('Cat')['Cat'].transform('count')
    map3_ge5_unique_fpd = os.path.join(output_directory, f'{base_name}_Map3_ONLY_NOT_in_Design_LUT.csv') #UPDATE this gives you a csv output of only unique not in design file tiles + bc1 combinations
    map3_filtered_unique.to_csv(map3_ge5_unique_fpd, index=False)
    
    
    #delete map2 to save mem
    del map2
    gc.collect()

    # Calculate tbcov and tcov
    tbcov = map3['Cat'].value_counts().to_frame().reset_index()
    tcov = map3['Tiles'].value_counts().to_frame().reset_index()
    bccov = map3['AD BCs'].value_counts().to_frame().reset_index()
    
    # Count unique values in the Tiles column where Designed == 0 or 1
    tcov_designed_0 = map3.loc[map3['Designed'] == 0, 'Tiles'].nunique()
    tcov_designed_1 = map3.loc[map3['Designed'] == 1, 'Tiles'].nunique()

    #Count ADBC that appear in both the designed and not designed Tiles
    tiles_designed_0s = set(map3.loc[map3['Designed'] == 0, 'AD BCs'].unique())
    tiles_designed_1s = set(map3.loc[map3['Designed'] == 1, 'AD BCs'].unique())
    # Find the intersection (common elements in both lists)
    common_tiles = tiles_designed_0s.intersection(tiles_designed_1s)
    # Get the count of common unique tiles
    common_tiles_count = len(common_tiles)

    #Count Cat that appear in both the designed and not designed Tiles
    tcov_designed_0c = map3.loc[map3['Designed'] == 0, 'Cat'].nunique()
    tcov_designed_1c = map3.loc[map3['Designed'] == 1, 'Cat'].nunique()
        
    # Create summary
    # Append Map3 and unique count information to summary dictionary
    summary_dict['Category'].append(f'{base_name} Map3 Shape')
    summary_dict['Read Count'].append(map3.shape[0])
    summary_dict['Category'].append(f'{base_name} All Unique Tiles Count')
    summary_dict['Read Count'].append(tcov.shape[0])
    summary_dict['Category'].append(f'{base_name} Not in Design File Unique Tiles Count')
    summary_dict['Read Count'].append(tcov_designed_0)
    summary_dict['Category'].append(f'{base_name} In Design File Unique Tiles Count')
    summary_dict['Read Count'].append(tcov_designed_1)
    
    summary_dict['Category'].append(f'{base_name} All Unique Tile + BC Count')
    summary_dict['Read Count'].append(tbcov.shape[0])
    summary_dict['Category'].append(f'{base_name} Not in Design File Unique Tile + BC Count')
    summary_dict['Read Count'].append(tcov_designed_0c)
    summary_dict['Category'].append(f'{base_name} In Design File Unique Tile + BC Count')
    summary_dict['Read Count'].append( tcov_designed_1c)

    summary_dict['Category'].append(f'{base_name} All Unique AD BCs Count')
    summary_dict['Read Count'].append(bccov.shape[0])
    summary_dict['Category'].append(f'{base_name} Not in Design File Unique ADBCs Count')
    summary_dict['Read Count'].append(len(tiles_designed_0s))
    summary_dict['Category'].append(f'{base_name} In Design File Unique ADBCs Count')
    summary_dict['Read Count'].append(len(tiles_designed_1s))
    summary_dict['Category'].append(f'{base_name} ADBCs Overlap in Designed and Not Designed Count')
    summary_dict['Read Count'].append(common_tiles_count)

    
    #delete to save mem
    del map3, tbcov, tcov
    gc.collect()

# Loop through each .csv file in the input directory 
#can have many files in the directory or one, all will be processes seperately
for file in os.listdir(input_directory):
    if file.endswith('.csv'):
        file_path = os.path.join(input_directory, file)
        process_replicate(file_path)

# Convert the summary dictionary to a DataFrame
summary_df = pd.DataFrame.from_dict(summary_dict)

# Save the combined summary to a CSV file
summary_path = os.path.join(output_directory, 'Summary_Not_In_Design_File.csv')
summary_df.to_csv(summary_path, index=False)
print('Finished processing all replicates.')