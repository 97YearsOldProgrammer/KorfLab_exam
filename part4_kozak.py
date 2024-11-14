import gzip
import re
import argparse
import json
import tool

parser = argparse.ArgumentParser(description='PWM for Kozak sequence.')
parser.add_argument('file', type=str, help='name of genebank file')
arg = parser.parse_args()

# collecting CDS , trying to put into a 2dimensional matrix

CDS  = []                                           # this is where every genetic codon start
rCDS = []                                           # complement start codon

with gzip.open(arg.file, 'rt') as fp:
    
    condition = False
    sequence = []

    while True:
        
        line = fp.readline()
        if not line: break
        line = line.strip()
        
        # this part is for collecting position of starting codon
        if line.startswith('CDS'):
            
            # used for collecting complement
            if 'complement' in line: 
                
                if 'join' in line:
                    rseq = line.split('join(')[-1].split('..')[1].split(',')[0].replace(')', '').strip()                
                else:
                    rseq = line.split('(')[-1].split('..')[1].replace(')', '').strip()
                
                rCDS.append(rseq)
                                
            elif  line.endswith('K'): continue     # there is one protein sequence ends with K
            
            elif  'join' in line:
                rseq = line.split('join(')[-1].split('..')[0].split(',')[0] 
                rCDS.append(rseq)
                
            else:
                seq = line[3:] 
                i   = seq.index('.')   
                seq = seq[3:i]       
                seq = seq.lstrip()        		   # removing extra space bar before ouput
                CDS.append(seq)

        # this is for collecting the DNA sequence        
        if 'ORIGIN' in line:
            condition = True  
            continue  

        if condition:
            regex = '[^atcg]' 
            nline = re.sub(regex, '', line)
            sequence.append(nline.strip())  

    full_seq = ''.join(sequence)

# my counting format is dumb, have to turn it into uppercase
full_seq = full_seq.upper()

kozakseq = []  # where the kozak sequence would be stored
rkozakseq = [] # we extract first, and then do transcription to each sequence

for start_codon in CDS:
    
    kozak_seq = full_seq[ int(start_codon)-11: int(start_codon)+3 ]
    kozakseq.append(kozak_seq)
    
for start_codon in rCDS:
    
    kozak_seq = full_seq[ int(start_codon)-4 : int(start_codon)+10]
    rkozakseq.append(kozak_seq)

# transcription for reverse strand

for seq in rkozakseq:
    seq = tool.revercomp(seq)
    kozakseq.append(seq)

# count how many times each letter exists
# for existence of PWM

frequency = {}  # dictionary for counting PFW

a = 0

d1 = {	'A': 0, 
		'C': 0, 
		'G': 0,
		'T': 0 		}

for i in range(14):
	a += 1
	frequency[a] = d1.copy()    # i don't even know if we don't use copy, it would be the same dictionary

# start counting

for seq in kozakseq:
    for n, base in enumerate(seq):
        if base in 'ACGT':
            frequency[n+1][base] += 1

# final output
print(json.dumps(frequency, indent=4))
