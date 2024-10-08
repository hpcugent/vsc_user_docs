# VS Code Tunnel

Please keep in mind, that this is not a `VS Code` manual,
it is only our recommendation how to connect to the {{ hpcinfra }} using the `VS Code` tunnel. 

For `VS Code` documentation, see <https://code.visualstudio.com/docs>

We only support `VS Code` tunnel access via the `VS Code` application (installed locally).
To connect to the `VS Code` tunnel using the URL via a web browser is not supported,
since web access might not work from all browser or operational system.
The only confirmed way to connect via a browser is using Windows 11 and Edge. 

## Prerequisites

We do recommend to install the [remote development](https://code.visualstudio.com/docs/remote/remote-overview)
extension pack for the `VS Code` App.


## Connection

In the [web portal](./web_portal.md), under the "Interactive Apps" choose `VS Code` Tunnel,
select the parameters and launch your job by clicking ++"Launch"++
When your job has started, connect by clicking ++"Connect"++

In the new browser tab or window, for the question
`How would you like to log in to Visual Studio Code?` choose `Microsoft Account` 
(using the arrow keys on your keyboard, then hit ++"Enter"++).
Then follow the instruction to authenticate yourself.

!!! Warning

    If you are an UGent user, and you get an error message something like "You do not have access to this"
    during the Microsoft Authentication, then you might have to
    [whitelist yourself](https://dictselfservice.ugent.be/index.php?page=requestform&form=deviceCodeAuth)
    You can use as motivation "Needed for `VS Code` tunnel for HPC" (You have to do it only once.)
    
    Please be aware, that it might take up to half an hour until the whitelisting become effective.


If you are not connected automatically to the tunnel, please select "connect to..." and then
"Connect to Tunnel" using Microsoft Account and select the tunnel named `vsc-<your vsc account>-<cluster>`.
Please note that right now you can only have one tunnel per cluster.

If you are asked to update `VS Code` CLI on your remote server, choose ++"Not Now"++.
You do not have permission to update the CLI, as it is centrally installed.
This means that your `VS Code` App is newer than the CLI on our systems.
We update the centrally installed CLI time to time,
but the upgrade rate of the App/CLI is very high,
so it is hard for us to follow it tightly.
If you suspect that the too old version of CLI might cause problem, please send us a
[software installation request](https://www.ugent.be/hpc/en/support/software-installation-request)
for `code-cli`. 

Please do not use `VS Code` to ssh to the login nodes,
but always use a `VS Code` Tunnel connection,
preferably using the [interactive and debug cluster](./interactive_debug.md) 

