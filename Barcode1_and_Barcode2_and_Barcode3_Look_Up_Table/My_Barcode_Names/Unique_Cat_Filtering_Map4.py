import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
import gc

############################
# Create parser for command-line arguments
#input is a directory incase you want to subject multiple map4 files to the same thresholding (sometimes I do merge and intersect map4 at same time)
parser = argparse.ArgumentParser(description='Process input CSV files and perform filtering and analysis.')
parser.add_argument('-i', '--input_dir', type=str, required=True, help='Input directory containing map4 CSV files')

# Parse the command-line arguments 
args = parser.parse_args()

# Use the parsed arguments 
input_directory = args.input_dir

# Extract the base name of the input directory
base_name = os.path.basename(input_directory.rstrip('/'))

#UPDATE names if you want 
# Global Variables
Lib_Name = 'TL4S1'
Fig_Format = 'jpeg'
Thres_TBcov = 5 #UPDATE to the read min threshold you want = critical 

# Define the output directory within the current directory
output_directory = os.path.join(os.getcwd(), f'{Lib_Name}_{base_name}_filtered_map4_unique_Cat')
os.makedirs(output_directory, exist_ok=True)

# Define the summary directory within the output directory
summary_dir = os.path.join(output_directory, f'{Lib_Name}_filtered_map4_summary')
os.makedirs(summary_dir, exist_ok=True)

