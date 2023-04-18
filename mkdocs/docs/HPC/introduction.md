# Introduction to HPC
## What is HPC?

"**High Performance Computing**" (HPC) is computing on a "*Supercomputer*", a computer with at the
frontline of contemporary processing capacity -- particularly speed of
calculation and available memory.

While the supercomputers in the early days (around 1970) used only a few
processors, in the 1990s machines with thousands of processors began to
appear and, by the end of the 20th century, massively parallel
supercomputers with tens of thousands of "off-the-shelf" processors were
the norm. A large number of dedicated processors are placed in close
proximity to each other in a computer cluster.

A **computer cluster** consists of a set of loosely or tightly connected computers that work
together so that in many respects they can be viewed as a single system.

The components of a cluster are usually connected to each other through
fast local area networks ("LAN") with each *node* (computer used as a
server) running its own instance of an operating system. Computer
clusters emerged as a result of convergence of a number of computing
trends including the availability of low cost microprocessors,
high-speed networks, and software for high performance distributed
computing.

Compute clusters are usually deployed to improve performance and
availability over that of a single computer, while typically being more
cost-effective than single computers of comparable speed or
availability.

Supercomputers play an important role in the field of computational
science, and are used for a wide range of computationally intensive
tasks in various fields, including quantum mechanics, weather
forecasting, climate research, oil and gas exploration, molecular
modelling (computing the structures and properties of chemical
compounds, biological macromolecules, polymers, and crystals), and
physical simulations (such as simulations of the early moments of the
universe, airplane and spacecraft aerodynamics, the detonation of
nuclear weapons, and nuclear fusion). [^1]

## What is the {{ hpcinfra }}?

The {{ hpc }} is a collection of computers with AMD and/or Intel CPUs, running a
Linux operating system, shaped like pizza boxes and stored above and
next to each other in racks, interconnected with copper and fiber
cables. Their number crunching power is (presently) measured in hundreds
of billions of floating point operations (gigaflops) and even in
teraflops.

![](../img/ch1-cables1.png){ width=245px }
![](../img/ch1-cables2.png){ width=245px }
![](../img/ch1-cables3.png){ width=245px }

The {{ hpcinfra }} relies on parallel-processing technology to offer {{ university }} researchers an
extremely fast solution for all their data processing needs.


{% if site == antwerpen -%}

The {{ hpc }} consists of:

<center>

|In technical terms                           | ... in human terms                             |
|:--------------------------------------------|:---------------------------------------------- |
| over 280 nodes and over 11000 cores         |  ... or the equivalent of 2750 quad-core PCs   |
| over 500 Terabyte of online storage         |  ... or the equivalent of over 60000 DVDs      |
| up to 100 Gbit InfiniBand fiber connections |  ... or allowing to transfer 3 DVDs per second |

</center>

{%- endif %}

The {{ hpc }} currently consists of:

{% if site == antwerpen -%}
Leibniz:

1.  144 compute nodes with 2 14-core Intel E5-2680v4 CPUs (Broadwell
    generation, 2.4 GHz) and 128 GB RAM, 120 GB local disk

2.  8 compute nodes with 2 14-core Intel E5-2680v4 CPUs (Broadwell
    generation, 2.4 GHz) and 256 GB RAM, 120 GB local disk

3.  24 "hopper" compute nodes (recovered from the former Hopper cluster)
    with 2 ten core Intel E5-2680v2 CPUs (Ivy Bridge generation, 2.8
    GHz), 256 GB memory, 500 GB local disk

4.  2 GPGPU nodes with 2 14-core Intel E5-2680v4 CPUs (Broadwell
    generation, 2.4 GHz), 128 GB RAM and two NVIDIA Tesla P100 GPUs with
    16 GB HBM2 memory per GPU, 120 GB local disk

5.  1 vector computing node with 1 12-core Intel Xeon Gold 6126 (Skylake
    generation, 2.6 GHz), 96 GB RAM and 2 NEC SX-Aurora Vector Engines
    type 10B (per card 8 cores @1.4 GHz, 48 GB HBM2), 240 GB local disk

