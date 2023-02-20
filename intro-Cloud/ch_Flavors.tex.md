# Instance types and flavors

VSC Tier1 Cloud provides several virtual machine instance types and
flavors to fit different use cases. Each instance type provides several
flavor sizes to give different combinations of CPU, memory, GPU and
network resources.

## Instance Types {#sec:instance-types}

The following table provides the current main instance types available
from the VSC Tier1 Cloud infrastructure:


:::

| **UPSv1**                          | **CPUv1**                       | **GPUv2**            | **GPUv3**            |
|------------------------------------|---------------------------------|----------------------|----------------------|
|- AMD Epyc 7542 2.9GHz              |- Intel Xeon CPU E5-2670 2.60GHz |- AMD Epyc 7542 2.9GHz|- AMD Epyc 7542 2.9GHz
|- 25Gbit Ethernet                   |- 10Gbit Ethernet                |- 25Gbit Ethernet     |- 25Gbit Ethernet     
|- vCPU oversubscription 2:1         |                                 |                      |                      
|- Uninterruptible Power Supply (UPS)|    |                      |- Uninterruptible Power Supply (UPS)
| | |- 1 full GPU NVIDIA Tesla4|- 1 full GPU NVIDIA Ampere A2 

:::

Each instance type is appropriate for different workloads: (**CPUv1**) for
regular CPU usage, (**GPUvx**) for GPU computations, or (**UPSv1**) for VMs that need to
be connected to an uninterruptible power supply. VMs using UPS will keep
up and running even if the datacenter suffers an unexpected power cut.
(**CPUv1**) and (**GPUv2**) virtual machines are not supported by an UPS and will go
offline when an unexpected power cut occurs.

VSC Tier-1 Cloud instance types also provide different kind of network
performance specifications. All the instance types are able to connect
to the available networks: public network, VSC network and shared
filesystem network (NFS). Note that VSC and shared file system network
access is only made available if explicitly requested in the project
application.

VSC network gives an optimal path towards other VSC sites. This is ideal
for high performance connections between different clusters and services
within VSC. E.g. when you intend to do high data volume reshuffling
between VMs and other Tier-1 components.

Cloud projects should request VSC network if they want to connect to VSC
Data component (<https://www.vscentrum.be/data>) with iRODS and Globus
from their Tier1 Cloud VMs.

On the other hand, the shared filesystem network is required by the
OpenStack shared filesystem service (Manila) (see chapter 10 for more information).

## Flavor Sizes {#sec:flavor-sizes}

A flavor size is a set of virtualized hardware resources to a virtual
machine (VM) instance like system memory size (RAM), virtual cores
(vCPUs) or the root filesystem size.

The flavor's root disk size is the amount of disk space used by the root
(*/*) partition, an ephemeral disk that the base image is copied into
(see section [launch an instance](./ch_LaunchInstances.tex.md#launch-an-instance)
 for more information about VM persistent/non-persistent instances).

The flavor's root ephemeral storage is only used when booting from a
non-persistent VM, but is not used when booting from a persistent
storage volume or persistent VM. The flavor's root ephemeral size is not
taken into account to calculate the project's local storage quota
either. You can also create a persistent volume and choose the desired
filesystem size for your persistent VM during the instantiation. VM
persistent volumes could be resized later if that is necessary (see
chapter [launch an instance](./ch_LaunchInstances.tex.md#launch-an-instance)
 for more information).

VSC Tier-1 Cloud VM flavors are grouped by instance types (see table
[1.2](#table:flavor-size)). Several flavor sizes are available for
each instance type, differing in the number of allocated vCPUs, RAM and
storage size. Every GPU flavor in addition allocates one full GPU card. The
various VM flavors can be used in different combinations to fit
different workload hardware requirements.

:::


| Name            |    RAM| Disk    | VCPUs |
|-----------------|-------|---------|-------|
| CPUv1.nano      |  64Kb |    1Gb  |     1 |
| CPUv1.tiny      | 512Kb |   10Gb  |     1 |
| UPSv1.medium    |   4Gb |   30Gb  |     2 |
| UPSv1.large     |   8Gb |   40Gb  |     4 |
| UPSv1.2xlarge   |  60Gb |   40Gb  |    16 |
| GPUv2.small     |   2Gb |   20Gb  |     1 |
| GPUv2.medium    |   4Gb |   30Gb  |     2 |
| GPUv2.large     |   8Gb |   40Gb  |     4 |
| GPUv2.2xlarge   |  60Gb |   40Gb  |    16 |
| UPSv1.3xlarge   | 120Gb |   80Gb  |    16 |
| CPUv1.1_3xlarge | 180Gb |   80Gb  |    14 |
| CPUv1.4xlarge   | 360Gb |   80Gb  |    20 |
| CPUv1.small     |   2Gb |   20Gb  |     1 |
| GPUv3.small     |   2Gb |   20Gb  |     1 |
| GPUv3.medium    |   4Gb |   30Gb  |     2 |
| GPUv3.large     |   8Gb |   40Gb  |     4 |
| GPUv3.2xlarge   |  60Gb |   40Gb  |    16 |
| CPUv1.medium    |   4Gb |   30Gb  |     2 |
| CPUv1.large     |   8Gb |   40Gb  |     4 |
| CPUv1.xlarge    |  16Gb |   40Gb  |     8 |
| CPUv1.2xlarge   |  60Gb |   40Gb  |    16 |
| CPUv1.3xlarge   | 120Gb |   80Gb  |    16 |
| CPUv1.1_2xlarge |  60Gb |   40Gb  |     8 |
| UPSv1.small     |   2Gb |   20Gb  |     1 |


:::

E.g. The **GPUv2**._large_ OpenStack flavor will instantiate a VM with 4 AMD Epyc
7542 2.9GHz vCPUs, with 1 NVIDIA Tesla4 GPU, 8GB of RAM, and a 40GB
root disk.
