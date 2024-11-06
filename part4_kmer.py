import argparse
import itertools
import gzip
import tool

parser = argparse.ArgumentParser(description='K-mer Locations.')
parser.add_argument('file', type=str, help='name of fasta file')
parser.add_argument('-k' ,'--kvalue', type=int, default=3,
    help='kvalue [%(default)i]')
arg = parser.parse_args()
seqs = []

# i am not using the one from Dr.Korf here
# since we don't actually go this over on large fasta or multi fasta file
# that would rearrange my rest of code
# this is how kmer program would work on single fasta file with low k value

# extracting sequence from fasta file

with gzip.open(arg.file, 'rt') as fp:

    while True:
        line = fp.readline()
        if line == '': break
        line = line.rstrip()
        if line.startswith('>'): continue
        seqs.append(line)

seq = ''.join(seqs)

# creating reverse strand

rseqs = []

for bps in seq:
	if 		bps == 'A': rseqs.append('T')
	elif 	bps == 'T': rseqs.append('A')
	elif	bps == 'C': rseqs.append('G')
	elif	bps == 'G': rseqs.append('C')
	rseq = ''.join(rseqs)


# creating diciontary for data storage

d_forward = dict()
d_reverse = dict()

for nts in itertools.product('ACGT', repeat = arg.kvalue):
	kmer = ''.join(nts)
	d_forward[kmer] = []
	d_reverse[kmer] = []
	
# collecting kmers for both forward and reverse

x = -1
y = 0

for i in range ( len(seq) - arg.kvalue + 1 ):

	x += 1
	y -= 1

	# create forward sequence
	km  = seq[ 0+x : x+arg.kvalue ]
	x1 = str(x+1)
	d_forward[km].append(x1)

	# create backward sequence
	rkm = rseq[ 0+y : y+ arg.kvalue*-1 : -1 ]
	y1 = str(y*-1+1)
	d_reverse[rkm].append(y1)

# make a filter for final output

d_filter  = [k for k, v in d_forward.items() if not v]
rd_filter = [k for k, v in d_reverse.items() if not v]


for k in d_filter:
	del d_forward[k]

for k in rd_filter:
	del d_reverse[k]

# final output for forward

print()
print(f'forward sequence\t')

for k, v in d_forward.items():
	print(f"{k} {' '.join(v)}")

# final output for reverse

print(f'reverse sequence\t')

for k, v in d_reverse.items():
	print(f"{k} {' '.join(v)}")