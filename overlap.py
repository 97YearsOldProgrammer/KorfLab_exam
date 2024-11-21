import argparse
import gzip
from datetime import datetime

start = datetime.now()

parser = argparse.ArgumentParser(description='variant reporter')
parser.add_argument('gff', type=str, help='GFF file (gzip file)')
arg = parser.parse_args()

gff = {}

with gzip.open( arg.gff,'rt') as fp:
    for line in fp:
        if line.startswith('#'): continue
        x = line.split()
        pol = x[6]
        if pol not in gff: gff[pol] = []
        typ = x[2]
        beg = x[3]
        end = x[4]
        if typ == 'gene': 
            gff[pol].append( (beg, end) )

events = []
gene_polarity = {}  # Initialize gene_polarity here

x = 0
for pol in gff:
    for beg, end in gff[pol]:
        idx = x
        x += 1
        # Store polarity
        gene_polarity[idx] = pol
        # Append events with positions as integers
        events.append({
            'position': int(beg),
            'polarity': pol,
            'index': int(idx),
            'type': 'beg'
        })
        events.append({
            'position': int(end),
            'polarity': pol,
            'index': int(idx),
            'type': 'end'
        })

# Assign priority
priority1 = {'beg': 1, 'end': 2}
priority2 = {'+': 1, '-': 2}

# Function for sorting events
def key_sort(x):
    return (
        x['position'],
        priority1[x['type']],
        priority2[x['polarity']]
    )

events.sort(key=key_sort)

# Initialize a set for active genes
genes = set()
overlaps = []

for event in events:
    typ = event['type']
    idx = event['index']
    pol = event['polarity']
    # beg event
    if typ == 'beg':
        for index in genes:
            active_pol = gene_polarity[index]
            # Define overlap type based on polarities
            if pol == active_pol:
                overlap_typ = 'Same-Strand'
            else:
                overlap_typ = 'Opposite-Strand'
            overlaps.append((idx, pol, index, active_pol, overlap_typ))
        # Add current gene to active genes
        genes.add(idx)
        
    elif typ == 'end':
        # Remove gene from active genes
        genes.remove(idx)

# Output the overlaps (optional)
for idx1, pol1, idx2, pol2, overlap_typ in overlaps:
    print(f"Gene {idx1} ({pol1}) overlaps with Gene {idx2} ({pol2}) {overlap_typ}")

end = datetime.now()
print(end - start)