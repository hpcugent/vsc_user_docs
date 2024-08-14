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

Importing libraries in a notebook running on the HPC isn't as straight forward as on notebooks running on your local machine. You can only import libraries that are part of certain modules on the HPC. To find the right module, first look at the toolchain used by the Jupyter notebook version. This can be found when looking at the `JupyterNotebook version` field when creating a new Jupyter notebook session. In the image above `7.2.0` is the notebook version and `GCCcore 13.2.0`is the toolchain used.

After checking the toolchain, you can search the correct module using a shell environment. You can do this by clicking on `Clusters`>`_login Shell Access` in the web portal.

<center>
![image](img/ood_jupyter_open_shell.png)
</center>

Using `module available` followed by a library name will print all modules in which your library is included. For example if you want to make use of SciPy, it will look like this:

```shell 
$ module available Scipy

----------------------------------------------------------------------------------- /apps/gent/RHEL8/zen2-ib/modules/all ------------------------------------------------------------------------------------
   SciPy-bundle/2019.10-foss-2019b-Python-2.7.16     SciPy-bundle/2020.03-intel-2020a-Python-3.8.2    SciPy-bundle/2021.05-gomkl-2021a                 SciPy-bundle/2022.05-intel-2022a
   SciPy-bundle/2019.10-foss-2019b-Python-3.7.4      SciPy-bundle/2020.03-iomkl-2020a-Python-3.8.2    SciPy-bundle/2021.05-intel-2021a                 SciPy-bundle/2023.02-gfbf-2022b
   SciPy-bundle/2019.10-intel-2019b-Python-2.7.16    SciPy-bundle/2020.11-foss-2020b-Python-2.7.18    SciPy-bundle/2021.10-foss-2021b-Python-2.7.18    SciPy-bundle/2023.07-gfbf-2023a
   SciPy-bundle/2019.10-intel-2019b-Python-3.7.4     SciPy-bundle/2020.11-foss-2020b                  SciPy-bundle/2021.10-foss-2021b                  SciPy-bundle/2023.11-gfbf-2023b     (D)
   SciPy-bundle/2020.03-foss-2020a-Python-3.8.2      SciPy-bundle/2020.11-intel-2020b                 SciPy-bundle/2021.10-intel-2021b                 scipy/1.4.1-foss-2019b-Python-3.7.4
   SciPy-bundle/2020.03-intel-2020a-Python-2.7.18    SciPy-bundle/2021.05-foss-2021a                  SciPy-bundle/2022.05-foss-2022a

  Where:
   D:  Default Module

If you need software that is not listed, request it via https://www.ugent.be/hpc/en/support/software-installation-request
```

To check if a module uses the right toolchain, use the `module show` command:

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
This prints a lot of information about the module, including all libraries that are part of it. It also shows which toolchain is used in the line `load("Python/3.11.5-GCCcore-13.2.0")`.

Because this is the same toolchain as the one used by the Jupyter notebook version in this example, we can include this module without errors. To do this, add the line `module load "module_name"` in the `Custom code`-field:

<center>
![image](img/ood_jupyter_custom_code.png)
</center>

If you want to check the compatibility of your Jupyter notebook version and modules without launching a notebook, you can load the module of your preferred Jupyter notebook version followed by all the modules for your libraries in a shell environment. If this does not throw any errors, the modules are compatible. For our example, this would look as follows:

```shell
$ module load JupyterNotebook/7.2.0-GCCcore-13.2.0
$ module load SciPy-bundle/2023.07-gfbf-2023a # we expect errors since this is a module that uses a different toolchain
Lmod has detected the following error:  ...

$ module load SciPy-bundle/2023.11-gfbf-2023b # Now no errors are thrown since this module uses the same toolchain as the notebook
```
