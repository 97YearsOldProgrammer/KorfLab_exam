import argparse
import gzip

parser = argparse.ArgumentParser(description='variant reporter')
parser.add_argument('gff', type=str, help='GFF file (gzip file)')
parser.add_argument('vcf', type=str, help='VCF file (gzip file)')
arg = parser.parse_args()

vcf = {}
gff = {}

# used for later arranging the events
def key_sort(x):
    return (x['position'], priority[ x['type'] ])

# credit to dr.korf, this is so nice
with gzip.open (arg.gff, 'rt') as fp:
    for line in fp:
        x = line.split()
        chm = x[0]
        typ = x[2]
        beg = int( x[3] )
        end = int( x[4] )
        if chm not in gff: gff[chm] = []
        gff[chm].append( (beg, end, typ) )

# collecting location from vcf file
with gzip.open(arg.vcf, 'rt') as fp:
    for line in fp:
        y = line.split()
        chm = y[0]
        location = int( y[1] )               # for later comparison
        if chm not in vcf: vcf[chm] = []
        vcf[chm].append(location)

# repeating over different chromosome
for chm in gff:
    
    # skip those who are mistakenly input mtDNA
    if chm not in vcf: continue

    # sweeping line algorithm
    events = []

    # nested loop for all of the chromosome

    # create event for gcf file
    for beg, end, typ in gff[chm]:
    
        events.append({
            'position': beg,
            'type': 'beg',
            'trait': typ
        })
    
        events.append({
            'position': end,
            'type': 'end',
            'trait': typ
        })

    # create event for vcf file
    for idx, point in enumerate(vcf[chm]):
        events.append({
            'position': point,
            'type': 'point',
            'index': idx
        })

    # priority of event
    priority = {
        'beg': 1,
        'point': 2,
        'end': 3
        }

    # using sort to put those event as a line with order
    events.sort( key = key_sort )

    # creating set for output 
    # idk set, tuition video suggest this

    active = set()
    point_trait = [set() for _ in vcf[chm] ]

    # loop through the events
    for event in events:
    
        if   event['type'] == 'beg': active.add( event['trait'] )
        
        elif event['type'] == 'end':
        
            if event['trait'] in active:
                active.remove( event['trait'] )
        
        elif event['type'] == 'point':
            idx = event['index']
            point_trait[idx] = active.copy() 

    # format output
    for idx, point in enumerate( vcf[chm] ):
        traits = point_trait[idx]
    
        # skip those location without traits
        if traits:
            traits_output = ', '.join(traits)
            print(f'{chm}\t{point}\t{traits_output}') 
