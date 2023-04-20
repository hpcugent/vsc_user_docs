# Using the HPC-UGent web portal

The HPC-UGent web portal provides "one stop shop" for the HPC-UGent
infrastructure. It is based on [Open OnDemand](https://openondemand.org/) (or `OoD`
for short).

Via this web portal you can upload and download files, create, edit,
submit, and monitor jobs, run GUI applications, and connect via SSH, all
via a standard web browser like Firefox, Chrome or Safari. You do not
need to install or configure any client software, and no SSH key is
required to connect to your VSC account via this web portal.\
Please note that we do recommend to use our interactive and debug
cluster (see chapter [HPC-UGent interactive and debug cluster](./interactive_gent.md)) with `OoD`.

To connect to the HPC-UGent infrastructure via the web portal, visit:

<center>
<https://login.hpc.ugent.be>
</center>

Note that you may only see a "*Submitting...*" message appear for a
couple of seconds, which is perfectly normal.

Through this web portal, you can:

-   browse through the files & directories in your VSC account, and
    inspect, manage or change them;

-   consult active jobs (across all HPC-UGent Tier-2 clusters);

-   submit new jobs to the HPC-UGent Tier-2 clusters, either from
    existing job scripts or from job templates;

-   start an interactive graphical user interface (a desktop
    environment), either on the login nodes or on a cluster workernode;

-   open a terminal session directly in your web browser;

