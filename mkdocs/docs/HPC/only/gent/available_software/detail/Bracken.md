---
hide:
  - toc
---

Bracken
=======


Bracken (Bayesian Reestimation of Abundance with KrakEN) is a highly accurate statistical method that computes the abundance of species in DNA sequences from a metagenomics sample. Braken uses the taxonomy labels assigned by Kraken, a highly accurate metagenomics classification algorithm, to estimate the number of reads originating from each species present in a sample. Kraken classifies reads to the best matching location in the taxonomic tree, but does not estimate abundances of species. We use the Kraken database itself to derive probabilities that describe how much sequence from each genome is identical to other genomes in the database, and combine this information with the assignments for a particular sample to estimate abundance at the species level, the genus level, or above. Combined with the Kraken classifier, Bracken produces accurate species- and genus-level abundance estimates even when a sample contains two or more near-identical species.NOTE: Bracken is compatible with both Kraken 1 and Kraken 2. However, the default kmer length is different depending on the version of Kraken used. If you use Kraken 1 defaults, specify 31 as the kmer length. If you use Kraken 2 defaults, specify 35 as the kmer length.

https://ccb.jhu.edu/software/bracken/
# Available modules


The overview below shows which Bracken installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using Bracken, load one of these modules using a `module load` command like:

```shell
module load Bracken/2.9-GCCcore-10.3.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Bracken/2.9-GCCcore-10.3.0|x|x|x|x|x|x|
|Bracken/2.7-GCCcore-11.2.0|x|x|x|-|x|x|
