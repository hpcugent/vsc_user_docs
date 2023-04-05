{% set exampledir = 'examples/Running_jobs_with_input_output_data' %}

# Running jobs with input/output data

You have now learned how to start a batch job and how to start an
interactive session. The next question is how to deal with input and
output files, where your standard output and error messages will go to
and where that you can collect your results.

## The current directory and output and error files

### Default file names

First go to the directory:

<pre><code><b>$ cd ~/{{ exampledir }}</b>
</code></pre>

List and check the contents with:

<pre><code><b>ls -l</b>
total 2304
-rwxrwxr-x 1 {{ userid }}   682 Sep 13 11:34 file1.py
-rw-rw-r-- 1 {{ userid }}   212 Sep 13 11:54 file1a.pbs
-rw-rw-r-- 1 {{ userid }}   994 Sep 13 11:53 file1b.pbs
-rw-rw-r-- 1 {{ userid }}   994 Sep 13 11:53 file1c.pbs
-rw-r--r-- 1 {{ userid }}  1393 Sep 13 10:41 file2.pbs
-rwxrwxr-x 1 {{ userid }}  2393 Sep 13 10:40 file2.py
-rw-r--r-- 1 {{ userid }}  1393 Sep 13 10:41 file3.pbs
-rwxrwxr-x 1 {{ userid }}  2393 Sep 13 10:40 file3.py
</code></pre>

Now, let us inspect the contents of the first executable (which is just
a Python script with execute permission).

<center>-- file1.py --</center>
```python
{% include "./examples/Running_jobs_with_input_output_data/file1.py" %}
```

The code of the Python script, is self explanatory:

1.  In step 1, we write something to the file `hello.txt` in the current
    directory.

2.  In step 2, we write some text to stdout.

3.  In step 3, we write to stderr.

Check the contents of the first job script:

<center>-- file1a.pbs --</center>
```bash
{% include "./examples/Running_jobs_with_input_output_data/file1a.pbs" %}
```

You'll see that there are NO specific PBS directives for the placement
of the output files. All output files are just written to the standard
paths.

Submit it:

<pre><code><b>$ qsub file1a.pbs</b>
</code></pre>

After the job has finished, inspect the local directory again, i.e., the
directory where you executed the *qsub* command:

<pre><code><b>ls -l</b>
total 3072
-rw-rw-r-- 1 {{ userid }}   90 Sep 13 13:13 Hello.txt
-rwxrwxr-x 1 {{ userid }}  693 Sep 13 13:03 file1.py*
-rw-rw-r-- 1 {{ userid }}  229 Sep 13 13:01 file1a.pbs
-rw------- 1 {{ userid }}   91 Sep 13 13:13 file1a.pbs.e{{ jobid }}
-rw------- 1 {{ userid }}  105 Sep 13 13:13 file1a.pbs.o{{ jobid }}
-rw-rw-r-- 1 {{ userid }}  143 Sep 13 13:07 file1b.pbs
-rw-rw-r-- 1 {{ userid }}  177 Sep 13 13:06 file1c.pbs
-rw-r--r-- 1 {{ userid }} 1393 Sep 13 10:41 file2.pbs
-rwxrwxr-x 1 {{ userid }} 2393 Sep 13 10:40 file2.py*
-rw-r--r-- 1 {{ userid }} 1393 Sep 13 10:41 file3.pbs
-rwxrwxr-x 1 {{ userid }} 2393 Sep 13 10:40 file3.py*
</code></pre>

Some observations:

1.  The file `Hello.txt` was created in the current directory.

2.  The file `file1a.pbs.o{{ jobid }}` contains all the text that was written to
    the standard output stream ("stdout").

3.  The file `file1a.pbs.e{{ jobid }}` contains all the text that was written to
    the standard error stream ("stderr").

Inspect their contents ... and remove the files

<pre><code><b>$ cat Hello.txt</b>
<b>$ cat file1a.pbs.o{{ jobid }}</b>
<b>$ cat file1a.pbs.e{{ jobid }}</b>
<b>$ rm Hello.txt file1a.pbs.o{{ jobid }} file1a.pbs.e{{ jobid }}</b>
</code></pre>

!!! tip
    Type `cat H` and press the Tab button (looks like ++tab++), and it **expand** will into
    `cat Hello.txt`.

### Filenames using the name of the job

Check the contents of the job script and execute it.

