#!/usr/bin/env python3

### Fasta file splitter
# Splits a fasta file into a desired number of files
# Split occurs almost evenly - any remaining sequences are added one sequence per file

# Import packages
import re
import argparse
import sys

# Parse arguments
parser = argparse.ArgumentParser(
	description='Evenly split a fasta file.',
	epilog='Files created will be named after original file with appended "-1", "-2", etc.')
parser.add_argument('-i', '--input', type=str, dest='input', 
	help='input fasta file to split')
parser.add_argument('-n', '--num', type=int, dest='numFiles', 
	help='number of resulting files (default = 10)', default=10)
parser.add_argument('-w', '--wrap', type=int, dest='wrapSeq', 
	help='number of characters per line of sequence (no wrapping by default)', default=0)
args = parser.parse_args()

# Define arguments
seqFile = args.input
numFiles = args.numFiles
wrapSeq = args.wrapSeq

# Check required arguments
if seqFile is None:
	print('ERROR: no input file specified.')
	print('-------------------------------')
	parser.print_help()
	sys.exit()

# Initiate list of all sequences
Sequences = []

with open(seqFile, "r") as fh:
		for line in fh:
				line = line.strip('\n')
				match = re.search('^>', line)
				if match:
						summaryLine = line
						Sequences.append( [summaryLine, ''] )
				else:
						Sequences[-1][1]  += line

numSeq = len(Sequences)

# Check that the number of files to produce is not greater than the number of sequences
# If ok, show number of sequences and continue
if numSeq >= numFiles:
	print( str(numSeq) + ' sequences in fasta file ' + '"' + seqFile + '"' )
else:
	print( f'ERROR: desired number of files ({numFiles}), is greater than the number of sequences ({numSeq}).' )
	sys.exit()

# Show splitting information
print( 'Splitting into ' + str(numFiles) + ' files' )

# Calculate number of sequences per file for splitting
seqPerFile = int(numSeq/numFiles)
remainingSeq = remainSeq = numSeq%numFiles

# Each for loop creates a sequence file
for x in range(numFiles):
		with open(seqFile + '-' + str(x+1), "w") as fh:
				# Add one additional sequence?
				if remainingSeq > 0:
						writeAdditional = 1
				else:
						writeAdditional = 0
				# Number of sequences to write to this file
				numSeq2write = seqPerFile + writeAdditional
				remainingSeq -= 1
				# Write each sequence into file in original sequence order
				for i in range(numSeq2write):
					targetSeq = Sequences.pop(0)
					summaryLine = targetSeq[0]
					sequence = targetSeq[1]
					fh.write(summaryLine + '\n')
					if wrapSeq == 0:
						fh.write(sequence + '\n')
					else:
						for n in range(0, len(sequence), wrapSeq):
							fh.write(sequence[n:n+wrapSeq] + '\n')



