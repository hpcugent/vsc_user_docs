---
hide:
  - toc
---

PyTables
========


PyTables is a package for managing hierarchical datasets and designed to efficiently and easily cope with extremely large amounts of data. PyTables is built on top of the HDF5 library, using the Python language and the NumPy package. It features an object-oriented interface that, combined with C extensions for the performance-critical parts of the code (generated using Cython), makes it a fast, yet extremely easy to use tool for interactively browse, process and search very large amounts of data. One important feature of PyTables is that it optimizes memory and disk resources so that data takes much less space (specially if on-flight compression is used) than other solutions such as relational or object oriented databases.

https://www.pytables.org
# Available modules


The overview below shows which PyTables installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using PyTables, load one of these modules using a `module load` command like:

```shell
module load PyTables/3.8.0-foss-2022a
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|PyTables/3.8.0-foss-2022a|x|x|x|x|x|x|
|PyTables/3.6.1-intel-2020b|-|x|x|-|x|x|
|PyTables/3.6.1-intel-2020a-Python-3.8.2|x|x|x|x|x|x|
|PyTables/3.6.1-fosscuda-2020b|-|-|-|-|x|-|
|PyTables/3.6.1-foss-2021b|x|x|x|x|x|x|
|PyTables/3.6.1-foss-2021a|x|x|x|x|x|x|
|PyTables/3.6.1-foss-2020b|-|x|x|x|x|x|
|PyTables/3.6.1-foss-2020a-Python-3.8.2|-|x|x|-|x|x|
|PyTables/3.6.1-foss-2019b-Python-3.7.4|-|x|x|-|x|x|
|PyTables/3.5.2-intel-2019b-Python-2.7.16|-|x|-|-|-|x|


### PyTables/3.8.0-foss-2022a

This is a list of extensions included in the module:

blosc2-2.0.0, tables-3.8.0