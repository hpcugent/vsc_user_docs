---
hide:
  - toc
---

Bowtie2
=======


Bowtie 2 is an ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences. It is particularly good at aligning reads of about 50 up to 100s or 1,000s of characters, and particularly good at aligning to relatively long (e.g. mammalian) genomes. Bowtie 2 indexes the genome with an FM Index to keep its memory footprint small: for the human genome, its memory footprint is typically around 3.2 GB. Bowtie 2 supports gapped, local, and paired-end alignment modes.

http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
# Available modules


The overview below shows which Bowtie2 installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using Bowtie2, load one of these modules using a `module load` command like:

```shell
module load Bowtie2/2.4.5-GCC-11.3.0
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Bowtie2/2.4.5-GCC-11.3.0|x|x|x|x|x|x|
|Bowtie2/2.4.4-GCC-11.2.0|x|x|x|-|x|x|
|Bowtie2/2.4.2-GCC-10.2.0|-|x|x|x|x|x|
|Bowtie2/2.4.1-GCC-9.3.0|-|x|x|-|x|x|
|Bowtie2/2.3.5.1-iccifort-2019.5.281|-|x|-|-|-|-|
|Bowtie2/2.3.5.1-GCC-8.3.0|-|x|x|-|x|x|
