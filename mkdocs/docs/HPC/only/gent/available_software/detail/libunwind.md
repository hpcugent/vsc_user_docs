---
hide:
  - toc
---

libunwind
=========


The primary goal of libunwind is to define a portable and efficient C programming interface (API) to determine the call-chain of a program. The API additionally provides the means to manipulate the preserved (callee-saved) state of each call-frame and to resume execution at any point in the call-chain (non-local goto). The API supports both local (same-process) and remote (across-process) operation. As such, the API is useful in a number of applications

https://www.nongnu.org/libunwind/
# Available modules


The overview below shows which libunwind installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using libunwind, load one of these modules using a `module load` command like:

```shell
module load libunwind/1.6.2-GCCcore-12.3.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|libunwind/1.6.2-GCCcore-12.3.0|x|x|x|x|x|x|
|libunwind/1.6.2-GCCcore-12.2.0|x|x|x|x|x|x|
|libunwind/1.6.2-GCCcore-11.3.0|x|x|x|x|x|x|
|libunwind/1.5.0-GCCcore-11.2.0|x|x|x|x|x|x|
|libunwind/1.4.0-GCCcore-10.3.0|x|x|x|x|x|x|
|libunwind/1.4.0-GCCcore-10.2.0|x|x|x|x|x|x|
|libunwind/1.3.1-GCCcore-9.3.0|-|x|x|-|x|x|
|libunwind/1.3.1-GCCcore-8.3.0|x|x|x|-|x|x|
|libunwind/1.3.1-GCCcore-8.2.0|-|x|-|-|-|-|
