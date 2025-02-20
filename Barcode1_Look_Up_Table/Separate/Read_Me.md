**Goal of This Folder**
The goal of the files in this folder are to processing sequncing reads to associaate a barcode (referred to as BC1 or ADBC) with a particular longer sequence of interest that is also on the read (referred to as Tile). These steps help make a look up table to asociate these two sequences so that in the future if you do sequencing that only allows you to retrieve the barcode, you will be able to use the barcode to look up in the table created here what longer tile sequence it corresponds to.

**What is in this folder**
The sepearte version of BC1 LUT has many seperate scripts and BASH files that I used when first creating these to make it easier for debugging steps. The Combined folder has consolidated versions of these steps. 

Currently all files are in a python file + matching BASH file format except for CCS5 that creates graphs with is a JupiterNotebook file. The combined version will have python script submittable version of this. However sometimes it can be helpful to use JN to edit graph scales/bins real time and test diff graph propterties to get best visibility of data depending on the data size/distribution. 

**File Naming:**

**CC** - for the author initials

**S#** - for step number

**S#Optional** - if there is Optional after a step number then that step can be skipped if the addional feature of the Step is not desired

**_BASH.sh** - all BASH files end with this to help make them stand out. Designed origionally for submitting to Berkeley Savio high-prformance computing cluster with SLURM job scheduler. Will need to at least add an account to make it work. Most of the wall cock times are much longer than would be needed.

**ADBC** - BC1 is referred to as ADBC often in the code because the origional BC1 is based on an Activation Domain Barcode. Feel free to modify if you want but this name is relied on often throughout all of the steps code so make sure you update everything.

**#UPDATE** - you should search for #UPDATE throuhgout the sript before running the code becuase I have started comments with that if you need to update something in that area to be compatible with your system. Usually updating naming of how you want your files to be saved, file type, unique sequences the code searches for, and correct lengths of sequences expected.



**What files do:**

**CCS1** : organize paired sequencing reads (can be done via Labtools pear script) into a dataframe. Look for reads that contain correct BC1 and Tile sequneces based on flanking sequences, length, and presence in design file. Input .fastq paired seq file and .txt design file. Input pathways hardcoded into BASH file. Output of .csv summary table and .csv Map1 table. 

**CCS2** : Creates Map2 and Map3. Map2 drops rows from Map1 that have a 0 quality score for any categories (not correct length and/or not in design file).Map2 also drops all columns besides Tile and ADBC. ADBC stands for Activation Domain Barcode aka BC1. Map3 is a copy of Map2 with an additional 'Cat' column for concatenation because it creates a column with Tile and ADBC connected via '-'. Input .csv file of Map1 table, hardcode pathway into BASH file. Output .csv of Map2, .csv of Map3, .csv summary table. 

**CCS3Optional** : If you want to look for No Tile controls and make a note of BC1 barcodes that correspond to those use this code. Looks for correct BC1 but Tile length of 0. Input .csv Map1 and outputs an additional .csv Map3 for No Tile controls and .csv summary table. 

**CCS4Optional** : If you did CCS3Optionial use this step to merge your origional Map3 from CCS2 with the Map3 of No Tile controls. Merges 2 .csv files that are in a input directory based on the files having the same columns, so could use it for other purposes if needed. Need to input the directory when you call the BASH script. ex: sbatch CCS4Optional_Merge_Normal_and_Control_Map3_BASH.sh /pathway/to/input/directory

**CCS5** : Jupiter Notebook for making graphs for Map1 and Map3. Map1 graphs can be used to better visualize quality and length distributions of Tile and BC1. Map3 graphs can be used to see the Tile+BC1 coverage and unique tiles represented. 

**CCS6Optional**: If you have multiple sequencing reps this is where you compare them. Seq reps = same library but labeled with different indexes before sequencing to help better catch sequencing errors. You can choose to Merge the reads from the two seq reps if you have low coverage of your library or you can choose to intersect the sequencing reps (only keep reads where the Tile+BC pair shows up in both sequencing reps at least once). Intersect is good if you are deeply sequenced but at very high sequencing depths  you can start to see sequencing errors appear in both reps. Up until this point sequencing reps should have been taken through all parts of the process seperately (create all previous maps for seperately). Inputs hardcoded: R1 .csv file of the first seq rep, R2 .csv file of the second seq rep, following those --intersect to run intersect funtion and/or --merge to run merge function. Outputs will be .csv summary files, .csv Intersected Map3, .csv Merged Map3, graphs of unique tiles and tile barcode coverage. 

**CCS7** : Finally make your BC1 look up table (LUT) of all unique Tile + BC1 ccombinations that you will use later when you only have the BC1 to map it back to this LUT to determine which Tile the BC1 corresponds to. Input an input directory containing .csv Map3 files when you call the BASH script. It will process each file in the directory seperately. You will need to update the read Threshold cut off usually based on graphs produced of Tile+BC coverage when expontial scale histogram transitions from exponential to bell curve shape. 




