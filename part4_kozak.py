import gzip
import re
import argparse
import json
import tool

parser = argparse.ArgumentParser(description='PWM for Kozak sequence.')
parser.add_argument('file', type=str, help='name of genebank file')
arg = parser.parse_args()

# Collecting CDS, trying to put into a 2-dimensional matrix

CDS = []    # This is where every genetic codon start
rCDS = []   # Complement start codon

with gzip.open(arg.file, 'rt') as fp:
    
    condition = False
    sequence = []

    while True:
        
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        
        # This part is for collecting position of starting codon
        if line.startswith('CDS'):
            
            # Used for collecting complement
            if 'complement' in line:
                if 'join' in line: continue
                else:
                    rseq = line.split('(')[-1].split('..')[1].replace(')', '').strip()
                rCDS.append(rseq)
            # There is one protein sequence that ends with 'K'
            elif line.endswith('K'):
                continue     
            elif 'join' in line: continue
            else:
                seq = line[3:] 
                i = seq.index('.')
                seq = seq[3:i]
                seq = seq.lstrip()    # Removing extra space before output
                CDS.append(seq)
        # This is for collecting the DNA sequence        
        if 'ORIGIN' in line:
            condition = True  
            continue  

        if condition:
            regex = '[^atcg]' 
            nline = re.sub(regex, '', line)
            sequence.append(nline.strip())  

    full_seq = ''.join(sequence)

# Converting to uppercase
full_seq = full_seq.upper()

kozakseq = []   # Where the Kozak sequences will be stored
rkozakseq = []  # We extract first, and then do transcription to each sequence

for start_codon in CDS:
    kozak_seq = full_seq[int(start_codon) - 11: int(start_codon) + 3]
    kozakseq.append(kozak_seq)
    
for start_codon in rCDS:
    kozak_seq = full_seq[int(start_codon) - 4: int(start_codon) + 10]
    rkozakseq.append(kozak_seq)

# Transcription for reverse strand

for seq in rkozakseq:
    seq = tool.revercomp(seq)
    kozakseq.append(seq)

# Count how many times each letter exists for PWM

frequency = {}  # Dictionary for counting PWM

a = 0

d1 = {
    'A': 0,
    'C': 0,
    'G': 0,
    'T': 0
}

for i in range(14):
    a += 1
    frequency[a] = d1.copy()    # Using copy to avoid referencing the same dictionary

# Start counting

for seq in kozakseq:
    for n, base in enumerate(seq):
        if base in 'ACGT':
            frequency[n + 1][base] += 1

# Final output
print(json.dumps(frequency, indent=4))
