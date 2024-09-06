
# Migration to RHEL9 operation system (Tier-2)

During the second half of 2024 we will migrate the HPC-UGent Tier-2 clusters that 
are using RHEL 8 as operating system to **RHEL9 (Red Hat Enterprise Linux 9)**.
This includes clusters `skitty`, `joltik`, `doduo`, `accelgor`, `donphan` and `gallade` 
(see also the [infrastructure overview](https://www.ugent.be/hpc/en/infrastructure)), 
as well as switching the Tier-2 login nodes to new ones running RHEL9.

## Motivation

Migrating to RHEL8 is done to bring all clusters in line with the most recent 
cluster that are already running RHEL9 (shinx).

This makes the maintenance of the HPC-UGent Tier-2 infrastructure significantly easier, 
since we only need to take into account a single operating system version going forward.

It will also bring you the latest versions in operating system software, with more 
features and improved security.

## Impact on the login nodes

As a general rule, the OS of your login node should match the operating system of the cluster 
you are running on. To make this more transparent, you will be prompted when loading 
a cluster module with a different operation system.

    module swap cluster/shinx

    The following have been reloaded with a version change:
    1) cluster/doduo => cluster/shinx         3) env/software/doduo => env/software/shinx
    2) env/slurm/doduo => env/slurm/shinx     4) env/vsc/doduo => env/vsc/shinx

    We advise you to log in to a RHEL 9 login node when using the shinx cluster.
    The shinx cluster is using RHEL 9 as operating system,
    while the login node you are logged in to is using RHEL 8.
    To avoid problems with testing installed software or submitting jobs,
    it is recommended to switch to a RHEL 9 login node by running 'ssh login9'.

Initially there will be only one RHEL 9 login node. As needed a second one will be added.

When the default cluster (doduo) migrates to RHEL 9 the corresponding login nodes 
will also become default (when you do `ssh vsc4xxxx@login.hpc.ugent.be`). 
When they are no longer needed the old RHEL 8 login nodes will be shut down.

### Limits

To encourage only using the login nodes as an entry point to the HPC-UGent infrastructure, 
user limits will be enforced on the RHEL9 login nodes. (This was already the case for the
RHEL8 login nodes, but the limits are a bit stricter now.)

This includes (per user):
* max. of 2 CPU's in use
* max. 8 GB of memory in use

For more intensive tasks you can use the 
[interative and debug clusters](https://docs.hpc.ugent.be/interactive_debug/) 
through the [web portal](https://login.hpc.ugent.be).

## Impact on central software stack

The migration to RHEL8 as operating system should not impact your workflow, 
everything will basically be working as it did before (incl. job submission, etc.).

However, there will be impact on the availability of software that is made available via modules.

**Software that was installed with an older compiler toolchain will no 
longer be available once the clusters have been updated to RHEL9.**

This includes all software installations on top of a toolchain that is older than 
`foss/2023a`, `gompi/2023a`, `intel/2023a`, `iimpi/2023a`, `GCC(core)/12.3.0`.

The `module` command will produce a clear warning when you are loading modules 
that are using a toolchain that will no longer be available after the cluster 
has been migrated to RHEL9.
For example:

    foss/2019a:
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
    iimpi/2023a, intel/2023a, and newer versions.

    You should update your workflow or job script to use more recent software
    installations, or accept that the modules you currently rely on will soon
    no longer be available.

    To request a more recent version of the software you are using,
    please submit a software installation request via:

    https://www.ugent.be/hpc/en/support/software-installation-request

    The HPC-UGent Tier-2 clusters running RHEL 8 will be migrated to RHEL 9.

    For more information, see https://docs.hpc.ugent.be/migration_to_rhel9/

    If you have any questions, please contact hpc@ugent.be .

If you require software that is currently only available with an older toolchain 
on the HPC-UGent Tier-2 clusters that are still running RHEL8, 
check via `module avail` if a more recent version is installed that you can switch to, 
or submit a [software installation request](https://www.ugent.be/hpc/en/support/software-installation-request) 
so we can provide a more recent installation of that software which you can adopt.

It is a good idea to test your software on `shinx` to be sure if it still works. 
We will provide more nodes to test on in the future.

## Planning

We plan to migrate the HPC-UGent Tier-2 clusters that are still 
using RHEL 8 to RHEL 9 one by one, following the schedule outlined below.

| ***cluster*** | ***migration start*** | ***migration completed on*** |
| --- | ---- | --- |
| skitty | 30th of September 2024 | |
| joltik | October 2024 | |
| accelgor | November 2024 | |
| gallade | December 2024 | |
| donphan | February 2025 | |
| doduo (default cluster) | February 2025 | |
| login nodes switch | February 2025 | |

Donphan, doduo and the login node switch will be done at the same time.

We will keep this page up to date when more specific dates have been planned.
