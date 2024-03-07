---
hide:
  - toc
---

LLVM
====


The LLVM Core libraries provide a modern source- and target-independent optimizer, along with code generation support for many popular CPUs (as well as some less common ones!) These libraries are built around a well specified code representation known as the LLVM intermediate representation ("LLVM IR"). The LLVM Core libraries are well documented, and it is particularly easy to invent your own language (or port an existing compiler) to use LLVM as an optimizer and code generator.

https://llvm.org/
# Available modules


The overview below shows which LLVM installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using LLVM, load one of these modules using a `module load` command like:

```shell
module load LLVM/16.0.6-GCCcore-12.3.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|LLVM/16.0.6-GCCcore-12.3.0|x|x|x|x|x|x|
|LLVM/15.0.5-GCCcore-12.2.0|x|x|x|x|x|x|
|LLVM/14.0.6-GCCcore-12.3.0-llvmlite|x|x|x|x|x|x|
|LLVM/14.0.6-GCCcore-12.2.0-llvmlite|x|x|x|x|x|x|
|LLVM/14.0.3-GCCcore-11.3.0|x|x|x|x|x|x|
|LLVM/12.0.1-GCCcore-11.2.0|x|x|x|x|x|x|
|LLVM/11.1.0-GCCcore-10.3.0|x|x|x|x|x|x|
|LLVM/11.0.0-GCCcore-10.2.0|x|x|x|x|x|x|
|LLVM/10.0.1-GCCcore-10.2.0|-|x|x|x|x|x|
|LLVM/9.0.1-GCCcore-9.3.0|-|x|x|-|x|x|
|LLVM/9.0.0-GCCcore-8.3.0|x|x|x|-|x|x|
|LLVM/8.0.1-GCCcore-8.3.0|x|x|x|-|x|x|
|LLVM/7.0.1-GCCcore-8.2.0|-|x|-|-|-|-|
