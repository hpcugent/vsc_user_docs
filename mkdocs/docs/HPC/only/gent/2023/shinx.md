# New Tier-2 cluster: `shinx`

In October 2023, a new pilot cluster was added to the HPC-UGent Tier-2 infrastructure: `shinx`.

This page provides some important information regarding this cluster, and how it differs from the clusters
it is replacing (`swalot` and `victini`).

If you have any questions on using `shinx`, you can [contact the {{ hpcteam }}]({{ hpc_support_url }}).

For software installation requests, please use the [request form](https://www.ugent.be/hpc/en/support/software-installation-request).

---

## `shinx`: generic CPU cluster

`shinx` is a new CPU-only cluster.

It replaces `swalot`, which was retired on **Wednesday 01 November 2023**,
and `victini`, which ws retired on **Monday 05 February 2024**.

It is primarily for regular CPU compute use.

This cluster consists of 48 workernodes, each with:

* 2x 96-core AMD EPYC 9654 (Genoa @ 2.4 GHz) processor;
* ~360 GiB of RAM memory;
* 400GB local disk;
* NDR-200 InfiniBand interconnect;
* RHEL9 as operating system;

To start using this cluster from a terminal session, first run:
```
module swap cluster/shinx
```

You can also start (interactive) sessions on `shinx` using the [HPC-UGent web portal](../../../web_portal.md).

### Differences compared to `swalot` and `victini`.

#### CPUs

The most important difference between `shinx` and `swalot`/`victini` workernodes is in the CPUs:
while `swalot` and `victini` workernodes featured *Intel* CPUs, `shinx` workernodes have `AMD Genoa` CPUs.

Although software that was built on a `swalot` or `victini` workernode with compiler options that enable architecture-specific
optimizations (like GCC's `-march=native`, or Intel compiler's `-xHost`) might still run on
a `shinx` workernode, it is recommended to recompile the software to benefit from the support for
`AVX-512` vector instructions (which is missing on `swalot`).

#### Cluster size

The `shinx` cluster is significantly bigger than `swalot` and `victini` in number of cores, and number of cores per workernode,
but not in number of workernodes. In particular, requesting all cores via `ppn=all` might be something to reconsider.

The amount of available memory per core is `1.9 GiB`, which is lower then the `swalot` nodes which had `6.2 GiB` per core
and the `victini` nodes that had `2.5 GiB` per core.


### Comparison with `doduo`

As `doduo` is the current largest CPU cluster of the UGent Tier-2 infrastructure, and it is also based on `AMD EPYC` CPUs,
we would like to point out that, roughly speaking, one `shinx` node is equal to 2 `doduo` nodes.

Although software that was built on a `doduo` workernode with compiler options that enable architecture-specific
optimizations (like GCC's `-march=native`, or Intel compiler's `-xHost`) might still run on
 a `shinx` workernode, it is recommended to recompile the software to benefit from the support for
`AVX-512` vector instructions (which is missing from `doduo`).

### Other remarks

* Possible issues with thread pinning: we have seen, especially on `Tier-1 dodrio` cluster, that in certain cases
thread pinning is invoked where it is not expected. Typical symptom is that all the processes that are started are pinned
to a single core. Always report this issue when it occurs.
You can try yourself to mitigate this by setting `export OMP_PROC_BIND=false`, but always report it so we can keep track of this problem.
It is not recommended to always set this workaround, only for the specific tools that are affected.


---

## Shinx pilot phase (23/10/2023-15/07/2024)

As usual with any pilot phase, you need to be member of the `gpilot` group, and to start using this cluster run:

```
module swap cluster/.shinx
```

Because the delivery time of the infiniband network is very high, we only expect to have all material end of February 2024.
However, all the workernodes will already be delivered in the week of 20 October 2023

As such, we will have an extended pilot phase in 3 stages:

### Stage 0: 23/10/2023-17/11/2023

* Minimal cluster to test software and nodes
    * Only 2 or 3 nodes available
    * FDR or EDR infiniband network
    * EL8 OS

* Retirement of `swalot cluster` (as of 01 November 2023)
* Racking of stage 1 nodes

### Stage 1: 01/12/2023-01/03/2024

* 2/3 cluster size
    * 32 nodes (with max job size of 16 nodes)
    * EDR Infiniband
    * EL8 OS

* Retirement of `victini` (as of 05 February 2023)
* Racking of last 16 nodes
* Installation of NDR/NDR-200 infiniband network

### Stage 2 (19/04/2024-15/07/2024)

* Full size cluster
    * 48 nodes (no job size limit)
    * NDR-200 Infiniband (single switch Infiniband topology)
    * EL9 OS

* We expect to plan a full Tier-2 downtime in May 2024 to cleanup, refactor and renew the core networks
(ethernet and infiniband) and some core services. It makes no sense to put `shinx` in production before
that period, and the testing of the `EL9` operating system will also take some time.


### Stage 3 (15/07/2024 - )

* Cluster in production using EL9 (starting with 9.4). Any user can now submit jobs.


### Using `doduo` software

For benchmarking and/or compatibility testing, you can use try to use `doduo` software stack by adding
the following line in the job script before the actual software is loaded:

```
module swap env/software/doduo
```

We mainly expect problems with this in stage 2 of the pilot phase (and in later production phase),
due to the change in OS.
