# Python 

This page provides information on how to use Python on the HPC systems.
It shows how to load Python modules and Python packages, 
and how to run Python scripts interactively and using job scripts.

## Python modules

The HPC systems provide a number of Python modules that you can load into your environment.
To see a list of available Python modules, you can run:

```bash
$ module avail Python/
```

For example, to load Python 3.11, you can run:

```bash
$ module load Python/3.11.3-GCCcore-12.3.0
```

This will load Python into your environment:

```
$ python --version
Python 3.11.3
```

## Python packages as modules

Python packages can be divided into two categories: standard library packages and third-party packages.
The standard library packages are included with Python and do not need to be installed separately.
Third-party packages need to be installed before they can be used in your Python code.

We cannot allow users to install packages into the system-wide Python installation.
Instead, we provide a large number of Python packages as modules that can be loaded into your environment.
Once loaded, you can use the packages in your Python code.

## Finding packages 

If you need a particular Python package that is not part of the standard library, 
you can search for it using the `module avail` command. 
For example, to search for the `beautifulsoup` package, you can run:

```bash
$ module avail beautifulsoup
BeautifulSoup/4.10.0-GCCcore-10.3.0
...
BeautifulSoup/4.12.2-GCCcore-13.2.0 (D)
```

This will show you all available versions of the `beautifulsoup` package.

!!! Note
    Not all Python packages can be found by searching for the package name. 
    Some packages are installed as extensions of modules. 
    For example, `numpy`, `scipy` and `pandas` are part of the `SciPy-bundle` module. 
    You can use the following command to check which extensions are included in a module (if any):
    
    ```bash
    module show <module_name>
    ```

If you cannot find a package, it could be that it is not available as a module.
You can send us a [software installation request]({{ hpc_software_install }}), 
or you can install the package in a [Python virtual environment](./setting_up_python_virtual_environments.md).

## Loading packages

If your python script does not use any third-party packages, you only have to load a Python module.
If you need to use a third-party package, you will need to load the corresponding module.
Loading such a module will also load a Python module, so you do not need to load both.

For example, loading the `SciPy-bundle` module will also load the Python module:

```bash
$ module load SciPy-bundle/2023.11-gfbf-2023b
$ module list
Currently Loaded Modules:
 ...
 21) Python/3.11.5-GCCcore-13.2.0
 ...
 27) SciPy-bundle/2023.11-gfbf-2023b
```

## Example: Running Python scripts

There are multiple ways to run Python scripts on the HPC systems. 
You can start an interactive session on a cluster and run your script manually,
or you can submit a job using a job script. 
This section will show you how to run Python scripts using both methods on the following example script:

```python title="script.py"
import numpy as np

random_numbers = np.random.rand(5)

print(f"Random numbers: {random_numbers}")
```

First, we select a toolchain of the SciPy bundle module, which contains the `numpy` package, along with a Python module:

```bash
$ module avail SciPy-bundle
```

We will use the `SciPy-bundle/2023.11-gfbf-2023b` toolchain.
Next, we decide on which cluster we want to run the script. 
For this example, we will use the `donphan` cluster.

To switch to the `donphan` cluster, we run:

```bash
$ module swap cluster/donphan
```

### Interactive session

To run the script interactively, we need to start an interactive session on the cluster (`donphan` in this case):

```bash
$ qsub -I
```

Once the interactive session is started, we can load the `SciPy-bundle` module and run the script:

```bash
$ module load SciPy-bundle/2023.11-gfbf-2023b
```

Now we can run the script:

```bash
$ python script.py
```

### Job script

To run the script using a job script, 
we need to create a job script that will load the `SciPy-bundle` module and run the script:

```bash title="jobscript.pbs"
#!/bin/bash

# Basic parameters
#PBS -N python_job_example            ## Job name
#PBS -l nodes=1:ppn=1                 ## 1 node, 1 processors per node
#PBS -l walltime=01:00:00             ## Max time your job will run (no more than 72:00:00)

module load SciPy-bundle/2023.11-gfbf-2023b   # Load the SciPy module, which includes the numpy package
cd $PBS_O_WORKDIR                             # Change working directory to the location where the job was submitted
python script.py                              # Run your Python script
```

To submit the job, run:

```bash
qsub jobscript.pbs
```

After some time, two files will be created in the directory where the job was submitted: 
`python_job_example.o{{jobid}}` and `python_job_example.e{{jobid}}`, where {{jobid}} is the id of your job.
The `.o` file contains the output of the job.

