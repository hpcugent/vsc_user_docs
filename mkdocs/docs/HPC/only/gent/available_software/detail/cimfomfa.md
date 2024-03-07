---
hide:
  - toc
---

cimfomfa
========


This library supports both MCL, a cluster algorithm for graphs, and zoem, amacro/DSL language. It supplies abstractions for memory management, I/O,associative arrays, strings, heaps, and a few other things. The string libraryhas had heavy testing as part of zoem. Both understandably and regrettably Ichose long ago to make it C-string-compatible, hence nul bytes may not be partof a string. At some point I hope to rectify this, perhaps unrealistically.

https://github.com/micans/cimfomfa
# Available modules


The overview below shows which cimfomfa installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using cimfomfa, load one of these modules using a `module load` command like:

```shell
module load cimfomfa/22.273-GCCcore-12.3.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|cimfomfa/22.273-GCCcore-12.3.0|x|x|x|x|x|x|