<center>-- file1b.pbs --</center>
```bash
{% include "./examples/Running_jobs_with_input_output_data/file1b.pbs" %}
```

Inspect the contents again ... and remove the generated files:

<pre><code><b>$ ls</b>
Hello.txt file1a.pbs file1c.pbs file2.pbs file3.pbs my_serial_job.e{{ jobid }}
file1.py* file1b.pbs file2.py* file3.py* my_serial_job.o{{ jobid }}
<b>$ rm Hello.txt my_serial_job.*</b>
</code></pre>

Here, the option "`-N`" was used to explicitly assign a name to the job.
This overwrote the JOBNAME variable, and resulted in a different name
for the *stdout* and *stderr* files. This name is also shown in the
second column of the "`qstat`" command. If no name is provided, it
defaults to the name of the job script.

### User-defined file names

You can also specify the name of *stdout* and *stderr* files explicitly
by adding two lines in the job script, as in our third example:

<center>-- file1c.pbs --</center>
```bash
{% include "./examples/Running_jobs_with_input_output_data/file1c.pbs" %}
```

## Where to store your data on the HPC

The {{ hpc }} cluster offers their users several locations to store their data.
Most of the data will reside on the shared storage system, but all
compute nodes also have their own (small) local disk.

### Pre-defined user directories

Three different pre-defined user directories are available, where each
directory has been created for different purposes. The best place to
store your data depends on the purpose, but also the size and type of
usage of the data.

The following locations are available:
<table>
    <tr>
        <td colspan="1">
            <b>Variable</b>
        </td>
        <td colspan="1">
            <b>Description</b>
        </td>
    </tr>
    <tr>
        <td colspan="2">
            <center><i>Long-term storage slow filesystem, intended for smaller files</i></center>
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <t>$VSC_HOME</t>
        </td>
        <td colspan="1">
            For your configuration files and other small files, see <a href="./#your-home-directory-vsc_home">the section on your home directory.</a>
            The default directory is <tt>user/{{ site }}/xxx/{{ userid }}</tt>.
            The same file system is accessible from all sites, i.e., you'll see the same contents in $VSC_HOME on all sites.
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <t>$VSC_DATA</t>
        </td>
        <td colspan="1">
            A bigger "workspace", for <b>datasets</b>, results, logfiles, etc. see <a href="./#your-data-directory-vsc_data">the section on your data directory.</a>
            The default directory is <tt>data/{{ site }}/xxx/{{ userid }}</tt>.
            The same file system is accessible from all sites.
        </td>
    </tr>
    <tr>
        <td colspan="2">
            <center><i>Fast temporary storage</i></center>
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <t>$VSC_SCRATCH_NODE</t>
        </td>
        <td colspan="1">
            For <b>temporary</b> or transient data on the local compute node, where fast access is important; see <a href="./#your-scratch-space-vsc_scratch">the section on your scratch space.</a>
            This space is available per node. The default directory is <tt>/tmp</tt>. On different nodes, you'll see different content.
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <t>$VSC_SCRATCH</t>
        </td>
        <td colspan="1">
            For <b>temporary</b> or transient data that has to be accessible from all nodes of a cluster (including the login nodes) <br>
            The default directory is <tt>scratch/{{ site }}/xxx/{{ userid }}</tt>. This directory is cluster- or site-specific: On different sites, and sometimes on different clusters on the same site, you'll get a different directory with different content.
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <t>$VSC_SCRATCH_SITE</t>
        </td>
        <td colspan="1">
            Currently the same as $VSC_SCRATCH, but could be used for a scratch space shared accross all clusters at a site in the future. See <a href="./#your-scratch-space-vsc_scratch">the section on your scratch space.</a>
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <t>$VSC_SCRATCH_GLOBAL</t>
        </td>
        <td colspan="1">
            Currently the same as $VSC_SCRATCH, but could be used for a scratch space shared accross all clusters of the VSC in the future. See <a href="./#your-scratch-space-vsc_scratch">the section on your scratch space.</a>
        </td>
    </tr>
{% if site == gent %}
    <tr>
        <td colspan="1">
            <t>$VSC_SCRATCH_CLUSTER</t>
        </td>
        <td colspan="1">
            The scratch filesystem closest to the cluster.
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <t>$VSC_SCRATCH_ARCANINE</t>
        </td>
        <td colspan="1">
            A separate (smaller) shared scratch filesystem, powered by SSDs. This scratch filesystem is intended for very I/O-intensive workloads. Note that this filesystem is not available on the cluster victini.
        </td>
    </tr>
{% endif %}
</table>

