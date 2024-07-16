# Python Virtual Environments (venv's)

## Introduction

Python virtual environments (venv's) are a way to create isolated Python environments.
You can install packages in a venv without affecting the system Python installation.
This is useful when you need to use a package that is not available as a module on the HPC cluster.

## Creating a venv

A venv can be created with the following commands:

```bash
$ python -m venv myenv      # Create a new venv named myenv
$ source myenv/bin/activate # Activate the venv
```

After activating the venv, you can install packages with `pip`:

```bash
$ pip install example_package1
$ pip install example_package2
```

It is now possible to run Python scripts that use the installed packages in the venv. To deactivate the venv, run:

```bash
$ deactivate
```

!!! note
    Always prefer to use modules if they are available. 
    Modules are compiled and optimized for the HPC cluster, while packages installed with `pip` are not.
    To check if a package is available as a module, you can use the following command:

    ```bash
    $ module av package_name
    ```

## Combining venv's with modules

You can combine packages installed in a venv with modules. The following script uses 
pytorch (which is available as a module) and Poutyne (which is not available as a module):

```python title="pytorch_poutine_example.py"
import torch
import poutyne

...
```

We load a PyTorch package as a module and install Poutyne in a venv:

```bash
$ ml PyTorch/2.1.2-foss-2023a
$ python -m venv myenv
$ source myenv/bin/activate
$ pip install Poutyne
```

While in the virtual environment, we can run the script without any issues:

```bash
$ python pytorch_poutine_example.py
```

!!! warning
    Activating a virtual environment (venv) created on a different cluster can cause issues. 
    This happens because the binaries in the venv from cluster A might not work with the CPU architecture of cluster B.
    
    For example, if we create a venv on the skitty cluster,

    ```bash
    $ module swap cluster/skitty
    $ qsub -I
    $ python -m venv myenv
    ```

    return to the login node by pressing CTRL+D and try to use the virtual environment:

    ```bash
    $ source myenv/bin/activate
    $ python
    Illegal instruction (core dumped)
    ```

    we are presented with the illegal instruction error. More info on this [here](troubleshooting.md#illegal-instruction-error)


## Creating a virtual environment on a specific cluster

To create a virtual environment for a specific cluster, you need to start an interactive shell on that cluster.
Let's say you want to create a virtual environment on the `skitty` cluster.

```bash
$ module swap cluster/skitty
$ qsub -I
```

After some time, a shell will be started on the `skitty` cluster. 
You can now create a virtual environment as described in [the first section](#creating-a-venv).
This virtual environment can be used by jobs running on the `skitty` cluster.

## Using virtual environments in job scripts

After creating a virtual environment for a cluster, you need to activate it in your job script. 

```bash title="jobscript.pbs"
#!/bin/bash

# Basic parameters
#PBS -N jobname           ## Job name
#PBS -l nodes=1:ppn=2     ## 1 node, 2 processors per node (ppn=all to get a full node)
#PBS -l walltime=01:00:00 ## Max time your job will run (no more than 72:00:00)

module load [module]
module load [module]

cd $PBS_O_WORKDIR         # Change working directory to the location where the job was submitted

source myenv/bin/activate # Activate the virtual environment
python myscript.py        # Run your Python script, or any other command within the virtual environment
deactivate                # Deactivate the virtual environment
```

## Troubleshooting

### Error: cannot open shared object file: No such file or directory

There are two main reasons why this error could occur.

1. you have not loaded the python module that was used to create the virtual environment.
2. you added or removed modules while in the virtual environment.

#### Entering a virtual environment while the python module used to create it is not active

When you load a python module and use that to make a virtual environment, you need to make sure that the same module 
is loaded when you enter the environment. This is because the virtual environment keeps a reference to the base python 
used to create it.

The following commands illustrate this issue:

```bash
$ module load Python/3.10.8-GCCcore-12.2.0  # Load a python module
$ python -m venv myenv                      # Create a virtual environment with loaded python module
$ module purge                              # Remove all loaded modules
$ source myenv/bin/activate                 # Activate the virtual environment
$ python                                    # Start python
python: error while loading shared libraries: libpython3.10.so.1.0: cannot open shared object file: No such file or directory
```

Here, the virtual environment tries to use the python module that was loaded when the environment was created, which is no longer available.
The solution is to load the same python module before activating the virtual environment:

```bash
$ module load Python/3.10.8-GCCcore-12.2.0  # Load the same python module
$ source myenv/bin/activate                 # Activate the virtual environment
```

#### modifying modules while in a virtual environment

You must not delete or add modules while in a virtual environment. 
Adding and removing modules modifies the `$PATH` variable in the current shell. When activating a virtual environment,
it will store the `$PATH` variable of the shell at that moment. If you modify the `$PATH` variable while in a virtual environment by loading or deleting modules,
and deactivate the virtual environment, the `$PATH` variable will be reset to the one stored in the virtual environment.
trying to use those modules will lead to errors:

```bash
$ module load Python/3.10.8-GCCcore-12.2.0  # Load a python module
$ python -m venv myenv                      # Create a virtual environment
$ source myenv/bin/activate                 # Activate the virtual environment (saves state of $PATH)
$ module purge                              # Unload all modules (modifies the $PATH)
$ deactivate                                # Deactivate the virtual environment (resets $PATH to saved state)
$ python                                    # PATH contains a reference to the unloaded module
python: error while loading shared libraries: libpython3.10.so.1.0: cannot open shared object file: No such file or directory
```

The solution is to only modify modules when not in a virtual environment.