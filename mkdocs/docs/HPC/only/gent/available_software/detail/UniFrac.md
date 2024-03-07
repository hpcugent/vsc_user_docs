---
hide:
  - toc
---

UniFrac
=======


UniFrac is the de facto repository for high-performance phylogenetic diversitycalculations. The methods in this repository are based on an implementation ofthe Strided State UniFrac algorithm which is faster, and uses less memory thanFast UniFrac. Strided State UniFrac supports Unweighted UniFrac, WeightedUniFrac, Generalized UniFrac, Variance Adjusted UniFrac and meta UniFrac, inboth double and single precision (fp32). This repository also includes StackedFaith (manuscript in preparation), a method for calculating Faith's PD that isfaster and uses less memory than the Fast UniFrac-based referenceimplementation.

https://github.com/biocore/unifrac-binaries
# Available modules


The overview below shows which UniFrac installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using UniFrac, load one of these modules using a `module load` command like:

```shell
module load UniFrac/1.3.2-foss-2022a
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|UniFrac/1.3.2-foss-2022a|x|x|x|x|x|x|
