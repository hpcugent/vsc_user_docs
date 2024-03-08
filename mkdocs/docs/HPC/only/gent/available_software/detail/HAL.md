---
hide:
  - toc
---

HAL
===


HAL is a structure to efficiently store and index multiple genome alignmentsand ancestral reconstructions. HAL is a graph-based representation whichprovides several advantages over matrix/block-based formats such as MAF, such asimproved scalability and the ability to perform queries with respect to anarbitrary reference or subtree.This package includes the HAL API and several analysis and conversion toolswhich are described below. HAL files are presently stored in either HDF5 or mmapformat, but we note that the tools and most of the API are format-independent,so other databases could be implemented in the future.

https://github.com/ComparativeGenomicsToolkit/hal
# Available modules


The overview below shows which HAL installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using HAL, load one of these modules using a `module load` command like:

```shell
module load HAL/2.1-foss-2020b
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|HAL/2.1-foss-2020b|-|x|x|x|x|x|


### HAL/2.1-foss-2020b

This is a list of extensions included in the module:

addict-2.2.1, blessed-1.18.1, dill-0.3.4, docker-4.3.1, enlighten-1.10.1, newick-1.3.0, prefixed-0.3.2, toil-5.3.0, websocket-client-1.1.0