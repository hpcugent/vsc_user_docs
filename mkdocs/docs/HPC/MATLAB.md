# MATLAB

!!! note
    To run a MATLAB program on the {{ hpcinfra }} **you must compile it first**,
    because the MATLAB license server is not accessible from cluster workernodes
    (except for the interactive debug cluster).

    Compiling MATLAB programs is only possible on the [interactive debug cluster](interactive_debug.md),
    **not** on the {{ hpcsite}} login nodes where resource limits w.r.t. memory and max. number of progress are too strict.

## Why is the MATLAB compiler required?

The main reason behind this alternative way of using MATLAB is
licensing: only a limited number of MATLAB sessions can be active at the
same time. However, once the MATLAB program is compiled using the MATLAB
compiler, the resulting stand-alone executable can be run without
needing to contact the license server.

Note that a license is required for the MATLAB Compiler, see
<https://nl.mathworks.com/help/compiler/index.html>. If the `mcc`
command is provided by the MATLAB installation you are using, the MATLAB
compiler can be used as explained below.

{% if site == gent %}
Only a limited amount of MATLAB sessions can be active at the same time
because there are only a limited amount of MATLAB research licenses
available on the {{university}} MATLAB license server. If each job would need a
license, licenses would quickly run out.
{% endif %}
## How to compile MATLAB code

Compiling MATLAB code can only be done from the login nodes, because
only login nodes can access the MATLAB license server, workernodes on
clusters cannot.

To access the MATLAB compiler, the `MATLAB` module should be loaded
first. Make sure you are using the same `MATLAB` version to compile and
to run the compiled MATLAB program.

```
$ module avail MATLAB/
----------------------/apps/gent/RHEL8/zen2-ib/modules/all----------------------
   MATLAB/2021b    MATLAB/2022b-r5 (D)
$ module load MATLAB/2021b
```

After loading the `MATLAB` module, the `mcc` command can be used. To get
help on `mcc`, you can run `mcc -?`.

To compile a standalone application, the `-m` flag is used (the `-v`
flag means verbose output). To show how `mcc` can be used, we use the
`magicsquare` example that comes with MATLAB.

First, we copy the `magicsquare.m` example that comes with MATLAB to
`example.m`:

```
cp $EBROOTMATLAB/extern/examples/compiler/magicsquare.m example.m
```

To compile a MATLAB program, use `mcc -mv`:

```
mcc -mv example.m
Opening log file:  {{homedir}}/java.log.34090
Compiler version: 8.3 (R2021b)
Dependency analysis by REQUIREMENTS.
Parsing file "{{homedir}}/example.m"
	(Referenced from: "Compiler Command Line").
Deleting 0 temporary MEX authorization files.
Generating file "{{homedir}}/readme.txt".
Generating file "run\_example.sh".
```

### Libraries

To compile a MATLAB program that *needs a library*, you can use the
`-I library_path` flag. This will tell the compiler to also look for
files in `library_path`.

It's also possible to use the `-a path` flag. That will result in all
files under the `path` getting added to the final executable.

For example, the command `mcc -mv example.m -I examplelib -a datafiles`
will compile `example.m` with the MATLAB files in `examplelib`, and will
include all files in the `datafiles` directory in the binary it
produces.

### Memory issues during compilation

If you are seeing Java memory issues during the compilation of your
MATLAB program on the login nodes, consider tweaking the default maximum
heap size (128M) of Java using the `_JAVA_OPTIONS` environment variable
with:

```
export _JAVA_OPTIONS="-Xmx64M"
```

The MATLAB compiler spawns multiple Java processes. Because of the
default memory limits that are in effect on the login nodes, this might
lead to a crash of the compiler if it's trying to create to many Java
processes. If we lower the heap size, more Java processes will be able
to fit in memory.

Another possible issue is that the heap size is too small. This could
result in errors like:

```
Error: Out of memory
```

A possible solution to this is by setting the maximum heap size to be
bigger:

```
export _JAVA_OPTIONS="-Xmx512M"
```

## Multithreading

MATLAB can only use the cores in a single workernode (unless the
Distributed Computing toolbox is used, see
<https://nl.mathworks.com/products/distriben.html>).

The amount of workers used by MATLAB for the parallel toolbox can be
controlled via the `parpool` function: `parpool(16)` will use 16
workers. It's best to specify the amount of workers, because otherwise
you might not harness the full compute power available (if you have too
few workers), or you might negatively impact performance (if you have
too many workers). By default, MATLAB uses a fixed number of workers
(12).

You should use a number of workers that is equal to the number of cores
you requested when submitting your job script (the `ppn` value, see [Generic resource requirements](../running_batch_jobs/#generic-resource-requirements)).
You can determine the right number of workers to use via the following
code snippet in your MATLAB program:

```matlab title="parpool.m"
{% include "./examples/MATLAB/parpool.m" %}
```

See also [the parpool
documentation](https://nl.mathworks.com/help/distcomp/parpool.html).

## Java output logs

Each time MATLAB is executed, it generates a Java log file in the users
home directory. The output log directory can be changed using:

```
MATLAB_LOG_DIR=<OUTPUT_DIR>
```

where `<OUTPUT_DIR>` is the name of the desired output directory. To
create and use a temporary directory for these logs:

```
# create unique temporary directory in $TMPDIR (or /tmp/$USER if
$TMPDIR is not defined)
# instruct MATLAB to use this directory for log files by setting $MATLAB_LOG_DIR
$  export MATLAB_LOG_DIR=$ (mktemp -d -p $TMPDIR:-/tmp/$USER)
```

You should remove the directory at the end of your job script:

```
rm -rf $MATLAB_LOG_DIR
```

## Cache location

When running, MATLAB will use a cache for performance reasons. This
location and size of this cache can be changed through the
`MCR_CACHE_ROOT` and `MCR_CACHE_SIZE` environment variables.

The snippet below would set the maximum cache size to 1024MB and the
location to `/tmp/testdirectory`.

```
export MATLAB_CACHE_ROOT=/tmp/testdirectory 
export MATLAB_CACHE_SIZE=1024M 
```

So when MATLAB is running, it can fill up to 1024MB of cache in
`/tmp/testdirectory`.

## MATLAB job script

All of the tweaks needed to get MATLAB working have been implemented in
an example job script. This job script is also available on the HPC.
<!-- %TODO: where? -->

```bash title="jobscript.sh"
{% include "./examples/MATLAB/jobscript.sh" %}
```
