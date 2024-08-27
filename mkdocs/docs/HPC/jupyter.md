# Jupyter notebook

## What is a Jupyter notebook

A [Jupyter notebook](https://jupyter.org/) is an interactive, web-based environment that allows you to create documents that contain live code, equations, visualizations, and plaintext. The code blocks in these documents can be used to write Python, Java, R and Julia code, among others. The combination of code executions with text and visual outputs make it a useful tool for data analysis, machine learning and educational purposes.

## Using Jupyter Notebooks on the HPC

### Launching a notebook using the web portal

Through the [HPC-UGent web portal](web_portal.md) you can easily start a Jupyter notebook on a workernode, via the *Jupyter Notebook* button under the *Interactive Apps* menu item.

<center>
![image](img/ood_start_jupyter.png)
</center>

After starting the Jupyter notebook using the *Launch* button, you will see it being added in state *Queued* in the overview of interactive sessions (see *My Interactive Sessions* menu item):

<center>
![image](img/ood_jupyter_queued.png)
</center>

When your job hosting the Jupyter notebook starts running, the status will first change the *Starting*:

<center>
![image](img/ood_jupyter_starting.png)
</center>

and eventually the status will change to *Running*, and you will be able to connect to the Jupyter environment using the blue *Connect to Jupyter* button:

<center>
![image](img/ood_jupyter_running.png)
</center>

This will launch the Jupyter environment in a new browser tab, where you can open an existing notebook by navigating to the directory where it is located and clicking it. You can also create a new notebook by clicking on `File`>`New`>`Notebook`:

<center>
![image](img/ood_jupyter_new_notebook.png)
</center>

### Using extra Python packages

A number of Python packages are readily available in modules on the HPC. To illustrate how to use them in a Jupyter notebook, we will make use of an example where we want to use numpy in our notebook.
The first thing we need to do is finding the modules that contain our package of choice. For numpy, this would be the `SciPy-bundle` modules.

To find the appropriate modules, it is recommended to use the shell within the web portal under `Clusters`>`>_login Shell Access`.

<center>
![image](img/ood_jupyter_open_shell.png)
</center>

We can see all available versions of the SciPy module by using `module available SciPy`:

```shell 
$ module available SciPy-bundle

------------------ /apps/gent/RHEL8/zen2-ib/modules/all ------------------
    SciPy-bundle/2022.05-foss-2022a    SciPy-bundle/2023.11-gfbf-2023b (D)
    SciPy-bundle/2023.07-gfbf-2023a

  Where:
   D:  Default Module
...
```

Not all modules will work for every notebook, we need to use the one that uses the same toolchain as the notebook we want to launch. To find that toolchain, we can look at the `JupyterNotebook version` field when creating a notebook. In our example `7.2.0` is the version of the notebook and `GCCcore/13.2.0` is the toolchain used.

<center>
![image](img/ood_jupyter_version.png)
</center>

Most modules' names end with the version of the toolchain used by the module (for example `plotly.py/5.18.0-GCCcore-13.2.0`), however for our SciPy module, that is not the case.
To find the toolchain used by such a module (and the packages contained within a module), we can make use of `module show <module_name>`:

```shell
$ module show SciPy-bundle/2023.11-gfbf-2023b
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   /apps/gent/RHEL8/zen2-ib/modules/all/SciPy-bundle/2023.11-gfbf-2023b.lua:
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
help([[
Description
===========
Bundle of Python packages for scientific software
More information
================
 - Homepage: https://python.org/
Included extensions
===================
beniget-0.4.1, Bottleneck-1.3.7, deap-1.4.1, gast-0.5.4, mpmath-1.3.0,
numexpr-2.8.7, numpy-1.26.2, pandas-2.1.3, ply-3.11, pythran-0.14.0,
scipy-1.11.4, tzdata-2023.3, versioneer-0.29
]])
whatis("Description: Bundle of Python packages for scientific software")
whatis("Homepage: https://python.org/")
whatis("URL: https://python.org/")
whatis("Extensions: beniget-0.4.1, Bottleneck-1.3.7, deap-1.4.1, gast-0.5.4, mpmath-1.3.0, numexpr-2.8.7, numpy-1.26.2, pandas-2.1.3, ply-3.11, pythran-0.14.0, scipy-1.11.4, tzdata-2023.3, versioneer-0.29")
conflict("SciPy-bundle")
load("gfbf/2023b")
load("Python/3.11.5-GCCcore-13.2.0")
load("Python-bundle-PyPI/2023.10-GCCcore-13.2.0")
load("pybind11/2.11.1-GCCcore-13.2.0")
prepend_path("CMAKE_PREFIX_PATH","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b")
prepend_path("LIBRARY_PATH","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b/lib")
prepend_path("PATH","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b/bin")
setenv("EBROOTSCIPYMINBUNDLE","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b")
setenv("EBVERSIONSCIPYMINBUNDLE","2023.11")
setenv("EBDEVELSCIPYMINBUNDLE","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b/easybuild/SciPy-bundle-2023.11-gfbf-2023b-easybuild-devel")
prepend_path("PYTHONPATH","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b/lib/python3.11/site-packages")
prepend_path("CPATH","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b/lib/python3.11/site-packages/numpy/core/include")
prepend_path("LD_LIBRARY_PATH","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b/lib/python3.11/site-packages/numpy/core/lib")
prepend_path("LIBRARY_PATH","/apps/gent/RHEL8/zen2-ib/software/SciPy-bundle/2023.11-gfbf-2023b/lib/python3.11/site-packages/numpy/core/lib")
setenv("EBEXTSLISTSCIPYMINBUNDLE","numpy-1.26.2,ply-3.11,gast-0.5.4,beniget-0.4.1,pythran-0.14.0,versioneer-0.29,scipy-1.11.4,numexpr-2.8.7,Bottleneck-1.3.7,tzdata-2023.3,pandas-2.1.3,mpmath-1.3.0,deap-1.4.1")
```

The toolchain used can then for example be found within the line `load("Python/3.11.5-GCCcore-13.2.0")` and the included Python packages under the line `Included extensions`.

It is also recommended to doublecheck the compatibility of the Jupyter notebook version and the extra modules by loading them all in a shell environment. 
To do so, find the module containing the correct Jupyter notebook version (for our example case this is `JupyterNotebook/7.2.0-GCCcore-13.2.0`) and then use `module load <module_name>` for every module as follows:

```shell
$ module load JupyterNotebook/7.2.0-GCCcore-13.2.0
$ module load SciPy-bundle/2023.11-gfbf-2023b
```
This throws no errors, since this module uses the same toolchain as the notebook

If we use a different SciPy module that uses an incompatible toolchain, we will get errors when trying to load it.

```shell
$ module load JupyterNotebook/7.2.0-GCCcore-13.2.0
$ module load SciPy-bundle/2023.07-gfbf-2023a
Lmod has detected the following error:  ...
```

Now that we found the right module for the notebook, add `module load <module_name>` in the `Custom code` field when creating a notebook and you can make use of the packages within that notebook.

<center>
![image](img/ood_jupyter_custom_code.png)
</center>