# Python Virtual Environment Wrapper Script

`vsc-venv` is a script that encapsulates the creation and management of Python virtual environments. 
This avoids multiple issues with the default `venv` command on the HPC. 


One issue is that a virtual environment created for one cluster might not work on another. 
Additionally, when activating a virtual environment, 
the same centrally installed modules used during its creation must also be loaded.
the `vsc-venv` command manages multiple virtual environments for different clusters in a transparent way.

## Usage

A virtual environment can be created by running the following command:

```bash
source vsc-venv create [module_script]
```

Here, an optional module script can be provided to load the required modules before creating the virtual environment.

To activate a virtual environment, run the following command:

```bash
source vsc-venv activate
```

To install dependencies in a virtual environment, run:

```bash
vsc-venv install <requirements>
```

Requirements should be a file containing the dependencies to install.
At this point, `pip install <package>` can also be used to install, 
but we recommend using a file like `requirements.txt` to record the packages.

Now, the software can be run and use packages installed in the virtual environment, along with centrally installed modules.
To deactivate the virtual environment, run:

```bash
deactivate
```

## Example 

Suppose the following files are present in the directory:

**modules.sh:**
```bash
ml Python/3.7.2-GCCcore-8.2.0
```

and **requirements.txt:**
```bash
requests
```

We run the following commands to make an environment and install the packages.

```bash
source vsc-venv create modules.sh
```

This creates a 
