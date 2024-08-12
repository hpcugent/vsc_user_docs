# Using Jupyter Notebooks on the HPC

Through the web portal you can easily start a [Jupyter notebook](https://jupyter.org/) on a workernode, via the *Jupyter Notebook* button under the *Interactive Apps* menu item.

<center>
![image](img/ood_start_jupyter.png)
</center>

######## Something about the options and the import difficulties with a nice picture

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

This will launch the Jupyter environment in a new browser tab, where you can open an existing notebook by navigating to the directory where it located and clicking it, or using the *New* menu on the top right:

<center>
![image](img/ood_jupyter_new_notebook.png)
</center>