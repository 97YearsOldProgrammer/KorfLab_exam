"""					it's too messed for diretly save the temrinal output				"""
"""					this is the breakdown about how did i do 							"""
"""					there are actually way more steps and trails						"""


# i cannot track how i download miniconda, i did this yesterday 
# after i get conda


conda deactivate 													# exit the base environment
conda create -n blastlegacy -c bioconda blast-legacy				# not working; error: cannot find the package from bioconda
conda search -c bioconda | grep '^blast'							# check whether there is blast-legacy in bioconda

# it took me pretty long to figure this out
# i then decide to download blast manunally from online package
# i download the package manually

conda create --name blastlegacy  									# create environment for this
conda activate
conda install ~/Downloads/blast-legacy-2.2.26-h527b516_4.tar.bz2 	# install blast


blastall --help
formatdb --help

# extract the NP_4146081.1

zless ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa.gz 
touch NP_4146081.faa 
nano NP_4146081.faa 

# start seaching

gunzip ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa.gz
formatdb -i ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa 
blastall -p blastp -i ~/Code/korflab_exam/NP_4146081.faa -d ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa -e 1e-5 -o output.md


# the result: it is stored inside the output.md under this reprocitory

