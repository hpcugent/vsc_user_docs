# OpenFOAM

In this chapter, we outline best practices for using the centrally
provided OpenFOAM installations on the VSC {{hpc}} infrastructure.

## Different OpenFOAM releases

There are currently three different sets of versions of OpenFOAM
available, each with its own versioning scheme:

-   OpenFOAM versions released via <http://openfoam.com>: `v3.0+`,
    `v1706`

    -   see also <http://openfoam.com/history/>

-   OpenFOAM versions released via <https://openfoam.org>: `v4.1`,
    `v5.0`

    -   see also <https://openfoam.org/download/history/>

-   OpenFOAM versions released via
    <http://wikki.gridcore.se/foam-extend>: `v3.1`

Make sure you know which flavor of OpenFOAM you want to use, since there
are important differences between the different versions w.r.t.
features. If the OpenFOAM version you need is not available yet, see [I want to use software that is not available on the clusters yet](../FAQ/#i-want-to-use-software-that-is-not-available-on-the-clusters-yet).

## Documentation & training material

The best practices outlined here focus specifically on the use of
OpenFOAM on the VSC {{hpc}} infrastructure. As such, they are intended to
augment the existing OpenFOAM documentation rather than replace it. For
more general information on using OpenFOAM, please refer to:

-   OpenFOAM websites:

    -   <https://openfoam.com>

    -   <https://openfoam.org>

    -   <http://wikki.gridcore.se/foam-extend>

-   OpenFOAM user guides:

    -   <https://www.openfoam.com/documentation/user-guide>

    -   <https://cfd.direct/openfoam/user-guide/>

-   OpenFOAM C++ source code guide: <https://cpp.openfoam.org>

-   tutorials: <https://wiki.openfoam.com/Tutorials>

-   recordings of "*Introduction to OpenFOAM*" training session at
    UGent (May 2016):
    <https://www.youtube.com/playlist?list=PLqxhJj6bcnY9RoIgzeF6xDh5L9bbeK3BL>

Other useful OpenFOAM documentation:

-   <https://github.com/ParticulateFlow/OSCCAR-doc/blob/master/openFoamUserManual_PFM.pdf>

-   <http://www.dicat.unige.it/guerrero/openfoam.html>

## Preparing the environment

To prepare the environment of your shell session or job for using
OpenFOAM, there are a couple of things to take into account.

### Picking and loading an `OpenFOAM` module

First of all, you need to pick and load one of the available `OpenFOAM`
modules. To get an overview of the available modules, run
'`module avail OpenFOAM`'. For example:

<pre><code>$ <b>module avail OpenFOAM</b>
------------------ /apps/gent/CO7/sandybridge/modules/all ------------------
   OpenFOAM/v1712-foss-2017b     OpenFOAM/4.1-intel-2017a
   OpenFOAM/v1712-intel-2017b    OpenFOAM/5.0-intel-2017a
   OpenFOAM/2.2.2-intel-2017a    OpenFOAM/5.0-intel-2017b
   OpenFOAM/2.2.2-intel-2018a    OpenFOAM/5.0-20180108-foss-2018a
   OpenFOAM/2.3.1-intel-2017a    OpenFOAM/5.0-20180108-intel-2017b
   OpenFOAM/2.4.0-intel-2017a    OpenFOAM/5.0-20180108-intel-2018a
   OpenFOAM/3.0.1-intel-2016b    OpenFOAM/6-intel-2018a            (D)
   OpenFOAM/4.0-intel-2016b
</code></pre>

To pick a module, take into account the differences between the
different OpenFOAM versions w.r.t. features and API (see also [Different OpenFOAM releases](./#different-openfoam-releases)). If
multiple modules are available that fulfill your requirements, give
preference to those providing a more recent OpenFOAM version, and to the
ones that were installed with a more recent compiler toolchain; for
example, prefer a module that includes `intel-{{ current_year}}b` in its name over one
that includes `intel-{{ current_year}}a`.

To prepare your environment for using OpenFOAM, load the `OpenFOAM`
module you have picked; for example:

<pre><code>$ <b>module load OpenFOAM/4.1-intel-2017a</b>
</code></pre>

### Sourcing the `$FOAM_BASH` script

OpenFOAM provides a script that you should `source` to further prepare
the environment. This script will define some additional environment
variables that are required to use OpenFOAM. The `OpenFOAM` modules
define an environment variable named `FOAM_BASH` that specifies the
location to this script. Assuming you are using `bash` in your shell
session or job script, you should always run the following command after
loading an `OpenFOAM` module:

<pre><code>$ <b>source $FOAM_BASH</b>
</code></pre>

### Defining utility functions used in tutorial cases

If you would like to use the `getApplication`, `runApplication`,
`runParallel`, `cloneCase` and/or `compileApplication` functions that
are used in OpenFOAM tutorials, you also need to `source` the
`RunFunctions` script:

<pre><code>$ <b> source $WM_PROJECT_DIR/bin/tools/RunFunctions</b>
</code></pre>

Note that this needs to be done **after** sourcing `$FOAM_BASH` to make sure
`$WM_PROJECT_DIR` is defined.

### Dealing with floating-point errors

If you are seeing `Floating Point Exception` errors, you can undefine
the `$FOAM_SIGFPE` environment variable that is defined by the
`$FOAM_BASH` script as follows:

<pre><code>$ <b>unset $FOAM_SIGFPE</b>
</code></pre>

Note that this only prevents OpenFOAM from propagating floating point
exceptions, which then results in terminating the simulation. However,
it does not prevent that illegal operations (like a division by zero)
are being executed; if `NaN` values appear in your results, floating
point errors are occurring.

As such, **you should *not* use this in productions runs. Instead, you should track down the root cause of the floating
point errors, and try to prevent them from occurring at all.

## OpenFOAM workflow

The general workflow for OpenFOAM consists of multiple steps. Prior to
running the actual simulation, some *pre-processing* needs to be done:

-   generate the mesh;

-   decompose the domain into subdomains using `decomposePar` (only for
    parallel OpenFOAM simulations);

After running the simulation, some *post-processing* steps are typically
performed:

-   reassemble the decomposed domain using `reconstructPar` (only for
    parallel OpenFOAM simulations, and optional since some
    postprocessing can also be done on decomposed cases);

-   evaluate or further process the simulation results, either visually
    using ParaView (for example, via the `paraFoam` tool; use
    `paraFoam -builtin` for decomposed cases) or using command-line
    tools like `postProcess`; see also
    <https://cfd.direct/openfoam/user-guide/postprocessing>.

Depending on the size of the domain and the desired format of the
results, these pre- and post-processing steps can be run either
before/after the job running the actual simulation, either on the HPC
infrastructure or elsewhere, or as a part of the job that runs the
OpenFOAM simulation itself.

Do make sure you are using the same OpenFOAM version in each of the
steps. Meshing can be done sequentially (i.e., on a single core) using
for example `blockMesh`, or in parallel using more advanced meshing
tools like `snappyHexMesh`, which is highly recommended for large cases.
For more details, see <https://cfd.direct/openfoam/user-guide/mesh/>.

One important aspect to keep in mind for 'offline' pre-processing is
that the domain decomposition needs to match the number of processor
cores that are used for the actual simulation, see also [Domain decomposition and number of processor cores](./#domain-decomposition-and-number-of-processor-cores).

For post-processing you can either download the simulation results to a
local workstation, or do the post-processing (interactively) on the HPC
infrastructure, for example on the login nodes or using an interactive
session on a workernode. This may be interesting to avoid the overhead
of downloading the results locally.

## Running OpenFOAM in parallel

For general information on running OpenFOAM in parallel, see
<https://cfd.direct/openfoam/user-guide/running-applications-parallel/>.

### The `-parallel` option

When running OpenFOAM in parallel, **do not forget to specify the `-parallel` option**, to avoid running the same OpenFOAM
simulation $N$ times, rather than running it once using $N$ processor
cores.

You can check whether OpenFOAM was run in parallel in the output of the
main command: the OpenFOAM header text should only be included *once* in
the output, and it should specify a value different than '`1`' in the
`nProcs` field. Note that most pre- and post-processing utilities like
`blockMesh`, `decomposePar` and `reconstructPar` can not be run in
parallel.

### Using `mympirun`

It is highly recommended to use the `mympirun` command when running
parallel OpenFOAM simulations rather than the standard `mpirun` command;
see [Mympiprun](../mympirun/#mympirun) for more information on `mympirun`.

See [Basic usage](../mympirun/#basic-usage) for how to get started with `mympirun`.

To pass down the environment variables required to run OpenFOAM (which
were defined by the `$FOAM_BASH` script, see [Preparing the environment](./#preparing-the-environment)) to each of the MPI
processes used in a parallel OpenFOAM execution, the
`$MYMPIRUN_VARIABLESPREFIX` environment variable must be defined as
follows, prior to running the OpenFOAM simulation with `mympirun`:

<pre><code>$ <b>export MYMPIRUN_VARIABLESPREFIX=WM_PROJECT,FOAM,MPI</b>
</code></pre>

Whenever you are instructed to use a command like `mpirun -np <N> ...`,
use `mympirun ...` instead; `mympirun` will automatically detect the
number of processor cores that are available (see also [Controlling number of processes](../mympirun/#controlling-number-of-processes)).

### Domain decomposition and number of processor cores

To run OpenFOAM in parallel, you must decompose the domain into multiple
subdomains. Each subdomain will be processed by OpenFOAM on one
processor core.

Since `mympirun` will automatically use all available cores, you need to
make sure that the number of subdomains matches the number of processor
cores that will be used by `mympirun`. If not, you may run into an error
message like:

<pre><code>number of processor directories = 4 is not equal to the number of processors = 16
</code></pre>

In this case, the case was decomposed in 4 subdomains, while the
OpenFOAM simulation was started with 16 processes through `mympirun`. To
match the number of subdomains and the number of processor cores used by
`mympirun`, you should either:

-   adjust the value for `numberOfSubdomains` in
    `system/decomposeParDict` (and adjust the value for `n` accordingly
    in the domain decomposition coefficients), and run `decomposePar`
    again; or

-   submit your job requesting exactly the same number of processor
    cores as there are subdomains (see the number of `processor*`
    directories that were created by `decomposePar`)

See [Controlling number of processes](../mympirun/#controlling-number-of-processes) to control the number of process `mympirun` will start.

This is interesting if you require more memory per core than is
available by default. Note that the decomposition method being used
(which is specified in `system/decomposeParDict`) has significant impact
on the performance of a parallel OpenFOAM simulation. Good decomposition
methods (like `metis` or `scotch`) try to limit communication overhead
by minimising the number of processor boundaries.

To visualise the processor domains, use the following command:

<pre><code>$ <b>mympirun foamToVTK -parallel -constant -time 0 -excludePatches '(".*.")'</b>
</code></pre>

and then load the VTK files generated in the `VTK` folder into ParaView.

## Running OpenFOAM on a shared filesystem 

OpenFOAM is known to significantly stress shared filesystems, since a
lot of (small) files are generated during an OpenFOAM simulation. Shared
filesystems are typically optimised for dealing with (a small number of)
large files, and are usually a poor match for workloads that involve a
(very) large number of small files (see also
<http://www.prace-ri.eu/IMG/pdf/IO-profiling_with_Darshan-2.pdf>).

Take into account the following guidelines for your OpenFOAM jobs, which
all relate to input parameters for the OpenFOAM simulation that you can
specify in `system/controlDict` (see also
<https://cfd.direct/openfoam/user-guide/controldict>).

-   instruct OpenFOAM to write out results at a reasonable frequency, **certainly *not*** for every single time step}; you can control this using the `writeControl`, `writeInterval`, etc. keywords;

-   consider only retaining results for the last couple of time steps,
    see the `purgeWrite` keyword;

-   consider writing results for only part of the domain (e.g., a line
    of plane) rather than the entire domain;

-   if you do not plan to change the parameters of the OpenFOAM
    simulation while it is running, **set <tt>runTimeModifiable</tt> to <tt>false</tt>** to avoid that OpenFOAM re-reads each
    of the `system/*Dict` files at every time step;

-   if the results per individual time step are large, consider setting
    `writeCompression` to `true`;

For modest OpenFOAM simulations where a single workernode suffices,
consider using the local disk of the workernode as working directory
(accessible via `$VSC_SCRATCH_NODE`), rather than the shared
`$VSC_SCRATCH` filesystem. **Certainly do not use a subdirectory in `$VSC_HOME` or `$VSC_DATA`, since these shared filesystems are too slow
for these type of workloads.

{% if site == gent %}
For large parallel OpenFOAM simulations on the {{university}} Tier-2 clusters, consider
using the alternative shared scratch filesystem `$VSC_SCRATCH_ARCANINE`
(see [Pre-defined user directories](../running_jobs_with_input_output_data/#pre-defined-user-directories)).
{% endif %}

These guidelines are especially important for large-scale OpenFOAM
simulations that involve more than a couple of dozen of processor cores.

## Using own solvers with OpenFOAM 

See <https://cfd.direct/openfoam/user-guide/compiling-applications/>.

## Example OpenFOAM job script

Example job script for `damBreak` OpenFOAM tutorial (see also
<https://cfd.direct/openfoam/user-guide/dambreak>):

<center>-- OpenFOAM_damBreak.sh --</center>
```bash
{% include "./examples/OpenFOAM/OpenFOAM_damBreak.sh" %}
```
