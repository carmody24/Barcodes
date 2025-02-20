**Goal of this Folder**

The goal of this code is to process double barcoded sequencing data and create a look up table similar to Barcode1 look up table, except this time instead of BC1 + Tile the LUT will be BC1 + BC2. The same methods are used to indentify quality reads that contain the BCs between specific flanking sequences and checking that the BC are the correct length. There is not design file needed in any of these code because there are no Tile here. The final LUT for this step will be filtered based on specific threshold input. 

**Important Features**

This script is meant for processing sequencing data resulting from a 4 bin cell sort based on GFP activity. So for each bin seperate Map files and graphs will be created. When determinng thresholds the bins for each replicate will be combined to prevent BC1+BC2 combinations that only appear in some of the bins from being eliminated, because ideally that would be the case. The threshold will be created based on the combined bins to generate a look up table. This LUT will then be applied indvidually to each bin, filtering to only keep BC1+BC2 combinations that appear in the LUT.  
