---
hide:
  - toc
---

Sabre
=====


Sabre is a tool that will demultiplex barcoded reads into separate files. It will work on both single-end and paired-end data in fastq format. It simply compares the provided barcodes with each read and separates the read into its appropriate barcode file, after stripping the barcode from the read (and also stripping the quality values of the barcode bases).

https://github.com/najoshi/sabre
# Available modules


The overview below shows which Sabre installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using Sabre, load one of these modules using a `module load` command like:

```shell
module load Sabre/2013-09-28-GCC-12.2.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Sabre/2013-09-28-GCC-12.2.0|x|x|x|x|x|x|
