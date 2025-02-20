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
output_directory = os.path.join(os.getcwd(), 'No_Tile_Map3_Output')
os.makedirs(output_directory, exist_ok=True)

# Initialize a dictionary for the summary
summary_dict = {'Category': [], 'Read Count': []}

def process_replicate(file_path):
    Lib_Name = 'No_Tile_Control'#UPDATE if you want  a different name for all files in the folder to contain
    base_name = os.path.splitext(os.path.basename(file_path))[0] #remainder of the name for the output file is based on the input file's name
    df = pd.read_csv(file_path)

    # Remove rows that have an 'X' in any of their cells
    # an X was previously added to columns where the pre and post sequences that flank the tile and/or BC1 weren't found in the read
    df = df[~df.isin(['X']).any(axis=1)]

    # Filter rows
    #UPDATE the BC1 length to the correct length, the tile length should always be 0 if looking for No Tile controls 
    map2 = df[(df['T Len'] == 0) & (df['A Len'] == 11)]

    # Check columns to ensure 'Tiles' is present
    print(f"Columns after filtering for {base_name}:", df.columns)

    # Save Map2, you can save if you want but Map2 doesn't get used for anything 
    # map2_path = os.path.join(output_directory, f'{base_name}_No_Tile_Control_Map2.csv')
    # map2.to_csv(map2_path, index=False)

    # Append Map1 shape information to summary dictionary
    summary_dict['Category'].append(f'{base_name} Map1 Shape')
    summary_dict['Read Count'].append(df.shape[0])
    # Append Map1 shape information to summary dictionary
    summary_dict['Category'].append(f'{base_name} Map2 Shape')
    summary_dict['Read Count'].append(map2.shape[0])

    #delete df to save mem
    del df
    gc.collect()

    # Create Map3
    map3 = map2.drop(columns=['Reads', 'T Qual', 'A Qual', 'T Len', 'Designed', 'A Len'])
    print(f"Columns in map3 for {base_name}:", map3.columns)

    # Ensure 'Tiles' column is in map3, even if it is empty
    if 'Tiles' not in map3.columns:
        map3['Tiles'] = ''

    # Create 'Cat' column
    map3['Cat'] = map3['Tiles'] + '-' + map3['AD BCs']

    # Modify 'Tiles' column to replace empty values with 'NoADC'
    # NoADC is No Activation Domain Control I add something to the no tile control rows so it is easier in the future where sometimes functions cause rows with nothing in it are dropped
    map3['Tiles'] = map3['Tiles'].replace('', 'NoADC')

    # Save Map3
    map3_path = os.path.join(output_directory, f'{base_name}_No_Tile_Control_Map3.csv')
    map3.to_csv(map3_path, index=False)

    #delete map2 to save mem
    del map2
    gc.collect()

    # Calculate tbcov and tcov
    tbcov = map3['Cat'].value_counts().to_frame().reset_index()
    tcov = map3['Tiles'].value_counts().to_frame().reset_index()

    # Create summary
    # Append Map3 and unique count information to summary dictionary
    summary_dict['Category'].append(f'{base_name} Map3 Shape')
    summary_dict['Read Count'].append(map3.shape[0])
    summary_dict['Category'].append(f'{base_name} Unique Tiles Count')
    summary_dict['Read Count'].append(tcov.shape[0])
    summary_dict['Category'].append(f'{base_name} Unique Tile + BC Count')
    summary_dict['Read Count'].append(tbcov.shape[0])

    # Generate graphs
    #The graphs have uf or Unfiltered because in future steps these graphs will be made but have minimum read count filters done before 
    
    #normal axis scale
    def analyze_tcov_nom(map3_data, name):
        sns.histplot(x='count', data=map3_data, bins=50)
        plt.title(f'{Lib_Name} {name} Unique Tile Coverage Unfiltered')
        f_path = os.path.join(output_directory, f'{Lib_Name}_{name}_Tcov_uf_Map3.jpg')
        plt.savefig(f_path, format='jpeg')
        plt.clf()
    #exponential scale axis
    def analyze_tbcov_exp(map3_data, name):
        sns.histplot(data=map3_data, x='count', log_scale=(True, True), bins=50)
        plt.title(f'{Lib_Name} {name} Unique Tile + BC Coverage Unfiltered')
        f_path = os.path.join(output_directory, f'{Lib_Name}_{name}_TBcov_exp_uf_Map3.jpg')
        plt.savefig(f_path, format='jpeg')
        plt.clf()

    # Call the graph functions with the calculated tcov and tbcov
    analyze_tcov_nom(tcov, base_name)
    analyze_tbcov_exp(tbcov, base_name)

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
summary_path = os.path.join(output_directory, 'Summary_No_Tile_Control.csv')
summary_df.to_csv(summary_path, index=False)
print('Finished processing all replicates.')
