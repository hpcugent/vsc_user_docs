---
hide:
  - toc
---

pkg-config
==========


pkg-config is a helper tool used when compiling applications and libraries. It helps you insert the correct compiler options on the command line so an application can use gcc -o test test.c `pkg-config --libs --cflags glib-2.0` for instance, rather than hard-coding values on where to find glib (or other libraries).

http://www.freedesktop.org/wiki/Software/pkg-config/
# Available modules


The overview below shows which pkg-config installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using pkg-config, load one of these modules using a `module load` command like:

```shell
module load pkg-config/0.29.2-GCCcore-12.2.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|pkg-config/0.29.2-GCCcore-12.2.0|x|x|x|x|x|x|
|pkg-config/0.29.2-GCCcore-11.3.0|x|x|x|x|x|x|
|pkg-config/0.29.2-GCCcore-11.2.0|x|x|x|x|x|x|
|pkg-config/0.29.2-GCCcore-10.3.0|x|x|x|x|x|x|
|pkg-config/0.29.2-GCCcore-10.2.0|x|x|x|x|x|x|
|pkg-config/0.29.2-GCCcore-9.3.0|x|x|x|x|x|x|
|pkg-config/0.29.2-GCCcore-8.3.0|x|x|x|-|x|x|
|pkg-config/0.29.2-GCCcore-8.2.0|-|x|-|-|-|-|
|pkg-config/0.29.2|x|x|x|-|x|x|
