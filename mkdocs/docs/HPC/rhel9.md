# Migration to RHEL 9 operation system (Tier-2)

Starting September 2024 we will gradually migrate the HPC-UGent Tier-2 clusters that
are using RHEL 8 as operating system (OS) to **RHEL 9 (Red Hat Enterprise Linux 9)**.
This includes clusters `skitty`, `joltik`, `doduo`, `accelgor`, `donphan` and `gallade`
(see also the [infrastructure overview](https://www.ugent.be/hpc/en/infrastructure)),
as well as switching the Tier-2 login nodes to new ones running RHEL 9.

## Motivation

Migrating to RHEL 9 is done to bring all clusters in line with the most recent
cluster that is already running RHEL 9 (`shinx`).

This makes the maintenance of the HPC-UGent Tier-2 infrastructure significantly easier,
since we only need to take into account a single operating system version going forward.

It will also bring you the latest versions in operating system software, with more
features, performance improvements, and enhanced security.

## Impact on the HPC-UGent Tier-2 login nodes {: #login_nodes_impact }

As a general rule, the OS of the login node should match the OS of the cluster
you are running on. To make this more transparent, you will be warned when loading
a `cluster` module for a cluster than is running an OS that is different than that
of the login node you are on.

For example, on the current login nodes (`gligar07` + `gligar08`) which are still using RHEL 8,
you will see a warning like:
```
$ module swap cluster/shinx
...
We advise you to log in to a RHEL 9 login node when using the shinx cluster.
The shinx cluster is using RHEL 9 as operating system,
while the login node you are logged in to is using RHEL 8.
To avoid problems with testing installed software or submitting jobs,
it is recommended to switch to a RHEL 9 login node by running 'ssh login9'.
```

Initially there will be only one RHEL 9 login node. As needed a second one will be added.

When the default cluster (`doduo`) is migrated to RHEL 9 the corresponding login nodes
will also become default when you log in via `login.hpc.ugent.be`
When they are no longer needed the RHEL 8 login nodes will be shut down.

### User limits (CPU time, memory, ...) {: #login_nodes_limits }

To encourage only using the login nodes as an entry point to the HPC-UGent infrastructure,
user limits will be enforced on the RHEL 9 login nodes. This was already the case for the
RHEL 8 login nodes, but the limits are a bit stricter now.

This includes (per user):

* max. of 2 CPU cores in use
* max. 8 GB of memory in use

For more intensive tasks you can use the
[interactive and debug clusters](interactive_debug.md)
through the [web portal](web_portal.md).

## Impact on central software stack {: #software_impact }

The migration to RHEL 8 as operating system should not impact your workflow,
everything will basically be working as it did before (incl. job submission, etc.).

However, there will be impact on the availability of software that is made available via modules.

**Software that was installed with an older compiler toolchain will no
longer be available once the clusters have been updated to RHEL 9.**

This includes all software installations on top of a compiler toolchain that is older than:

* `GCC(core)/12.3.0`
* `foss/2023a`
* `intel/2023a`
* `gompi/2023a`
* `iimpi/2023a`
* `gfbf/2023a`

(or another toolchain with a year-based version older than `2023a`)

The `module` command will produce a clear warning when you are loading modules
that are using a toolchain that will no longer be available after the cluster
has been migrated to RHEL 9.
For example:

```
foss/2022b:
   ___________________________________
  /  This module will soon no longer  \
  \  be available on this cluster!    /
   -----------------------------------
         \   ^__^
          \  (xx)\_______
             (__)\       )\/\
              U  ||----w |
                 ||     ||

Only modules installed with a recent toolchain will still be available
when this cluster has been migrated to the RHEL 9 operating system.
Recent toolchains include GCC(core)/12.3.0, gompi/2023a, foss/2023a,
iimpi/2023a, intel/2023a, gfbf/2023a, and newer versions.

You should update your workflow or job script to use more recent software
installations, or accept that the modules you currently rely on will soon
no longer be available.

To request a more recent version of the software you are using,
please submit a software installation request via:

https://www.ugent.be/hpc/en/support/software-installation-request

The HPC-UGent Tier-2 clusters running RHEL 8 will be migrated to RHEL 9.

For more information, see https://docs.hpc.ugent.be/rhel9/

If you have any questions, please contact hpc@ugent.be .
```

If you require software that is currently only available with an older toolchain
on the HPC-UGent Tier-2 clusters that are still running RHEL 8,
check via `module avail` if a more recent version is installed that you can switch to,
or submit a [software installation request](https://www.ugent.be/hpc/en/support/software-installation-request)
so we can provide a more recent installation of that software which you can adopt.

It is a good idea to test your software on the `shinx` cluster,
which is already running RHEL 9 as operating system,
to be sure if it still works.
We will provide more RHEL 9 nodes on other clusters to test on soon.

## Planning

We plan to migrate the HPC-UGent Tier-2 clusters that are still
using RHEL 8 to RHEL 9 one by one, following the schedule outlined below.

| ***cluster*** | ***migration start*** | ***migration completed on*** |
| --- | ---- | --- |
| `skitty` | Monday 30 September 2024 | Tuesday 1 October 2024 |
| `joltik` | Monday 21 October 2024 | Tuesday 22 October 2024 |
| `accelgor` | Tuesday 26 November 2024 | Tuesday 27 November 2024 |
| `gallade` | January 2025 | |
| `donphan` | February 2025 | |
| `doduo` (default cluster) | February 2025 | |
| login nodes switch | February 2025 | |

Migration of the `donphan` and `doduo` clusters to RHEL 9 and switching `login.hpc.ugent.be` to RHEL 9 login nodes
will be done at the same time.

We will keep this page up to date when more specific dates have been planned.

!!! warning
    This planning above is subject to change, some clusters may get migrated later than originally planned.

    **Please check back regularly.**

## Questions

If you have any questions related to the migration to the RHEL 9 operating system,
please [contact the {{ hpcteam }}]({{ hpc_support_url }}).
