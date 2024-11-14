import argparse
import gzip
import tool
from datetime import datetime

parser = argparse.ArgumentParser(description='K-mer Locations.')
parser.add_argument('file', type=str, help='name of fasta file')
parser.add_argument('-k' ,'--kvalue', type=int, default=3,
    help='kvalue [%(default)i]')
parser.add_argument('-r' ,'--reverse', action = 'store_true', 
    help='softmask for reverse kmer')
arg = parser.parse_args()
    
# delete later, test time scale only
start = datetime.now()

seqs = []
# extracting sequence from fasta file
with gzip.open(arg.file, 'rt') as fp:

    while True:
        line = fp.readline()
        if line == '': break
        line = line.rstrip()
        if line.startswith('>'): continue
        seqs.append(line)

seq = ''.join(seqs)

# optimize sliding window algorithmn

kmer = seq[ : arg.kvalue ]
d_forward = {kmer: [1]}
                    
# output for forward strand
for i in range(0, len(seq) - arg.kvalue +1 ):
                    
    kmer = kmer[1:] + seq[i + arg.kvalue - 1]
    
    if kmer in d_forward:
        d_forward[kmer].append(i+1)
    else: 
        d_forward[kmer] = [i+1]
                    
# creating reverse strand
if arg.reverse:
    rseqs = tool.revcomp(seq)
    rseq = ''.join(rseqs)
    rkmer = seq[ : arg.kvalue ]
    d_reverse = {rkmer: [1]}
    

# collecting kmers for both forward and reverse
if arg.reverse:
                    
    for i in range(0, len(rseq) - arg.kvalue +1 ):
                    
        rkmer = rkmer[1:] + rseq[i + arg.kvalue - 1]
    
        if rkmer in d_reverse:
            d_reverse[rkmer].append(i+1)
        
        else: 
            d_reverse[rkmer] = [i+1]

# final output for forward
print(f'>forward sequence')

for kmer in d_forward:
    positions = ' '.join( map(str, d_forward[kmer]) )
    print(f"{kmer} {positions}")
            

# final output for reverse
if arg.reverse:
    print(f'\n>reverse sequence')
                    
    for rkmer in d_reverse:
        positions = ' '.join( map(str, d_reverse[rkmer]) )
        print(f"{rkmer} {positions}")

# delete later, test time scale only
end = datetime.now()
print(end - start)