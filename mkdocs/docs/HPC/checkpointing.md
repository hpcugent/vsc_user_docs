# Checkpointing { #ch:checkpointing}

## Why checkpointing?

If you want to run jobs that require wall time than the maximum wall
time per job and/or want to avoid you lose work because of power outages
or system crashes, you need to resort to checkpointing.

## What is checkpointing?

Checkpointing allows for running jobs that run for weeks or months, by
splitting the job into smaller parts (called subjobs) which are executed
consecutively. Each time a subjob is running out of requested wall time,
a snapshot of the application memory (and much more) is taken and
stored, after which a subsequent subjob will pick up the checkpoint and
continue.

## How to use checkpointing?

Using checkpointing is very simple: just use `csub` instead of `qsub` to
submit a job.

The `csub` command creates a wrapper around your job script, to take
care of all the checkpointing stuff.

In practice, you (usually) don't need to adjust anything, except for the
command used to submit your job.

Checkpointing does not require any changes to the application you are
running, and should support most software.

## Usage and parameters

An overview of the usage and various command line parameters is given
here.

### Submitting a job

Typically, a job script is submitted with checkpointing support enabled
by running:

::: prompt
csub -s job_script.sh
:::

The `-s` flag specifies the job script to run.

### Caveat: don't create local directories

One important caveat is that the job script (or the applications run in
the script) should *not* create its own local temporary directories,
because those will not (always) be restored when the job is restarted
from checkpoint.

### PBS directives

Most PBS directives (`#PBS …` specified in the job script will be
ignored. There are a few exceptions however, i.e., `# PBS -N <name>`
(job name) and all `-l` directives (`# PBS -l`), e.g., `nodes`, `ppn`,
`vmem` (virtual memory limit), etc. Controlling other job parameters
(like requested walltime per sub-job) should be specified on the `csub`
command line.

### Getting help

Help on the various command line parameters supported by `csub` can be
obtained using `-h` or `--help`.

### Local files (`–pre` / `–post`)

The `--pre` and `--post` parameters control whether local files are
copied or not. The job submitted using `csub` is (by default) run on the
local storage provided by a particular workernode. Thus, no changes will
be made to the files on the shared storage.

If the job script needs (local) access to the files of the directory
where `csub` is executed, `--pre` flag should be used. This will copy
all the files in the job script directory to the location where the job
script will execute.

If the output of the job (`stdout`/`stderr`) that was run, or additional
output files created by the job in its working directory are required,
the `--post` flag should be used. This will copy the entire job working
directory to the location where `csub` was executed, in a directory
named `result.<jobname>`. An alternative is to copy the interesting
files to the shared storage at the end of the job script.

### Running on shared storage (`–shared`)

If the job needs to be run on the shared storage, `--shared` should be
specified. You should enable this option by default, because it makes
the execution of the underlying `csub` script more robust: it doesn't
have to copy from/to the local storage on the workernode. When enabled,
the job will be run in a subdirectory of `$VSC_SCRATCH/chkpt`. All files
produced by the job will be in `$VSC_SCRATCH/chkpt/<jobid>/` while the
job is running.

Note that if files in the directory where the job script is located are
required to run the job, you should also use `--pre`.

### Job wall time (`–job_time`, `–chkpt_time`)

To specify the requested wall time per subjob, use the `--job-time`
parameter. The default setting is 10 hours per (sub)job. Lowering this
will result in more frequent checkpointing, and thus more (sub)jobs.

To specify the time that is reserved for checkpointing the job, use
`--chkpt_time`. By default, this is set to 15 minutes which should be
enough for most applications/jobs. *Don't change this unless you really
need to*.

The total requested wall time per subjob is the sum of both `job_time`
and `chkpt_time`.

If you would like to time how long the job executes, just prepend the
main command in your job script with the time command `time`, e.g.:

::: prompt
time main_command
:::

The `real` time will not make sense, as it will also include the time
passed between two checkpointed subjobs. However, the `user` time should
give a good indication of the actual time it took to run your command,
even if multiple checkpoints were performed.

### Resuming from last checkpoint (`–resume`)

The `--resume` option allows you to resume a job from the last available
checkpoint in case something went wrong (e.g., accidentally deleting a
(sub)job using `qdel`, a power outage or other system failure, ...).

Specify the job name as returned after submission (and as listed in
`$VSC_SCRATCH/chkpt`). The full job name consists of the specified job
name (or the script name if no job name was specified), a timestamp and
two random characters at the end, for example `my_job_name._133755.Hk`
or `script.sh._133755.Hk`.

Note: When resuming from checkpoint, you can change the wall time
resources for your job using the `--job_time` and `--chkpt_time`
options. This should allow you to continue from the last checkpoint in
case your job crashed due to an excessively long checkpointing time.

In case resuming fails for you, please contact , and include the output
of the `csub --resume` command in your message.

## Additional options

### Array jobs (`-t`)

`csub` has support for checkpointing array jobs with the `-t <spec>`
flag on the `csub` command line. This behaves the same as `qsub`, see .

### Pro/epilogue mimicking (`–no_mimic_pro_epi`)

The option `--no_mimic_pro_epi` disables the workaround currently
required to resolve a permissions problem when using actual Torque
prologue/epilogue scripts. Don't use this option unless you really know
what you are doing.

### Cleanup checkpoints (`–cleanup_after_restart`)

Specifying this option will make the wrapper script remove the
checkpoint files after a successful job restart. This may be desirable
in cause you are short on storage space.

Note that we don't recommend setting this option, because this way you
won't be able to resume from the last checkpoint when something goes
wrong. It may also prevent the wrapper script from reattempting to
resubmit a new job in case an infrequent known failure occurs. So, don't
set this unless you really need to.

### No cleanup after job completion (`–no_cleanup_chkpt`)

Specifying this option will prevent the wrapper script from cleaning up
the checkpoints and related information once the job has finished. This
may be useful for debugging, since this also preserves the
`stdout`/`stderr` of the wrapper script.

*Don't set this unless you know what you are doing*.
