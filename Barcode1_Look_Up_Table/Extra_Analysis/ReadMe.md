These files contain different analysis that can be done on BC1 Look Up Table seq data to give you more information or help troubleshooting.


**CC_M3_Including_Not_In_Design_File**
Looks through Map1 to find rows where the tile and bc1 are the correct length but the tile is not found in the design file. Takes input directory containing Map1 csv files via command input and processes them separately. Output currently only a look up table of unique Tile + BC1 combinations that are not in the design file (Designed == 0) but have the correct tile length (T Qual ==1) and correct bc1 length (A Qual ==1). If you uncomment certain parts of code additional csv output can be generated.


**CC_M3_Including_Not_In_T_Length_File**
Looks through Map1 to find rows where the bc1 is correct length, but the tile is not the correct length (and by default is also not found in the design file). Takes input directory containing Map1 csv files via command input and processes them separately. Output currently only a look up table of unique Tile + BC1 combinations that are not the correct tile length (T Qual == 0) but have the correct bc1 length (A Qual ==1). If you uncomment certain parts of code additional csv output can be generated.

