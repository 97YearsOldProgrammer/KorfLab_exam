## Korflab_exam Direction ##


+ [Part 2](part2_part3.md)
+ [Part 3](part2_part3.md)
+ [Part 4]()
    + [entropy.py](part4_entropy.py)
    + [kmer.py](part4_kmer.py)
    + [kozak.py](part4_kozak.py)
    + [overlap.py](part4_overlap.py)
    
----------------------------------------------------------------------------------------------------

## Version Information ##

+ [2nd](#2nd)
+ [3rd](#3rd)
+ [4th](#4th)

------------------------------------------------------------------------------

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

------------------------------------------------------------------------------

## 4th ##
Probably this gonna be the last version of this exam, or it should have been. Since everything would be works okay for the korf labbioinformatics exam. I just haven't move the reprocitory for not sending Dr.korf another URL. There are two majority update for this verion, one is minor, another, kinda also minor.  

## Kozak ##
Just refresh my biological perspective about eukaryotes. Right now I understand those split in `.gbff` are actually not split genes. Now the Kozak sequence gonna be okay. Here is the quick link to the new [kozak.py](part4_kozak.py).

## Overlap ##

### time report ###

This time we have the brand new overlap here. I basically modified based on the sweeping line algorithm for previous overlap problem of `gff and vcf` file of C.elegans. I hope it wouldn't have biological problem with my understanding toward overlap gene in this one that compare two `gff` file. Thus, it would takes more time for finish it. Otherwise, it gonna makes me like a dumb. By the way, it actually take 

> __0:00:00.023074__ seconds  
__785__ overlap genes exit in E.coli gff file.  

Well, the time actually take 4 time less than what we spend on comparing gff and vcf file. I guess this is somehow understandable and explainable, since the __time complexity__ are different. Numerically, 

> it gonna take __2*n + m__ for vcf and gcf of C.elegan  
> it gonna take __2*n + i__ for gff of E.coli  
>> n is (number of genes in gff)  
>> m is number of base pair in vcf)
>> i is the maximum number of overlap gene in E.coli at per overlapped region

and there are _10474_ base pair spot in vcf, _21770_ different trait and combination in gff fr C.elegan, which in total is _32244_. Wow, about the E.coli, there are _4337_ CDS and __about__ _785_ gene, which in total is _5122_. Now it's could be numerically explainable this is faster than previous task. 

### pros and cons ###
This algorithm is pretty fast, even though I am not sure about other algorithm for this overlap gene. Btw I guess there isn't few that are faster than this. Then, what's pros and cons about it?

>pros: fast  
>cons: the actual time complexity for me to take on this task is __2*n + (i-1)!__  

Notice there is actually a factorial notation on there, which means it gonna be really bad once we have to use it on a larger gene dataset. Something just wrong with the code that it is not the fastest way for it should be. This could be improved, btw I just need more time __~~lazy~~__. In reality, there are actually less than _785_ overlap gene in E.coli. Since each time there are region that are more than 2, there would be 1 more overlapped gene. Luckily, there isn't that much overlap gene that satisfied this condition in E.coli.

### visualization ###
There is one thing that brothers me a lot. That in reality, for problems that mostly I am gonna to encounter, there isn't actually answer to it, or I have to figure this out very seriously. Since I don't know how many overlap gene are there, there is also no online research paper that reports it. Generative AI ain't that reliable on this stuff. Thus, I have to have faith on myself. Then, I tried two ways for generating plot for this part. 

The first one it [matplot](overlap_visualize1.py). I would say it is a definitely bad choice for doing so, and nobody want to do so.   
The second one is a download package with suggestion from generative AI by using [plotly](overlap_visualize2.py). This kinda better than using the matplot, btw it definitely requires more edition for a fit version of overlap gene. 
