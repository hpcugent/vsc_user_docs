---
hide:
  - toc
---

GObject-Introspection
=====================


GObject introspection is a middleware layer between C libraries (using GObject) and language bindings. The C library can be scanned at compile time and generate a metadata file, in addition to the actual native C library. Then at runtime, language bindings can read this metadata and automatically provide bindings to call into the C library.

https://gi.readthedocs.io/en/latest/
# Available modules


The overview below shows which GObject-Introspection installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using GObject-Introspection, load one of these modules using a `module load` command like:

```shell
module load GObject-Introspection/1.76.1-GCCcore-12.3.0
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|GObject-Introspection/1.76.1-GCCcore-12.3.0|x|x|x|x|x|x|
|GObject-Introspection/1.74.0-GCCcore-12.2.0|x|x|x|x|x|x|
|GObject-Introspection/1.72.0-GCCcore-11.3.0|x|x|x|x|x|x|
|GObject-Introspection/1.68.0-GCCcore-11.2.0|x|x|x|x|x|x|
|GObject-Introspection/1.68.0-GCCcore-10.3.0|x|x|x|x|x|x|
|GObject-Introspection/1.66.1-GCCcore-10.2.0|x|x|x|x|x|x|
|GObject-Introspection/1.64.0-GCCcore-9.3.0-Python-3.8.2|-|x|x|-|x|x|
|GObject-Introspection/1.63.1-GCCcore-8.3.0-Python-3.7.4|x|x|x|-|x|x|
