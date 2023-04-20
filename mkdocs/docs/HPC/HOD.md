# Hanythingondemand (HOD)

Hanythingondemand (or HOD for short) is a tool to run a Hadoop (Yarn)
cluster on a traditional HPC system.

## Documentation

The official documentation for HOD version 3.0.0 and newer is available
at <https://hod.readthedocs.org/en/latest/>. The slides of the 2016 HOD
training session are available at
<http://users.ugent.be/~kehoste/hod_20161024.pdf>.

## Using HOD

Before using HOD, you first need to load the `hod` module. We don't
specify a version here (this is an exception, for most other modules you
should, see [Using explicit version numbers](../running_batch_jobs/#using-explicit-version-numbers)) because newer versions might include important bug fixes.

<pre><code>$ <b>module load hod</b>
</code></pre>

### Compatibility with login nodes

The `hod` modules are constructed such that they can be used on the {{hpcinfra}}
login nodes, regardless of which `cluster` module is loaded (this is not
the case for software installed via modules in general, see [Running software that is incompatible with host](../troubleshooting/#running-software-that-is-incompatible-with-host)).

As such, you should experience no problems if you swap to a different
cluster module before loading the `hod` module and subsequently running
|hod|.

For example, this will work as expected:

<pre><code>$ <b>module swap cluster/{{othercluster}}</b>
$ <b>module load hod</b>
$ <b>hod</b>
hanythingondemand - Run services within an HPC cluster
usage: hod <subcommand> [subcommand options]
Available subcommands (one of these must be specified!):
    batch           Submit a job to spawn a cluster on a PBS job controller, run a job script, and tear down the cluster when it's done
    clean           Remove stale cluster info.
...
</code></pre>

Note that also modules named `hanythingondemand/*` are available. These
should however not be used directly, since they may not be compatible
with the login nodes (depending on which cluster they were installed
for).

### Standard HOD configuration

The `hod` module will also put a basic configuration in place for HOD,
by defining a couple of `$HOD_*` environment variables:

<pre><code>$ <b>module load hod</b>
$ <b>env | grep HOD | sort</b>
HOD_BATCH_HOD_MODULE=hanythingondemand/3.2.2-intel-2016b-Python-2.7.12
HOD_BATCH_WORKDIR=$VSC_SCRATCH/hod
HOD_CREATE_HOD_MODULE=hanythingondemand/3.2.2-intel-2016b-Python-2.7.12
HOD_CREATE_WORKDIR=$VSC_SCRATCH/hod
</code></pre>

By defining these environment variables, we avoid that you have to
specify `--hod-module` and `--workdir` when using `hod batch` or
`hod create`, since they are strictly required.

If you want to use a different parent working directory for HOD, it
suffices to either redefine `$HOD_BATCH_WORKDIR` and
`$HOD_CREATE_WORKDIR`, or to specify `--workdir` (which will override
the corresponding environment variable).

Changing the HOD module that is used by the HOD backend (i.e., using
`--hod-module` or redefining `$HOD_*_HOD_MODULE`) is strongly
discouraged.

### Cleaning up

After HOD clusters terminate, their local working directory and cluster
information is typically not cleaned up automatically (for example,
because the job hosting an interactive HOD cluster submitted via
`hod create` runs out of walltime).

These HOD clusters will still show up in the output of `hod list`, and
will be marked as `<job-not-found>`.

You should occasionally clean this up using `hod clean`:

<pre><code>$ <b>module list</b>
Currently Loaded Modulefiles:
  1) cluster/{{defaultcluster}}(default)   2) pbs_python/4.6.0            3) vsc-base/2.4.2              4) hod/3.0.0-cli

$ <b>hod list</b>
Cluster label	Job ID		   State                Hosts
example1        {{jobid}}         &lt;job-not-found&gt;     &lt;none&gt;

$ <b>hod clean</b>
Removed cluster localworkdir directory /user/scratch/gent/vsc400/vsc40000/hod/hod/{{jobid}} for cluster labeled example1
Removed cluster info directory /user/home/gent/vsc400/vsc40000/.config/hod.d/wordcount for cluster labeled example1

$ <b>module swap cluster/{{othercluster}}</b>
Cluster label	Job ID				            State              	Hosts
example2		98765.master19.{{othercluster}}.gent.vsc	&lt;job-not-found&gt;     &lt;none&gt;

$ <b>hod clean</b>
Removed cluster localworkdir directory /user/scratch/gent/vsc400/vsc40000/hod/hod/98765.master19.{{othercluster}}.gent.vsc for cluster labeled example2
Removed cluster info directory /user/home/gent/vsc400/vsc40000/.config/hod.d/wordcount for cluster labeled example2
</code></pre>
Note that **only HOD clusters that were submitted to the currently loaded `cluster` module will be cleaned up**.

## Getting help

If you have any questions, or are experiencing problems using HOD, you
have a couple of options:

-   Subscribe to the HOD mailing list via
    <https://lists.ugent.be/wws/info/hod>, and contact the HOD users and
    developers at hod@lists.ugent.be.

-   Contact the {{hpcteam}} via {{hpcinfo}}

-   Open an issue in the `hanythingondemand` GitHub repository, via
    <https://github.com/hpcugent/hanythingondemand/issues>.
