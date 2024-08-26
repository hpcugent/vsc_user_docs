# Python Virtual Environment Wrapper Script

`vsc-venv` is a script that encapsulates the creation and management of Python virtual environments. 
This avoids multiple issues with the default `venv` command on the HPC. 


One issue is that a virtual environment created for one cluster might not work on another. 
Additionally, when activating a virtual environment, 
the same centrally installed modules used during its creation must also be loaded.
the `vsc-venv` command manages multiple virtual environments for different clusters in a transparent way, 
while guaranteeing the same module environment.

## Usage

A virtual environment can be activated by running the following command:

```bash
source vsc-venv activate <requirements> [module_script]
```

Here, `requirements` is the path to a file containing the python dependencies to install in the virtual environment.
An optional module script can be provided to load the required modules before creating the virtual environment.

Automatically, the modules are loaded and the environment is activated. 
When running this command for the first time, the dependencies from the requirement file are installed.

Now, the software can be run and use packages installed in the virtual environment, along with centrally installed modules.
To deactivate the virtual environment, run:

```bash
source vsc-venv deactivate
```

## Example

Suppose we are on the login node, and we want to make a virtual environment for doduo, which is loaded by default.
The following files are present in the current directory:

**modules.sh:**
```bash
ml Python/3.12.3-GCCcore-13.3.0
```

and **requirements.txt:**
```bash
requests
```

We run the following commands to enter the environment

```bash
source vsc-venv activate requirements.txt modules.sh
```

As this creates the virtual environment for the first time, the `venvs` folder is created. 
Within this folder, a new folder is created for the virtual environment `venv-RHEL8-zen2`.

Now, python 3.12 is loaded and the user can use the `requests` package.

To deactivate the virtual environment, run:

```bash
source vsc-venv deactivate
```

### joltik

If we want to create a virtual environment for joltik, we can run the following commands:

```bash
module swap cluster/joltik
qsub -I
source vsc-venv activate requirements.txt modules.sh
```

the venvs folder now contains two folders:

```bash
$ ls venvs/
venv-RHEL8-cascadelake	
venv-RHEL8-zen2
```
