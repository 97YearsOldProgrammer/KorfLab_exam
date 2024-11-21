import argparse
import gzip
import plotly.graph_objects as go

parser = argparse.ArgumentParser(description='Variant reporter')
parser.add_argument('gff', type=str, help='GFF file (gzip file)')
arg = parser.parse_args()

genes = []
region_start = None
region_end = None

with gzip.open(arg.gff, 'rt') as fp:
    for line in fp:
        if line.startswith('#'):
            continue
        x = line.strip().split('\t')
        typ = x[2]
        beg = int(x[3])
        end = int(x[4])
        if typ == 'gene':
            pol = x[6]
            genes.append({'start': beg, 'end': end, 'strand': pol})
        elif typ == 'region':
            region_start = beg
            region_end = end

events = []
for idx, gene in enumerate(genes):
    events.append({'position': gene['start'], 'type': 'beg', 'index': idx})
    events.append({'position': gene['end'], 'type': 'end', 'index': idx})

events.sort(key=lambda x: (x['position'], 0 if x['type'] == 'beg' else 1))

y_levels = []
genes_y = [None] * len(genes)

for event in events:
    idx = event['index']
    gene = genes[idx]
    if event['type'] == 'beg':
        assigned = False
        for y_level, active_genes in enumerate(y_levels):
            conflict = False
            for active_idx in active_genes:
                active_gene = genes[active_idx]
                if not (gene['end'] <= active_gene['start'] or gene['start'] >= active_gene['end']):
                    conflict = True
                    break
            if not conflict:
                genes_y[idx] = y_level
                active_genes.append(idx)
                assigned = True
                break
        if not assigned:
            y_levels.append([idx])
            genes_y[idx] = len(y_levels) - 1
    elif event['type'] == 'end':
        y_level = genes_y[idx]
        y_levels[y_level].remove(idx)

fig = go.Figure()

for idx, gene in enumerate(genes):
    start = gene['start']
    end = gene['end']
    y = genes_y[idx]
    pol = gene['strand']
    color = 'orange' if pol == '+' else 'blue'
    fig.add_trace(go.Scatter(
        x=[start, end],
        y=[y, y],
        mode='lines',
        line=dict(color=color, width=3),
        hoverinfo='text',
        text=f"Gene {idx}<br>Strand: {pol}<br>Start: {start}<br>End: {end}"
    ))

# Adjust layout
fig.update_layout(
    title='Interactive Gene Overlaps Visualization',
    xaxis_title='Base Pairs (bp)',
    yaxis_title='Gene Level',
    hovermode='closest',
    legend_title='Strand',
    showlegend=False,
    width=1200,
    height=600
)

# legend
fig.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='lines',
    line=dict(color='orange'),
    name='+ Strand'
))
fig.add_trace(go.Scatter(
    x=[None],
    y=[None],
    mode='lines',
    line=dict(color='blue'),
    name='- Strand'
))

fig.show()
