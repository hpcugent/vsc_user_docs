---
hide:
  - toc
---

SSW
===


SSW is a fast implementation of the Smith-Waterman algorithm, which uses the Single-Instruction Multiple-Data (SIMD) instructions to parallelize the algorithm at the instruction level. SSW library provides an API that can be flexibly used by programs written in C, C++ and other languages. We also provide a software that can do protein and genome alignment directly. Current version of our implementation is ~50 times faster than an ordinary Smith-Waterman. It can return the Smith-Waterman score, alignment location and traceback path (cigar) of the optimal alignment accurately; and return the sub-optimal alignment score and location heuristically.

https://github.com/mengyao/Complete-Striped-Smith-Waterman-Library
# Available modules


The overview below shows which SSW installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using SSW, load one of these modules using a `module load` command like:

```shell
module load SSW/1.1-GCCcore-10.2.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|SSW/1.1-GCCcore-10.2.0|-|x|x|-|x|x|
