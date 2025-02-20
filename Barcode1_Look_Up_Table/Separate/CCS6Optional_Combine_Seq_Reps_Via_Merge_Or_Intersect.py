import pandas as pd
import gc
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Global Variables
#UPDATE names to fit with you library 
Lib_Name = 'Lib_1'
Output_Directory = f'{Lib_Name}_CCS6_M_and_I'
os.makedirs(Output_Directory, exist_ok=True)
Fig_Format = 'jpeg'
#unfiltered because there will later be a read threshold cut off and have these graphs made again with filtered data
def analyze_tcov_nom(map3_data, name): 
    sns.histplot(x='count', data=map3_data, bins=50)
    plt.title(f'{Lib_Name} {name} Unique Tile Coverage Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_{name}_Tcov_uf_Map3.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_tbcov_nom(map3_data, name): 
    sns.histplot(x='count', data=map3_data, bins=50)
    plt.title(f'{Lib_Name} {name} Unique Tile + BC Coverage Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_{name}_TBcov_uf_Map3.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_tcov_exp(map3_data, name): 
    sns.histplot(x='count', data=map3_data, log_scale=(True, True), bins=50)
    plt.title(f'{Lib_Name} {name} Unique Tile Coverage Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_{name}_Tcov_uf_exp_Map3.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def analyze_tbcov_exp(map3_data, name): 
    sns.histplot(data=map3_data, x='count', log_scale=(True, True), bins=50) 
    plt.title(f'{Lib_Name} {name} Unique Tile + BC Coverage Unfiltered')
    f_path = os.path.join(Output_Directory, f'{Lib_Name}_{name}_TBcov_exp_uf_Map3.jpg')
    plt.savefig(f_path, format=Fig_Format)
    plt.clf()

def combine_maps(map3_rep1, map3_rep2):
    Rep1 = pd.read_csv(map3_rep1)
    Rep2 = pd.read_csv(map3_rep2)

    merged = pd.concat([Rep1, Rep2])
    fM_path = os.path.join(Output_Directory, f'{Lib_Name}_merged_Map3.csv')
    merged.to_csv(fM_path, index=False)

    tcov_merged = merged['Tiles'].value_counts().to_frame().reset_index()
    tbcov_merged = merged['Cat'].value_counts().to_frame().reset_index()

    Map3_Summary_Dict = {
        'Category': [
            f'Shape of Rep1 Map3',
            f'Shape of Rep2 Map3',
            'Section: Merged Seq Reps',
            'Merged shape Map3',
            'Merged Unique Tiles Counts',
            'Merged Unique Tile + BC Count'
        ],
        'Read Count': [
            Rep1.shape[0],
            Rep2.shape[0],
            '',
            merged.shape[0],
            tcov_merged.shape[0],
            tbcov_merged.shape[0]
        ]
    }
    Map3_Summary_Dict_df = pd.DataFrame.from_dict(Map3_Summary_Dict)
    sum3_f_p = os.path.join(Output_Directory, f'{Lib_Name}_Summary_Merged_Map3.csv')
    Map3_Summary_Dict_df.to_csv(sum3_f_p, index=False)

    analyze_tbcov_exp(tbcov_merged, 'Merged')
    analyze_tcov_exp(tcov_merged, 'Merged')
    analyze_tcov_nom(tcov_merged, 'Merged')
    analyze_tbcov_nom(tbcov_merged, 'Merged')

    del merged, Rep1,  Rep2
    gc.collect()

def intersect_maps(map3_rep1, map3_rep2):
    Rep1 = pd.read_csv(map3_rep1)
    Rep2 = pd.read_csv(map3_rep2)

    common_cats = set(Rep1['Cat']) & set(Rep2['Cat'])
    Rep1_filtered = Rep1[Rep1['Cat'].isin(common_cats)]
    Rep2_filtered = Rep2[Rep2['Cat'].isin(common_cats)]
    intersected = pd.concat([Rep1_filtered, Rep2_filtered])

    fI_path = os.path.join(Output_Directory, f'{Lib_Name}_Intersected_Map3.csv')
    intersected.to_csv(fI_path, index=False)

    tcov_inter = intersected['Tiles'].value_counts().to_frame().reset_index()
    tbcov_inter = intersected['Cat'].value_counts().to_frame().reset_index()

    Map3_Summary_Dict = {
        'Category': [
            'Section: Intersected Seq Reps',
            'Intersected Shape Map3',
            'Intersected Unique Tiles Counts',
            'Intersected Unique Tile + BC Count'
        ],
        'Read Count': [
            '',
            intersected.shape[0],
            tcov_inter.shape[0],
            tbcov_inter.shape[0]
        ]
    }
    Map3_Summary_Dict_df = pd.DataFrame.from_dict(Map3_Summary_Dict)
    sum3_f_p = os.path.join(Output_Directory, f'{Lib_Name}_Summary_Intersected_Map3.csv')
    Map3_Summary_Dict_df.to_csv(sum3_f_p, index=False)

    analyze_tbcov_exp(tbcov_inter, 'Intersected')
    analyze_tcov_exp(tcov_inter, 'Intersected')
    analyze_tcov_nom(tcov_inter, 'Intersected')
    analyze_tbcov_nom(tbcov_inter, 'Intersected')

    del Rep1, Rep2, intersected
    gc.collect()
    
#you can call one or both intersect and/or merge 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine and/or intersect Map3 files.')
    parser.add_argument('-r1', '--rep1', type=str, required=True, help='Path to Rep1 Map3 CSV file')
    parser.add_argument('-r2', '--rep2', type=str, required=True, help='Path to Rep2 Map3 CSV file')
    parser.add_argument('-m', '--merge', action='store_true', help='Merge the Map3 files')
    parser.add_argument('-i', '--intersect', action='store_true', help='Intersect the Map3 files')
    args = parser.parse_args()

    if args.combine:
        combine_maps(args.rep1, args.rep2)
    if args.intersect:
        intersect_maps(args.rep1, args.rep2)

    print('Finished with Everything')
