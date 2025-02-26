# R libraries

Please keep in mind, that this is not a general manual
abut installing `R` libraries, but only system specific information about self 
installed R libraries at {{ hpcinfra }}.

Our infrastructure contains different CPU architectures, that are
not necessarily compatible with each other. Additionally, we have 
multiple versions of `R` installed with different versions of toolchains, and by default,
self installed libraries are installed in separate directories based only
on R major and minor versions.

In this way, you might use self installed R libraries on incompatible architectures and/or
compiled with incompatible toolchains, which might lead to hangs or other types of errors.

When you load a centrally installed `R` module we make sure that self installed libraries 
will be installed to an operational system, architecture, toolchain, and `R` version
dependent directory. The location of this directory by default is
(by setting `R_LIBS_USER` environmental variable to)
`$VSC_DATA/local_R_LIBS/$VSC_OS_LOCAL/$VSC_ARCH_LOCAL/<R version>-<toolchain>`.

If you would like to have another location (for example you are using a central location
in your VO), you should set the environmental variable `R_LIBS_BASEDIR` to the desired location
*before* you load any centrally installed `R` module. In this case, the location of the
directory for self installed `R` libraries will be
`$R_LIBS_BASEDIR/local_R_LIBS/$VSC_OS_LOCAL/$VSC_ARCH_LOCAL/<R version>-<toolchain>`.
If this directory is not writable, you can still be able to use already installed 
`R` libraries from that location, but you will not be able to install `R` libraries 
yourself.

You can always check the default location(s) of `R` libraries by issuing `.libPaths()` command
in `R`. This command will show the library locations ordered by their priorities. 

Please be aware that if you have installed an `R` libraries yourself in the past, you might have to 
reinstall those if you want to use them:
- on a different cluster
- with a different version of `R`
- with an `R` compiled with a different version of toolchain
- if the operational system is changed/updated. 

