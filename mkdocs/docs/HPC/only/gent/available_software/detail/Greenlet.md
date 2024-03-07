---
hide:
  - toc
---

Greenlet
========


The greenlet package is a spin-off of Stackless, a version of CPython thatsupports micro-threads called "tasklets". Tasklets run pseudo-concurrently (typically in a singleor a few OS-level threads) and are synchronized with data exchanges on "channels".A "greenlet", on the other hand, is a still more primitive notion of micro-thread with no implicitscheduling; coroutines, in other words. This is useful when you want to control exactly when your code runs.

https://github.com/python-greenlet/greenlet
# Available modules


The overview below shows which Greenlet installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using Greenlet, load one of these modules using a `module load` command like:

```shell
module load Greenlet/2.0.2-foss-2022b
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Greenlet/2.0.2-foss-2022b|x|x|x|x|x|x|
|Greenlet/2.0.2-foss-2022a|x|x|x|x|x|x|