6.  1 Xeon Phi node with 2 14-core Intel E5-2680v4 CPUs (Broadwell
    generation, 2.4 GHz), 128 GB RAM and Intel Xeon Phi 7220P PCIe card
    with 16 GB of RAM, 120 GB local disk

7.  1 visualisation node with 2 14-core Intel E5-2680v4 CPUs (Broadwell
    generation, 2.4 GHz), 256 GB RAM and with a NVIDIA P5000 GPU, 120 GB
    local disk

The nodes are connected using an InfiniBand EDR network except for the
"hopper" compute nodes that utilize FDR10 InfiniBand.

Vaughan:

1.  104 compute nodes with 2 32-core AMD Epyc 7452 (2.35 GHz) and 256 GB
    RAM, 240 GB local disk

The nodes are connected using an InfiniBand HDR100 network.
{%- endif %}

{% if site == leuven -%}
1.  ThinKing (thin node cluster)

    -   176 compute nodes with 2 10-core Ivy Bridge processors, 64 GB
        memory, 300 GB local disk, QDR-IB network

    -   32 compute nodes with 2 10-core Ivy Bridge processors, 128 GB
        memory, 300 GB local disk, QDR-IB network

    -   48 compute nodes with 2 12-core Ivy Bridge processors, 64 GB
        memory, 300 GB local disk, QDR-IB network

2.  Accelerator partition

    -   8 nodes with 2 8-core Sandy Bridge processors, 64 GB memory, 300
        GB local disk, DDR-IB network, 2 K20 NVIDIA GPGPUs

    -   8 nodes with 2 8-core Sandy Bridge processors, 64 GB memory, 300
        GB local disk, DDR-IB network, 2 Intel Xeon Phis

    -   4 nodes with 2 6-core Xeon 5650 Westmere processors, 24 GB
        memory, 300 GB local disk, DDR-IB network, 2 Tesla M2070 GPGPUs

    -   5 nodes with 2 10-core Haswell Xeon E5-2650v3 processors, 64 GB
        memory, 300 GB local disk, DDR-IB network, 2 Tesla K40 GPGPUs

3.  Visualization partition

    -   2 nodes with 2 10-core Haswell Xeon E5-2650v3 processors, 128 GB
        memory, 300 GB local disk, DDR-IB network, 2 NVIDIA Quadro K5200
        GPUs (visualization nodes)

4.  Cerebro (shared memory SMP section)

    -   64 sockets with 10-core Xeon E5-4650 processors, total 14 TB
        memory, SGI-proprietary NUMAlink6 interconnect, 1 partition has
        480 cores and 12 TB RAM and another partition has 160 cores and
        2 TB RAM, both partitions have 10TB local scratch space
{%- endif %}

{% if site == brussel -%}
a mix of nodes with AMD and Intel CPUs and different interconnects in
different sections of the cluster. The cluster also contains a number of
nodes with NVIDIA GPGPUs. For an up to date list of all clusters and
their hardware, see 
<https://vscdocumentation.readthedocs.io/en/latest/brussels/tier2_hardware.html>.
{%- endif %}

{% if site == gent -%}
a set of different compute clusters. For an up to date list of all
clusters and their hardware, see <https://vscdocumentation.readthedocs.io/en/latest/gent/tier2_hardware.html>.
{%- endif %}

{% if site == antwerpen -%}
All the nodes in the {{ hpc }} run under the "{{ operatingsystem }}" operating system, which is a clone
of "{{ operatingsystembase }}", with *cgroups* support. 
{%- endif %}

{% if site == leuven %}
All the nodes in the run under the "{{ operatingsystem }}"
operating system. 
{%- endif %}

{% if site == brussel -%}
All the nodes in the run under the "{{ operatingsystem }}" operating
system, which is a clone of "{{ operatingsystembase }}", with *cpuset* support.
{%- endif %}

{% if site == gent -%}
**Job management** and **job scheduling** are performed by Slurm with a Torque frontend. We advise users to
adhere to Torque commands mentioned in this document. 
{%- endif %}

{% if site != gent -%}
Two tools perform the **Job management** and **job scheduling**:

1.  TORQUE: a resource manager (based on PBS);

2.  Moab: job scheduler and management tools.
{%- endif %}

