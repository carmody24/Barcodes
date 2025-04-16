import random
import argparse
from Bio import SeqIO
import os

def downsample_fastq(input_file, output_file, fraction):
    """Randomly selects a fraction of reads from a FASTQ file."""
    with open(input_file, "r") as handle:
        records = list(SeqIO.parse(handle, "fastq"))

    subset_size = int(len(records) * fraction)
    sampled_records = random.sample(records, subset_size)

    with open(output_file, "w") as out_handle:
        SeqIO.write(sampled_records, out_handle, "fastq")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downsample FASTQ files.")
    parser.add_argument("input_fastq", help="Input FASTQ file")
    parser.add_argument("output_fastq", help="Output FASTQ file")
    parser.add_argument("fraction", type=float, help="Fraction of reads to retain (0-1)")

    args = parser.parse_args()

    downsample_fastq(args.input_fastq, args.output_fastq, args.fraction)

    print(f"Downsampling completed: {args.input_fastq} -> {args.output_fastq}")
