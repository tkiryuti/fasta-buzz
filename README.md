# fasta-buzz
Set of scripts to split or subsample FASTA files.

* [`fasta-split.py`](#splitting-fasta-files) - Splitting a FASTA file
* [`seq-report.py`](#reporting-sequences-in-fasta-file) - Reporting sequences in FASTA file

## Splitting FASTA files
`fasta-split.py` evenly distributes sequences in a FASTA file among a desired number of files.

### __Examples__ 

See the help message at any time:
``` bash
./fasta-split.py -h
```

Split a FASTA file "seq.fasta" into 10 files by default: "seq.fasta-1", "seq.fasta-2", ... "seq.fasta-10":
``` bash
./fasta-split.py -i seq.fasta
```

Split a FASTA file "seq.fasta" into 5 files by default: "seq.fasta-1", "seq.fasta-2", ... "seq.fasta-5" and
wrap sequences with 60 characters per line:
``` bash
./fasta-split.py -i seq.fasta -n 5 -w 60
```

## Reporting sequences in FASTA file
`seq-report.py` prints a table of sequence lengths and descriptions from a FASTA file.

### __Examples__ 

See the help message at any time:
``` bash
./seq-report.py -h
```

See sequence information (length and description) from a FASTA file "seq.fasta":
``` bash
./seq-report.py -i seq.fasta
```

See sequence information in brief, from the first 10 sequences of "seq.fasta":
``` bash
./seq-report.py -i seq.fasta -b
```

## __Troubleshooting__ 

If permission is denied for running any script, add permission to execute for user and group. For example:
``` bash
chmod ug+x fasta-split.py
```
