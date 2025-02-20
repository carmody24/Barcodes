**Goal of this Folder**
The goal of the files in this folder are to processing sequncing reads to associaate a barcode (referred to as BC1 or ADBC) with a particular longer sequence of interest that is also on the read (referred to as Tile). These steps help make a look up table to asociate these two sequences so that in the future if you do sequencing that only allows you to retrieve the barcode, you will be able to use the barcode to look up in the table created here what longer tile sequence it corresponds to. 

Files in this folder have more consolidated script versions of what are in the seperate folder. All steps have a python file and a matching BASH file because the sripts were designed to be submitted to Berkeley Savio high performance computing cluster. 

**File Naming:**

**CC** - intials of author

**S#** - step number. some will have multiple numbers that are not in order in this folder because it is a combination of steps that are in the Seperate folder.

**S#Optional** - an optional step, usually the same as what is in the seperate folder.

**_BASH.sh** - all BASH files have this ending name to help them stand out. All BASH files will need the pathways to the hardcoded documents/script updated and the account added. The wall clock time is typically mush more than needed out of precaution. 

**ADBC** - BC1 is referred to as ADBC often in the code because the origional BC1 is based on an Activation Domain Barcode. Feel free to modify if you want but this name is relied on often throughout all of the steps code so make sure you update everything. 

**#UPDATE** - you should search for #UPDATE throuhgout the sript before running the code becuase I have started comments with that if you need to update something in that area to be compatible with your system. Usually updating naming of how you want your files to be saved, file type, unique sequences the code searches for, and correct lengths of sequences expected.



**What Files Do:**

**CCS1_2_5:** Combines steps 1,2, and 5 from the seperate folder. Hardcoded inputs in the BASH file of the paired reads .fastq file and the tile desin .txt file. It processes these reads and looks for tile and BC1 based on updated pre and post sequences that are expected and gives the read a quality score based on if it matches the expected tile or BC1 length (1=match, 0=any other length), also if the tile is in the design file or not is checked. This data is Map1. Map2 is a filtered version of Map1 that only keeps rows where there are are reads that pass the length and design quality checks and removes all columns except the Tile and ADBC column. Map3 is a copy of Map2 with an additional column 'Cat' for concatenate beacuase you link together the Tile and ADBC in this row with a '-'. You will use Map3 csv output in the next steps. Graphs of Map1 and Map3 are made to help visualize the distribution of different quality checks (tile and ADBC length) and coverage of unique tiles and unique tile + ADBC combinations. In seperate folder the CCS5 script is a Jupitor Notebook script for making graphs if you want to do that part seperately so you can adjust the graph parameters to get better visibility and see the changes you make real time. 

**CCS3Optional:** If you want to look for No Tile controls and make a note of BC1 barcodes that correspond to those use this code. Looks for correct BC1 but Tile length of 0. Input .csv Map1 and outputs an additional .csv Map3 for No Tile controls and .csv summary table.

**CCS4Optional:** If you did CCS3Optionial use this step to merge your origional Map3 from CCS2 with the Map3 of No Tile controls. Merges 2 .csv files that are in a input directory based on the files having the same columns, so could use it for other purposes if needed. Need to input the directory when you call the BASH script. ex: sbatch CCS4Optional_Merge_Normal_and_Control_Map3_BASH.sh /pathway/to/input/directory

**CCS6Optional:** If you have multiple sequencing reps this is where you compare them. Seq reps = same library but labeled with different indexes before sequencing to help better catch sequencing errors. You can choose to Merge the reads from the two seq reps if you have low coverage of your library or you can choose to intersect the sequencing reps (only keep reads where the Tile+BC pair shows up in both sequencing reps at least once). Intersect is good if you are deeply sequenced but at very high sequencing depths you can start to see sequencing errors appear in both reps. Up until this point sequencing reps should have been taken through all parts of the process seperately (create all previous maps for seperately). Inputs hardcoded: R1 .csv file of the first seq rep, R2 .csv file of the second seq rep, following those --intersect to run intersect funtion and/or --merge to run merge function. Outputs will be .csv summary files, .csv Intersected Map3, .csv Merged Map3, graphs of unique tiles and tile barcode coverage.

**CCS7:** Finally make your BC1 look up table (LUT) of all unique Tile + BC1 combinations that you will use later when you only have the BC1 from you final sequencing. You can use this table to map BC1 back to this LUT to determine which Tile the BC1 corresponds to. Input an input directory containing .csv Map3 files when you call the BASH script. It will process each file in the directory seperately. You will need to update the read Threshold cut off usually based on graphs produced of Tile+BC coverage when expontial scale histogram transitions from exponential to bell curve shape.







