# Frequently Asked Questions (FAQ)

{% if site == gent %}

New users should consult the [Introduction to HPC](https://www.ugent.be/hpc/en/training/2023/introhpcugent)
to get started, which is a great resource for learning the basics, troubleshooting, and looking up specifics.

If you want to use software that's not yet installed on the HPC, send us a
[software installation request]({{ hpc_software_install }}).

Overview of HPC-UGent Tier-2 [infrastructure]({{ hpc_infrastructure_url }})

{% endif %}

## Composing a job

### How many cores/nodes should I request?

An important factor in this question is how well your task is being parallelized:
does it actually run faster with more resources? You can test this yourself:
start with 4 cores, then 8, then 16... The execution time should each time be reduced to
around half of what it was before. You can also try this with full nodes: 1 node, 2 nodes.
A rule of thumb is that you're around the limit when you double the resources but the
execution time is still ~60-70% of what it was before. That's a signal to stop increasing the core count.

See also: [Running batch jobs](../running_batch_jobs).

### Which packages are available?

When connected to the HPC, use the commands `module avail [search_text]` and `module spider [module]`
to find installed modules and get information on them.

Among others, many packages for both Python and R are readily available on the HPC.
These aren't always easy to find, though, as we've bundled them together.

Specifically, the module `SciPy-bundle` includes numpy, pandas, scipy and a few others.
For R, the normal R module has many libraries included. The bundle `R-bundle-Bioconductor`
contains more libraries.
Use the command `module spider [module]` to find the specifics on these bundles.

{% if site == gent %}
If the package or library you want is not available, send us a
[software installation request]({{ hpc_software_install }}).
{% endif %}

### How do I choose the job modules?

Modules each come with a suffix that describes the _toolchain_ used to install them.

Examples:

*   AlphaFold/2.2.2-**foss-2021a**

*   tqdm/4.61.2-**GCCcore-10.3.0**

*   Python/3.9.5-**GCCcore-10.3.0**

*   matplotlib/3.4.2-**foss-2021a**

Modules from the same toolchain always work together, and modules from a
\*different version of the same toolchain\* never work together.

The above set of modules works together: an overview of compatible toolchains can be found here:
<https://docs.easybuild.io/en/latest/Common-toolchains.html#overview-of-common-toolchains>.

You can use `module avail [search_text]` to see which versions on which toolchains are available to use.

{% if site == gent %}
If you need something that's not available yet, you can request it through a
[software installation request]({{ hpc_software_install }}).
{% endif %}

It is possible to use the modules without specifying a version or toolchain. However,
this will probably cause incompatible modules to be loaded. Don't do it if you use multiple modules.
Even if it works now, as more modules get installed on the HPC, your job can suddenly break.

## Troubleshooting

### My modules don't work together

When incompatible modules are loaded, you might encounter an error like this:

```shell
{{ lmod_error }}
```

You should load another `foss` module for that is compatible with the currently
loaded version of `GCC`.
Use `ml spider foss` to get an overview of the available versions.

Modules from the same toolchain always work together, and modules from a
_different version of the same toolchain_ never work together.

An overview of compatible toolchains can be found here:
<https://docs.easybuild.io/en/latest/Common-toolchains.html#overview-of-common-toolchains>.

See also: [How do I choose the job modules?](#how-do-i-choose-the-job-modules)

### My job takes longer than 72 hours

The 72 hour walltime limit will not be extended. However, you can work around this barrier:

* Check that all available resources are being used. See also:
    * [How many cores/nodes should I request?](#how-many-coresnodes-should-i-request).
    * [My job is slow](#my-job-runs-slower-than-i-expected).
    * [My job isn't using any GPUs](#my-job-isnt-using-any-gpus).
* Use a faster [cluster]({{ hpc_infrastructure_url }}).
* Divide the job into more parallel processes.
* Divide the job into shorter processes, which you can submit as separate jobs.
* Use the built-in checkpointing of your software.

### Job failed: SEGV Segmentation fault

Any error mentioning `SEGV` or ` Segmentation fault/violation` has something to do with a memory error.
If you weren't messing around with memory-unsafe applications or programming, your job probably hit its memory limit.

When there's no memory amount specified in a job script, your job will get access to a proportional
share of the total memory on the node: If you request a full node, all memory will be available.
If you request `8` cores on a cluster where nodes have `2x18` cores, you will get `8/36 = 2/9`
of the total memory on the node.

Try requesting a bit more memory than your proportional share, and see if that solves the issue.

See also: [Specifying memory requirements](../fine_tuning_job_specifications/#specifying-memory-requirements).

### My compilation/command fails on login node

When logging in, you are using a connection to the login nodes. There are somewhat strict
limitations on what you can do in those sessions: check out the output of `ulimit -a`.
Specifically, the memory and the amount of processes you can use may present an issue.
This is common with MATLAB compilation and Nextflow. An error caused by the login session
limitations can look like this: `Aborted (core dumped)`.

It's easy to get around these limitations: start an interactive session on one of the clusters.
Then, you are acting as a node on that cluster instead of a login node. Notably, the
[debug/interactive cluster](../interactive_debug) will grant such a session immediately, while other clusters might make you wait a bit.
Example command: `ml swap cluster/donphan && qsub -I -l nodes=1:ppn=8`

See also: [Running interactive jobs](../running_interactive_jobs).

### My job isn't using any GPUs

Only two clusters have GPUs. Check out the [infrastructure overview]({{ hpc_infrastructure_url }}),
to see which one suits your needs. Make sure that you manually switch to the GPU cluster _before_ you submit
the job. Inside the job script, you need to explicitly request the GPUs:
`#PBS -l nodes=1:ppn=24:gpus=2`

Some software modules don't have GPU support, even when running on the GPU cluster. For example,
when running `module avail alphafold` on the joltik cluster, you will find versions on both
the _foss_ toolchain and the _fossCUDA_ toolchain. Of these, only the _CUDA_ versions will
use GPU power. When in doubt, CUDA means GPU support.

{% if site == gent %}
See also: [HPC-UGent GPU clusters](../gpu_gent).
{% endif %}

### My job runs slower than I expected

There are a few possible causes why a job can perform worse than expected.

Is your job using all the available cores you've requested? You can test this by increasing and
decreasing the core amount: If the execution time stays the same, the job was not using all cores.
Some workloads just don't scale well with more cores. If you expect the job to be very parallelizable
and you encounter this problem, maybe you missed some settings that enable multicore execution.
See also: [How many cores/nodes should i request?](#how-many-coresnodes-should-i-request)

Does your job have access to the GPUs you requested?
See also: [My job isn't using any GPUs](#my-job-isnt-using-any-gpus)

Not all file locations perform the same. In particular, the `$VSC_HOME` and `$VSC_DATA`
directories are, relatively, very slow to access. Your jobs should rather use the
`$VSC_SCRATCH` directory, or other fast locations (depending on your needs), described
in [Where to store your data on the HPC](../running_jobs_with_input_output_data/#where-to-store-your-data-on-the-hpc).
As an example how to do this: The job can copy the input to the scratch directory, then execute
the computations, and lastly copy the output back to the data directory.
Using the home and data directories is especially a problem when UGent isn't your home institution:
your files may be stored, for example, in Leuven while you're running a job in Ghent.

### My MPI job fails

Use `mympirun` in your job script instead of `mpirun`. It is a tool that makes sure everything
gets set up correctly for the HPC infrastructure. You need to load it as a module in your
job script: `module load vsc-mympirun`.

To submit the job, use the `qsub` command rather than `sbatch`. Although both will submit a job,
`qsub` will correctly interpret the `#PBS` parameters inside the job script. `sbatch` might not
set the job environment up correctly for mympirun/OpenMPI.

See also: [Multi core jobs/Parallel Computing](../multi_core_jobs)
and [Mympirun](../mympirun).

### `mympirun` seems to ignore its arguments

For example, we have a simple script (`./hello.sh`):

```bash
#!/bin/bash 
echo "hello world"
```

And we run it like `mympirun ./hello.sh --output output.txt`.

To our surprise, this doesn't output to the file `output.txt`, but to
standard out! This is because `mympirun` expects the program name and
the arguments of the program to be its last arguments. Here, the
`--output output.txt` arguments are passed to `./hello.sh` instead of to
`mympirun`. The correct way to run it is:

```shell
mympirun --output output.txt ./hello.sh
```

### When will my job start?

{% if site == gent%}
See the explanation about how jobs get prioritized in [When will my job start](../running_batch_jobs/#when-will-my-job-start). 

{% else %}

In practice, it's
impossible to predict when your job(s) will start, since most currently
running jobs will finish before their requested walltime expires. 
New jobs may be submitted by other users that are assigned a higher
priority than your job(s). 
You can use the `squeue --start` command to get an estimated start time for your jobs in the queue.
Keep in mind that this is just an estimate.

{% endif %}


### Why do I get a "No space left on device" error, while I still have storage space left?

When trying to create files, errors like this can occur:

```shell
No space left on device
```

The error "`No space left on device`" can mean two different things:

- all available *storage quota* on the file system in question has been used;
- the *inode limit* has been reached on that file system.

An *inode* can be seen as a "file slot", meaning that when the limit is reached, no more additional files can be created.
There is a standard inode limit in place that will be increased if needed. 
The number of inodes used per file system can be checked on [the VSC account page](https://account.vscentrum.be).

Possible solutions to this problem include cleaning up unused files and directories or 
[compressing directories with a lot of files into zip- or tar-files](linux-tutorial/manipulating_files_and_directories.md#zipping-gzipgunzip-zipunzip).

If the problem persists, feel free to [contact support](FAQ.md#i-have-another-questionproblem).

## Other

### Can I share my account with someone else?

**NO.** You are not allowed to share your VSC account with anyone else, it is
strictly personal. 
{% if site == gent %}
See
<https://helpdesk.ugent.be/account/en/regels.php>. 
{% endif %}
{% if site == leuven %}
For KU Leuven, see
<https://admin.kuleuven.be/personeel/english_hrdepartment/ICT-codeofconduct-staff#section-5>.
For Hasselt University, see <https://www.uhasselt.be/intra/IVC>. 
{% endif %}
{% if site == brussel %}
See <https://www.vub.ac.be/sites/vub/files/reglement-gebruik-ict-infrastructuur.pdf>.
{% endif %}
{% if site == antwerpen %}
See <https://pintra.uantwerpen.be/bbcswebdav/xid-23610_1> 
{% endif %}
{% if site == gent %}
If you want to share data, there are alternatives (like a shared directories in VO
space, see [Virtual organisations](../running_jobs_with_input_output_data/#virtual-organisations)).
{% endif %}

### Can I share my data with other {{hpc}} users?

Yes, you can use the `chmod` or `setfacl` commands to change permissions
of files so other users can access the data. For example, the following
command will enable a user named "otheruser" to read the file named
`dataset.txt`. See

```
$ setfacl -m u:otheruser:r dataset.txt
$ ls -l dataset.txt
-rwxr-x---+ 2 {{userid}} mygroup      40 Apr 12 15:00 dataset.txt
```

For more information about `chmod` or `setfacl`, see
[Linux tutorial](linux-tutorial/manipulating_files_and_directories.md#changing-permissions-chmod).

### Can I use multiple different SSH key pairs to connect to my VSC account?

Yes, and this is recommended when working from different computers.
Please see [Adding multiple SSH public keys](account.md#adding-multiple-ssh-public-keys-optional) on how to do this.

### I want to use software that is not available on the clusters yet

{% if site == gent %}

Please fill out the details about the software and why you need it in
this form:
<https://www.ugent.be/hpc/en/support/software-installation-request>.
When submitting the form, a mail will be sent to {{hpcinfo}} containing all the
provided information. The HPC team will look into your request as soon
as possible you and contact you when the installation is done or if
further information is required. 
{% else %}
Please send an e-mail to {{hpcinfo}} that includes:

-   What software you want to install and the required version

-   Detailed installation instructions

-   The purpose for which you want to install the software

{% endif %}

If the software is a Python package, you can manually
[install it in a virtual environment](./setting_up_python_virtual_environments.md).
Note that it is still preferred to submit a software installation request, 
as the software installed by the HPC team will be optimized for the HPC environment.
This can lead to dramatic performance improvements.

!!! warning
    Do not use `pip install --user` to install software, as this places packages 
    in `~/.local/lib/python*/site-packages`, potentially causing conflicts with software installed by the HPC team. 
    
    Also, avoid using `pip install --prefix` or `pip install --target` with `$PYTHONPATH`, 
    since `$PYTHONPATH` is a global setting that affects all Python versions.
    When `$PYTHONPATH` includes directories with packages from different Python versions, it can lead to conflicts. 

    Instead, use a Python virtual environment for package installations in your home directory. 
    For guidance on setting up virtual environments, 
    refer to the [Python virtual environments setup guide](./setting_up_python_virtual_environments.md).

### VO: how does it work?

A Virtual Organisation consists of a number of members and moderators. A moderator can:

*   Manage the VO members (but can't access/remove their data on the system).

*   See how much storage each member has used, and set limits per member.

*   Request additional storage for the VO.

One person can only be part of one VO, be it as a member or moderator.
It's possible to leave a VO and join another one. However, it's not
recommended to keep switching between VO's (to supervise groups, for example).

See also: [Virtual Organisations](running_jobs_with_input_output_data.md#virtual-organisations).

{% if site == gent %}
### My UGent shared drives don't show up

After mounting the UGent shared drives with `kinit your_email@ugent.be`,
you might not see an entry with your username when listing `ls /UGent`.
This is normal: try `ls /UGent/your_username` or `cd /UGent/your_username`, and you should be able to access the drives.
Be sure to use your UGent username and not your VSC username here.

See also: [Your UGent home drive and shares](running_jobs_with_input_output_data.md#your-ugent-home-drive-and-shares).
{% endif %}


### My home directory is (almost) full, and I don't know why

Your home directory might be full without looking like it due to hidden files.
Hidden files and subdirectories have a name starting with a dot and do not show up when running `ls`.
If you want to check where the storage in your home directory is used, you can make use of the [`du` command](running_jobs_with_input_output_data.md#check-your-quota) to find out what the largest files and subdirectories are:

```shell
du -h --max-depth 1 $VSC_HOME | egrep '[0-9]{3}M|[0-9]G'
```

The `du` command returns the size of every file and subdirectory in the $VSC_HOME directory. This output is then piped into an [`egrep`](linux-tutorial/beyond_the_basics.md#searching-file-contents-grep) to filter the lines to the ones that matter the most.

The `egrep` command will only let entries that match with the specified regular expression `[0-9]{3}M|[0-9]G` through, which corresponds with files that consume more than 100 MB.


### How can I get more storage space?


[By default](running_jobs_with_input_output_data.md#quota) you get 3 GB of storage space for your home directory and 25 GB in your personal directories on both the data (`$VSC_DATA`) and scratch (`$VSC_SCRATCH`) filesystems.
It is not possible to expand the storage quota for these personal directories.

You can get more storage space through a [Virtual Organisation (VO)](running_jobs_with_input_output_data.md#virtual-organisations),
which will give you access to the [additional directories](running_jobs_with_input_output_data.md#vo-directories) in a subdirectory specific to that VO (`$VSC_DATA_VO` and `$VSC_SCRATCH_VO`).
The moderators of a VO can [request more storage](running_jobs_with_input_output_data.md#requesting-more-storage-space) for their VO.


### Why can't I use the `sudo` command?

When you attempt to use sudo, you will be prompted for a password. 
However, you cannot enter a valid password because this feature is reserved exclusively for HPC administrators.

`sudo` is used to execute a command with administrator rights, which would allow you to make system-wide changes.
You are only able to run commands that make changes to the directories that your VSC account has access to,
like your home directory, your personal directories like $VSC_DATA and $VSC_SCRATCH, 
or shared VO/group directories like $VSC_DATA_VO and $VSC_SCRATCH_VO.

A lot of tasks can be performed without `sudo`, including installing software in your own account.

**Installing software**

- If you know how to install the software without using `sudo`, you are welcome to proceed with the installation.
- If you are unsure how to install the software, you can submit a [software installation request](https://www.ugent.be/hpc/en/support/software-installation-request), and the HPC-UGent support team will handle the installation for you.


### I have another question/problem

Who can I contact?

*   General questions regarding HPC-UGent and VSC: <hpc@ugent.be>

*   HPC-UGent Tier-2: <hpc@ugent.be>

*   VSC Tier-1 compute: <compute@vscentrum.be>

*   VSC Tier-1 cloud: <cloud@vscentrum.be>
