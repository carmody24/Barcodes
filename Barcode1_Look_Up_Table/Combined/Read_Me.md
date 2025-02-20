Files in this folder have more consolidated script versions of what are in the seperate folder.

**File Naming:**

**CC** - intials of author

**S#** - step number. some will have multiple numbers that are not in order in this folder because it is a combination of steps that are in the Seperate folder.

**S#Optional** - an optional step, usually the same as what is in the seperate folder.

**_BASH.sh** - all BASH files have this ending name to help them stand out. All BASH files will need the pathways to the hardcoded documents/script updated and the account added. The wall clock time is typically mush more than needed out of precaution. 

**ADBC** - BC1 is referred to as ADBC often in the code because the origional BC1 is based on an Activation Domain Barcode. Feel free to modify if you want but this name is relied on often throughout all of the steps code so make sure you update everything. 

**#UPDATE** - you should search for #UPDATE throuhgout the sript before running the code becuase I have started comments with that if you need to update something in that area to be compatible with your system. Usually updating naming of how you want your files to be saved, file type, unique sequences the code searches for, and correct lengths of sequences expected.



**What Files Do:**

**CCS1_2_5** - Combines steps 1,2, and 5 from the seperate folder. Hardcoded inputs in the BASH file of the paired reads .fastq file and the tile desin .txt file. It processes these reads and looks for tile and BC1 based on updated pre and post sequences that are expected and gives the read a quality score based on if it matches the expected tile or BC1 length (1=match, 0=any other length), also if the tile is in the design file or not is checked. This data is Map1. Map2 is a filtered version of Map1 that only keeps rows where there are are reads that pass the length and design quality checks and removes all columns except the Tile and ADBC column. Map3 is a copy of Map2 with an additional column 'Cat' for concatenate beacuase you link together the Tile and ADBC in this row with a '-'. You will use Map3 csv output in the next steps. Graphs of Map1 and Map3 are made to help visualize the distribution of different quality checks (tile and ADBC length) and coverage of unique tiles and unique tile + ADBC combinations. 









