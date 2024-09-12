# Python Virtual Environment Wrapper Script

`vsc-venv` is a script that encapsulates the creation and management of Python virtual environments. 
This avoids multiple issues with the default `venv` included in Python (`python -m venv`).


One issue is that a virtual environment created for one cluster might not work on another. 
Additionally, when activating a virtual environment, 
the same centrally installed modules used during its creation must also be loaded.
the `vsc-venv` command manages multiple virtual environments for different clusters in a transparent way, 
while guaranteeing the same module environment.

## Usage

A virtual environment can be activated by running the following command:

```bash
source ./vsc-venv.sh --activate --requirements <requirements> [--modules module_file]
```

Here, `requirements` is the path to a file containing the python dependencies to install in the virtual environment.
An optional `module_file` can be provided, which lists the modules to load before activating the virtual environment.

Automatically, the modules are loaded and the environment is activated. 
When running this command for the first time, the dependencies from the requirements file are installed.

Now, the software can be run and Python packages installed in the virtual environment can be used, along with software provided via centrally installed modules.

You can get insights on the current environment using the following commands:
```
python --version    # Python version
pip list            # List of installed Python packages
module list         # List of loaded modules
```

To deactivate the virtual environment, run:

```bash
source ./vsc-venv.sh --deactivate
```

## Example

Suppose we are on the HPC-UGent Tier-2 login nodes, and we want to make a virtual environment for doduo, the default cluster.
The following files are present in the current directory:

**modules.txt:**
```bash
Python/3.12.3-GCCcore-13.3.0
SciPy-bundle/2024.05-gfbf-2024a
```

and **requirements.txt:**
```
requests
```

For more info on the `requirements.txt` file, 
see the [pip documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/).

We run the following commands to enter the environment

```bash
source ./vsc-venv.sh --activate --requirements requirements.txt --modules modules.txt
```

As this creates the virtual environment for the first time, a `venvs` subdirectory is created in the current directory. 
Within `venvs/`, an additional subdirectory is created for the virtual environment: `venv-RHEL8-zen2`.

Now, Python 3.12 is loaded and both the `numpy` (provided by the `SciPy-bundle` module) and `requests` Python packages can be used.

To deactivate the virtual environment, run:

```bash
source ./vsc-venv.sh --deactivate
```

### joltik

If we want to create a virtual environment for joltik, we can run the following commands:

```bash
module swap cluster/joltik
qsub -I
cd my_project
source ./vsc-venv.sh --activate --requirements requirements.txt --modules modules.txt
```

the venvs folder now contains two folders:

```bash
$ ls venvs/
venv-RHEL8-cascadelake	
venv-RHEL8-zen2
```