{% if site == leuven -%}
**Accounting** is handled by a third tool, i.e., MAM (Moab Accounting Manager).
{%- endif %}

{% if site == antwerpen -%}
For maintenance and monitoring, we use:

1.  Ganglia: monitoring software;

2.  Icinga and Nagios: alert manager.
{%- endif %}

{% if site == leuven -%}
For maintenance and monitoring, we use:

1.  Ganglia: monitoring software;

2.  HP Insight Cluster Management Utility.
{%- endif %}

{% if site == leuven -%}
For maintenance and monitoring, we use:

1.  Bright Cluster Manager;

2.  Zabbix: monitoring system.
{%- endif %}

## What the HPC infrastucture is *not*

The HPC infrastructure is *not* a magic computer that automatically:

1.  runs your PC-applications much faster for bigger problems;

2.  develops your applications;

3.  solves your bugs;

4.  does your thinking;

5.  ...

6.  allows you to play games even faster.

The {{ hpc }} does not replace your desktop computer.


## Is the {{ hpc }} a solution for my computational needs?

### Batch or interactive mode?

Typically, the strength of a supercomputer comes from its ability to run
a huge number of programs (i.e., executables) in parallel without any
user interaction in real time. This is what is called "running in batch
mode".

It is also possible to run programs at the {{ hpc }}, which require user
interaction. (pushing buttons, entering input data, etc.). Although
technically possible, the use of the {{ hpc }} might not always be the best and
smartest option to run those interactive programs. Each time some user
interaction is needed, the computer will wait for user input. The
available computer resources (CPU, storage, network, etc.) might not be
optimally used in those cases. A more in-depth analysis with the {{ hpc }} staff
can unveil whether the {{ hpc }} is the desired solution to run interactive
programs. Interactive mode is typically only useful for creating quick
visualisations of your data without having to copy your data to your
desktop and back.

### What are cores, processors and nodes?

In this manual, the terms core, processor and node will be frequently
used, so it's useful to understand what they are.

Modern servers, also referred to as *(worker)nodes* in the context of
HPC, include one or more sockets, each housing a multi-*core*
*processor* (next to memory, disk(s), network cards, ...). A modern
*processor* consists of multiple CPUs or *cores* that are used to
execute *computations*.

### Parallel or sequential programs? 

#### Parallel programs

**Parallel computing** is a form of computation in which many calculations are carried out
simultaneously. They are based on the principle that large problems can
often be divided into smaller ones, which are then solved concurrently
("in parallel").

Parallel computers can be roughly classified according to the level at
which the hardware supports parallelism, with multicore computers having
multiple processing elements within a single machine, while clusters use
multiple computers to work on the same task. Parallel computing has
become the dominant computer architecture, mainly in the form of
multicore processors.

The two parallel programming paradigms most used in HPC are:

-   OpenMP for shared memory systems (multithreading): on multiple cores
    of a single node

-   MPI for distributed memory systems (multiprocessing): on multiple
    nodes

**Parallel programs** are more difficult to write than sequential ones, because concurrency
introduces several new classes of potential software bugs, of which race
conditions are the most common. Communication and synchronisation
between the different subtasks are typically some of the greatest
obstacles to getting good parallel program performance.

#### Sequential programs

Sequential software does not do calculations in parallel, i.e., it only
uses *one single core of a single workernode*. **It does not become faster by just throwing more cores at it**: it can only use one
core.

It is perfectly possible to also run purely **sequential programs** on the {{ hpc }}.

Running your sequential programs on the most modern and fastest
computers in the {{ hpc }} can save you a lot of time. But it also might be
possible to run multiple instances of your program (e.g., with different
input parameters) on the {{ hpc }}, in order to solve one overall problem (e.g.,
to perform a parameter sweep). This is another form of running your
sequential programs in parallel.

### What programming languages can I use?

You can use *any* programming language, *any* software package and *any*
library provided it has a version that runs on Linux, specifically, on
the version of Linux that is installed on the compute nodes, {{ operatingsystem }}.

For the most common **programming languages**, a compiler is available on {{ operatingsystem }}. Supported and common
programming languages on the {{ hpc }} are C/C++, FORTRAN, Java, Perl, Python,
MATLAB, R, etc.