def process_map4_file(file_path):
    Map4_Summary_Dict = {
        'Category': [],
        'Read Count': []
    }

    base_name = os.path.splitext(os.path.basename(file_path))[0] #naming of output file based on input file name
    
    # Load map4 file
    map4 = pd.read_csv(file_path)

    ### add inintal counts to summary table 
    # Add info to summary dict
    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append('Initial Individual Counts')

    Map4_Summary_Dict['Category'].append('Initial Map4 Unique Cat')
    Map4_Summary_Dict['Read Count'].append(map4.shape[0])
    
    # Count unique Tiles initially
    initial_unique_adbc2 = map4['ADBC2'].nunique()
    Map4_Summary_Dict['Category'].append('Initial Unique ADBC2')
    Map4_Summary_Dict['Read Count'].append(initial_unique_adbc2)

    # Count unique Tiles initially
    initial_unique_hawk = map4['HawkBCs'].nunique()
    Map4_Summary_Dict['Category'].append('Initial Unique HawkBCs')
    Map4_Summary_Dict['Read Count'].append(initial_unique_hawk)

    # Count unique Tiles initially
    initial_unique_rtbc = map4['RTBC'].nunique()
    Map4_Summary_Dict['Category'].append('Initial Unique RTBC')
    Map4_Summary_Dict['Read Count'].append(initial_unique_rtbc)
    
    # Count unique Tiles initially
    initial_unique_ha = map4['HA'].nunique()
    Map4_Summary_Dict['Category'].append('Initial Unique HA')
    Map4_Summary_Dict['Read Count'].append(initial_unique_ha)

    # Unique RTBC per HA 
    rtbc_per_ha = map4.groupby('HA')['RTBC'].nunique()
    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(rtbc_per_ha, bins=range(1, rtbc_per_ha.max() + 2), edgecolor='black')
    plt.title('Initial Histogram of Unique RTBCs per HA')
    plt.xlabel('Number of Unique RTBCs')
    plt.ylabel('Number of HA Entries')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_uniRTBCperHA_cov_initial.{Fig_Format}'))
    plt.clf()
    
    # add summary stats to summary table
    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append('Initial Unique RTBC per HA')

    Map4_Summary_Dict['Category'].append('Min')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_ha.min()}')

    Map4_Summary_Dict['Category'].append('Max')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_ha.max()}')

    Map4_Summary_Dict['Category'].append('Median')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_ha.median()}')
    
    Map4_Summary_Dict['Category'].append('Mean')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_ha.mean():.2f}')
   

    # Unique HA per RTBC  
    ha_per_rtbc = map4.groupby('RTBC')['HA'].nunique()
    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(ha_per_rtbc, bins=range(1, ha_per_rtbc.max() + 2), edgecolor='black')
    plt.title('Initial Histogram of Unique HA per RTBC')
    plt.xlabel('Number of Unique HA Values')
    plt.ylabel('Number of RTBC Entries')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_uniHAperRTBC_cov_initial.{Fig_Format}'))
    plt.clf()
    
    #Cat_Cov
    plt.figure(figsize=(8,6))
    plt.hist(map4['Cat_Count'], bins=50, edgecolor='black')  # adjust bins as needed
    plt.xlabel("Cat_Count", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title("Initial Histogram of Cat_Count", fontsize=14)
    plt.yscale("linear")  # change to "log" if you want log scale
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_cat_count_hist_initial.{Fig_Format}'))
    plt.clf()
    
    

    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append('Initial Unique HA per RTBC')

    Map4_Summary_Dict['Category'].append('Min')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc.min()}')

    Map4_Summary_Dict['Category'].append('Max')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc.max()}')

    Map4_Summary_Dict['Category'].append('Median')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc.median()}')
    
    Map4_Summary_Dict['Category'].append('Mean')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc.mean():.2f}')

    # Filter out rows where one RTBC maps to multiple HA but will keep if 90% of the times the RTBC appears it is with 1 HA
    THRESH = 0.9  # UPDATE if you want a stronger or weaker filter

    # total Cat_Count per RTBC-HA
    rtbc_ha_counts = map4.groupby(['RTBC', 'HA'])['Cat_Count'].sum().reset_index(name='count')
    # fraction each HA represents for its RTBC
    rtbc_ha_counts['frac'] = rtbc_ha_counts['count'] / rtbc_ha_counts.groupby('RTBC')['count'].transform('sum')
    # per-RTBC stats
    max_frac_per_rtbc = rtbc_ha_counts.groupby('RTBC')['frac'].max()        # top HA fraction per RTBC
    unique_ha_per_rtbc = map4.groupby('RTBC')['HA'].nunique()               # how many distinct HAs each RTBC maps to
    # identify RTBCs to remove:
    #    condition = maps to >1 HA AND no HA reaches the THRESH
    rtbcs_to_remove = max_frac_per_rtbc[(unique_ha_per_rtbc.loc[max_frac_per_rtbc.index] > 1) &
                                        (max_frac_per_rtbc < THRESH)].index
    # all HAs associated with those RTBCs
    has_to_remove = map4.loc[map4['RTBC'].isin(rtbcs_to_remove), 'HA'].unique()
    # final filtered dataframe: drop rows where RTBC is bad OR HA is one of those HAs
    map4_filtered_weak = map4[~map4['RTBC'].isin(rtbcs_to_remove) & ~map4['HA'].isin(has_to_remove)].copy()

    ha_per_rtbc_filtered_w = map4_filtered_weak.groupby('RTBC')['HA'].nunique()
    #they should all equal 1 because the graph is made after filtering so that all RTBC should have a unique HA
    plt.figure(figsize=(10, 6))
    plt.hist(ha_per_rtbc_filtered_w, bins=range(1, ha_per_rtbc_filtered_w.max() + 2), edgecolor='black')
    plt.title(f'Histogram of Unique HA per RTBC Filtered {THRESH}%')
    plt.xlabel('Number of Unique HA Values')
    plt.ylabel('Number of RTBC Entries')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_uniHAperRTBC_cov_filtered_{THRESH}.{Fig_Format}'))
    plt.clf()

    rtbc_per_hat_filtered_w = map4_filtered_weak.groupby('HA')['RTBC'].nunique()
    plt.figure(figsize=(10, 6))
    plt.hist(rtbc_per_hat_filtered_w, bins=range(1, rtbc_per_hat_filtered_w.max() + 2), edgecolor='black')
    plt.title(f'Histogram of Unique RTBCs per HA Filtered {THRESH}%')
    plt.xlabel('Number of Unique RTBCs')
    plt.ylabel('Number of HA Entries')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_uniRTBCperHA_cov_filtered_{THRESH}.{Fig_Format}'))

    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append(f'Unique RTBC per HA {THRESH}% Filter')

    Map4_Summary_Dict['Category'].append('Min')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_hat_filtered_w.min()}')

    Map4_Summary_Dict['Category'].append('Max')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_hat_filtered_w.max()}')

    Map4_Summary_Dict['Category'].append('Median')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_hat_filtered_w.median()}')
    
    Map4_Summary_Dict['Category'].append('Mean')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_hat_filtered_w.mean():.2f}')


    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append(f'Unique HA per RTBC {THRESH}% Filter')

    Map4_Summary_Dict['Category'].append('Min')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc_filtered_w.min()}')

    Map4_Summary_Dict['Category'].append('Max')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc_filtered_w.max()}')

    Map4_Summary_Dict['Category'].append('Median')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc_filtered_w.median()}')
    
    Map4_Summary_Dict['Category'].append('Mean')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc_filtered_w.mean():.2f}')


    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append(f'After {THRESH}% Match Filter Individual Counts')

    Map4_Summary_Dict['Category'].append('Unique Cat Read Count')
    Map4_Summary_Dict['Read Count'].append(map4_filtered_weak.shape[0])
    
    # Count unique Tiles initially
    initial_unique_adbc2_2w = map4_filtered_weak['ADBC2'].nunique()
    Map4_Summary_Dict['Category'].append('Unique ADBC2')
    Map4_Summary_Dict['Read Count'].append(initial_unique_adbc2_2w)

    # Count unique Tiles initially
    initial_unique_hawk2w = map4_filtered_weak['HawkBCs'].nunique()
    Map4_Summary_Dict['Category'].append('Unique HawkBCs')
    Map4_Summary_Dict['Read Count'].append(initial_unique_hawk2w)

    # Count unique Tiles initially
    initial_unique_rtbc2w = map4_filtered_weak['RTBC'].nunique()
    Map4_Summary_Dict['Category'].append('Unique RTBC')
    Map4_Summary_Dict['Read Count'].append(initial_unique_rtbc2w)
    
    # Count unique Tiles initially
    initial_unique_ha2w = map4_filtered_weak['HA'].nunique()
    Map4_Summary_Dict['Category'].append('Unique HA')
    Map4_Summary_Dict['Read Count'].append(initial_unique_ha2w)

    #you can uncomment out this to produce a file of the FULL df after initial filtering but I found it unnessicary 
    #dffpw = os.path.join(output_directory, f'{Lib_Name}_{base_name}_map4_{THRESH}_match_filter.csv')
    #map4_filtered_strong.to_csv(dffpw, index=False)

    ###Stronger filter, only keep if 100% of time RTBC maps to one HA
    # Identify RTBCs with more than 1 unique HA
    bad_rtbc = ha_per_rtbc[ha_per_rtbc > 1].index
    # Identify all HAs associated with those RTBCs
    bad_ha = map4.loc[map4['RTBC'].isin(bad_rtbc), 'HA'].unique()
    # Remove rows with bad RTBCs or bad HAs
    map4_filtered_strong = map4[~map4['RTBC'].isin(bad_rtbc) & ~map4['HA'].isin(bad_ha)]
    
    ha_per_rtbc_filtered = map4_filtered_strong.groupby('RTBC')['HA'].nunique()
    #they should all equal 1 because the graph is made after filtering so that all RTBC should have a unique HA
    plt.figure(figsize=(10, 6))
    plt.hist(ha_per_rtbc_filtered, bins=range(1, ha_per_rtbc_filtered.max() + 2), edgecolor='black')
    plt.title('Histogram of Unique HA per RTBC Filtered 100%')
    plt.xlabel('Number of Unique HA Values')
    plt.ylabel('Number of RTBC Entries')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_uniHAperRTBC_cov_filtered_100.{Fig_Format}'))
    plt.clf()

    rtbc_per_hat_filtered = map4_filtered_strong.groupby('HA')['RTBC'].nunique()
    plt.figure(figsize=(10, 6))
    plt.hist(rtbc_per_hat_filtered, bins=range(1, rtbc_per_hat_filtered.max() + 2), edgecolor='black')
    plt.title('Histogram of Unique RTBCs per HA Filtered 100%')
    plt.xlabel('Number of Unique RTBCs')
    plt.ylabel('Number of HA Entries')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_uniRTBCperHA_cov_filtered_100.{Fig_Format}'))


    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append('Unique RTBC per HA 100% Mapping')

    Map4_Summary_Dict['Category'].append('Min')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_hat_filtered.min()}')

    Map4_Summary_Dict['Category'].append('Max')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_hat_filtered.max()}')

    Map4_Summary_Dict['Category'].append('Median')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_hat_filtered.median()}')
    
    Map4_Summary_Dict['Category'].append('Mean')
    Map4_Summary_Dict['Read Count'].append(f'{rtbc_per_hat_filtered.mean():.2f}')


    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append('Unique HA per RTBC 100% mapping (all should be 1 now)')

    Map4_Summary_Dict['Category'].append('Min')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc_filtered.min()}')

    Map4_Summary_Dict['Category'].append('Max')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc_filtered.max()}')

    Map4_Summary_Dict['Category'].append('Median')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc_filtered.median()}')
    
    Map4_Summary_Dict['Category'].append('Mean')
    Map4_Summary_Dict['Read Count'].append(f'{ha_per_rtbc_filtered.mean():.2f}')


    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append('After 100% Match Filter Individual Counts')

    Map4_Summary_Dict['Category'].append('Unique Cat Read Count')
    Map4_Summary_Dict['Read Count'].append(map4_filtered_strong.shape[0])
    
    # Count unique Tiles initially
    initial_unique_adbc2_2 = map4_filtered_strong['ADBC2'].nunique()
    Map4_Summary_Dict['Category'].append('Unique ADBC2')
    Map4_Summary_Dict['Read Count'].append(initial_unique_adbc2_2)

    # Count unique Tiles initially
    initial_unique_hawk2 = map4_filtered_strong['HawkBCs'].nunique()
    Map4_Summary_Dict['Category'].append('Unique HawkBCs')
    Map4_Summary_Dict['Read Count'].append(initial_unique_hawk2)

    # Count unique Tiles initially
    initial_unique_rtbc2 = map4_filtered_strong['RTBC'].nunique()
    Map4_Summary_Dict['Category'].append('Unique RTBC')
    Map4_Summary_Dict['Read Count'].append(initial_unique_rtbc2)
    
    # Count unique Tiles initially
    initial_unique_ha2 = map4_filtered_strong['HA'].nunique()
    Map4_Summary_Dict['Category'].append('Unique HA')
    Map4_Summary_Dict['Read Count'].append(initial_unique_ha2)


    #you can uncomment out this to produce a file of the FULL df after initial filtering but I found it unnessicary 
    #dffp = os.path.join(output_directory, f'{Lib_Name}_{base_name}_map4_100_match_filter.csv')
    #map4_filtered_strong.to_csv(dffp, index=False)

    # Filter the DataFrame based on the read_cut_off threshold and export dfs
    read_cut_off = 5 #UPDATE with diff read cutoff
    weak_filtered_df = map4_filtered_weak[map4_filtered_weak['Cat_Count'] >= read_cut_off]
    dffww = os.path.join(output_directory, f'{Lib_Name}_{base_name}_map4_{THRESH}_match_read_{read_cut_off}_filter.csv')
    weak_filtered_df.to_csv(dffww, index=False)

    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append(f'Final Individual Counts {THRESH}% Mapping and {read_cut_off} reads min')

    Map4_Summary_Dict['Category'].append('Unique Cat')
    Map4_Summary_Dict['Read Count'].append(weak_filtered_df.shape[0])
    
    # Count unique Tiles initially
    initial_unique_adbc2fw = weak_filtered_df['ADBC2'].nunique()
    Map4_Summary_Dict['Category'].append('Unique ADBC2')
    Map4_Summary_Dict['Read Count'].append(initial_unique_adbc2fw)

    # Count unique Tiles initially
    initial_unique_hawkfw = weak_filtered_df['HawkBCs'].nunique()
    Map4_Summary_Dict['Category'].append('Unique HawkBCs')
    Map4_Summary_Dict['Read Count'].append(initial_unique_hawkfw)

    # Count unique Tiles initially
    initial_unique_rtbcfw = weak_filtered_df['RTBC'].nunique()
    Map4_Summary_Dict['Category'].append('Unique RTBC')
    Map4_Summary_Dict['Read Count'].append(initial_unique_rtbcfw)
    
    # Count unique Tiles initially
    initial_unique_hafw = weak_filtered_df['HA'].nunique()
    Map4_Summary_Dict['Category'].append('Unique HA')
    Map4_Summary_Dict['Read Count'].append(initial_unique_hafw)

    strong_filtered_df = map4_filtered_strong[map4_filtered_strong['Cat_Count'] >= read_cut_off]
    dffs = os.path.join(output_directory, f'{Lib_Name}_{base_name}_map4_100_match_read_{read_cut_off}_filter.csv')
    strong_filtered_df.to_csv(dffs, index=False)

    Map4_Summary_Dict['Category'].append('New Section')
    Map4_Summary_Dict['Read Count'].append(f'Final Individual Counts 100% Mapping and {read_cut_off} reads min')

    Map4_Summary_Dict['Category'].append('Unique Cat')
    Map4_Summary_Dict['Read Count'].append(strong_filtered_df.shape[0])
    
    # Count unique Tiles initially
    initial_unique_adbc2f = strong_filtered_df['ADBC2'].nunique()
    Map4_Summary_Dict['Category'].append('Unique ADBC2')
    Map4_Summary_Dict['Read Count'].append(initial_unique_adbc2f)

    # Count unique Tiles initially
    initial_unique_hawkf = strong_filtered_df['HawkBCs'].nunique()
    Map4_Summary_Dict['Category'].append('Unique HawkBCs')
    Map4_Summary_Dict['Read Count'].append(initial_unique_hawkf)

    # Count unique Tiles initially
    initial_unique_rtbcf = strong_filtered_df['RTBC'].nunique()
    Map4_Summary_Dict['Category'].append('Unique RTBC')
    Map4_Summary_Dict['Read Count'].append(initial_unique_rtbcf)
    
    # Count unique Tiles initially
    initial_unique_haf = strong_filtered_df['HA'].nunique()
    Map4_Summary_Dict['Category'].append('Unique HA')
    Map4_Summary_Dict['Read Count'].append(initial_unique_haf)

    #export summary csv
    map4_Summary_Dict_df = pd.DataFrame.from_dict(Map4_Summary_Dict)
    sum3_f_p = os.path.join(output_directory, f'{Lib_Name}_{base_name}_Filtering_Summary.csv')
    map4_Summary_Dict_df.to_csv(sum3_f_p, index=False)

    #Cat_Cov weak
    plt.figure(figsize=(8,6))
    plt.hist(weak_filtered_df['Cat_Count'], bins=50, edgecolor='black')  # adjust bins as needed
    plt.xlabel("Cat_Count", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title(f"Final Histogram of Cat_Count {THRESH}% Mapping {read_cut_off} read min", fontsize=14)
    plt.yscale("linear")  # change to "log" if you want log scale
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_cat_count_hist_final_{THRESH}_{read_cut_off}_read_min.{Fig_Format}'))
    plt.clf()
    
    #Cat_Cov strong
    plt.figure(figsize=(8,6))
    plt.hist(strong_filtered_df['Cat_Count'], bins=50, edgecolor='black')  # adjust bins as needed
    plt.xlabel("Cat_Count", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title(f"Final Histogram of Cat_Count 100% Mapping {read_cut_off} read min", fontsize=14)
    plt.yscale("linear")  # change to "log" if you want log scale
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_cat_count_hist_final_100_{read_cut_off}_read_min.{Fig_Format}'))
    plt.clf()
    
    #Cat_Cov weak log
    plt.figure(figsize=(8,6))
    plt.hist(weak_filtered_df['Cat_Count'], bins=50, edgecolor='black')  # adjust bins as needed
    plt.xlabel("Cat_Count", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title(f"Final Histogram of Cat_Count {THRESH}% Mapping {read_cut_off} read min Log", fontsize=14)
    plt.yscale("log")  # change to "log" if you want log scale
    plt.xscale("log")
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_cat_count_hist_final_{THRESH}_{read_cut_off}_read_min_log.{Fig_Format}'))
    plt.clf()
    
    #Cat_Cov strong log
    plt.figure(figsize=(8,6))
    plt.hist(strong_filtered_df['Cat_Count'], bins=50, edgecolor='black')  # adjust bins as needed
    plt.xlabel("Cat_Count", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title(f"Final Histogram of Cat_Count 100% Mapping {read_cut_off} read min Log", fontsize=14)
    plt.yscale("log")  # change to "log" if you want log scale
    plt.xscale("log")
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, f'{Lib_Name}_cat_count_hist_final_100_{read_cut_off}_read_min_log.{Fig_Format}'))
    plt.clf()

# Loop through each .csv file in the input directory
for file in os.listdir(input_directory):
    if file.endswith('.csv'):
        file_path = os.path.join(input_directory, file)
        process_map4_file(file_path)

print('Finished with Everything')
