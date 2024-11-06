Korflab Exam
============

## Contents ##

+ [Part Two Response](#part-two)
+ [Part Three Response](#part_three)
    - [Code](#code-part)
    - [Output](#output)

----------------------------------------------------------------------------
## Part Two ##

<br>

__Q1: Counting how many protein in `*.faa` file__

For `*.faa` file, each `>` means one protein sequence, so we just need to find how many `>` are there.   
By using code below, we could got the output: `4298`

```python
gunzip -c ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa.gz | grep "^>" | wc -l
```

<br>

__Q2: Counting how many coding sequences in `*.gbff` file__

For `*.gbff` file, this is typical genetic bank file that have multiple coding sequence.  
For counting how many coding sequence, we just need to count how many times CDS exits.  
Here is the output: `4357`

```python
gunzip -c ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_genomic.gbff.gz | grep "CDS" | wc -l
```

<br>

__Q3: Why there is such difference__

There is different between coding sequence from `*.gbff` file and `*.faa` file.   
Since there are compliment coding sequence in `*.gbff` file, that's why there is a difference between Q1 and Q2 output.
Here is the sample compliment sequence:

>CDS             complement(993277..994044)

<br>

__Q4: How many tRNA in the `*.gff` file__

For this task, it is kinda straightforward. All we need is tracking the third column of gff file. There are everything about different types of traits of it on there. After filtering everything except the third column, using the cut command. We just need to use the grep and send it toward word count. There are `86` tRNA in the `ecoli.gff`.

```python
gunzip -c ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_genomic.gff.gz | grep -v "^#" | cut -f 3 | grep "^tRNA" | wc -l
```

<br>

__Q5: How many of each type of features in the `*.gff` file__

For the `*.gff` file, the column 3 would be where those features located.   
To filter how much different type of features are there, we could also use uniq to finish that part.  
Below is the code I used for this task:

```python
gunzip -c ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_genomic.gff.gz | grep -v "^#" | cut -f 3 | sort | uniq -c
```

Using the code above, we would get the output in the ascending order as below.

```
Result is:

1    origin_of_replication  
1    region  
22   rRNA
48   sequence_feature
50   mobile_genetic_element
86   tRNA
99   ncRNA
145  pseudogene
207  exon
4337 CDS
4494 gene

```

----------------------------------------------------------------------------

## Part Three ##

### Code part ###

Since I don't save the part how I download the conda from safari. Here is the direct log of how I process with unknown package blast-legacy of conda. Code below is the first part that I tried to find blast-legacy package with conda.

```python
conda deactivate
conda create -n blastlegacy -c bioconda blast-legacy
conda search -c bioconda | grep '^blast'
```

This do not work at first, since the output from terminal always showed that there is no blast-legacy package under bioconda channel. Then I have to download the blast-legacy manually through online open-source website. 

```python
conda create --name blastlegacy 
conda activate
conda install ~/Downloads/blast-legacy-2.2.26-h527b516_4.tar.bz2 
```

I create an environment specifically for blast-legacy so that every package would not messed up inside the base environment. Then I used code to check how these command worked.

```python
blastall --help
formatdb --help
```
We are gonna using protein sequence of `NP_4146081.1`, here is how I extract that into a file so that I can work on this to search similar file using blastall.

```python
zless ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa.gz 
touch NP_4146081.faa 
nano NP_4146081.faa 
```
Code below is the formal search process that what I do for searching this protein sequence with e value 1e-5.

```python
gunzip ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa.gz
formatdb -i ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa 
blastall -p blastp -i ~/Code/korflab_exam/NP_4146081.faa -d ~/Code/korflab_exam/E.coli/GCF_000005845.2_ASM584v2_protein.faa -e 1e-5 -o output
```

### Output ###

Output of the part 3 is stored inside the [output](~/Code/korflab_exam/output.txt) under this repository.  
Here is the cloest protein sequence for `NP_4146081.1`.

```
>NP_415376.4 putrescine ABC transporter ATP binding subunit
           [Escherichia coli str. K-12 substr. MG1655]
          Length = 377
```

