---
hide:
  - toc
---

IDBA-UD
=======


IDBA-UD is a iterative De Bruijn Graph De Novo Assembler for Short ReadsSequencing data with Highly Uneven Sequencing Depth. It is an extension of IDBA algorithm.IDBA-UD also iterates from small k to a large k. In each iteration, short and low-depthcontigs are removed iteratively with cutoff threshold from low to high to reduce the errorsin low-depth and high-depth regions. Paired-end reads are aligned to contigs and assembledlocally to generate some missing k-mers in low-depth regions. With these technologies, IDBA-UDcan iterate k value of de Bruijn graph to a very large value with less gaps and less branchesto form long contigs in both low-depth and high-depth regions.

https://i.cs.hku.hk/~alse/hkubrg/projects/idba_ud/
# Available modules


The overview below shows which IDBA-UD installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using IDBA-UD, load one of these modules using a `module load` command like:

```shell
module load IDBA-UD/1.1.3-GCC-11.2.0
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|IDBA-UD/1.1.3-GCC-11.2.0|x|x|x|-|x|x|
|IDBA-UD/1.1.3-GCC-10.2.0|-|x|x|x|x|x|