Supported and commonly used compilers are 
{%- if site == antwerpen %} GCC, clang, J2EE and Intel {%- endif %}
{%- if site == leuven %} Cluster Studio. GCC, Intel and PGI. {%- endif %}
{%- if site == brussel %} GCC, clang, J2EE and Intel Cluster Studio.{%- endif %}
{%- if site == gent %} GCC and Intel.{%- endif %}

{% if site == antwerpen -%}
Commonly used software packages are:

-   in bioinformatics: beagle, Beast, bowtie, MrBayes, SAMtools

-   in chemistry: ABINIT, CP2K, Gaussian, Gromacs, LAMMPS, NWChem,
    Quantum Espresso, Siesta, VASP

-   in engineering: COMSOL, OpenFOAM, Telemac

-   in mathematics: JAGS, MATLAB, R

-   for visuzalization: Gnuplot, ParaView.

Commonly used libraries are Intel MKL, FFTW, HDF5, PETSc and Intel MPI,
OpenMPI. 
{%- endif %}

{%- if site == leuven -%}
Commonly used software packages are:

-   in bioinformatics: beagle, Beast, bedtools, bowtie, BWA, Mr. Bayes,
    TopHat, TRIQS,

-   in chemistry: CP2K, Gaussian, GROMACS, Molpro, NAMD, NWChem, Siesta,
    Turbomole, VASP, VMD,

-   in engineering: Abaqus, Ansys, Comsol, OpenFOAM,

-   in mathematics: JAGS, MATLAB, R, SAS,

-   for visuzalization: Gnuplot, IDL, Paraview, Tecplot, VisIt.

Commonly used libraries are: Intel MKL, FFTW, HDF5, PETSc, Intel MPI,
M(VA)PICH, OpenMPI, Qt, VTK and Mesa. 
{%- endif %}
{%- if site == brussel -%}
Commonly used software packages are CP2K, Gaussian, MATLAB, NWChem, R, ...

Commonly used Libraries are Intel MKL, FFTW, HDF5, netCDF, PETSc and
Intel MPI, OpenMPI.
{%- endif %}
Additional software can be installed "*on demand*". Please contact the {{ hpc }}
staff to see whether the {{ hpc }} can handle your specific requirements.

### What operating systems can I use? 

All nodes in the {{ hpc }} cluster run under {{ operatingsystem }}, which is a specific version of {{ operatingsystembase }}.
This means that all programs (executables) should be compiled for {{ operatingsystem }}.

Users can connect from any computer in the {{ university }} network to the {{ hpc }}, regardless
of the Operating System that they are using on their personal computer.
Users can use any of the common Operating Systems (such as Windows,
macOS or any version of Linux/Unix/BSD) and run and control their
programs on the {{ hpc }}.

A user does not need to have prior knowledge about Linux; all of the
required knowledge is explained in this tutorial.

### What does a typical workflow look like?

A typical workflow looks like:

1.  Connect to the login nodes with SSH (see [First Time connection to the HPC infrastructure](../connecting/#first-time-connection-to-the-hpc-infrastructure))

2.  Transfer your files to the cluster (see [Transfer Files to/from the HPC](../connecting/#transfer-files-tofrom-the-hpc))

3.  Optional: compile your code and test it (for compiling, see [Compiling and testing your software on the HPC]())

4.  Create a job script and submit your job (see [Running batch jobs]())

5.  Get some coffee and be patient:

    1.  Your job gets into the queue

    2.  Your job gets executed

    3.  Your job finishes

6.  Study the results generated by your jobs, either on the cluster or
    after downloading them locally.

### What is the next step? 

When you think that the {{ hpc }} is a useful tool to support your computational
needs, we encourage you to acquire a VSC-account (as explained in [Getting a HPC Account](../account)),
read [Connecting to the HPC infrastructure](../connecting), "Setting up the environment", and explore
chapters [Running interactive jobs]() to [Fine-tuning Job Specifications]() which will help you to transfer and run your programs on the {{ hpc }} cluster.

Do not hesitate to contact the {{ hpc }} staff for any help.

[^1]: Wikipedia: <http://en.wikipedia.org/wiki/Supercomputer>
