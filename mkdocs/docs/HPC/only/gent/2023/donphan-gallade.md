# New Tier-2 clusters: `donphan` and `gallade`

In April 2023, two new clusters were added to the HPC-UGent Tier-2 infrastructure: `donphan` and `gallade`.

This page provides some important information regarding these clusters, and how they differ from the clusters
they are replacing (`slaking` and `kirlia`, respectively).

If you have any questions on using `donphan` or `gallade`, you can [contact the {{ hpcteam }}]({{ hpc_support_url }}).

For software installation requests, please use the [request form](https://www.ugent.be/hpc/en/support/software-installation-request).

---

## `donphan`: debug/interactive cluster

`donphan` is the new debug/interactive cluster.

It replaces `slaking`, which will be retired on **Monday 22 May 2023**.

It is primarily intended for interactive use: interactive shell sessions, using GUI applications through the
[HPC-UGent web portal](../../../web_portal.md), etc.

This cluster consists of 12 workernodes, each with:

* 2x 18-core Intel Xeon Gold 6240 (Cascade Lake @ 2.6 GHz) processor;
* one *shared* NVIDIA Ampere A2 GPU (16GB GPU memory)
* ~738 GiB of RAM memory;
* 1.6TB NVME local disk;
* HDR-100 InfiniBand interconnect;
* RHEL8 as operating system;

To start using this cluster from a terminal session, first run:
```
module swap cluster/donphan
```

You can also start (interactive) sessions on `donphan` using the [HPC-UGent web portal](../../../web_portal.md).

### Differences compared to `slaking`

#### CPUs

The most important difference between `donphan` and `slaking` workernodes is in the CPUs:
while `slaking` workernodes featured *Intel Haswell* CPUs, which support SSE\*, AVX, and AVX2 vector instructions,
`donphan` features *Intel Cascade Lake* CPUs, which also support AVX-512 instructions, on top of SSE\*, AVX, and AVX2.

Although software that was built on a `slaking` workernode with compiler options that enable architecture-specific
optimizations (like GCC's `-march=native`, or Intel compiler's `-xHost`) should still run on
a `donphan` workernode, it is recommended to recompile the software to benefit from the support for
AVX-512 vector instructions.

#### Cluster size

The `donphan` cluster is significantly bigger than `slaking`, both in terms of number of workernodes and
number of cores per workernode, and hence the potential performance impact of oversubscribed cores (see below)
is less likely to occur in practice.

### User limits and oversubscription on `donphan`

By imposing strict user limits and using oversubscription on this cluster,
we ensure that anyone can get a job running without having to wait in the queue, albeit with limited resources.

The user limits for `donphan` include:
* max. 5 jobs in queue;
* max. 3 jobs running;
* max. of 8 cores in total for running jobs;
* max. 27GB of memory in total for running jobs;

The job scheduler is configured with to allow *oversubscription* of the available cores,
which means that jobs will continue to start even if all cores are already occupied by running jobs.
While this prevents waiting time in the queue, it does imply that performance will degrade when all cores are occupied
and additional jobs continue to start running.

### Shared GPU on `donphan` workernodes

Each `donphan` workernode includes a single NVIDIA A2 GPU that can be used for light compute workloads,
and to accelerate certain graphical tasks.

This GPU is *shared* across all jobs running on the workernode, and does not need to be requested explicitly
(it is always available, similar to the local disk of the workernode).

!!! warning

    Due to the shared nature of this GPU, you should assume that any data that is loaded in the GPU memory
    could potentially be accessed by other users, even after your processes have completed.

    There are no strong security guarantees regarding data protection when using this shared GPU!


---

## `gallade`: large-memory cluster

`gallade` is the new large-memory cluster.

It replaces `kirlia`, which will be retired on **Monday 22 May 2023**.

This cluster consists of 12 workernodes, each with:

* 2x 64-core AMD EPYC 7773X (Milan-X @ 2.2 GHz) processor;
* ~940 GiB of RAM memory;
* 1.5TB NVME local disk;
* HDR-100 InfiniBand interconnect;
* RHEL8 as operating system;

To start using this cluster from a terminal session, first run:
```
module swap cluster/gallade
```

You can also start (interactive) sessions on `gallade` using the [HPC-UGent web portal](../../../web_portal.md).

### Differences compared to `kirlia`

#### CPUs

The most important difference between `gallade` and `kirlia` workernodes is in the CPUs:
while `kirlia` workernodes featured *Intel Cascade Lake* CPUs, which support vector AVX-512 instructions
(next to SSE\*, AVX, and AVX2), `gallade` features *AMD Milan-X* CPUs, which implement the *Zen3 microarchitecture*
and hence do *not* support AVX-512 instructions (but do support SSE\*, AVX, and AVX2).

As a result, software that was built on a `kirlia` workernode with compiler options that enable architecture-specific
optimizations (like GCC's `-march=native`, or Intel compiler's `-xHost`) may not work anymore on
a `gallade` workernode, and will produce `Illegal instruction` errors.

Therefore, you may need to recompile software in order to use it on `gallade`.
Even if software built on `kirlia` does still run on `gallade`, it is strongly recommended to recompile it anyway,
since there may be signficant peformance benefits.

#### Memory per core

Although `gallade` workernodes have signficantly more RAM memory (~940 GiB) than `kirlia` workernodes had (~738 GiB),
the average amount of memory per core is significantly lower on `gallade` than it was on `kirlia`, because
a `gallade` workernode has 128 cores (so ~7.3 GiB per core on average), while a `kirlia` workernode had only 36 cores
(so ~20.5 GiB per core on average).

It is important to take this aspect into account when submitting jobs to `gallade`, especially when requesting
all cores via `ppn=all`. You may need to explictly request more memory (see also [here](../../../fine_tuning_job_specifications#pbs_mem)).
