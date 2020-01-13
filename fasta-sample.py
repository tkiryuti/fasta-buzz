#!/usr/bin/env python3

### Subsampler of sequences from FASTA file

# Import packages
import re
import sys
import argparse
import random

# Parse arguments
parser = argparse.ArgumentParser(
	description='Subsample sequences from FASTA file.',
	epilog='A FASTA file will be created named after original and appended with "-sampled".')
parser.add_argument('-i', '--input', type=str, dest='input',
	help='input FASTA file')
parser.add_argument('-n', '--num', type=int, dest='num',
	help='number of sequences to subsample from FASTA file')
parser.add_argument('-f', '--fraction', type=float, dest='fraction',
	help='fraction of sequences to subsample from FASTA file')
parser.add_argument('-r', '--random', dest='randomize', action='store_true',
	help='if chosen, random sampling is conducted. otherwise, prints sequences in same order as input.')
args = parser.parse_args()

# Define arguments
seqFile = args.input
numSeq = args.num
fractionSeq = args.fraction

# Check for required input for number or fraction of sequences
if fractionSeq is None and numSeq is None:
	print('ERROR: no number or fraction of sequences to subsample was specified.')
	print('-------------------------------------------------------------------')
	parser.print_help()
	sys.exit()

# Determine number of sequences in file
from subprocess import Popen, PIPE
grep = Popen(["grep", "^>", seqFile], stdout=PIPE)
count = Popen(["wc", "-l"], stdin=grep.stdout, stdout=PIPE)
grep.stdout.close() 
totalSeq = int(count.communicate()[0].decode("utf-8").strip('\n'))

# If fraction to subsample specified, convert to number of sequences
if fractionSeq is not None:
	numSeq = int( totalSeq*fractionSeq + 0.5 ) # rounds up if decimal portion is 0.5 or higher

# Open file handle for output file
outFile = seqFile + '-sampled'
outFH = open(outFile, "w")


if args.randomize is True:

	# Import sequences (for randomizing)
	Sequences = {}
	with open(seqFile, "r") as fh:
		for line in fh:
			match = re.search('^>', line)
			if match:
				summaryLine = line
				Sequences[ summaryLine ] = ''
			else:
				Sequences[ summaryLine ] += line
	
	# Randomize requence descriptions
	Descriptions = []
	for description in Sequences:
		Descriptions.append( description )
	random.shuffle( Descriptions )

	# Write sequences to output
	seqNumber = 0
	for description in Descriptions:
		seqNumber += 1
		if seqNumber == numSeq + 1:
			break
		outFH.write(description)
		outFH.write( Sequences[description] )

else:
	
	# Write sequences directly from input file to output
	with open(seqFile, "r") as fh:
		seqNumber = 0
		for line in fh:
			match = re.search('^>', line)
			if match:
				seqNumber += 1
			if seqNumber == numSeq + 1:
				break
			outFH.write(line)


# Close output file handle
outFH.close()
