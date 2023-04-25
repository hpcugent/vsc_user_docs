# Mympirun

`mympirun` is a tool to make it easier for users of HPC clusters to run
MPI programs with good performance. We strongly recommend to use
`mympirun` instead of `impirun`.

In this chapter, we give a high-level overview. For a more detailed
description of all options, see the [vsc-mympirun
README](https://github.com/hpcugent/vsc-mympirun/blob/master/README.md).

## Basic usage

Before using `mympirun`, we first need to load its module:

<pre><code>$ <b>module load vsc-mympirun</b>
</code></pre>

As an exception, we don't specify a version here. The reason is that we
want to ensure that the latest version of the `mympirun` script is
always used, since it may include important bug fixes or improvements.

The most basic form of using `mympirun` is
`mympirun [mympirun options] your_program [your_program options]`.

For example, to run a program named `example` and give it a single
argument (`5`), we can run it with `mympirun example 5`.

## Controlling number of processes

There are four options you can choose from to control the number of
processes `mympirun` will start. In the following example, the program
`mpi_hello` prints a single line:
`Hello world from processor <node> ...` (the sourcecode of `mpi_hello`
is [available in the vsc-mympirun
repository](https://github.com/hpcugent/vsc-mympirun/blob/master/testscripts/mpi_helloworld.c)).

By default, `mympirun` starts one process per *core* on every node you
assigned. So if you assigned 2 nodes with 16 cores each, `mympirun` will
start 2 . 16 = 32 test processes in total.

### `--hybrid`/`-h`

This is the most commonly used option for controlling the number of
processing.

The `--hybrid` option requires a positive number. This number specifies
the number of processes started on each available physical *node*. It
will ignore the number of available *cores* per node.

<pre><code>$ <b>echo $PBS_NUM_NODES</b>
2
$ <b>mympirun --hybrid 2 ./mpihello</b>
Hello world from processor node3400.doduo.os, rank 1 out of 4 processors 
Hello world from processor node3401.doduo.os, rank 3 out of 4 processors 
Hello world from processor node3401.doduo.os, rank 2 out of 4 processors 
Hello world from processor node3400.doduo.os, rank 0 out of 4 processors
</code></pre>

### Other options

There's also `--universe`, which sets the exact amount of processes
started by `mympirun`; `--double`, which uses double the amount of
processes it normally would; and `--multi` that does the same as
`--double`, but takes a multiplier (instead of the implied factor 2 with
`--double`).

See [vsc-mympirun
README](https://github.com/hpcugent/vsc-mympirun/blob/master/README.md)
for a detailed explanation of these options.

## Dry run

You can do a so-called "dry run", which doesn't have any side-effects,
but just prints the command that `mympirun` would execute. You enable
this with the `--dry-run` flag:

<pre><code>$ <b>mympirun --dry-run ./mpi_hello</b>
mpirun ... -genv I_MPI_FABRICS shm:dapl ... -np 16 ... ./mpi_hello
</code></pre>
