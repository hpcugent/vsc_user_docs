{% set directory="/arcanine/scratch/gent/apps/AlphaFold" %}
{% set version="20230310" %}
{% set readme="https://github.com/deepmind/alphafold/blob/main/README.md" %}
## What is AlphaFold?

AlphaFold is an AI system developed by DeepMind that predicts a protein’s 3D structure from its amino acid sequence. 
It aims to achieve accuracy competitive with experimental methods.

See <https://www.vscentrum.be/alphafold> for more information and there you can also find a getting started video recording if you prefer that. 

## Documentation & extra material

This chapter focuses specifically on the use of AlphaFold on the {{hpcinfra}}.
It is intented to augment the existing AlphaFold documentation rather than replace it.
It is therefore recommended to first familiarize yourself with AlphaFold. The following resources can be helpful:

- AlphaFold website: <https://alphafold.com/>
- AlphaFold repository: <https://github.com/deepmind/alphafold/tree/main>
- AlphaFold FAQ: <https://alphafold.com/faq>
- VSC webpage about AlphaFold: <https://www.vscentrum.be/alphafold>
- Introductory course on AlphaFold by VIB: <https://elearning.vib.be/courses/alphafold>
- "Getting Started with AlphaFold" presentation by Kenneth Hoste (HPC-UGent)
    - recording available [on YouTube](https://www.youtube.com/watch?v=jP9Qg1yBGcs)
    - slides available [here (PDF)](https://www.vscentrum.be/_files/ugd/5446c2_f19a8723f7f7460ebe990c28a53e56a2.pdf?index=true)
    - see also <https://www.vscentrum.be/alphafold>


## Using AlphaFold on {{hpcinfra}}

Several different versions of AlphaFold are installed on both the CPU and GPU HPC-UGent Tier-2 clusters, see the output of `module avail AlphaFold`.
If you run this command on a [GPU cluster](gpu.md), additional CUDA modules will show up:

```shell
$ module avail AlphaFold

------------ /apps/gent/RHEL8/cascadelake-volta-ib/modules/all -------------
   AlphaFold/2.0.0-fosscuda-2020b
   AlphaFold/2.1.1-fosscuda-2020b
   AlphaFold/2.1.2-foss-2021a-CUDA-11.3.1
   AlphaFold/2.2.2-foss-2021a-CUDA-11.3.1
   AlphaFold/2.3.0-foss-2021b-CUDA-11.4.1
   AlphaFold/2.3.1-foss-2022a-CUDA-11.7.0

--------------- /apps/gent/RHEL8/cascadelake-ib/modules/all ----------------
   AlphaFold/2.0.0-foss-2020b    AlphaFold/2.3.1-foss-2022a
   AlphaFold/2.1.2-foss-2021a    AlphaFold/2.3.4-foss-2022a-ColabFold (D)
   AlphaFold/2.2.2-foss-2021a

```

To use AlphaFold, you should load a particular module, for example:

```shell
module load AlphaFold/2.3.1-foss-2022a-CUDA-11.7.0
```

!!! Tip "We strongly advise loading a specific version of an AlphaFold module, so you know exactly which version is being used."

!!! Warning
    
    When using AlphaFold, you should submit jobs to a GPU cluster for better performance, see [GPU clusters](gpu.md).
    Later in this chapter, you will find a comparison between running AlphaFold on CPUs or GPUs.

Multiple revisions of the large database (~2.5TB) that is also required to run AlphaFold have been
made available on the HPC-UGent infrastructure in a central location ({{directory}}), 
so you do not have to download it yourself.

```shell
$ ls /arcanine/scratch/gent/apps/AlphaFold
20210812  20211201  20220701  20230310
```

The directories located there indicate when the data was downloaded, so that this leaves room for providing updated datasets later.

As of writing this documentation the latest version is `20230310`.

!!! Info
    
    The `arcanine scratch` shared filesystem is powered by fast SSD disks, 
    which is recommended for the AlphaFold data, because of random access I/O patterns.
    See [Pre-defined user directories](http://localhost:8000/HPC/Gent/running_jobs_with_input_output_data/#pre-defined-user-directories) to get more info about the arcanine filesystem.

The AlphaFold installations we provide have been modified a bit to facilitate the usage on {{hpcinfra}}.

### Setting up the environment

The location to the AlphaFold data can be specified via the `$ALPHAFOLD_DATA_DIR` environment variable, so you should define this variable in your AlphaFold job script:

```shell
export ALPHAFOLD_DATA_DIR={{directory}}/{{version}}
```

!!! Warning "Use newest version"
    
    Do not forget to replace `{{version}}` with a more up to date version if available.

### Running AlphaFold

AlphaFold provides run script called [run_alphafold.py](https://raw.githubusercontent.com/deepmind/alphafold/main/run_alphafold.py)

A symbolic link named *alphafold* that points to the this script is included,
so you can just use `alphafold` instead of `run_alphafold.py` or `python run_alphafold.py` after loading the AlphaFold module.

The `run_alphafold.py` script has also been slightly modified such that defining the `$ALPHAFOLD_DATA_DIR` (see [above](./#setting-up-the-environment)) is sufficient to pick up all the data provided in that location,
so you don't need to use options like `--data_dir` to specify the location of the data.

Similarly, the script was also tweaked such that the location to commands like `hhblits,hhsearch,jackhmmer,kalign` are already correctly set, so options like `--hhblits_binary_path` are **not** required.

For more information about the script and options see [this section]({{readme}}#running-alphafold) in the official [README]({{readme}}).

!!! WARNING "READ README"

    It is **strongly** advised to read the official [README]({{readme}}) provided by DeepMind before continuing.
    

### Controlling core count for `hhblits` and `jackhmmer`

The Python scripts that are used to run ***hhblits and jackhmmer*** have been tweaked so you can control how many cores are used for these tools,
rather than hardcoding it to 4 and 8 cores, respectively.

Using the `$ALPHAFOLD_HHBLITS_N_CPU` environment variable, you can specify how many cores should be used for running `hhblits`;
the default of 4 cores will be used if `$ALPHAFOLD_HHBLITS_N_CPU` is not defined. 

Likewise for `jackhmmer`, the core count can be controlled via `$ALPHAFOLD_JACKHMMER_N_CPU`.

!!! Info

    Tweaking this might not yield significant benefits, 
    as we have noticed that these tools may exhibit slower performance when utilizing more than 4/8 cores (though this behavior could vary based on the workload).

### CPU/GPU comparison

The provided timings were obtained by executing the `T1050.fasta` example, as outlined in the Alphafold [README]({{readme}}). 
For the corresponding jobscripts, they are available [here](./example-jobscripts).

Using `--db_preset=full_dbs`, the following runtime data was collected:

* CPU-only, on doduo, using 24 cores (1 node): 9h 9min
* CPU-only, on doduo, using 96 cores (1 full node): 12h 22min
* GPU on joltik, using 1 V100 GPU + 8 cores: 2h 20min
* GPU on joltik, using 2 V100 GPUs + 16 cores: 2h 16min

This highlights a couple of important attention points:

* Running AlphaFold on GPU is significantly faster than CPU-only (close to 4x faster for this particular example).
* Using more CPU cores may lead to *longer* runtimes, so be careful with using full nodes when running AlphaFold CPU-only.
* Using multiple GPUs results in barely any speedup (for this particular T1050.fasta example).

With `--db_preset=casp14`, it is clearly more demanding:

* On doduo, with 24 cores (1 node): still running after 48h...
* On joltik, 1 V100 GPU + 8 cores: 4h 48min

This highlights the difference between CPU and GPU performance even more.

## Example scenario

The following example comes from the official [Examples section]({{readme}}#examples) in the Alphafold [README]({{readme}}).
The run command is slightly different (see above: [Running AlphaFold](./running-alphafold)).

Do not forget to setup the environment (see above: [Setting up the environment](./setting-up-the-environment)).

### Folding a monomer

Say we have a monomer with the sequence `<SEQUENCE>`.
Create a file `monomer.fasta` with the following content:
```fasta
>sequence_name
<SEQUENCE>
```

Then run the following command in the same directory:
```shell
alphafold 
  --fasta_paths=monomer.fasta \
  --max_template_date=2021-11-01 \
  --model_preset=monomer \
  --output_dir=.
```

See [AlphaFold output]({{readme}}#alphafold-output), for information about the outputs.

!!! Info
    
    For more scenarios see the [example section]({{readme}}#examples) in the official [README]({{readme}}).
    

## Example jobscripts

The following two example job scripts can be used as a starting point for running AlphaFold.

The main difference between using a GPU or CPU in a job script is what module to load.
For running AlphaFold on GPU, use an AlphaFold module that mentions `CUDA` (or `cuda`),
for example `AlphaFold/2.3.1-foss-2022a-CUDA-11.7.0`.

To run the jobs cripts you need to create a file named `T1050.fasta` with the following content:

```fasta
>T1050 A7LXT1, Bacteroides Ovatus, 779 residues|
MASQSYLFKHLEVSDGLSNNSVNTIYKDRDGFMWFGTTTGLNRYDGYTFKIYQHAENEPGSLPDNYITDIVEMPDGRFWINTARGYVLFDKERDYFITDVTGFMKNLESWGVPEQVFVDREGNTWLSVAGEGCYRYKEGGKRLFFSYTEHSLPEYGVTQMAECSDGILLIYNTGLLVCLDRATLAIKWQSDEIKKYIPGGKTIELSLFVDRDNCIWAYSLMGIWAYDCGTKSWRTDLTGIWSSRPDVIIHAVAQDIEGRIWVGKDYDGIDVLEKETGKVTSLVAHDDNGRSLPHNTIYDLYADRDGVMWVGTYKKGVSYYSESIFKFNMYEWGDITCIEQADEDRLWLGTNDHGILLWNRSTGKAEPFWRDAEGQLPNPVVSMLKSKDGKLWVGTFNGGLYCMNGSQVRSYKEGTGNALASNNVWALVEDDKGRIWIASLGGGLQCLEPLSGTFETYTSNNSALLENNVTSLCWVDDNTLFFGTASQGVGTMDMRTREIKKIQGQSDSMKLSNDAVNHVYKDSRGLVWIATREGLNVYDTRRHMFLDLFPVVEAKGNFIAAITEDQERNMWVSTSRKVIRVTVASDGKGSYLFDSRAYNSEDGLQNCDFNQRSIKTLHNGIIAIGGLYGVNIFAPDHIRYNKMLPNVMFTGLSLFDEAVKVGQSYGGRVLIEKELNDVENVEFDYKQNIFSVSFASDNYNLPEKTQYMYKLEGFNNDWLTLPVGVHNVTFTNLAPGKYVLRVKAINSDGYVGIKEATLGIVVNPPFKLAAALQHHHHHH
```
<sub>source: <https://www.predictioncenter.org/casp14/target.cgi?target=T1050&view=sequence></sub>


### Job script for running AlphaFold on GPU

Job script that runs AlphaFold on GPU using 1 V100 GPU + 8 cores.

Swap to the `joltik` GPU before submitting it:

```shell
module swap cluster/joltik
```

<center>-- AlphaFold-gpu-joltik.sh --</center>

```bash
{% include "./examples/AlphaFold/AlphaFold-gpu-joltik.sh" %}
```

### Job script for running AlphaFold CPU-only

Jobscript that runs AlphaFold on CPU using 24 cores on one node.

<center>-- AlphaFold-cpu-doduo.sh --</center>

```bash
{% include "./examples/AlphaFold/AlphaFold-cpu-doduo.sh" %}
```

In case of problems or questions, don't hesitate to contact use at <{{hpcinfo}}>.
