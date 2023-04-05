# More on the HPC infrastructure
## Filesystems

Multiple different shared filesystems are available on the HPC
infrastructure, each with their own purpose. See 
[chapter *Running jobs with input/output data*, section *Where to store your data on the {{hpc}}* of the HPC manual](../intro-HPC/ch_running_jobs_with_input_output_data.md#where-to-store-your-data-on-the-hpc) for 
a list of available locations.

{% if site==gent %}
### VO storage
If you are a member of a (non-default) virtual organisation (VO), see
[Chapter *Running jobs with input/output data*, the section titled *Virtual Organisations*](../intro-HPC/ch_running_jobs_with_input_output_data.md#virtual-organisations), 
you have access to additional directories (with more quota) on the data and
scratch filesystems, which you can share with other members in the VO.
{% endif %}

### Quota
Space is limited on the cluster's storage. To check your quota, see
[Chapter *Running jobs with input/output data*, section titled *Pre-defined quota* of the HPC manual](../intro-HPC/ch_running_jobs_with_input_output_data.md#pre-defined-quotas).

To figure out where your quota is being spent, the `du` (isk sage)
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

More information is available in [chapter *Running batch jobs* of the HPC manual, section *Modules*](../intro-HPC/ch_running_batch_jobs.md#modules).

## Using the clusters
The use the clusters beyond the login node(s) which have limited resources, you
should create job scripts and submit them to the clusters.

Detailed information is available in [chapter *Running batch jobs* of the HPC manual, section *Defining and submitting your job*](../intro-HPC/ch_running_batch_jobs.md#defining-and-submitting-your-job).

## Exercises

Create and submit a job script that computes the sum of 1-100 using
Python, and prints the numbers to a *unique* output file in
`$VSC_SCRATCH`.

Hint: `python -c "print(sum(range(1, 101)))"`

-   How many modules are available for Python version 3.6.4?
-   How many modules get loaded when you load the `Python/3.6.4-intel-2018a` module?
-   Which `cluster` modules are available?
<!-- -->
-   What's the full path to your personal home/data/scratch directories?
-   Determine how large your personal directories are.
-   What's the difference between the size reported by `du -sh $HOME` and by `ls -ld $HOME`?
