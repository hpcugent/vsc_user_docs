# Conda

Conda is a software package manager for data science that allows unprivileged (non-administrative) users to search, 
fetch, install, upgrade, use, and manage supported open-source software packages and 
programming languages/libraries/environments in a directory they have write access to. 
Conda allows users to create reproducible scientific software environments

We do not recommend using conda environments on HPC clusters due to several common issues, 
which we will explain in this section. However, we do not forbid the use of conda entirely. In certain situations, 
such as testing software, creating new workflows, or teaching a course, it is perfectly acceptable to use it.

## Performance and Optimization

Conda's packages are pre-compiled binaries that are designed to work on a wide range of systems. 
This means they are not optimized for the specific architecture of HPC clusters, 
leading to potential performance drawbacks compared to modules compiled specifically for the HPC environment.

HPC modules on the other hand, are compiled for the specific architecture of the cluster,
and are optimized for performance.

## Compatibility and Dependency

Using Conda in conjunction with centrally installed modules can lead to conflicts and unexpected errors, 
making it difficult to debug and manage dependencies.

If you do wish to use conda, we recommend only using packages from conda itself, even when they are available as modules.
This will degrade performance, but will avoid conflicts between conda and module dependencies.

## Package Availability

Conda has a smaller repository of available packages compared to PyPI, the repository used by pip. 
This can limit the availability of specific tools or libraries needed for certain workflows.

## Environment and Installation Issues

### Home Directory Usage

by default, conda installs packages in the user's home directory, 
which can quickly fill up disk quotas due to the large number of files and directories it creates. 
This is particularly problematic in the HPC environment where home directory quotas are limited.

If you do wish to use conda, we recommend setting the conda package directory to a location with more storage 
space. This can be done by running: 

```bash
export CONDA_PKGS_DIRS=$VSC_DATA/conda_pkgs
```

before installing packages into a conda environment.


### Modification of Configuration Files

Conda modifies the .bashrc file in the user's home directory, 
which can lead to conflicts and unintended side effects in the user's environment setup.

You can avoid the change of the `.bashrc` file by activating the environment with `source activate full/path/to/myenv`
instead of `conda activate myenv`.