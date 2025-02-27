# R packages

!!! note
    Please keep in mind that this is not general documentation
    about installing `R` packages, but specific information about 
    self-installed R packages at the {{ hpcinfra }}.

The {{ hpcinfra }} contains different generations of CPUs, with different microarchitectures, that are
not necessarily compatible with each other. Additionally, we have 
multiple versions of `R` installed with different versions of toolchains, and by default,
self-installed packages are installed in separate directories based only
on `R` major and minor versions (only using `x.y` for R version `x.y.z`).

In this way, you might use self-installed `R` packages on incompatible CPU microarchitectures and/or
compiled with incompatible toolchains, or for a different major version of the operating system,
which might lead to hangs or other types of errors.

Since end of February 2025, we make sure that `R` packages that you install yourself will be installed
in a directory that is specific to the operating system version, CPU microarchitecture, toolchain,
and `R` version that is being used. The location of this directory by default is
(by setting `$R_LIBS_USER` environment variable to)
`$VSC_DATA/local_R_LIBS/$VSC_OS_LOCAL/$VSC_ARCH_LOCAL/<R version>-<toolchain>`.

### Controlling the location for self-installed R packages

If you would like to have another location (for example you are using a central location
in your Virtual Organisation), you should set the environment variable `$R_LIBS_BASEDIR` to the desired location
*before* you load any centrally installed `R` module. In this case, the location of the
directory for self-installed `R` packages will be
`$R_LIBS_BASEDIR/local_R_LIBS/$VSC_OS_LOCAL/$VSC_ARCH_LOCAL/<R version>-<toolchain>`.
If this directory is not writable, you will still be able to use already installed
`R` packages from that location, but you will not be able to install `R` packages 
yourself.

You can always check the default location(s) of `R` packages by issuing `.libPaths()` command
in `R`. This command will show the package locations, ordered by their priorities. 

### Missing R packages intalled before

Please be aware that if you have installed `R` packages yourself before end of February 2025,
then you have to reinstall all of them. You might have to reinstall self
installed `R` packages if you want to use them:

- on a different cluster
- with a different version of `R`
- with an `R` compiled with a different version of toolchain
- if the operating system was changed/updated. 

