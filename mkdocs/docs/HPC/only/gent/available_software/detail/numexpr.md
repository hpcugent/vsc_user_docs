---
hide:
  - toc
---

numexpr
=======


The numexpr package evaluates multiple-operator array expressions many times faster than NumPy can. It accepts the expression as a string, analyzes it, rewrites it more efficiently, and compiles it on the fly into code for its internal virtual machine (VM). Due to its integrated just-in-time (JIT) compiler, it does not require a compiler at runtime.

https://numexpr.readthedocs.io/en/latest/
# Available modules


The overview below shows which numexpr installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using numexpr, load one of these modules using a `module load` command like:

```shell
module load numexpr/2.7.1-intel-2020a-Python-3.8.2
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|numexpr/2.7.1-intel-2020a-Python-3.8.2|x|x|x|x|x|x|
|numexpr/2.7.1-intel-2019b-Python-2.7.16|-|x|-|-|-|x|
|numexpr/2.7.1-foss-2020a-Python-3.8.2|-|x|x|-|x|x|
|numexpr/2.7.1-foss-2019b-Python-3.7.4|-|x|x|-|x|x|
