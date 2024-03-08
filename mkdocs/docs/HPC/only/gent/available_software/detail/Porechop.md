---
hide:
  - toc
---

Porechop
========


Porechop is a tool for finding and removing adapters from Oxford Nanopore reads. Adapters on the ends of reads are trimmed off, and when a read has an adapter in its middle, it is treated as chimeric and chopped into separate reads. Porechop performs thorough alignments to effectively find adapters, even at low sequence identity

https://github.com/rrwick/Porechop
# Available modules


The overview below shows which Porechop installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using Porechop, load one of these modules using a `module load` command like:

```shell
module load Porechop/0.2.4-intel-2019b-Python-3.7.4
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Porechop/0.2.4-intel-2019b-Python-3.7.4|-|x|x|-|x|x|
