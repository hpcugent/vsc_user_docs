---
hide:
  - toc
---

QCA
===


Taking a hint from the similarly-named Java Cryptography Architecture, QCA aims to provide a straightforward and cross-platform crypto API, using Qt datatypes and conventions. QCA separates the API from the implementation, using plugins known as Providers. The advantage of this model is to allow applications to avoid linking to or explicitly depending on any particular cryptographic library. This allows one to easily change or upgrade crypto implementations without even needing to recompile the application! QCA should work everywhere Qt does, including Windows/Unix/MacOSX.

https://userbase.kde.org/QCA
# Available modules


The overview below shows which QCA installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using QCA, load one of these modules using a `module load` command like:

```shell
module load QCA/2.3.5-GCCcore-11.2.0
```

*(This data was automatically generated on Fri, 08 Mar 2024 at 09:35:19 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|QCA/2.3.5-GCCcore-11.2.0|x|x|x|x|x|x|