Since these directories are not necessarily mounted on the same
locations over all sites, you should always (try to) use the environment
variables that have been created.

We elaborate more on the specific function of these locations in the
following sections.

{% if site == gent %}
Note: `$VSC_SCRATCH_KYUKON` and `$VSC_SCRATCH` are the same directories
("kyukon" is the name of the storage cluster where the default shared
scratch filesystem is hosted).

For documentation about VO directories, see [the section on VO directories](./#vo-directories).
{% endif %}
### Your home directory ($VSC_HOME)

Your home directory is where you arrive by default when you login to the
cluster. Your shell refers to it as "~" (tilde), and its absolute path is
also stored in the environment variable $VSC_HOME. Your home directory
is shared across all clusters of the VSC.

The data stored here should be relatively small (e.g., no files or
directories larger than a few megabytes), and preferably should only
contain configuration files. Note that various kinds of configuration
files are also stored here, e.g., by MATLAB, Eclipse, ...

The operating system also creates a few files and folders here to manage
your account. Examples are:

| File or Directory | Description |
|:-----------------:|:------------:|
| .ssh/             | This directory contains some files necessary for you to login to the cluster and to submit jobs on the cluster. Do not remove them, and do not alter anything if you don't know what you are doing!|
| .bash_profile | When you login (type username and password) remotely via ssh, .bash_profile is executed to configure your shell before the initial command prompt.|
| .bashrc | This script is executed every time you start a session on the cluster: when you login to the cluster and when a job starts. |
| .bash_history | This file contains the commands you typed at your shell prompt, in case you need them again.|

{% if site != gent %}
Furthermore, we have initially created some files/directories there
(tutorial, docs, examples, examples.pbs) that accompany this manual and
allow you to easily execute the provided examples.
{% endif %}

### Your data directory ($VSC_DATA)

In this directory you can store all other data that you need for longer
terms (such as the results of previous jobs, ...). It is a good place
for, e.g., storing big files like genome data.

The environment variable pointing to this directory is $VSC_DATA. This
volume is shared across all clusters of the VSC. There are however no
guarantees about the speed you will achieve on this volume. For
guaranteed fast performance and very heavy I/O, you should use the
scratch space instead. 

{% if site == gent %}
If you are running out of quota on your
_$VSC_DATA filesystem you can request a VO. See on how to do this.
{% endif %}

### Your scratch space ($VSC_SCRATCH)

To enable quick writing from your job, a few extra file systems are
available on the compute nodes. These extra file systems are called
scratch folders, and can be used for storage of temporary and/or
transient data (temporary results, anything you just need during your
job, or your batch of jobs).

You should remove any data from these systems after your processing them
has finished. There are no guarantees about the time your data will be
stored on this system, and we plan to clean these automatically on a
regular base. The maximum allowed age of files on these scratch file
systems depends on the type of scratch, and can be anywhere between a
day and a few weeks. We don't guarantee that these policies remain
forever, and may change them if this seems necessary for the healthy
operation of the cluster.

Each type of scratch has its own use:

**Node scratch ($VSC_SCRATCH_NODE).**   Every node has its own scratch space, which is completely separated
    from the other nodes. On some clusters, it will be on a local disk
    in the node, while on other clusters it will be emulated through
    another file server. In many cases, it will be significantly slower
    than the cluster scratch as it typically consists of just a single
    disk. Some **drawsbacks** are that the storage can only be accessed on that
    particular node and that the capacity is often very limited (e.g.,
    100 GB). The performance will depend a lot on the particular
    implementation in the cluster. In many cases, it will be
    significantly slower than the cluster scratch as it typically
    consists of just a single disk. However, if that disk is local to
    the node (as on most clusters), the performance will not depend on
    what others are doing on the cluster.

**Cluster scratch ($VSC_SCRATCH).**  To allow a job running on multiple nodes (or multiple jobs running
    on separate nodes) to share data as files, every node of the cluster
    (including the login nodes) has access to this shared scratch
    directory. Just like the home and data directories, every user has
    its own scratch directory. Because this scratch is also available
    from the login nodes, you could manually copy results to your data
    directory after your job has ended. Also, this type of scratch is
    usually implemented by running tens or hundreds of disks in parallel
    on a powerful file server with fast connection to all the cluster
    nodes and therefore is often the fastest file system available on a
    cluster.
    You may not get the same file system on different clusters, i.e.,
    you may see different content on different clusters at the same
    institute. 
    {% if site == antwerpen %}
    At the time of writing, the cluster scratch space is
    shared between both clusters at the {{ university }}. This may change again in the future when storage gets updated.
    {% endif %}

**Site scratch ($VSC_SCRATCH_SITE).**  At the time of writing, the site scratch is just the same volume as
    the cluster scratch, and thus contains the same data. In the future
    it may point to a different scratch file system that is available
    across all clusters at a particular site, which is in fact the case
    for the cluster scratch on some sites.

**Global scratch ($VSC_SCRATCH_GLOBAL).**   At the time of writing, the global scratch is just the same volume
    as the cluster scratch, and thus contains the same data. In the
    future it may point to a scratch file system that is available
    across all clusters of the VSC, but at the moment of writing there
    are no plans to provide this.

{% if site == gent %}
### Your UGent home drive and shares

In order to access data on your UGent share(s), you need to stage-in the
data and stage-out afterwards. On the login nodes, it is possible to
access your UGent home drive and shares. To allow this you need a
ticket. This requires that you first authenticate yourself with your
UGent username and password by running:

<pre><code><b>$ kinit yourugentusername@UGENT.BE</b>
Password for yourugentusername@UGENT.BE:
</code></pre>

Now you should be able to access your files running

<pre><code><b>$ ls /UGent/yourugentusername</b>
home shares www
</code></pre>

Please note the shares will only be mounted when you access this folder.
You should specify your complete username - tab completion will not
work.

If you want to use the UGent shares longer than 24 hours, you should ask
a ticket for up to a week by running

<pre><code><b>$ kinit yourugentusername@UGENT.BE -r 7d</b>
</code></pre>

You can verify your authentication ticket and expiry dates yourself by
running klist

<pre><code><b>$ klist</b>
...
Valid starting     Expires            Service principal
14/07/20 15:19:13  15/07/20 01:19:13  krbtgt/UGENT.BE@UGENT.BE
	renew until 21/07/20 15:19:13

</code></pre>

Your ticket is valid for 10 hours, but you can renew it before it
expires.

To renew your tickets, simply run

<pre><code><b>$ kinit -R</b>
</code></pre>

If you want your ticket to be renewed automatically up to the maximum
expiry date, you can run

<pre><code><b>$ krenew -b -K 60</b>
</code></pre>

Each hour the process will check if your ticket should be renewed.

We strongly advise to disable access to your shares once it is no longer
needed:

<pre><code><b>$ kdestroy</b>
</code></pre>

If you get an error "*Unknown credential cache type while getting
default ccache*" (or similar) and you use , then please deactivate conda
before you use the commands in this chapter.

<pre><code><b>$ conda deactivate</b>
</code></pre>

### UGent shares with globus

In order to access your UGent home and shares inside the globus
endpoint, you first have to generate authentication credentials on the
endpoint. To do that, you have to ssh to the globus endpoint from a
loginnode. You will be prompted for your UGent username and password to
authenticate:

<pre><code><b>$ ssh globus</b>
UGent username:ugentusername
Password for ugentusername@UGENT.BE:
Shares are available in globus endpoint at /UGent/ugentusername/
Overview of valid tickets:
Ticket cache: KEYRING:persistent:xxxxxxx:xxxxxxx
Default principal: ugentusername@UGENT.BE

Valid starting     Expires            Service principal
29/07/20 15:56:43  30/07/20 01:56:43  krbtgt/UGENT.BE@UGENT.BE
	renew until 05/08/20 15:56:40
Tickets will be automatically renewed for 1 week
Connection to globus01 closed.
</code></pre>

Your shares will then be available at /UGent/ugentusername/ under the
globus VSC tier2 endpoint. Tickets will be renewed automatically for 1
week, after which you'll need to run this again. We advise to disable
access to your shares within globus once access is no longer needed:

<pre><code><b>$ ssh globus01 destroy</b>
Succesfully destroyed session
</code></pre>
{% endif %}

### Pre-defined quotas 

**Quota** is enabled on these directories, which means that the amount of data you
can store there is limited. This holds for both the total size of all
files as well as the total number of files that can be stored. The
system works with a soft quota and a hard quota. You can temporarily
exceed the soft quota, but you can never exceed the hard quota. The user
will get warnings as soon as he exceeds the soft quota.

{% if site == gent %}
To see your a list of your current quota, visit the VSC accountpage:
<https://account.vscentrum.be>. VO moderators can see a list of VO quota
usage per member of their VO via
<https://account.vscentrum.be/django/vo/>.
{% endif %}

{% if site == antwerpen %}
The amount of data (called "*Block Limits*") that is currently in use by
the user ("*KB*"), the soft limits ("*quota*") and the hard limits
("*limit"*) for all 3 file-systems are always displayed when a user
connects to the .

With regards to the *file limits*, the number of files in use
("*files*"), its soft limit ("*quota*") and its hard limit ("*limit*")
for the 3 file-systems are also displayed.

::: prompt
---------------------------------------------------------- Your quota
is:

Block Limits Filesystem KB quota limit grace home 177920 3145728 3461120
none data 17707776 26214400 28835840 none scratch 371520 26214400
28835840 none

File Limits Filesystem files quota limit grace home 671 20000 25000 none
data 103079 100000 150000 expired scratch 2214 100000 150000 none

----------------------------------------------------------
:::

Make sure to regularly check these numbers at log-in!
{% endif %}

{% if site == leuven %}
You can use `quota -s` to see your quota for `$VSC_HOME` and
`$VSC_DATA`. To see your quota for `$VSC_SCRATCH`, you can use
`mmlsquota vol_ddn2:leuven_scratch --block-size auto`.
{% endif %}
{% if site == brussel %}
You can use the `myquota` command to see your current usage on
`$VSC_HOME` and `$VSC_SCRATCH`.
{% endif %}

The rules are:

1.  You will only receive a warning when you have reached the soft limit
    of either quota.

2.  You *will* start losing data and get I/O errors when you reach the
    hard limit. In this case, data loss will occur since nothing can be
    written anymore (this holds both for new files as well as for
    existing files), until you free up some space by removing some
    files. Also note that you *will not* be warned when data loss
    occurs, so keep an eye open for the general quota warnings!

3.  The same holds for running jobs that need to write files: when you
    reach your hard quota, jobs will crash.

We do realise that quota are often observed as a nuisance by users,
especially if you're running low on it. However, it is an essential
feature of a shared infrastructure. Quota ensure that a single user
cannot accidentally take a cluster down (and break other user's jobs) by
filling up the available disk space. And they help to guarantee a fair
use of all available resources for all users. Quota also help to ensure
that each folder is used for its intended purpose.

## Writing Output files

!!! tip
    Find the code of the exercises in "~/{{ exampledir }}"

In the next exercise, you will generate a file in the $VSC_SCRATCH
directory. In order to generate some CPU- and disk-I/O load, we will

1.  take a random integer between 1 and 2000 and calculate all primes up
    to that limit;

2.  repeat this action 30.000 times;

3.  write the output to the "`primes_1.txt`" output file in the
    $VSC_SCRATCH-directory.

Check the Python and the PBS file, and submit the job: Remember that
this is already a more serious (disk-I/O and computational intensive)
job, which takes approximately 3 minutes on the {{ hpc }}.

<pre><code><b>$ cat file2.py</b>
<b>$ cat file2.pbs</b>
<b>$ qsub file2.pbs</b>
<b>$ qstat</b>
<b>$ ls -l</b>
<b>$ echo $VSC_SCRATCH</b>
<b>$ ls -l $VSC_SCRATCH</b>
<b>$ more $VSC_SCRATCH/primes_1.txt</b>
</code></pre>

## Reading Input files

!!! tip
    Find the code of the exercise "`file3.py`" in "~/{{ exampledir }}".

In this exercise, you will

1.  Generate the file "`primes_1.txt`" again as in the previous
    exercise;

2.  open the this file;

3.  read it line by line;

4.  calculate the average of primes in the line;

5.  count the number of primes found per line;

6.  write it to the "`primes_2.txt`" output file in the
    $VSC_SCRATCH-directory.

Check the Python and the PBS file, and submit the job:

<pre><code><b>$ cat file3.py</b>
<b>$ cat file3.pbs</b>
<b>$ qsub file3.pbs</b>
<b>$ qstat</b>
<b>$ ls -l</b>
<b>$ more $VSC_SCRATCH/primes_2.txt</b>
</code></pre>
## How much disk space do I get? 

### Quota

The available disk space on the {{ hpc }} is limited. The actual disk capacity,
shared by all users, can be found on the "Available hardware" page on
the website.
(<https://vscdocumentation.readthedocs.io/en/latest/hardware.html>) As
explained in [the section on predefined quota](./#pre-defined-quotas), this implies that there are also limits to:

-   the amount of disk space; and

-   the number of files

that can be made available to each individual {{ hpc }} user.

The quota of disk space and number of files for each {{ hpc }} user is:
{% if site == gent %}
| **Volume** | **Max. disk space** | **Max. # Files** |
|:-----------|:--------------------|:-----------------|
| HOME |     3 GB |  20000 |
| DATA |    25 GB | 100000 |
| SCRATCH | 25 GB | 100000 |
{% endif %}

{% if site == antwerpen %}
  --------- ------- --------
  HOME         3 GB    20000
  DATA        25 GB   100000
  SCRATCH     25 GB   100000
  --------- ------- --------
{% endif %}

!!! tip
    The first action to take when you have exceeded your quota is to clean
    up your directories. You could start by removing intermediate, temporary
    or log files. Keeping your environment clean will never do any harm.

!!! tip
    {% if site == (gent or brussel) %}
    If you obtained your VSC account via {{ university }}, you can get (significantly) more
    storage quota in the DATA and SCRATCH volumes by joining a Virtual Organisation (VO), see [the section on virtual organisations](./#virtual-organisations) for more information. In case of questions,
    contact {{ hpcinfo }}.
    {% endif %}
    {% if site == (leuven or antwerpen) %}
    Users can request for additional quota, which can be granted
    in duly justified cases. Please contact the {{ hpcteam }} staff.
    {% endif %}
### Check your quota

<!-- 
%% Kurt Lust: I've hidden the first part of this chapter as mmlsquota is only
%% for GPFS file systems (and not for , e.g., the NetApp in Leuven for home and data)
%% and as on several clusters, the explicit path is needed.
% In general it may be useful to see how much space (in KB) and how many files that you are using on any file system.  This information is also shown each time that you log in to the {{hpc}}

% \begin{prompt}
% %\shellcmd{mmlsquota}%
%                          Block Limits
% Filesystem   type     KB     quota     limit  in_doubt  grace
% data          USR  82944  26214400  28835840         0   none
% home          USR  34560   3145728   3461120         0   none
% scratch       USR  29472  26214400  28835840     19456   none

% |      File Limits
% Filesystem  files   quota   limit in_doubt  grace  Remarks
% Data           27  100000  150000        0   none
% Home          117   20000   25000        0   none
% Scratch        11  100000  150000       20   none
% \end{prompt} 
-->


{% if site == gent %}
You can consult your current storage quota usage on the {{ hpcinfra }} shared
filesystems via the VSC accountpage, see the "Usage" section at <https://account.vscentrum.be> .

VO moderators can inspect storage quota for all VO members via <https://account.vscentrum.be/django/vo/>.

To check your storage usage on the local scratch filesystems on VSC
sites other than {{ university }}, you can use the "`show_quota`" command (when logged
into the login nodes of that VSC site).

{% else %}
The "`show_quota`" command has been developed to show you the status of
your quota in a readable format:
<pre><code>$ <b>show_quota</b>
VSC_DATA:    used 81MB (0%)  quota 25600MB
VSC_HOME:    used 33MB (1%)  quota 3072MB
VSC_SCRATCH:   used 28MB (0%)  quota 25600MB
VSC_SCRATCH_GLOBAL: used 28MB (0%)  quota 25600MB
VSC_SCRATCH_SITE:   used 28MB (0%)  quota 25600MB
</code></pre>

or on the UAntwerp clusters
<pre><code>$ <b>module load scripts</b>
$ <b>show_quota</b>
VSC_DATA:    used 81MB (0%)  quota 25600MB
VSC_HOME:    used 33MB (1%)  quota 3072MB
VSC_SCRATCH:   used 28MB (0%)  quota 25600MB
VSC_SCRATCH_GLOBAL: used 28MB (0%)  quota 25600MB
VSC_SCRATCH_SITE:   used 28MB (0%)  quota 25600MB
</code></pre>

With this command, you can follow up the consumption of your total disk
quota easily, as it is expressed in percentages. Depending of on which
cluster you are running the script, it may not be able to show the quota
on all your folders. E.g., when running on the tier-1 system Muk, the
script will not be able to show the quota on $VSC_HOME or $VSC_DATA if
your account is a KU&nbsp;Leuven, UAntwerpen or VUB account.

{% endif %}
Once your quota is (nearly) exhausted, you will want to know which
directories are responsible for the consumption of your disk space. You
can check the size of all subdirectories in the current directory with
the "`du`" (**Disk Usage**) command:

<pre><code><b>$ du</b>
256 ./ex01-matlab/log
1536 ./ex01-matlab
768 ./ex04-python
512 ./ex02-python
768 ./ex03-python
5632
</code></pre>

This shows you first the aggregated size of all subdirectories, and
finally the total size of the current directory "." (this includes files
stored in the current directory).

If you also want this size to be "human readable" (and not always the
total number of kilobytes), you add the parameter "-h":

<pre><code><b>$ du -h</b>
256K ./ex01-matlab/log
1.5M ./ex01-matlab
768K ./ex04-python
512K ./ex02-python
768K ./ex03-python
5.5M .
</code></pre>

If the number of lower level subdirectories starts to grow too big, you
may not want to see the information at that depth; you could just ask
for a summary of the current directory:

<pre><code><b>$ du -s</b>
5632 .
<b>$ du -s -h</b>
</code></pre>

If you want to see the size of any file or top-level subdirectory in the
current directory, you could use the following command:

<pre><code><b>$ du -s -h *</b>
1.5M ex01-matlab
512K ex02-python
768K ex03-python
768K ex04-python
256K example.sh
1.5M intro-HPC.pdf
</code></pre>

Finally, if you don't want to know the size of the data in your current
directory, but in some other directory (e.g., your data directory), you
just pass this directory as a parameter. The command below will show the
disk use in your home directory, even if you are currently in a
different directory:

<pre><code><b>$ du -h $VSC_HOME/*</b>
22M {{ homedir }}/dataset01
36M {{ homedir }}/dataset02
22M {{ homedir }}/dataset03
3.5M {{ homedir }}/primes.txt
</code></pre>

{% if site == gent %}
{% else %}
We also want to mention the `tree` command, as it also provides an easy
manner to see which files consumed your available quotas. *Tree* is a
recursive directory-listing program that produces a depth indented
listing of files.


Try:

<pre><code><b>$ tree -s -d</b>
</code></pre>

However, we urge you to only use the `du` and `tree` commands when you
really need them as they can put a heavy strain on the file system and
thus slow down file operations on the cluster for all other users.
{% endif %}

## Groups

Groups are a way to manage who can access what data. A user can belong
to multiple groups at a time. **Groups can be created and managed without any interaction from the system administrators**.

Please note that changes are not instantaneous: it may take about an
hour for the changes to propagate throughout the entire HPC
infrastructure.

To change the group of a directory and it's underlying directories and
files, you can use:

<pre><code><b>$ chgrp -R groupname directory</b>
</code></pre>

### Joining an existing group

1.  Get the group name you want to belong to.

2.  Go to <https://account.vscentrum.be/django/group/new> and fill in
    the section named "Join group". You will be asked to fill in the
    group name and a message for the moderator of the group, where you
    identify yourself. This should look something like in the image below.

3.  After clicking the submit button, a message will be sent to the
    moderator of the group, who will either approve or deny the request.
    You will be a member of the group shortly after the group moderator
    approves your request.

![Joining a group.](../img/ch6-group-join.png)

### Creating a new group

1.  Go to <https://account.vscentrum.be/django/group/new> and scroll
    down to the section "Request new group". This should look something
    like in the image below.

2.  Fill out the group name. This cannot contain spaces.

3.  Put a description of your group in the "Info" field.

4.  You will now be a member and moderator of your newly created group.

![Creating a new group.](../img/ch6-group-new.png)

### Managing a group

Group moderators can go to
<https://account.vscentrum.be/django/group/edit> to manage their group
(see the image below). Moderators can invite and remove members. They can also promote
other members to moderator and remove other moderators.

![Creating a new group.](../img/ch6-group-edit.png)

### Inspecting groups

You can get details about the current state of groups on the HPC
infrastructure with the following command (`example` is the name of the
group we want to inspect):

<pre><code><b>$ getent group example</b>
example:*:1234567:vsc40001,vsc40002,vsc40003
</code></pre>

We can see that the VSC id number is 1234567 and that there are three
members in the group: `vsc40001`, `vsc40002` and `vsc40003`.

{% if site == (gent or brussel) %}
## Virtual Organisations

A Virtual Organisation (VO) is a special type of group. You can only be
a member of one single VO at a time (or not be in a VO at all). Being in
a VO allows for larger storage quota to be obtained (but these requests
should be well-motivated).

### Joining an existing VO

1.  Get the VO id of the research group you belong to (this id is formed 
    {%- if site == gent -%}
    by the letters `gvo`, followed by 5 digits). 
    {%- endif %}
    {%- if site == brussel -%}
    the letters `bvo`, followed by 5 digits). 
    {%- endif %}

2.  Go to <https://account.vscentrum.be/django/vo/join> and fill in the
    section named "Join VO". You will be asked to fill in the VO id and
    a message for the moderator of the VO, where you identify yourself.
    This should look something like in the image below.

3.  After clicking the submit button, a message will be sent to the
    moderator of the VO, who will either approve or deny the request.

![Joining a VO.](../img/ch6-VO-join.png)

### Creating a new VO

1.  Go to <https://account.vscentrum.be/django/vo/new> and scroll down
    to the section "Request new VO". This should look something like in the image below.

2.  Fill why you want to request a VO.

3.  Fill out the both the internal and public VO name. These cannot
    contain spaces, and should be 8-10 characters long. For example,
    `genome25` is a valid VO name.

4.  Fill out the rest of the form and press submit. This will send a
    message to the {{ hpc }} administrators, who will then either approve or deny
    the request.

5.  If the request is approved, you will now be a member and moderator
    of your newly created VO.

![Creating a new VO.](../img/ch6-VO-new.png)

### Requesting more storage space

If you're a moderator of a VO, you can request additional quota for the
VO and its members.

1.  Go to <https://account.vscentrum.be/django/vo/edit> and scroll down
    to "Request additional quota". See the image below to see how this looks.

2.  Fill out how much *additional* storage you want. In the screenshot
    below, we're asking for 500 GiB extra space for `VSC_DATA`, and for
    1 TiB extra space on `VSC_SCRATCH_KYUKON`.

3.  Add a comment explaining why you need additional storage space and
    submit the form.

4.  An {{ hpc }} administrator will review your request and approve or deny it.

![Requesting additional quota for the VO and its members.](../img/ch6-VO-request-additional-quota.png)

### Setting per-member VO quota

VO moderators can tweak how much of the VO quota each member can use. By
default, this is set to 50% for each user, but the moderator can change
this: it is possible to give a particular user more than half of the VO
quota (for example 80%), or significantly less (for example 10%).

Note that the total percentage can be above 100%: the percentages the
moderator allocates per user are *the maximum percentages* of storage
users can use.

1.  Go to <https://account.vscentrum.be/django/vo/edit> and scroll down
    to "Manage per-member quota share". See the image below to see how this looks.

2.  Fill out how much percent of the space you want each user to be able
    to use. Note that the total can be above 100%. In the screenshot
    below, there are four users. Alice and Bob can use up to 50% of the
    space, Carl can use up to 75% of the space, and Dave can only use
    10% of the space. So in total, 185% of the space has been assigned,
    but of course only 100% can actually be used.

![Setting per-member quota.](../img/ch6-VO-per-member-storage.png)

### VO directories

When you're a member of a VO, there will be some additional directories
on each of the shared filesystems available:

**VO scratch (`$VSC_SCRATCH_VO`)**:   A directory on the shared *scratch* filesystem shared by the members
    of your VO, where additional storage quota can be provided (see [the section on requesting more storage space](./#requesting-more-storage-space)).
    You can use this as an alternative to your personal `$VSC_SCRATCH`
    directory (see [the section on your scratch space](./#your-scratch-space-vsc_scratch)).

**VO data (`$VSC_DATA_VO`)**:   A directory on the shared *data* filesystem shared by the members of
    your VO, where additional storage quota can be provided (see ). You
    can use this as an alternative to your personal `$VSC_DATA`
    directory (see [the section on your data directory](./#your-data-directory-vsc_data)).

If you put `_USER` after each of these variable names, you can see your
personal folder in these filesystems. For example: `$VSC_DATA_VO_USER`
is your personal folder in your VO data filesystem (this is equivalent
to `$VSC_DATA_VO/$USER`), and analogous for `$VSC_SCRATCH_VO_USER`.{%- endif -%}