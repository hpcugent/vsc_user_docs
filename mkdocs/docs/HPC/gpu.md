# GPU clusters

## Submitting jobs

To submit jobs to the `joltik` GPU cluster, where each node provides 4
NVIDIA V100 GPUs (each with 32GB of GPU memory), use:

<pre><code>$ <b>module swap cluster/joltik</b>
</code></pre>

To submit to the `accelgor` GPU cluster, where each node provides 4
NVIDIA A100 GPUs (each with 80GB GPU memory), use:

<pre><code>$ <b>module swap cluster/accelgor</b>
</code></pre>

Then use the familiar `qsub`, `qstat`, etc. commands, taking into
account the guidelines outlined in
section [Requesting (GPU) resources](./#requesting-gpu-resources).

### Interactive jobs

To interactively experiment with GPUs, you can submit an interactive job
using `qsub -I` (and request one or more GPUs, see
section [Requesting (GPU) resources](./#requesting-gpu-resources)).

Note that due to a bug in Slurm you will currently not be able to be
able to interactively use MPI software that requires access to the GPUs.
If you need this, please contact use via {{hpcinfo}}.

## Hardware

See <https://www.ugent.be/hpc/en/infrastructure>.

## Requesting (GPU) resources

There are 2 main ways to ask for GPUs as part of a job:

-   Either as a node property (similar to the number of cores per node
    specified via `ppn`) using `-l nodes=X:ppn=Y:gpus=Z` (where the
    `ppn=Y` is optional), or as a separate resource request (similar to
    the amount of memory) via `-l gpus=Z`. Both notations give exactly
    the same result. The `-l gpus=Z` is convenient is you only need one
    node and you are fine with the default number of cores per GPU. The
    `-l nodes=...:gpus=Z` notation is required if you want to run with
    full control or in multinode cases like MPI jobs. If you do not
    specify the number of GPUs by just using `-l gpus`, you get by
    default 1 GPU.

-   As a resource of it's own, via `--gpus X`. In this case however, you
    are *not* guaranteed that the GPUs are on the same node, so your
    script or code must be able to deal with this.

<!-- %  TODO We are providing a parallel wrapper ``wurker'' in the ``vsc-mympirun'' module to help with this
%  (and with other more usual parallel work, similar to the usual ``worker'' or ``atools'' tools).
%\item As a partial node resource, via ``-l nodes=...:mps=Z'' or ``-l mps=Z''.
%  This triggers the Multi-Process Service (MPS, see https://docs.nvidia.com/deploy/pdf/CUDA_Multi_Process_Service_Overview.pdf),
%  a way to ask for part of a GPU. The ``mps=`` value is a percentage of a GPU, and when submitting the job,
%  you typically ask for a multiple of 100. The jobscript can then hand out portions of this (e.g. 50 per task) to the actual work.
%  This is useful when a single application or MPI task cannot utilise a single/full GPU, and there are many other similar tasks that
%  need to be processed or increasing the MPI ranks gives a speedup (e.g. when there is a significant portion of CPU work in the code).
%  Unfortunately, this is not a silver bullet, and might require some experimenting to found out any potential benefits and proper tuning.
%  TODO: how can a user now that an application is not using the full gpu resources?
%  TODO this needs testing and there are some constraints (eg one mps job per node and thus one user per node using MPS)
%  TODO needs proper integration with mypmirun / wurker
%  TODO add separate section on MPS -->

Some background:

-   The GPUs are constrained to the jobs (like the CPU cores), but do
    not run in so-called "exclusive" mode.

-   The GPUs run with the so-called "persistence daemon", so the GPUs is
    not re-initialised between jobs.

<!-- %  TODO: we need to fix this in the pro/epilogue scripts? is this similar to regular RAM? -->

<!-- %TODO: add examples ? -->

## Attention points

Some important attention points:

-   For MPI jobs, we recommend the (new) wrapper `mypmirun` from the
    `vsc-mympirun` module (`pmi` is the background mechanism to start
    the MPI tasks, and is different from the usual `mpirun` that is used
    by the `mympirun` wrapper). At some later point, we *might* promote
    the `mypmirun` tool or rename it, to avoid the confusion in the
    naming).

-   Sharing GPUs requires MPS. The Slurm built-in MPS does not really do
    want you want, so we will provide integration with `mypmirun` and
    `wurker`.

-   For parallel work, we are working on a `wurker` wrapper from the
    `vsc-mympirun` module that supports GPU placement and MPS, without
    any limitations wrt the requested resources (i.e. also support the
    case where GPUs are spread heterogenous over nodes from using the
    `--gpus Z` option).

-   Both `mypmirun` and `wurker` will try to do the most optimised
    placement of cores and tasks, and will provide 1 (optimal) GPU per
    task/MPI rank, and set one so-called *visible device* (i.e.
    `CUDA_VISIBLE_DEVICES` only has 1 ID). The actual devices are not
    constrained to the ranks, so you can access all devices requested in
    the job. *We know that at this moment, this is not working properly, but we are working on this. We advise against trying to fix this yourself.*

  <!-- % TODO: this is still not the case, due to bugs in slurm. For now, you will probably do not get optimal placement and/or more
  %than one visible device.
  %TODO: we need an easy way to toggle this behaviour.
  %TODO: should be configurable from qsub somehow. Or we need to wait for fix or patch it ourself. -->

<!-- %TODO: add section on mypmirun, but has nothing to do with joltik. It works on all ugent/slurm clusters with and supports intelmpi.
%Main advantages are single tool instead of per-MPI mpirun flavour, improved accouting and faster startup. -->

## Software with GPU support

Use `module avail` to check for centrally installed software.

The subsections below only cover a couple of installed software
packages, more are available.

### GROMACS

Please consult `module avail GROMACS` for a list of installed versions.

### Horovod

Horovod can be used for (multi-node) multi-GPU TensorFlow/PyTorch
calculations.

Please consult `module avail Horovod` for a list of installed versions.

Horovod supports TensorFlow, Keras, PyTorch and MxNet (see
<https://github.com/horovod/horovod#id9>), but should be run as an MPI
application with `mypmirun`. (Horovod also provides it's own wrapper
`horovodrun`, not sure if it handles placement and others correctly).

At least for simple TensorFlow benchmarks, it looks like Horovod is a
bit faster than usual autodetect multi-GPU TensorFlow without horovod,
but it comes at the cost of the code modifications to use horovod.

<!--
%TODO: use NCCL version (only check is to export NCCL_DEBUG=INFO)
%TODO: NCCL tuning https://docs.nvidia.com/deeplearning/sdk/nccl-developer-guide/docs/env.html
%-> joltik: NCCL_NET_GDR_LEVEL=4 -> in environment -->

### PyTorch

Please consult `module avail PyTorch` for a list of installed versions.

### TensorFlow

Please consult `module avail TensorFlow` for a list of installed
versions.

**Note: for running TensorFlow calculations on multiple GPUs and/or on more than one workernode, use `Horovod`, see section [Horovod](./#horovod).**

#### Example TensorFlow job script

<center>-- TensorFlow_GPU.sh --</center>
```bash
{% include "./examples/HPC-UGent-GPU-clusters/TensorFlow_GPU.sh" %}
```

<!-- %TODO: add intel cpu params (only for cpu, but mention it anyway) and data format (channel_first  / NCHW)
% OMP_NUM_THREADS=$PBS_VARIABLE_FOR_CORES
% KMP_BLOCKTIME=0
% KMP_AFFINITY="granularity=fine,verbose,compact,1,0"
% KMP_SETTINGS=1

%TODO: quid tensorcores and bfloat16 etc etc?

%TODO: even on single node, horovod is faster (5\%) with nccl? (at least for simple benchmark) -->

### AlphaFold

Please consult `module avail AlphaFold` for a list of installed
versions.

For more information on using AlphaFold, we strongly recommend the
VIB-UGent course available at
<https://elearning.bits.vib.be/courses/alphafold>.

## Getting help

In case of questions or problems, please contact the {{hpcteam}} via {{hpcinfo}}, and clearly
indicate that your question relates to the `joltik` cluster by adding
`[joltik]` in the email subject.
