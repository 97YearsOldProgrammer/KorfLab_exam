import gzip
import re
import argparse

parser = argparse.ArgumentParser(description='PWM for Kozak sequence.')
parser.add_argument('file', type=str, help='name of fasta file')
arg = parser.parse_args()

# collecting CDS , trying to put into a 2dimensional matrix

CDS = []											# this is where every genetic codon start
with gzip.open(arg.file, 'rt') as fp:

	while True:
		line = fp.readline()
		if not line: break
		line = line.strip()

		if line.startswith('CDS'):
			if    line.endswith(')'): continue	   # there is complement strand
			elif  line.endswith('K'): continue     # there is one protein sequence ends with K
			else:
				SEc = line[3:]                     # starting and ending codon
				i   = SEc.index('.')   
				stg = SEc[3:i]           
				stg = stg.lstrip()        		   # removing extra space bar before ouput
				CDS.append(stg)

# trying to get bottom of gbff file and those genetic information
# not sure where this can be done within previous opening

with gzip.open(arg.file, "rt") as file:
	condition = False
	sequence = []

	for line in file:

		if 'ORIGIN' in line:
			condition = True  
			continue  

		if condition:
			regex = '[^atcg]' 
			nline = re.sub(regex, '', line)
			sequence.append(nline.strip())  

	fullSeq = ''.join(sequence)

# trying to extract the kozak sequence which is -6 atg +4 inttotal of 14
# bc string start with 0 
# t would be the place inside the stg of CDS
# range would be stg-7 until stg+6

kozakseq = [] # where the kozak sequence would be stored

for stg in CDS:
	kozak_seq = (fullSeq[int(stg)-7:int(stg)+7])
	kozakseq.append(kozak_seq)


# count how many times each letter exists
# for existence of PWM

frequency = {}  # dictionary for counting PFW

a = 0

d1 = {	'A': 0, 
	  	'C': 0, 
	  	'G': 0,
	  	'T': 0 	}

for i in range(14):
	a += 1
	frequency[a] = d1.copy()    # i don't even know if we don't use copy, it would be the same dictionary

# start counting

for seq in kozakseq:
	n = 0
	for base in seq:

		if   base == 'a': frequency[n+1]['A'] += 1
		elif base == 'c': frequency[n+1]['C'] += 1
		elif base == 'g': frequency[n+1]['G'] += 1
		elif base == 't': frequency[n+1]['T'] += 1
		else: break

		n += 1

# final output

print(f'AC IMTSUOO1\nXX\nID ECKOZ\nXX\nDE not sure btw should be fine')
print(f'PO\tA\tC\tG\tT')

for i in range(14):
	print(f'{i+1:<8}{frequency[i+1]['A']:<8}{frequency[i+1]['C']:<8}{frequency[i+1]['G']:<8}{frequency[i+1]['T']:<8}')

print('XX')