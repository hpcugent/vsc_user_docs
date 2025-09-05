# Custom web portal app for ABAQUS (CAE course)

Cluster Desktop with Abaqus - course E071400
This app will launch an interactive desktop on a donphan node with 2 cores.
It will then start the Abaqus GUI after setting some environment variables.

Locked down options (in form.yml.erb):
-	Xfce desktop
-	1 node, 2 cores
-	Cluster donphan
-	Free selection 1-8 hours

Custom script is run (in template/desktops/custom.sh) that
-	Creates an environment variable file for Abaqus in the user home folder (abaqus_v6.env)
> `import os, re, glob, driverUtils`
> 
> `license_server_type=FLEXNET`
>
> `abaquslm_license_file="@<LICENSE_SERVER_ADDRESS>"`
>
> `#set plugin central directory correct. For each hpc cluster it is installed in a different location`
>
> `plugin_central_dir=os.environ.get("ABA_HOME",)+"/SMATfoResources/gui/plugins/"`
- executes commands:
  - `module load ABAQUS`
  - `vglrun abaqus cae`


