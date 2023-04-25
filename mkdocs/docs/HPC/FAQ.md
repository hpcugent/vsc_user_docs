# Frequently Asked Questions (FAQ)

{% if site == gent %}

New users should consult the [Introduction to HPC](https://www.ugent.be/hpc/en/training/2022/introhpcugent)
and the [HPC user manual](https://www.ugent.be/hpc/en/support/documentation.htm) to get started.

The [HPC user manual](https://www.ugent.be/hpc/en/support/documentation.htm) is a great resource
for troubleshooting and looking up specifics.

If you want to use software that's not yet installed on the HPC, send us a
[software installation request](https://www.ugent.be/hpc/en/support/software-installation-request).

Overview of HPC-UGent Tier-2 infrastructure:
[https://www.ugent.be/hpc/en/infrastructure](https://www.ugent.be/hpc/en/infrastructure)

{% endif %}

## Composing a job

### How many cores/nodes should I request?

An important factor in this question is how well your task is being parallellized:
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
[software installation request](https://www.ugent.be/hpc/en/support/software-installation-request).
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
[software installation request](https://www.ugent.be/hpc/en/support/software-installation-request).
{% endif %}

It is possible to use the modules without specifying a version or toolchain. However,
this will probably cause incompatible modules to be loaded. Don't do it if you use multiple modules.
Even if it works now, as more modules get installed on the HPC, your job can suddenly break.

### Job script template

This is a template for a job script, with commonly used parameters.
The basic parameters should always be used. Some notes on the situational parameters:

*   `-l mem`: If no memory parameter is given, the job gets access to an amount of
    memory proportional to the amount of cores requested.
    See also: [Job failed: SEGV Segmentation fault](#job-failed-segv-segmentation-fault)

*   `-m/-M`: the `-m` option will send emails to your email address registerd with VSC.
    Only if you want emails at some other address, you should use the `-M` option.

*   Replace the "`-placeholder text-`" with real entries.
    This notation is used to ensure `qsub` rejects invalid options.

*   To use a situational parameter, remove one '`#`' at the beginning of the line.

```shell
#!/bin/bash

# Basic parameters
#PBS -N jobname           ## Job name
#PBS -l nodes=1:ppn=2     ## 1 node, 2 processors per node (ppn=all to get a full node)
#PBS -l walltime=01:00:00 ## Max time your job will run (no more than 72:00:00)

# Situational parameters: remove one '#' at the front to use
##PBS -l gpus=1            ## GPU amount (only on accelgor or joltik)
##PBS -l mem=32gb          ## If not used, memory will be available proportional to the max amount
##PBS -m abe               ## Email notifications (abe=aborted, begin and end)
##PBS -M -email_address-   ## ONLY if you want to use a different email than your VSC address
##PBS -A -project-         ## Project name when credits are required (only Tier 1)

##PBS -o -filename-        ## Output log
##PBS -e -filename-        ## Error log


module load [module]
module load [module]

cd $PBS_O_WORKDIR         # Change working directory to the location where the job was submmitted

[commands]
```

Some [Job script examples](../jobscript_examples).

## Troubleshooting jobs

### My modules don't work together

When incompatible modules are loaded, you might encounter an error like this:

Lmod has detected the following error: A different version of the 'GCC' module
is already loaded (see output of 'ml').
You should load another 'foss' module for that is compatible with the currently
loaded version of 'GCC'.
Use 'ml spider foss' to get an overview of the available versions.

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
* Use a faster [cluster](https://www.ugent.be/hpc/en/infrastructure).
* Divide the job into more parallel processes.
* Divide the job into shorter processes, which you can submit as separate jobs.
* Use the built-in checkpointing of your software.

### Job failed: SEGV Segmentation fault

Any error mentioning SEGV or Segmentation fault/violation has something to do with a memory error.
If you weren't messing around with memory-unsafe applications or programming, your job probably hit its memory limit.

When there's no memory amount specified in a job script, your job will get access to a proportional
share of the total memory on the node: If you request a full node, all memory will be available.
If you request 8 cores on a cluster where nodes have 2x18 cores, you will get 8/36 = 2/9
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
Then, you are acting as a node on that cluster instead of a login node. Notably, the slaking
cluster will grant such a session immediately, while other clusters might make you wait a bit.
Example command: `ml sw cluster/slaking && qsub -I -l nodes=1:ppn=8`

See also: [Running interactive jobs](../running_interactive_jobs).

### My job isn't using any GPUs

Only two clusters have GPUs. Check out the [infrastructure overview](https://www.ugent.be/hpc/en/infrastructure),
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

Not all file locations perform the same. In particular, the \\$VSC\_HOME and \\$VSC\_DATA
directories are, relatively, very slow to access. Your jobs should rather use the
\\$VSC_SCRATCH directory, or other fast locations (depending on your needs), described
in [Where to store your data on the HPC](../running_jobs_with_input_output_data/#where-to-store-your-data-on-the-hpc).
As an example how do this: The job can copy the input to the scratch directory, then execute
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

<pre><code>$ <b>mympirun --output output.txt ./hello.sh</b>
</code></pre>

### When will my job start?

{% if site == gent%}
See the explanation about how jobs get prioritized in [When will my job start](../running_batch_jobs/#when-will-my-job-start). 

{% else %}

In practice it's
impossible to predict when your job(s) will start, since most currently
running jobs will finish before their requested walltime expires, and
new jobs by may be submitted by other users that are assigned a higher
priority than your job(s). You can use the `showstart` command. For more
information, see .

{% endif %}

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
See <http://www.vub.ac.be/sites/vub/files/reglement-gebruik-ict-infrastructuur.pdf>.
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

<pre><code>$ <b>setfacl -m u:otheruser:r dataset.txt</b>
$ <b>ls -l dataset.txt</b>
-rwxr-x---+ 2 {{userid}} mygroup      40 Apr 12 15:00 dataset.txt
</code></pre>

For more information about `chmod` or `setfacl`, see
[Linux tutorial](https://hpcugent.github.io/vsc_user_docs/linux-tutorial/manipulating_files_and_directories/#changing-permissions-chmod).
<!-- % \section{I no longer work for \university, can I transfer my data to another researcher working at \university}
% See https://github.com/hpcugent/vsc_user_docs/issues/230 -->

### Can I use multiple different SSH key pairs to connect to my VSC account?

Yes, and this is recommended when working from different computers.
Please see [Adding multiple SSH public keys](../account/#adding-multiple-ssh-public-keys-optional) on how to do this.

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

### Is my connection compromised? Remote host identification has changed

On Monday 25 April 2022, the login nodes received an update to RHEL8.
This means that the host keys of those servers also changed. As a result,
you could encounter the following warnings.

MacOS & Linux (on Windows, only the second part is shown):

```shell
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
xx:xx:xx.
Please contact your system administrator.
Add correct host key in /home/hostname/.ssh/known_hosts to get rid of this message.
Offending RSA key in /var/lib/sss/pubconf/known_hosts:1
RSA host key for user has changed and you have requested strict checking.
Host key verification failed.
```

Please follow the instructions at <https://www.ugent.be/hpc/en/infrastructure/migration\_to\_rhel8>
to ensure it really _is not a hacking attempt_ \- you will find the correct host key to compare.
You will also find how to hide the warning.

### VO: how does it work?

A Virtual Organisation consists of a number of members and moderators. A moderator can:

*   Manage the VO members (but can't access/remove their data on the system).

*   See how much storage each member has used, and set limits per member.

*   Request additional storage for the VO.

One person can only be part of one VO, be it as a member or moderator.
It's possible to leave a VO and join another one. However, it's not
recommended to keep switching between VO's (to supervise groups, for example).

See also: [Virtual Organisations](../running_jobs_with_input_output_data/#virtual-organisations).

{% if site == gent %}
### My UGent shared drives don't show up

After mounting the UGent shared drives with `kinit your_email@ugent.be`,
you might not see an entry with your username when listing `ls /UGent`.
This is normal: try `ls /UGent/your_username` or `cd /UGent/your_username`, and you should be able to access the drives.
Be sure to use your UGent username and not your VSC username here.

See also: [Your UGent home drive and shares](../running_jobs_with_input_output_data/#your-ugent-home-drive-and-shares).
{% endif %}

### I have another question/problem

Who can I contact?

*   General questions regarding HPC-UGent and VSC: <hpc@ugent.be>

*   HPC-UGent Tier-2: <hpc@ugent.be>

*   VSC Tier-1: <compute@vscentrum.be>

*   VSC Tier-1 cloud: <cloud@vscentrum.be>
