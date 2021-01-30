#!/usr/bin/env python3

## Filters a tabular BLAST output file by alignment fraction (alignment length / read length)
# Input tabular BlAST format must be the following (with the -outfmt flag):
# '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen'

### Set-up command line parser for this script
## Argparse tutorials:
# https://docs.python.org/3/howto/argparse.html
# https://docs.python.org/3/library/argparse.html
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="BLAST tabular file. Must be in format '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen'.")
parser.add_argument("-o", "--output", help="Path and location of output file.")
parser.add_argument("-c", "--cutoff", type=float, default=0.7, help="Cutoff of alignment fraction (alignment length / read length). Prints all matches at or above the cutoff. Default: 0.7")
args = parser.parse_args()

## Create a function to exit
def exit(message):
	print(message)
	parser.print_help()
	sys.exit()

## Exit if no arguments provided.
import sys
if len(sys.argv) == 1:
	exit('Error: no arguments provided.')

## Open tabular BLAST file handle
blast_file = args.input
if blast_file == None:
	exit('Error: please provide input BLAST tabular file.')
fh = open(blast_file, 'r')

## Open output file handle
output_file = args.output
if output_file == None:
	exit('Error: please provide desired output location.')
fhout = open(output_file, 'w')

## Store the alignment fraction threshold 
threshold = args.cutoff

## Read file line by line
for line in fh:
	# Turn line into list
	line = line.strip('\n').split('\t')
	# Get alignment length and read length
	alignment_length = float(line[3])
	read_length = float(line[12])
	# Calculate alignment fraction
	alignment_fraction = alignment_length/read_length
	# If alignment fraction is greater than or equal to the threshold, print the line
	if alignment_fraction >= threshold:
		# print('\t'.join(map(str,line)))
		line_out='\t'.join(map(str,line))
		fhout.write(line_out+'\n')

## Close file handles
fh.close()
fhout.close()