More detailed information is available below, as well as in the [Open
OnDemand
documentation](https://osc.github.io/ood-documentation/master/). A
walkthrough video is available on YouTube
[here](https://www.youtube.com/watch?v=4-w-4wjlnPk).

## Pilot access

### Known issues & limitations

##### Limited resources

All web portal sessions are currently served through a single separate
login node, so the available resources are relatively limited. We will
monitor the resources used by the active web portal sessions throughout
the pilot phase to evaluate whether more resources are required.

## Login

When visiting the HPC-UGent web portal you will be automatically logged
in via the VSC accountpage (see also 
Section [Applying for the account](../account/#applying-for-the-account)).

### First login

The first time you visit <https://login.hpc.ugent.be> permission will be
requested to let the web portal access some of your personal information
(VSC login ID, account status, login shell and institute name), as shown
in this screenshot below:

<center>
![image](img/ood_permission.png)
</center>

**Please click "Authorize" here.**

This request will only be made once, you should not see this again
afterwards.

## Start page

Once logged in, you should see this start page:

<center>
![image](img/ood_start.png)
</center>

This page includes a menu bar at the top, with buttons on the left
providing access to the different features supported by the web portal,
as well as a *Help* menu, your VSC account name, and a *Log Out* button
on the top right, and the familiar HPC-UGent welcome message with a
high-level overview of the HPC-UGent Tier-2 clusters.

If your browser window is too narrow, the menu is available at the top
right through the "hamburger" icon:

<center>
![image](img/ood_hamburger.png)
</center>

## Features

We briefly cover the different features provided by the web portal,
going from left to right in the menu bar at the top.

### File browser

Via the *Files* drop-down menu at the top left, you can browse through
the files and directories in your VSC account using an intuitive
interface that is similar to a local file browser, and manage, inspect
or change them.

The drop-down menu provides short-cuts to the different `$VSC_*`
directories and filesystems you have access to. Selecting one of the
directories will open a new browser tab with the *File Explorer*:

<center>
![image](img/ood_file_explorer.png)
</center>

Here you can:

-   Click a directory in the tree view on the left to open it;

-   Use the buttons on the top to:

    -   go to a specific subdirectory by typing in the path (via *Go
        To...*);

    -   open the current directory in a terminal (shell) session (via
        *Open in Terminal*);

    -   create a new file (via *New File*) or subdirectory (via *New
        Dir*) in the current directory;

    -   upload files or directories from your local workstation into
        your VSC account, in the currect directory (via *Upload*);

    -   show hidden files and directories, of which the name starts with
        a dot (`.`) (via *Show Dotfiles*);

    -   show the owner and permissions in the file listing (via *Show
        Owner/Mode*);

-   Double-click a directory in the file listing to open that directory;

-   Select one or more files and/or directories in the file listing,
    and:

    -   use the *View* button to see the contents (use the button at the
        top right to close the resulting popup window);

    -   use the *Edit* button to open a simple file editor in a new
        browser tab which you can use to make changes to the selected
        file and save them;

    -   use the *Rename/Move* button to rename or move the selected
        files and/or directories to a different location in your VSC
        account;

    -   use the *Download* button to download the selected files and
        directories from your VSC account to your local workstation;

    -   use the *Copy* button to copy the selected files and/or
        directories, and then use the *Paste* button to paste them in a
        different location;

    -   use the *(Un)Select All* button to select (or unselect) all
        files and directories in the current directory;

    -   use the *Delete* button to (**permanently!**) remove the selected files and
        directories;

For more information, see aslo
<https://www.osc.edu/resources/online_portals/ondemand/file_transfer_and_management>.

### Job management

Via the *Jobs* menu item, you can consult your active jobs or submit new
jobs using the *Job Composer*.

For more information, see the sections below as well as
<https://www.osc.edu/resources/online_portals/ondemand/job_management>.

#### Active jobs

To get an overview of all your currently active jobs, use the *Active
Jobs* menu item under *Jobs*.

A new browser tab will be opened that shows all your current queued
and/or running jobs:

<center>
![image](img/ood_active_jobs.png)
</center>

You can control which jobs are shown using the *Filter* input area, or
select a particular cluster from the drop-down menu *All Clusters*, both
at the top right.

Jobs that are still queued or running can be deleted using the red
button on the right.

Completed jobs will also be visible in this interface, but only for a
short amount of time after they have stopped running.

For each listed job, you can click on the arrow ($>$) symbol to get a
detailed overview of that job, and get quick access to the corresponding
output directory (via the *Open in File Manager* and *Open in Terminal*
buttons at the bottom of the detailed overview).

#### Job composer

To submit new jobs, you can use the *Job Composer* menu item under
*Jobs*. This will open a new browser tab providing an interface to
create new jobs:

<center>
![image](img/ood_job_composer.png)
</center>

This extensive interface allows you to create jobs from one of the
available templates, or by copying an existing job.

You can carefuly prepare your job and the corresponding job script via
the *Job Options* button and by editing the job script (see lower
right).

Don't forget to actually submit your job to the system via the green
*Submit* button!

##### Job templates

In addition, you can inspect provided job templates, copy them or even
create your own templates via the *Templates* button on the top:

<center>
![image](img/ood_job_templates.png)
</center>

### Shell access

Through the *Shell Access* button that is available under the *Clusters*
menu item, you can easily open a terminal (shell) session into your VSC
account, straight from your browser!

<center>
![image](img/ood_shell.png)
</center>

Using this interface requires being familiar with a Linux shell
environment (see
Appendix [Useful Linux Commands](../useful_linux_commands)).

To exit the shell session, type `exit` followed by *Enter* and then
close the browser tab.

Note that you can not access a shell session after you closed a browser
tab, even if you didn't exit the shell session first (unless you use
terminal multiplexer tool like `screen` or `tmux`).

### Interactive applications

#### Graphical desktop environment

To create a graphical desktop environment, use on of the *desktop on... node* buttons under *Interactive Apps* menu item. For example:

<center>
![image](img/ood_launch_desktop.png)
</center>

You can either start a desktop environment on a login node for some
lightweight tasks, or on a workernode of one of the HPC-UGent Tier-2
clusters if more resources are required. Keep in mind that for desktop
sessions on a workernode the regular queueing times are applicable
dependent on requested resources.

**Do keep in mind that desktop environments on a cluster workernode are limited to a maximum of 72 hours, just like regular jobs are.**

To access the desktop environment, click the *My Interactive Sessions*
menu item at the top, and then use the *Launch desktop on \... node*
button if the desktop session is *Running*:

<center>
![image](img/ood_desktop_running.png)
</center>

#### Jupyter notebook

Through the web portal you can easily start a [Jupyter
notebook](https://jupyter.org/) on a workernode, via the *Jupyter
Notebook* button under the *Interactive Apps* menu item.

<center>
![image](img/ood_start_jupyter.png)
</center>

After starting the Jupyter notebook using the *Launch* button, you will
see it being added in state *Queued* in the overview of interactive
sessions (see *My Interactive Sessions* menu item):

<center>
![image](img/ood_jupyter_queued.png)
</center>

When your job hosting the Jupyter notebook starts running, the status
will first change the *Starting*:

<center>
![image](img/ood_jupyter_starting.png)
</center>

and eventually the status will change to *Running*, and you will be able
to connect to the Jupyter environment using the blue *Connect to
Jupyter* button:

<center>
![image](img/ood_jupyter_running.png)
</center>

This will launch the Jupyter environment in a new browser tab, where you
can open an existing notebook by navigating to the directory where it
located and clicking it, or using the *New* menu on the top right:

<center>
![image](img/ood_jupyter_new_notebook.png)
</center>

Here's an example of a Jupyter notebook in action. Note that several
non-standard Python packages (like *numpy*, *scipy*, *pandas*,
*matplotlib*) are readily available:

<center>
![image](img/ood_jupyter_notebook_example.png)
</center>

## Restarting your web server in case of problems

In case of problems with the web portal, it could help to restart the
web server running in your VSC account.

You can do this via the *Restart Web Server* button under the *Help*
menu item:

<center>
![image](img/ood_help_restart_web_server.png)
</center>

Of course, this only affects your own web portal session (not those of
others).
