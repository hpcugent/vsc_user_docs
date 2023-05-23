# Apptainer (formally known as Singularity)

## What is Apptainer?

Apptainer is an open-source computer program that performs
operating-system-level virtualization (also known as containerisation).

One of the main uses of Apptainer is to bring containers and
reproducibility to scientific computing and the high-performance
computing (HPC) world. Using Apptainer/Singularity containers,
developers can work in reproducible environments of their choosing and
design, and these complete environments can easily be copied and
executed on other platforms.

For more general information about the use of Apptainer, please see the
official documentation at <https://apptainer.org/docs/>.

This documentation only covers aspects of using Apptainer on the
{{hpcinfra}} infrastructure.

## Restrictions on image location

Some restrictions have been put in place on the use of Apptainer. This
is mainly done for performance reasons and to avoid that the use of
Apptainer impacts other users on the system.

The Apptainer/Singularity image file must be located on either one of
the scratch filesystems, the local disk of the workernode you are using
or `/dev/shm`. The centrally provided `apptainer` command will refuse to
run using images that are located elsewhere, in particular on the
`$VSC_HOME`, `/apps` or `$VSC_DATA` filesystems.

In addition, this implies that running containers images provided via a
URL (e.g., `shub://...` or `docker://...`) will not work.

If these limitations are a problem for you, please let us know via {{hpcinfo}}.

## Available filesystems

All HPC-UGent shared filesystems will be readily available in an
Apptainer/Singularity container, including the home, data and scratch
filesystems, and they will be accessible via the familiar `$VSC_HOME`,
`$VSC_DATA*` and `$VSC_SCRATCH*` environment variables.

## Apptainer/Singularity Images

### Creating Apptainer/Singularity images

Creating new Apptainer/Singularity images or converting Docker images,
by default, requires admin privileges, which is obviously not available
on the {{hpcinfra}} infrastructure. However, if you use the `--fakeroot` option, you
can make new Apptainer/Singularity images or convert Docker images.

Due to the nature of `--fakeroot` option, we recommend to write your
Apptainer/Singularity image to a globally writable location, like
`/tmp`, or `/local` directories. Once the image is created, you should
move it to your desired destination. An example to make an
Apptainer/Singularity container:

<pre><code>$ <b>APPTAINER_CACHEDIR=/tmp/ \
APPTAINER_TMPDIR=/tmp/ \
apptainer build --fakeroot /tmp/tensorflow-21.10-tf1-py3.sif \
docker://nvcr.io/nvidia/tensorflow:21.10-tf1-py3</b>
</code></pre>

### Converting Docker images

For more information on converting existing Docker images to
Apptainer/Singularity images, see
<https://apptainer.org/docs/user/main/docker_and_oci.html>.

We strongly recommend the use of Docker Hub, see
<https://hub.docker.com/> for more information.

## Execute our own script within our container

Copy testing image from `/apps/gent/tutorials/Singularity` to
`$VSC_SCRATCH`:

<pre><code>$ <b>cp /apps/gent/tutorials/Singularity/CentOS7_EasyBuild.img $VSC_SCRATCH/</b>
</code></pre>

Create a job script like:

```bash
#!/bin/sh

#PBS -o apptainer.output
#PBS -e apptainer.error
#PBS -l nodes=1:ppn=1
#PBS -l walltime=12:00:00


apptainer exec $VSC_SCRATCH/CentOS7_EasyBuild.img ~/my_script.sh
```

Create an example `myscript.sh`:

```bash
#!/bin/bash

# prime factors
factor 1234567
```

## Tensorflow example

We already have a Tensorflow example image, but you can also convert the
Docker image (see <https://hub.docker.com/r/tensorflow/tensorflow>) to a
Apptainer/Singularity image yourself

Copy testing image from `/apps/gent/tutorials` to `$VSC_SCRATCH`:

<pre><code>$ <b>cp /apps/gent/tutorials/Singularity/Ubuntu14.04_tensorflow.img $VSC_SCRATCH/</b>
</code></pre>

```bash
#!/bin/sh
#
#
#PBS -o tensorflow.output
#PBS -e tensorflow.error
#PBS -l nodes=1:ppn=4
#PBS -l walltime=12:00:00
#

apptainer exec $VSC_SCRATCH/Ubuntu14.04_tensorflow.img python ~/linear_regression.py
```

You can download `linear_regression.py` from [the official Tensorflow
repository](https://github.com/tensorflow/tensorflow/blob/r1.12/tensorflow/examples/get_started/regression/linear_regression.py).

## MPI example

It is also possible to execute MPI jobs within a container, but the
following requirements apply:

-   Mellanox IB libraries must be available from the container (install
    the `infiniband-diags`, `libmlx5-1` and `libmlx4-1` OS packages)

-   Use modules within the container (install the `environment-modules`
    or `lmod` package in your container)

-   Load the required module(s) before `apptainer` execution.

-   Set `C_INCLUDE_PATH` variable in your container if it is required
    during compilation time
    (`export C_INCLUDE_PATH=/usr/include/x86_64-linux-gnu/:$C_INCLUDE_PATH`
    for Debian flavours)

Copy the testing image from `/apps/gent/tutorials/Singularity` to
`$VSC_SCRATCH`

<pre><code>$ <b>cp /apps/gent/tutorials/Singularity/Debian8_UGentMPI.img $VSC_SCRATCH/</b>
</code></pre>

For example to compile an [MPI
example](https://github.com/open-mpi/ompi/blob/master/examples/ring_c.c):

<pre><code>$ <b>module load intel</b>
$ <b>apptainer shell $VSC_SCRATCH/Debian8_UGentMPI.img</b>
$ <b>export LANG=C</b>
$ <b>export C_INCLUDE_PATH=/usr/include/x86_64-linux-gnu/:$C_INCLUDE_PATH</b>
$ <b>mpiicc ompi/examples/ring_c.c -o ring_debian</b>
$ <b>exit</b>
</code></pre>

Example MPI job script:

```bash
#!/bin/sh

#PBS -N mpi
#PBS -o apptainermpi.output
#PBS -e apptainermpi.error
#PBS -l nodes=2:ppn=15
#PBS -l walltime=12:00:00

module load intel vsc-mympirun
mympirun --impi-fallback apptainer exec $VSC_SCRATCH/Debian8_UGentMPI.img ~/ring_debian
```
