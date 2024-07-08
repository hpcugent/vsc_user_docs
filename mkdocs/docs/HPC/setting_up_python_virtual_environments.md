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

You can combine packages installed in a venv with modules. In the following example, 
we load a PyTorch package as a module and install Poutyne in a venv:

```bash
$ ml PyTorch/2.1.2-foss-2023a
$ python -m venv myenv
$ source myenv/bin/activate
$ pip install Poutyne
```

You can now use PyTorch and Poutyne in the same Python script:

```python
import torch
import poutyne

...
```

!!! warning
    Activating a venv that was creating on a different cluster can cause issues. 
    This is because the binaries placed in the venv on creation at cluster `A` might not be compatible with the CPU architecture of cluster `B`.
    To be safe, always create the virtual environment for the cluster you will be activating it on.

## Creating a virtual environment on a specific cluster
