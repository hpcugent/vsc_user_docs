# Singularity { #ch:singularity}

## What is Singularity?

Singularity is an open-source computer program that performs
operating-system-level virtualization (also known as containerisation).

One of the main uses of Singularity is to bring containers and
reproducibility to scientific computing and the high-performance
computing (HPC) world. Using Singularity containers, developers can work
in reproducible environments of their choosing and design, and these
complete environments can easily be copied and executed on other
platforms.

For more general information about the use of Singularity, please see
the official documentation at <https://www.sylabs.io/docs/>.

This documentation only covers aspects of using Singularity on the
infrastructure.

## Restrictions on image location

Some restrictions have been put in place on the use of Singularity. This
is mainly done for performance reasons and to avoid that the use of
Singularity impacts other users on the system.

The Singularity image file must be located on either one of the scratch
filesystems, the local disk of the workernode you are using or
`/dev/shm`. The centrally provided `singularity` command will refuse to
run using images that are located elsewhere, in particular on the
`$VSC_HOME`, `/apps` or `$VSC_DATA` filesystems.

In addition, this implies that running containers images provided via a
URL (e.g., `shub://...` or `docker://...`) will not work.

If these limitations are a problem for you, please let us know via .

## Available filesystems

All HPC-UGent shared filesystems will be readily available in a
Singularity container, including the home, data and scratch filesystems,
and they will be accessible via the familiar `$VSC_HOME`, `$VSC_DATA*`
and `$VSC_SCRATCH*` environment variables.

## Singularity Images

### Creating Singularity images

Creating new Singularity images or converting Docker images, by default,
requires admin privileges, which is obviously not available on the
infrastructure. However, if you use the `--fakeroot` option, you can
make new Singularity images or convert Docker images.

When you make Singularity or convert Docker images you have some
restrictions:

-   Due to the nature of `--fakeroot` option, we recommend to write your
    singularity image to a globally writable location, like `/tmp`, or
    `/local` directories. Once the images is created, you should move it
    to your desired destination.

### Converting Docker images

For more information on converting existing Docker images to Singularity
images, see
<https://www.sylabs.io/guides/3.4/user-guide/singularity_and_docker.html>.

We strongly recommend the use of Docker Hub, see
<https://hub.docker.com/> for more information.

## Execute our own script within our container

Copy testing image from `/apps/gent/tutorials/Singularity` to
`$VSC_SCRATCH`:

::: prompt
:::

Create a job script like:

Create an example `myscript.sh`:

::: code
bash #!/bin/bash

\# prime factors factor 1234567
:::

## Tensorflow example

We already have a Tensorflow example image, but you can also convert the
Docker image (see <https://hub.docker.com/r/tensorflow/tensorflow>) to a
Singularity image yourself

Copy testing image from `/apps/gent/tutorials` to `$VSC_SCRATCH`:

::: prompt
:::

You can download `linear_regression.py` from [the official Tensorflow
repository](https://github.com/tensorflow/tensorflow/blob/r1.12/tensorflow/examples/get_started/regression/linear_regression.py).

## MPI example

It is also possible to execute MPI jobs within a container, but the
following requirements apply:

-   Mellanox IB libraries must be available from the container (install
    the `infiniband-diags`, `libmlx5-1` and `libmlx4-1` OS packages)

-   Use modules within the container (install the `environment-modules`
    or `lmod` package in your container)

-   Load the required module(s) before `singularity` execution.

-   Set `C_INCLUDE_PATH` variable in your container if it is required
    during compilation time
    (`export C_INCLUDE_PATH=/usr/include/x86_64-linux-gnu/:$C_INCLUDE_PATH`
    for Debian flavours)

Copy the testing image from `/apps/gent/tutorials/Singularity` to
`$VSC_SCRATCH`

::: prompt
:::

For example to compile an [MPI
example](https://github.com/open-mpi/ompi/blob/master/examples/ring_c.c):

::: prompt
:::

Example MPI job script:
