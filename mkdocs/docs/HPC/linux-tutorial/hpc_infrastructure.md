# More on the HPC infrastructure
## Filesystems

Multiple different shared filesystems are available on the HPC
infrastructure, each with their own purpose. See section
[Where to store your data on the {{hpc}}](../running_jobs_with_input_output_data.md#where-to-store-your-data-on-the-hpc)
for a list of available locations.

{% if site==gent %}
### VO storage
If you are a member of a (non-default) virtual organisation (VO), see section
[Virtual Organisations](../running_jobs_with_input_output_data.md#virtual-organisations),
you have access to additional directories (with more quota) on the data and
scratch filesystems, which you can share with other members in the VO.
{% endif %}

### Quota
Space is limited on the cluster's storage. To check your quota, see section
[Pre-defined quota](../running_jobs_with_input_output_data.md#pre-defined-quotas).

To figure out where your quota is being spent, the `du` (**d**isk **u**sage)
command can come in useful:
<pre><code>$ <b>du -sh test</b>
59M test
</code></pre>

Do *not* (frequently) run `du` on directories where large amounts of
data are stored, since that will:

1.  take a long time

2.  result in increased load on the shared storage since (the metadata
    of) every file in those directories will have to be inspected.

## Modules

Software is provided through so-called environment modules.

The most commonly used commands are:

1.  `module avail`: show *all* available modules

2.  `module avail <software name>`: show available modules for a
    specific software name

3.  `module list`: show list of loaded modules

4.  `module load <module name>`: load a particular module

More information is available in section
[Modules](../running_batch_jobs.md#modules).

## Using the clusters
The use the clusters beyond the login node(s) which have limited resources, you
should create job scripts and submit them to the clusters.

Detailed information is available in section
[submitting your job](../running_batch_jobs.md#defining-and-submitting-your-job).

## Exercises

??? abstract "Create and submit a job script that computes the sum of 1-100 using Python, and prints the result to the standard output."
    
    We make the following job script:

    ```bash title="jobscript.pbs"
    #!/bin/bash
    
    # Basic parameters
    #PBS -N sum_1_to_100      ## Job name
    #PBS -l nodes=1:ppn=1     ## 1 node, 1 processor per node
    #PBS -l walltime=00:00:15 ## Max time your job will run (no more than 72:00:00)
    
    module load Python/3.10.4-GCCcore-11.3.0
    
    cd $PBS_O_WORKDIR         # Change working directory to the location where the job was submmitted
    
    python -c "print(sum(range(1, 101)))"
    ```

    We optionally switch to a cluster of choice, for example `skitty`:

    ```bashand prints the numbers to a *unique* output file in `$VSC_SCRATCH`.
    $ module swap cluster/skitty
    ```

    We submit the job script:

    ```bash
    $ qsub jobscript.pbs
    ```

    after some time, two files (`sum_1_to_100.e[JOBID]` and `sum_1_to_100.o[JOBID]`) should appear.
    The first one contains the error output, and is empty in this case. 
    The second one contains the output of the Python command.


??? abstract "How many modules are available for Python version 3.10?"
        
    We can use the `module avail` command to list all available modules.
    To filter the list for Python 3.10, we can use `module avail Python/3.10`.

    ```bash
    $ module avail Python/3.10
    ```

??? abstract "How many modules get loaded when you load the `Python/3.10.4-GCCcore-11.3.0` module?"
    
    We can use the `module load` command to load the Python module.
    After loading the module, we can use the `module list` command to list all loaded modules.
    
    ```bash
    $ module load Python/3.10.4-GCCcore-11.3.0
    $ module list
    ```
    
    These are the modules the python module depends on.


??? abstract "Which `cluster` modules are available?"
    
    We can use the `module avail` command to list all available modules.
    To filter the list for modules with the name `cluster`, we can use `module avail cluster`.

    ```bash
    $ module avail cluster
    ```
