import gzip
import sys
import math

# not copy-pasting from mcb185, btw borrowing idea

def read_fasta(filename):
    """ no copy pasting """
    if   filename == '-':          fp = sys.stdin
    elif filename.endswith('.gz'): fp = gzip.open(filename, 'rt')
    else:                          fp = open(filename)
    name = None
    seqs = []
    while True:
        line = fp.readline()
        if line == '': break
        line = line.rstrip()
        if line.startswith('>'):
            if len(seqs) > 0:
                yield(name, ''.join(seqs))
                name = line[1:]
                seqs = []
            else:
                name = line[1:]
        else:
            seqs.append(line)

    yield(name, ''.join(seqs))
    fp.close()
    
# calculating Shannon entropy of DNA sequences

def seq_en(seq, x):
	a = seq.count('A')
	if a != 0: ha = - a/x * math.log2( a/x )
	else: 	   ha = 0
	t = seq.count('T')
	if t != 0: ht = - t/x * math.log2( t/x )
	else: 	   ht = 0
	c = seq.count('C')
	if c != 0: hc = - c/x * math.log2( c/x )
	else:	   hc = 0	
	g = seq.count('G')
	if g != 0: hg = - g/x * math.log2( g/x )
	else:	   hg = 0
	se = ha + ht + hc + hg
	return se

# this is how to create the reverse strand

def revcomp(dna):
	rc = []
	for nt in dna[::-1]:
		if 	 nt == 'A': rc.append('T')
		elif nt == 'C': rc.append('G')
		elif nt == 'G': rc.append('C')
		elif nt == 'T': rc.append('A')
		else:			rc.append('N')
	return ''.join(rc)

def revercomp(sequence):
    
    comp_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
                 'a': 't', 't': 'a', 'c': 'g', 'g': 'c'}
    
    return ''.join(comp_dict.get(nt, nt) for nt in sequence[::-1])