import argparse
import gzip

# i don't quite understand the overlap problme
# here is what i did for unit 9 comparing. C.elegan.gff and C.elegan.vcf
# this is one part of it; not the everything between two file

parser = argparse.ArgumentParser(description='variant reporter')
parser.add_argument('gff', type=str, help='GFF file')
parser.add_argument('vcf', type=str, help='VCF file')
arg = parser.parse_args()

# creating dictionary for storing data

vcf = {  	'I':	[],
			'II': 	[],
			'III':	[],
			'IV':	[],
			'V':	[],
			'X':	[],		}

# collecting location from vcf file

with gzip.open(arg.vcf, 'rt') as fp:
	for line in fp:
		line = line.split()
		if line == '': break
		head = line[0]
		location = line[1]
		vcf[head].append(location)

# collecting information from gff file

index = []									# for the lower and upper bound

with gzip.open (arg.gff, 'rt') as fp:

	gff = {}
	variant = {}							# where we use number as key, value as variant type
	a = -1

	for line in fp:
		line = line.split()	
		a += 1

		if line[0] == 'I' and line[0].endswith('I'): 
			variant[a]= line[2]				# where we record different types of variant
			bound = (line[3], line[4])
			index.append(bound)


d = dict()

for i in vcf['I']: 							# plan on doing it seperately, start with catagory 'I'

	if bool(d):
		output = [k for k, v in d.items() if not v and k]
		output = ','.join(output)
		print(f'I\t{j}\t{output}')

	i = int(i)								# convert string into integer for later comparison
	j = i
	n = -1									# indice for the variant output to dictionary D
	c = 0
	d = dict()								# a diciontary used for storing unique type of variant
	loopkiller = False

	
	for lb, ub in index:
		
		lb = int(lb)
		ub = int(ub)

		n += 1
		if loopkiller: 	break				# do output while also break
		
		if  lb <= i and i <= ub: 

			c += 1							# count how many times has been within the range
			d[variant[n]] = ''

			if c >= 300:					# start time saver
				loopkiller = True			# since it is impossible for a value to have 300 times same variant inside it