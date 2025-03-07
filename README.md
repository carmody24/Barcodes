


**Credit**

Much of this code is dehrived from labtools code created by Jordan Stefani for Staller Lab seq proccessing. 

https://github.com/staller-lab/labtools/tree/main/src/labtools/adtools

**General Purpose**

Code was origionally made to analyze double barcoded sequencing data. Most scripts are designed to process large data files, run via BASH file, and be submitted to a high performace computing cluster that uses SLURM job scheduling. 

**Experimental Background**


Origional sequencing samples were PCR amplicons of gDNA extracted from 4 bin sort of genetically modified human cell line. Human cells contain a GFP reporter and a genomic landing pad that allows for integration of a synthetic transcription factor construct. Libraries screened have modifcations to the activation domain of the synthetic transcription factor and samples are sorted based on GFP actvity. Column headings and general naming for the code is based around this assay, but function of the code can be adapted to fit different double barcoded assays. 
