---
hide:
  - toc
---

segemehl
========


segemehl is a software to map short sequencer reads to reference genomes.  Unlike other methods, segemehl is able to detect not only mismatches but also insertions  and deletions. Furthermore, segemehl is not limited to a specific read length and is able  to mapprimer- or polyadenylation contaminated reads correctly. segemehl implements a matching  strategy based on enhanced suffix arrays (ESA). Segemehl now supports the SAM format, reads  gziped queries to save both disk and memory space and allows bisulfite sequencing mapping  and split read mapping.

https://www.bioinf.uni-leipzig.de/Software/segemehl/
# Available modules


The overview below shows which segemehl installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using segemehl, load one of these modules using a `module load` command like:

```shell
module load segemehl/0.3.4-GCC-11.2.0
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|segemehl/0.3.4-GCC-11.2.0|x|x|x|x|x|x|
|segemehl/0.3.4-GCC-10.2.0|-|x|x|x|x|x|
