# Job script examples

## Simple job script template

This is a template for a job script, with commonly used parameters.
The basic parameters should always be used. Some notes on the situational parameters:

*   `-l mem`: If no memory parameter is given, the job gets access to an amount of
    memory proportional to the amount of cores requested.
    See also: [Job failed: SEGV Segmentation fault](../FAQ/#job-failed-segv-segmentation-fault)

*   `-m/-M`: the `-m` option will send emails to your email address registerd with VSC.
    Only if you want emails at some other address, you should use the `-M` option.

*   Replace the "`-placeholder text-`" with real entries.
    This notation is used to ensure `qsub` rejects invalid options.

*   To use a situational parameter, remove one '`#`' at the beginning of the line.

```shell
#!/bin/bash

# Basic parameters
#PBS -N jobname           ## Job name
#PBS -l nodes=1:ppn=2     ## 1 node, 2 processors per node (ppn=all to get a full node)
#PBS -l walltime=01:00:00 ## Max time your job will run (no more than 72:00:00)

# Situational parameters: remove one '#' at the front to use
##PBS -l gpus=1            ## GPU amount (only on accelgor or joltik)
##PBS -l mem=32gb          ## If not used, memory will be available proportional to the max amount
##PBS -m abe               ## Email notifications (abe=aborted, begin and end)
##PBS -M -email_address-   ## ONLY if you want to use a different email than your VSC address
##PBS -A -project-         ## Project name when credits are required (only Tier 1)

##PBS -o -filename-        ## Output log
##PBS -e -filename-        ## Error log


module load [module]
module load [module]

cd $PBS_O_WORKDIR         # Change working directory to the location where the job was submmitted

[commands]
```

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
