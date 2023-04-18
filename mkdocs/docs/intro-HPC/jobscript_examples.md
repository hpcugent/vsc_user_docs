# Job script examples

## Single-core job

Here's an example of a single-core job script:
<p style="text-align: center">single_core.sh</p>

```shell
{% include "examples/Job-script-examples/single_core.sh" %}
```


1.  Using `#PBS` header lines, we specify the resource requirements for
    the job, see [Apendix B](torque_options.md) for a list of these options.

2.  A module for `Python 3.6` is loaded, see also section [Modules](running_batch_jobs.md#modules).

3.  We stage the data in: the file `input.txt` is copied into the
    "working" directory, see chapter [Running jobs with input/output data](running_jobs_with_input_output_data.md).

4.  The main part of the script runs a small Python program that counts
    the number of characters in the provided input file `input.txt`.

5.  We stage the results out: the output file `output.txt` is copied
    from the "working directory" (`$TMPDIR`|) to a unique directory in
    `$VSC_DATA`. For a list of possible storage locations, see subsection [ Pre-defined user directories](running_jobs_with_input_output_data.md#pre-defined-user-directories).

## Multi-core job

Here's an example of a multi-core job script that uses `mympirun`:

<p style="text-align: center">multi_core.sh</p>

```shell
{% include "examples/Job-script-examples/multi_core.sh" %}
```


An example MPI hello world program can be downloaded from
<https://github.com/hpcugent/vsc-mympirun/blob/master/testscripts/mpi_helloworld.c>.

## Running a command with a maximum time limit

If you want to run a job, but you are not sure it will finish before the
job runs out of walltime and you want to copy data back before, you have
to stop the main command before the walltime runs out and copy the data
back.

This can be done with the `timeout` command. This command sets a limit
of time a program can run for, and when this limit is exceeded, it kills
the program. Here's an example job script using `timeout`:

<p style="text-align: center">timeout.sh</p>

```shell
{% include "examples/Job-script-examples/timeout.sh" %}
```

The example program used in this script is a dummy script that simply
sleeps a specified amount of minutes:

<p style="text-align: center">example_program.sh</p>

```shell
{% include "examples/Job-script-examples/example_program.sh" %}
```