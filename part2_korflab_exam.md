"""					here is the output for part2 of korflab_exam				"""
#
#
#
#



# Q1:	counting how many protein in *.faa file
# 
# gunzip -c ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa.gz | grep -v "^>" | wc -c
#

Result is:

 1348714



# Q2:	counting how many coding sequences in *.gbff file
#
# gunzip -c ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_genomic.gbff.gz | grep "^\s*/translation=" | cut -d '=' -f2 | cut -c 2- | wc -c 
#

"""					this code could be better, some " notation be removed for more precise ouput 			"""

Result is:

  191054



# Q3:	why there is such huge difference
#
# I think gbff file contain translation information of CDS, btw for each CDS, there could be 
# ultilze, arranged, and combine in several way for different function
#



# Q4:	how many tRNA in the *.gff file
# 
# gunzip -c ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_genomic.gff.gz | grep -v "^#" | cut -f 3 | grep "^tRNA" | wc -l
# 

Result is:

      86



# Q5:	how many of each type of features in the *.gff file
#
# gunzip -c ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_genomic.gff.gz | grep -v "^#" | cut -f 3 | sort | uniq -c 
#

Result is:

   1 origin_of_replication
   1 region
  22 rRNA
  48 sequence_feature
  50 mobile_genetic_element
  86 tRNA
  99 ncRNA
 145 pseudogene
 207 exon
4337 CDS
4494 gene





