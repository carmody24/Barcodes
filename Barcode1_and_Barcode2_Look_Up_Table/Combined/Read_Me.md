Some steps combined 


**CC_Sort1_M1_M2_M3_Graphs** - Command input of pathway to an input directory that contains all of your files that have .fastq format. If your files are in a diff format will need to update BASH file. Will output for each file in the input directory will make BC1 length and quality graphs and BC2 lengths and quality graphs, Map1 and Map3 csv files. 

**CC_Sort3Optional** - Command input of pathway to an input directory that contains all of the Map3 csv files for one rep. This script will merge all of the csv files and then output a summary table of the number of unique BC1-BC2 combinations that have appear for various counts ( 1,000 BC1-BC2 with at least 100 read coverage). This is meant to help you determine the threshold you want to actually use quickly without using the computional rescources and time to generate filtered csv files for all the thresholds. If you already know the threshold you want to use you can skip this. All the bins are mereged to determine this threshold because ideally most BC1-BC2 combos only appear in one or two bins. 

**CC_Sort4** - Command input of pathway to an input directory that contains all of the Map3 csv files for one rep. Creates a lookup table of unique Bc1-BC2 combinations that appear greater than or equal to the number of times that is set by the threshold cut off that is input in the python code. Output a look up table csv that you can use to filter your Map3 csv files and contains the counts for each unique Bc1-BC2 combination.

**CC_Sort5**  Command input of pathway to the look up table csv file created in CC_Sort4 and then pathway to an input directory that contains all of the Map3 csv files. This will output a folder containing all of the Map3 files filtered based on the LUT table and a summary of the total reads starting vs after filtering. 
