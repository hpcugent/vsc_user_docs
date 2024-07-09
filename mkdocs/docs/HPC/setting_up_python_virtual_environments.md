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
    Activating a venv that was creating on a different cluster can cause issues. 
    This is because the binaries placed in the venv on creation at cluster `A` might not be compatible with the CPU architecture of cluster `B`.
    // TODO: Give an example of this


## Creating a virtual environment on a specific cluster

To create a virtual environment for a specific cluster, you need to start an interactive shell on that cluster.
Let's say you want to create a virtual environment on the `skitty` cluster.

```bash
$ module swap cluster/skitty
$ qsub -I
```

After some time, a shell will be started on the `skitty` cluster. 
You can now create a virtual environment as described in [this section](#creating-a-venv).
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

// TODO troubleshooting for: python: error while loading shared libraries: libpython3.10.so.1.0: cannot open shared object file: No such file or directory. 
// Happens when making an env with a python module loaded an entering the env without that module bein loaded anymore.
