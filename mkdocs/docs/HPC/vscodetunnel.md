# VS Code Tunnel

Please keep in mind, that this is not a `VS Code` manual,
it is only our recommendation how to connect to the {{ hpcinfra }} using the `VS Code` tunnel. 

For `VS Code` documentation, see <https://code.visualstudio.com/docs>

We only support `VS Code` tunnel access via the `VS Code` application installed on your local computer.

Connecting to the `VS Code` tunnel using the URL via a web browser is not supported, since web access might not work from all browser or operational system.
The only confirmed way to connect via a browser is using Windows 11 and Edge.

Please note that right now you can only have **one tunnel per cluster**.

!!! note

    Please do not use `VS Code` to ssh to the login nodes, but always use a `VS Code` Tunnel connection, preferably using the [interactive and debug cluster](./interactive_debug.md).

## Prerequisites

We do recommend to install the [remote development](https://code.visualstudio.com/docs/remote/remote-overview) extension pack for the `VS Code` application.


## Connection

In the [web portal](./web_portal.md), under the "Interactive Apps" choose "VS Code Tunnel",
select the parameters and launch your job by clicking ++"Launch"++
When your job has started, connect by clicking ++"Connect"++

A new browser tab or window will open, showing a terminal session. For the question `How would you like to log in to Visual Studio Code?` choose `Microsoft Account` (using the arrow keys on your keyboard, then hit ++"Enter"++).

An URL and authentication code are shown. Click the URL to open it, then enter the authentication code, select your Microsoft account and click ++"Continue"++. The tunnel is now ready to be used.

!!! Warning

    If you are an UGent user, and you get an error message like "You do not have access to this"
    during the Microsoft Authentication, then you might have to
    [whitelist yourself](https://dictselfservice.ugent.be/index.php?page=requestform&form=deviceCodeAuth)
    You can use as motivation "Needed for `VS Code` tunnel for HPC" (You have to do it only once.)

    The ability to whitelist yourself is only available for UGent staff. Other users should request to be whitelisted via <{{ hpcinfo }}>.
    
    Please be aware, that it might take up to half an hour until the whitelisting become effective.

Launch the `VS Code` application on your local computer and click the button in the bottom left corner to "Open a remote window".

When asked to "Select an option to open a Remote Window", select "Tunnel", which will automatically install
the "Remote-tunnels" extension (if not already installed).

If you are not connected automatically to the tunnel, please select "Connect to..." and then "Connect to Tunnel". When asked "What type of account did you use to start this tunnel", select "Microsoft account". 
In the newly opened browser tab or window saying "The extension 'Remote - Tunnels' wants to sign in using Microsoft",
click ++"Allow"++.

Then select the tunnel named `vsc-<your vsc account>-<cluster>`.

!!! note

    If you are asked to update `VS Code` CLI on your remote server, choose ++"Not Now"++.
    You do not have permission to update the CLI, as it is centrally installed on our systems.

    This means that your `VS Code` application is newer than the CLI on our systems.
    We update the centrally installed CLI from time to time, but the upgrade rate of the application/CLI is very high,
    so it is hard for us to follow it tightly.

    If you suspect that the too old version of CLI might cause problem, please send us a [software installation request](https://www.ugent.be/hpc/en/support/software-installation-request) for `code-cli`. 

