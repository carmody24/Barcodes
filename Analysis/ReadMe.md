files for analaysis like downsampling 

***Correlations_and_Skew JN:*** 
Input 2 CSV files outputs different correlation graphs of the entire dataset and the top 10% of the dataset. Need the files to have a similar column that you can compare unique entries with and need an additional column of the counts of each unique item in the column you are comparing. For example I have 2 csv files that has Barcode1 column in each of them and another column called Read_Counts in each of the files that is the number of reads I have for each Barcode1. I compare the abundance of Barcode1 in different steps of my cloning process to see if the abundance of unique things stays similar and if within each step there is skew.

***Downsample*** 
Randomly downsamples each fastq file within input folder taking a percentage of the total reads based on an input percentage specified in the BASH file (currently at 10%). New downsampled versions of each fastq file are created. Can be used to see if you are oversequencing if you maintain diversity and relative abundance with downsampled dataset. 


***Summary Table Merger***
Many of my scripts process folders filled with files seperately and then produce seperate summary csv files. This script takes an input folder of all of the summary csv files of the same type (same column headings) and combines them. Most summary tables show how counts change after each filtering step so the code also calculates the percentage of the total remaining after each step. There are different parts commented out to use depending on the number of counts you are keeping track of so use the correct one based on your needs (ex: read count only, read count and unique AD barcode count, etc.) 
