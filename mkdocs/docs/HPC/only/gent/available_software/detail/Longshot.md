---
hide:
  - toc
---

Longshot
========


Longshot is a variant calling tool for diploid genomes using long error prone reads such as Pacific Biosciences (PacBio) SMRT and Oxford Nanopore Technologies (ONT). It takes as input an aligned BAM file and outputs a phased VCF file with variants and haplotype information. It can also output haplotype-separated BAM files that can be used for downstream analysis. Currently, it only calls single nucleotide variants (SNVs).

https://github.com/pjedge/longshot
# Available modules


The overview below shows which Longshot installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using Longshot, load one of these modules using a `module load` command like:

```shell
module load Longshot/0.4.5-GCCcore-11.3.0
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Longshot/0.4.5-GCCcore-11.3.0|x|x|x|x|x|x|
|Longshot/0.4.3-GCCcore-10.2.0|-|-|x|-|x|-|
|Longshot/0.4.1-GCCcore-8.3.0|-|x|-|-|-|-|
