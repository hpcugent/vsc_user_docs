# Python Virtual Environments (venv's)

## Introduction

A Python virtual environment ("venv" for short)
is a tool to create an isolated Python workspace.
Within this isolated environment,
you can install additional Python packages without affecting the system-wide Python installation.
Because a normal user cannot install packages globally,
using a virtual environment allows you to install packages locally without needing administrator privileges.
This is especially useful when you need to use a package that is not available as a module on the HPC cluster.

## Managing Python Environments

This section will explain how to create, activate, use and deactivate Python virtual environments.

### Creating a Python virtual environment

A Python virtual environment can be created with the following command:

```bash
$ python -m venv myenv      # Create a new virtual environment named 'myenv'
```

This command creates a new subdirectory named `myenv` in the current working directory. 
This directory will contain the packages, scripts, and binaries that are needed to manage the virtual environment.

### Activating a virtual environment

To use the virtual environment, you need to *activate* it. 
This will modify the shell environment to use the Python interpreter and packages from the virtual environment.

```bash
$ source myenv/bin/activate                    # Activate the virtual environment
```

### Installing packages in a virtual environment

After activating the virtual environment, you can install additional Python packages with `pip install`:

```bash
$ pip install example_package1
$ pip install example_package2
```

These packages will be scoped to the virtual environment and will not affect the system-wide Python installation, 
and are only available when the virtual environment is activated.
No administrator privileges are required to install packages in a virtual environment.

It is now possible to run Python scripts that use the installed packages in the virtual environment.

!!! note
    Always prefer to use Python packages that are centrally installed, which are available via the environment modules interface.
    Software installations available via the modules interface are compiled and optimized for the HPC cluster, while packages installed with `pip` are not.
    To check if a package is available as a module, you can use the following command:

    ```bash
    $ module av package_name
    ```

    Some Python packages are installed as extensions of modules. For example, `numpy`, `scipy` and `pandas` are 
    part of the `SciPy-bundle` module. You can use

    ```bash
    $ module show <module_name>
    ```

    to check which extensions are included in a module, if any.


### Deactivating a virtual environment

When you are done using the virtual environment, you can deactivate it.
To do that, run:

```bash
$ deactivate
```

## Combining virtual environments with centrally installed modules

You can combine Python packages installed in a virtual environment with environment modules. 
The following script uses PyTorch (which is available as a module)
and Poutyne (which we assume is not centrally installed):

```python title="pytorch_poutyne.py"
import torch
import poutyne

...
```

We load a PyTorch package as a module and install Poutyne in a virtual environment:

```bash
$ module load PyTorch/2.1.2-foss-2023a
$ python -m venv myenv
$ source myenv/bin/activate
$ pip install Poutyne
```

While the virtual environment is activated, we can run the script without any issues:

```bash
$ python pytorch_poutyne.py
```


## Creating a virtual environment for a specific cluster

To create a virtual environment for a specific cluster, you need to start an interactive shell on that cluster.
Let's say you want to create a virtual environment on the `donphan` cluster.

```bash
$ module swap cluster/donphan
$ qsub -I
```

After some time, a shell will be started on the `donphan` cluster. 
You can now create a virtual environment as described in [the first section](#creating-a-venv).
This virtual environment can be used by jobs running on the `donphan` cluster.


## Example Python job

This section will combine the concepts discussed in the previous sections to:

1. Create a virtual environment on a specific cluster.
2. Combine packages installed in the virtual environment with modules.
3. Submit a job script that uses the virtual environment.

The example script that we will run is the following:

```python title="pytorch_poutyne.py"
import torch
import poutyne

print(f"The version of PyTorch is: {torch.__version__}")
print(f"The version of Poutyne is: {poutyne.__version__}")
```

First, we create a virtual environment on the `donphan` cluster:

```bash
$ module swap cluster/donphan
$ qsub -I
# Load module dependencies
$ module load PyTorch/2.1.2-foss-2023a
$ python -m venv myenv
$ source myenv/bin/activate
# install virtual environment dependencies
$ pip install Poutyne
$ deactivate
```

We exit the interactive shell by pressing `CTRL+D` and create a job script that loads the PyTorch module, 
enters the virtual environment and executes the script:

```bash title="jobscript.pbs"
#!/bin/bash

# Basic parameters
#PBS -N python_job_example    ## Job name
#PBS -l nodes=1:ppn=1         ## 1 node, 1 processors per node
#PBS -l walltime=01:00:00     ## Max time your job will run (no more than 72:00:00)

module load PyTorch/2.1.2-foss-2023a   # Load the PyTorch module

cd $PBS_O_WORKDIR             # Change working directory to the location where the job was submitted

source myenv/bin/activate     # Activate the virtual environment
python pytorch_poutyne.py     # Run your Python script, or any other command within the virtual environment
deactivate                    # Deactivate the virtual environment
```

Next, we submit the job script:

```bash
$ qsub jobscript.pbs
```

Two files will be created in the directory where the job was submitted: `python_job_example.o[job_id]` and `python_job_example.e[job_id]`.
The `.o` file contains the output of the job.


## Troubleshooting

### Illegal instruction error

Activating a virtual environment created on a different cluster can cause issues. 
This happens
because the binaries in the virtual environments from cluster A might not work with the CPU architecture of cluster B.

For example, if we create a virtual environment on the skitty cluster,

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

### Error: cannot open shared object file: No such file or directory

There are two main reasons why this error could occur.

1. you have not loaded the python module that was used to create the virtual environment.
2. you added or removed modules while the virtual environment was activated.

#### Entering a virtual environment while the Python module used to create it is not active

If you loaded a `Python` module when creating a virtual environment, you need to make sure that the same module 
is loaded when you enter the environment. This is because the virtual environment keeps a reference to the base python 
used to create it.

The following commands illustrate this issue:

```bash
$ module load Python/3.10.8-GCCcore-12.2.0  # Load a python module
$ python -m venv myenv                      # Create a virtual environment with loaded python module
$ module purge                              # Remove all loaded modules (WRONG!)
$ source myenv/bin/activate                 # Activate the virtual environment
$ python                                    # Start python
python: error while loading shared libraries: libpython3.10.so.1.0: cannot open shared object file: No such file or directory
```

Here, the virtual environment tries to use the python module that was loaded when the environment was created.
Since we used `module purge`, that module is no longer available.
The solution is to load the same python module before activating the virtual environment:

```bash
$ module load Python/3.10.8-GCCcore-12.2.0  # Load the same python module
$ source myenv/bin/activate                 # Activate the virtual environment
```

#### Modifying modules while in a virtual environment

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