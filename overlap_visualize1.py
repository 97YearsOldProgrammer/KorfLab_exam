import argparse
import gzip
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='variant reporter')
parser.add_argument('gff', type=str, help='GFF file (gzip file)')
arg = parser.parse_args()

gff = {}
region = []

with gzip.open( arg.gff,'rt') as fp:
    for line in fp:
        if line.startswith('#'): continue
        x = line.split()
        pol = x[6]
        if pol not in gff: gff[pol] = []
        typ = x[2]
        beg = x[3]
        end = x[4]
        if     typ == 'gene':
            gff[pol].append( (beg, end) )
        elif   typ == 'region':
            region.append(beg)
            region.append(end)

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
    y   = 0
    # beg event
    if typ == 'beg':
        for index in genes:
            y -= 1
            active_pol = gene_polarity[index]
            overlaps.append( {'start': idx, 'end': index, 'strand': pol, 'y': y} )
        genes.add(idx)
    # remove the index from the set
    elif typ == 'end':
        genes.remove(idx)

# 提取数据
y_values = [ gene['y'] for gene in overlaps ]
x_starts = [ gene['start'] for gene in overlaps ]
x_ends = [ gene['end'] for gene in overlaps ]
colors = ['orange' if gene['strand'] == '+' else 'blue' for gene in overlaps]

# 绘制基因水平线
plt.hlines(y=y_values, xmin=x_starts, xmax=x_ends, colors=colors, linewidth=2)

# 绘制基因组主线
genome_start = min(x_starts)
genome_end = max(x_ends)
plt.hlines(y=0, xmin=genome_start, xmax=genome_end, colors='black', linewidth=1)

plt.xlabel("Base Pairs (bp)")
plt.ylabel("Gene Level")
plt.title("Overlap Gene Visualization for E.coli")
plt.legend(handles=[
    plt.Line2D([0], [0], color='orange', label='+ Strand'),
    plt.Line2D([0], [0], color='blue', label='- Strand')
])
plt.tight_layout()
plt.show()
