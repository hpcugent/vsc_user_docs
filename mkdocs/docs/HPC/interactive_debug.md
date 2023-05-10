# Interactive and debug cluster { #ch:interactive_ugent}

## Purpose { #sec:interactive_ugent_pupose}

The purpose of this cluster is to give the user an environment where
there should be no waiting in the queue to get access to a limited
number of resources. This environment allows a user to immediatelty
start working, and is the ideal place for interactive work such as
development, debugging and light production workloads (typically
sufficient for training and/or courses).
<br></br>This enviroment should be seen as an extension of the login nodes,
instead of a dedicated compute resource. The interactive cluster is
*overcommitted*, which means that more CPU cores can be requested for
jobs than physically exist in the cluster. Obviously, the performance of
this cluster heavily depends on the workloads and the actual overcommit
usage. Be aware that jobs can slow down or speed up during their
execution.
<br></br>Due to the restrictions and sharing of the CPU resources (see
section [Restrictions and overcommit factor](./#restrictions-and-overcommit-factor)) jobs on this cluster
should normally start more or less immediately. The tradeoff is that
performance must not be an issue for the submitted jobs. This means that
typical workloads for this cluster should be limited to:

-   Interactive jobs (see
    chapter [Running interactive jobs](../running_interactive_jobs/#running-interactive-jobs))

-   Cluster desktop sessions (see
    chapter [Using the HPC-UGent web portal](../web_portal/#using-the-hpc-ugent-web-portal))

-   Jobs requiring few resources

-   Debugging programs

-   Testing and debugging job scripts

## Submitting jobs

To submit jobs to the HPC-UGent interactive and debug cluster nicknamed
`slaking`, first use:

<pre><code>$ <b>module swap cluster/slaking</b>
</code></pre>

Then use the familiar `qsub`, `qstat`, etc. commands (see
chapter [Running batch jobs](../running_batch_jobs/#running-batch-jobs)).

### Restrictions and overcommit factor 

Some limits are in place for this cluster:

-   each user may have at most 5 jobs in the queue (both running and
    waiting to run);

-   at most 3 jobs per user can be running at the same time;

-   running jobs may allocate no more than 8 CPU cores and no more than
    27200 MiB of memory in total, per user;

In addition, the cluster has an overcommit factor of 6. This means that
6 times more cores can be allocated than physically exist.
Simultaneously, the default memory per core is 6 times less than what
would be available on a non-overcommitted cluster.

Please note that based on the (historical) workload of the interactive
and debug cluster, the above restrictions and the overcommitment ratio
might change without prior notice.
