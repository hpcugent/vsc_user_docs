# Known issues

This page provides details on a couple of known problems, and the workarounds that are available for them.

If you have any questions related to these issues, please [contact the {{ hpcteam }}]({{ hpc_support_url }}).

* [`Operation not permitted` error for MPI applications](#openmpi_libfabric_operation_not_permitted)

---

## `Operation not permitted` error for MPI applications {: #openmpi_libfabric_operation_not_permitted :}

When running an MPI application that was installed with a `foss` toolchain, you may run into crash with an error message like:

```
Failed to modify UD QP to INIT on mlx5_0: Operation not permitted
```

This error means that an internal problem has occurred in OpenMPI.


### Cause of the problem

This problem was introduced with the OS updates that were installed on the HPC-UGent and VSC Tier-1 Hortense clusters
mid February 2024, most likely due to updating the Mellanox OFED kernel module.

It seems that having OpenMPI consider both UCX and libfabric as "backends" to use the high-speed interconnect
(InfiniBand) is causing this problem: the error message is reported by UCX, but the problem only occurs when OpenMPI
is configured to also consider libfabric.

### Affected software

We have been notified that this error may occur with various applications, including (but not limited to)
CP2K, LAMMPS, netcdf4-python, SKIRT, ...


### Workarounds

#### Use latest `vsc-mympirun` {: #openmpi_libfabric_mympirun :}

A workaround as been implemented in `mympirun` (version 5.4.0).

Make sure you use the latest version of `vsc-mympirun` by using the following (version-less) `module load`
statement in your job scripts:

```
module load vsc-mympirun
```

and launch your MPI application using the `mympirun` command.

For more information, see the [`mympirun`](mympirun.md) documentation.


#### Configure OpenMPI to not use libfabric via environment variables {: #openmpi_libfabric_env_vars :}

If using `mympirun` is not an option, you can configure OpenMPI to not consider libfabric (and only use UCX)
by setting the following environment variables (in your job script or session environment):

```
export OMPI_MCA_btl='^uct,ofi'
export OMPI_MCA_pml='ucx'
export OMPI_MCA_mtl='^ofi'
```


### Resolution

We will re-install the affected OpenMPI installations during the scheduled maintenance of 13-17 May 2024
(see also [VSC status page](https://status.vscentrum.be)).

---
