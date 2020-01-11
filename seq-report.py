#!/usr/bin/env python3

### Sequence detector
# Prints sequence length and description for each sequence in a FASTA file in tabular form

# Import packages
import re
import sys
import argparse

# Parse arguments
parser = argparse.ArgumentParser(
	description='See sequence information (length and description) from a FASTA file.')
parser.add_argument('-i', '--input', type=str, dest='input',
	help='input fasta file')
parser.add_argument('-b', '--brief', action='store_true', dest='brief',
	help='only view results for first 10 sequences')
args = parser.parse_args()

# Define arguments
seqFile = args.input
brief = args.brief

# Header for output
print( 'Number' + '\t' + 'Length' + '\t' + 'Description' )

with open(seqFile, "r") as fh:
	sequence = ''
	seqNumber = 0
	for line in fh:
		line = line.strip('\n')
		match = re.search('^>', line)
		if match:
			# Reached new summary line, print information of previous sequence
			if sequence is not '':
				seqNumber += 1
				print( f'{seqNumber}\t{len(sequence)}\t{summaryLine}' )
			# Define new summary line, reset "sequence"
			summaryLine = line
			sequence = ''
		else:
			sequence  += line.strip('*')
		# Print only 10 sequences if brief
		if brief is True:
			if seqNumber == 10:
				print('.\n.\n.')
				break

# Print entry about last squence
if sequence is not '':
	seqNumber += 1
	print( f'{seqNumber}\t{len(sequence)}\t{summaryLine}' )
