import argparse
import sys
import math
import gzip


parser = argparse.ArgumentParser(description='DNA entropy filter.')

parser.add_argument('file', type=str, help='name of fasta file')

parser.add_argument('-s', '--size', type=int, default=11,
	help='window size [%(default)i]')

parser.add_argument('-e', '--entropy', type=float, default=1.4,
	help='entropy threshold [%(default).3f]')

arg = parser.parse_args()


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


x = str(arg.entropy).split('.')
y = int(''.join(x))

lcomplex = []
result	 = []
m        = 0

with gzip.open(arg.file, 'rt') as fp:



	for line in fp:

		seqs = list(line)
		k	 = -1

		if line[0] == '>':
			name = line[0:] 
			continue

		for i in range( len(line) - arg.size +1 ):

			part = line[ i:i+ arg.size ]
			en_f = seq_en( part, arg.size )
			en 	 = int( round(en_f, ndigits=1 ) * 10 ) 
			k	+= 1

			if en < y:

				for j in range(arg.size): 

					if m == arg.size: 
						m = 0 
						low_complex = ''.join(seqs)
						lcomplex.append( low_complex )
						break

					m += 1
					if 	 seqs[k+m-1] == 'A': seqs[k+m-1] = 'a'
					elif seqs[k+m-1] == 'C': seqs[k+m-1] = 'c'
					elif seqs[k+m-1] == 'G': seqs[k+m-1] = 'g'
					elif seqs[k+m-1] == 'T': seqs[k+m-1] = 't'

print()
print(name, end="")
for seq in lcomplex:
	print(seq, end="")