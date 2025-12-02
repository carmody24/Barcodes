**UMI RNA Analysis Post Sanj**

JN for analysing RNA data with UMIs collected from human cell gene expression experiment. The look up table associated with this experiment to map the barcodes back to the origional tile used is in the Barcode1_Barcode2_and_Barcode3 folder. It is labeled Post_Sanj because there is initial RNA processing and error correcting that is done with script made by Sanjana that is required before this step, I will link to it when she finishes the final version. Currently my script relies on names that I have been using in my experiments so they would need to be modified for more meaningful names. Inputs: step1 map - csv file associating barcode combinations with tiles from plasmid pool sequencing, look up table = csv file used to associate metadata step1 based on tile matching specific protein sequence. RNA data = csv file containing preprocessed RNA data with UMI counts for each unique barcode combination. 

Current nomenclature:

Barcode Columns - 'HawkBCs' = designed barcode for tile,'ADBC2' = random barcode for tile,'RTBC' = random  barcode for reporter, 'Designed' = long protein sequence the tile barcode maps back to, referred to AD for activation domain because that is what is being looked at in this study

Concatenated Barcode Combinations Columns- 'HA' = (HawkBCs-ADBC2) is used as the AD barcode that is used for counting AD UMIs, 'HAR'(HawkBCs-ADBC2-RTBC) comes from the step1 map and was used to match AD barcode UMI counts with Reporter barcode UMI counts, 'Cat' (HawkBCs-ADBC2-RTBC-Designed) this is the most often used combination because it most accurately identifies unique tile integrations. 

Other Columns in RNA Data: 'number' = sample number used to parse RNA data into seperate dataframes based on their sample origin for outlier removal and comparison. 'AD_umi_count_complex' and AD_umi_count_simple' = AD barcode UMI count based on two different counting methods. 'RTBC_umi_count_complex' and RTBC_umi_count_simple'= Reporter barcode UMI count  based on two different counting methods.

MetaData Columns - 'Mutation'= identifier for type of variant made ( ex: 1-3-4-2 shuffle, S > A at position 49, etc.), 'Mutant Sequence'= protein sequence of tile, 'Gene Name' = gene the tile origionated from. These columns are used to associate metadata with step1 (if not done so already) and the RNA data. 


