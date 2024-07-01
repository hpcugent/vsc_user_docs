---
hide:
  - toc
---

Shasta
======


The goal of the Shasta long read assembler is to rapidly produce accurate assembled sequence using DNA reads generatedby Oxford Nanopore flow cells as input. Computational methods used by the Shasta assembler include:Using a run-length representation of the read sequence. This makes the assembly process more resilient to errors inhomopolymer repeat counts, which are the most common type of errors in Oxford Nanopore reads. Using in some phases ofthe computation a representation of the read sequence based on markers, a fixed subset of short k-mers (k ≈ 10).

https://github.com/chanzuckerberg/shasta
# Available modules


The overview below shows which Shasta installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using Shasta, load one of these modules using a `module load` command like:

```shell
module load Shasta/0.8.0-foss-2020b
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Shasta/0.8.0-foss-2020b|-|x|x|x|x|x|
