The sepearte version of BC1 LUT has many seperate scripts and BASH files that I used when first creating these to make it easier for debugging steps.

In the future I will add an additional Combined folder that will consolidate the steps into fewer scripts for steps that do not require analysis/interperataion of the results before moving onto the next step.

File Naming:

**CC** - for the author initials

**S#** - for step number

**S#Optional** - if there is Optional after a step number then that step can be skipped if the addional feature of the Step is not desired

**_BASH.sh** - all BASH files end with this to help make them stand out. Designed origionally for submitting to Berkeley Savio high-prformance computing cluster with SLURM job scheduler. Will need to at least add an account to make it work. Most of the wall cock times are much longer than would be needed.

