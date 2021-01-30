#!/usr/bin/env python3

## Selects one best match per query of tabular BLAST output file.
# The query should be the reads/metagenome and the reference the genome/MAG. 
# Input tabular BLAST output must be sorted, at least by the first column (query sequence id)
# It is recommended to filter the BLAST output by alignment length / read length before sorting (filter-blast-by-alignment.py)
# Input tabular BlAST format must be the following (with the -outfmt flag):
# '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen'

### Set-up command line parser for this script
## Argparse tutorials:
# https://docs.python.org/3/howto/argparse.html
# https://docs.python.org/3/library/argparse.html
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="BLAST tabular file. Must be sorted in advance!!! Must be in format '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen'.")
parser.add_argument("-o", "--output", help="Path and location of output file.")
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
	exit('Error: please provide input BLAST tabular file. Must be sorted in advance!!!')
fh = open(blast_file, 'r')

## Open output file handle
output_file = args.output
if output_file == None:
	exit('Error: please provide desired output location.')
fhout = open(output_file, 'w')

## Import any other necessary modules
import random

## Open tabular BLAST file handle
blast_file = args.input
fh = open(blast_file, 'r')

def store_line():
	## Reads a line from the BLAST file and stores it in a list with ids as strings and values as float
	# Read a line of data
	line = fh.readline()
	# If line is empty, we reached the end of file.
	if line == '':
		return ['']
	# Turn line into list
	line = line.strip('\n').split('\t')
	# Output the line (now a list)
	return line

def process_query(current_line):
	## Read and process all lines with the same query
	# Before starting loop of reading lines, copy current line to previous line
	previous_line = current_line.copy()
	# Initiate best line list
	best_lines_list = [current_line.copy()]
	# Initiate best bit-score for comparisons
	best_bitscore = float(current_line[11])
	# Initiate best e-value for comparisons
	best_evalue = float(current_line[10])
	## Enter a loop of readling lines and doing process until reach a line for next query
	while True:
		## Use "store_line" function to read in a line
		current_line = store_line()
		## Check if reached next query. Stop function (breaks this loop) if different query.
		if current_line[0] != previous_line[0]:
			# Choose a best match at random if multiple, or takes the only result from list if one.
			best_match = random.choice(best_lines_list)
			return current_line, best_match
		## Find highest bitscore, then smallest e-value (http://www.metagenomics.wiki/tools/blast/evalue)
		## If have multiple entries with same bitscore and e-value, shuffle them and choose one at random
		# Store line with highest bitscore
		current_bitscore = float(current_line[11])
		if current_bitscore > best_bitscore:
			# If get higher bitscore, update best lines list since all bitscores there are lower.
			best_lines_list = [current_line.copy()] 
		elif current_bitscore == best_bitscore:
			# If get same bitscore, check e-value
			current_evalue = float(current_line[10])
			if current_evalue < best_evalue:
				# If current line we are checking has a smaller e-value that's better to replace the best line.
				best_lines_list = [current_line.copy()]
			elif current_evalue > best_evalue:
				# If current line has a larger e-value, don't need the current line so go to next loop iteration.
				continue
			elif current_evalue == best_evalue:
				# If get same bitscore and e-value, append line to list of best lines
				best_lines_list.append(current_line)
		## Store current line as previous before reading next line
		previous_line = current_line.copy()

## Read first line. For only the first case, make previous_line a copy of this.
current_line = store_line()

## Apply the function above to each set of results that have the same query (read) 
while True:
	# Stop when reached end of file.
	if current_line == ['']:
		break
	# Process set of results with same query/read.
	current_line, best_match = process_query(current_line)
	# Print the best match.
	# print('\t'.join(map(str,best_match)))
	line_out='\t'.join(map(str,best_match))
	fhout.write(line_out+'\n')

## Close file handle
fh.close()
fhout.close()
