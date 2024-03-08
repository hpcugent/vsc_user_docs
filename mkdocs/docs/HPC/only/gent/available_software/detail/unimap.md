---
hide:
  - toc
---

unimap
======


Unimap is a fork of minimap2 optimized for assembly-to-referencealignment. It integrates the minigraph chaining algorithm and can align throughlong INDELs (up to 100kb by default) much faster than minimap2. Unimap is abetter fit for resolving segmental duplications and is recommended over minimap2for alignment between high-quality assemblies.Unimap does not replace minimap2 for other types of alignment. It drops thesupport of multi-part index and short-read mapping. Its long-read alignment isdifferent from minimap2 but is not necessarily better. Unimap is more of aspecialized minimap2 at the moment.

https://github.com/lh3/unimap
# Available modules


The overview below shows which unimap installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using unimap, load one of these modules using a `module load` command like:

```shell
module load unimap/0.1-GCCcore-10.2.0
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|unimap/0.1-GCCcore-10.2.0|-|x|x|x|x|x|
