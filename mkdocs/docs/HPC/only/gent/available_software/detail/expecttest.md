---
hide:
  - toc
---

expecttest
==========


This library implements expect tests (also known as "golden" tests). Expect tests are a method of writing tests where instead of hard-coding the expected output of a test, you run the test to get the output, and the test framework automatically populates the expected output. If the output of the test changes, you can rerun the test with the environment variable EXPECTTEST_ACCEPT=1 to automatically update the expected output.

https://github.com/ezyang/expecttest
# Available modules


The overview below shows which expecttest installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using expecttest, load one of these modules using a `module load` command like:

```shell
module load expecttest/0.1.5-GCCcore-12.3.0
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|expecttest/0.1.5-GCCcore-12.3.0|x|x|x|x|x|x|
|expecttest/0.1.3-GCCcore-12.2.0|x|x|x|x|x|x|
|expecttest/0.1.3-GCCcore-11.3.0|x|x|x|x|x|x|
|expecttest/0.1.3-GCCcore-11.2.0|x|x|x|x|x|x|
|expecttest/0.1.3-GCCcore-10.3.0|x|x|x|x|x|x|
|expecttest/0.1.3-GCCcore-10.2.0|x|-|-|-|-|-|
