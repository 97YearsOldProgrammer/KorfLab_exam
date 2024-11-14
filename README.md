# Korflab_exam Direction


+ [Part 2](part2_part3.md)
+ [Part 3](part2_part3.md)
+ [Part 4]()
    + [entropy.py](part4_entropy.py)
    + [kmer.py](part4_kmer.py)
    + [kozak.py](part4_kozak.py)
    + [overlap.py](part4_overlap.py)
    
----------------------------------------------------------------------------------------------------

## Version Information ##

<br>

## 2nd ##

This is the second version of korf_lab exam. There are tons of update from its previous version.  
In this version, we have:  

+ Correct `.md` format for part 2 and part 3  
+ Integrated library coding for part4 python codes
    - neater overall coding
    - usage for defined function
    - corrected [entropy.py](part4_entropy.py)

------------------------------------------------------------------------------


## 3rd ##

This is the log for third version of korf_lab exam. Except minor changes in part 2. The majority update for this version is part4 of exam.  
In this version, we have:

+ [entropy](part4_entropy.py) 
    + have a new softmask
+ [kmer](part4_kmer.py)
    + using sliding window algorithmn instead of itertool
    + two kinds of algorithm ( [kmer1](part4_kmer.py) and [kmer2](part4_kmer_reallyfaster.py) )
+ [kozak](part4_kozak.py)
    + Program would now open the file once
    + complement strand is also included
    + position become -10 and +1 (not sure, btw same as MCB185)
    
<br>

### Entropy ###

There is a new softmask option for swtiching between lowercase or N for low entropy region.


### Kmer ###

I tried to run my first response that used itertool and putting everything into the dictionary. It perform horrible with high k-value. That's totally reasonable. Then, I realize it would be way better if we actually do the simple sliding window algorithmn here, since we don't need to actually report the missing k-mers for this task. Here is what I get for how long it took for whole script [kmer_program](part4_kmer.py) on the both E.coli forward and reverse DNA sequence.

> when k = 40, it take  
0:00:40.051787  

I remember from MCB185, there is once mentioned we could do another type of kmer then stepping through each k-valued sequence, using the method to remove the last and then add the first character of k-valued sequence. [new kmer](part4_kmer_reallyfaster.py). It just a little bit faster.

> when k = 40, it take   
0:00:38.731973

### Kozak ###

It now support reading the complement strand. Actually, this is not that hard for doing that. Update overall code style tideness. It also now would finish everything with opening file once. I also have question on the split part of the gene bank file.

### Overlap ###

I learn about we could do like a statistical index like `zipcode` as Dr.Korf mentioned to me last time. So that we could escape repetiting everything through each boundary with time complexity m*n for a single chromosome. I don't figured out this actually, rather I did `sweep-line algorithm` for this. This only take 

>0:00:00.087278 seconds

to operate on every chromosome between gff and vcf file. The previous algorithm take 

>0:00:02.079991 

on a single chromosome I. And it gonna be around **12.48** seconds 6*02.079991 for six chromosomes of C.elegan. If we do divid them up, we would see this is **143** times faster. What a tremendous improve. I know we supposed not to search or grap information from online sources, which is the rule of this test. Btw I come up with idea that this task for reaching overlap between gff and vcf is similar to the idea:

+ each chromosome = A straight line in one dimension space 
+ each boundary in gff file = A colorful (their trait) segementation 
+ each location in vcf file = A spot on the line

Uh, and I just searched up the algorithm for seperating different segments on a huge line. It comes up with the sweeping line algorithm. I think this gonna fits more for this question. Since,

+ the output trait gonna be more precise
+ not sure, btw it would be faster

### Bed, gff Overlap ###

Sadly, I tried for multiple website like NCBI, ensembl, UCSC browser. Like non of them worked. UCSC is the one that most likely work, btw it failed with some obscured issue. I know it is essential to be a bioinformatics with such ability to extract information. I should learn this. Maybe I would find gff --> bed converter to do that by myself.