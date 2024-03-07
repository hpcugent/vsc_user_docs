---
hide:
  - toc
---

minimap2
========


Minimap2 is a fast sequence mapping and alignmentprogram that can find overlaps between long noisy reads, or map longreads or their assemblies to a reference genome optionally with detailedalignment (i.e. CIGAR). At present, it works efficiently with querysequences from a few kilobases to ~100 megabases in length at an errorrate ~15%. Minimap2 outputs in the PAF or the SAM format. On limitedtest data sets, minimap2 is over 20 times faster than most otherlong-read aligners. It will replace BWA-MEM for long reads and contigalignment.

https://github.com/lh3/minimap2
# Available modules


The overview below shows which minimap2 installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using minimap2, load one of these modules using a `module load` command like:

```shell
module load minimap2/2.26-GCCcore-12.3.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|minimap2/2.26-GCCcore-12.3.0|x|x|x|x|x|x|
|minimap2/2.26-GCCcore-12.2.0|x|x|x|x|x|x|
|minimap2/2.24-GCCcore-11.3.0|x|x|x|x|x|x|
|minimap2/2.24-GCCcore-11.2.0|x|x|x|-|x|x|
|minimap2/2.22-GCCcore-11.2.0|x|x|x|-|x|x|
|minimap2/2.20-GCCcore-10.3.0|x|x|x|-|x|x|
|minimap2/2.20-GCCcore-10.2.0|-|x|x|-|x|x|
|minimap2/2.18-GCCcore-10.2.0|-|x|x|x|x|x|
|minimap2/2.17-GCCcore-9.3.0|-|x|x|-|x|x|
|minimap2/2.17-GCC-8.3.0|-|x|x|-|x|x|
