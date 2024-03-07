---
hide:
  - toc
---

PyVCF3
======


A VCFv4.0 and 4.1 parser for Python. The intent of this module is to mimic thecsv module in the Python stdlib, as opposed to more flexible serializationformats like JSON or YAML. vcf will attempt to parse the content of each recordbased on the data types specified in the meta-information lines -- specificallythe ##INFO and ##FORMAT lines. If these lines are missing or incomplete, itwill check against the reserved types mentioned in the spec. Failing that, itwill just return strings.PyVCF3 has been created because the Official PyVCF repository is no longermaintained and do not accept any pull requests. This fork is for python 3 onlyand has been published on pyPI as PyVCF3.

https://github.com/dridk/PyVCF3
# Available modules


The overview below shows which PyVCF3 installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using PyVCF3, load one of these modules using a `module load` command like:

```shell
module load PyVCF3/1.0.3-GCCcore-11.3.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|PyVCF3/1.0.3-GCCcore-11.3.0|x|x|x|x|x|x|


### PyVCF3/1.0.3-GCCcore-11.3.0

This is a list of extensions included in the module:

PyVCF3-1.0.3