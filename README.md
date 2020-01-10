# fasta-buzz
Set of scripts to split or subsample FASTA files.

## Splitting FASTA files
`fasta-split.py` evenly distributes sequences in a FASTA file among a desired number of files.

### __Examples__ 

See the help message at any time:
``` bash
./fasta-split.py -h
```

Split a fasta file "seq.faa" into 10 files by default: "seq.faa-1", "seq.faa-2", ... "seq.faa-10" in which
sequences do not wrap by default:
``` bash
./fasta-split.py -i seq.faa
```

Split a fasta file "seq.faa" into 5 files by default: "seq.faa-1", "seq.faa-2", ... "seq.faa-10" and
wrap sequences with 60 characters per line:
``` bash
./fasta-split.py -i seq.faa -n 5 -w 60
```

### __Troubleshooting__ 

If permission is denied for running `fasta-split.py` then add permission to execute for user and group:
``` bash
chmod ug+x fasta-split.py
```

