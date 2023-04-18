# Graphical applications with VNC

{% if site == gent %}
**VNC is still available at UGent site but we encourage our users to replace VNC by X2Go client**.
Please see [Graphical applications with X2Go](../x2go/#graphical-applications-with-x2go) for more information.
{% endif %}

Virtual Network Computing is a graphical desktop sharing system that
enables you to interact with graphical software running on the HPC
infrastructure from your own computer.

**Please carefully follow the instructions below, since the procedure to connect to a VNC server running on the HPC infrastructure is not trivial, due to security constraints.**

## Starting a VNC server

First login on the login node (see [First time connection to the HPC infrastructure](../connecting/#first-time-connection-to-the-hpc-infrastructure), then start `vncserver` with:

<pre><code>$ <b>vncserver -geometry 1920x1080 -localhost</b>
You will require a password to access your desktops.

Password:<b>&lt;enter a secure password&gt;</b>
Verify:<b>&lt;enter the same password&gt;</b>
Would you like to enter a view-only password (y/n)? <b>n</b>
A view-only password is not used

New '<b>{{loginhost}}:6</b> ({{userid}})' desktop is {{loginhost}}:6

Creating default startup script {{homedir}}.vnc/xstartup
Creating default config {{homedir}}.vnc/config
Starting applications specified in {{homedir}}.vnc/xstartup
Log file is {{homedir}}.vnc/{{loginhost}}:6.log
</code></pre>

**When prompted for a password, make sure to enter a secure password: if someone can guess your password, they will be able to do anything with your account you can!**

Note down the details in bold: the hostname (in the example: `{{loginhost}}`) and the
(partial) port number (in the example: `6`).

It's important to remember that VNC sessions are permanent. They survive
network problems and (unintended) connection loss. This means you can
logout and go home without a problem (like the terminal equivalent
`screen` or `tmux`). This also means you don't have to start `vncserver`
each time you want to connect.

## List running VNC servers 

You can get a list of running VNC servers on a node with

<pre><code>$ <b>vncserver -list</b>
TigerVNC server sessions:

X DISPLAY #	PROCESS ID
:6		    30713
</code></pre>

This only displays the running VNC servers on **the login node you run the command on**.

To see what login nodes you are running a VNC server on, you can run the
`ls .vnc/*.pid` command in your home directory: the files shown have the
hostname of the login node in the filename:

<pre><code>$ <b>cd $HOME</b>
$ <b>ls .vnc/*.pid</b>
.vnc/{{loginhost}}:6.pid
.vnc/{{altloginhost}}:8.pid
</code></pre>

This shows that there is a VNC server running on `{{loginhost}}` on port 5906 and
another one running `{{altloginhost}}` on port 5908 (see also [Determining the source/destination port](./#determining-the-sourcedestination-port)).

## Connecting to a VNC server

The VNC server runs on a (in the example above, on `{{loginhost}}`).

In order to access your VNC server, you will need to set up an SSH
tunnel from your workstation to this login node (see [Setting up the SSH tunnel(s)](./#setting-up-the-ssh-tunnels)).

Login nodes are rebooted from time to time. You can check that the VNC
server is still running in the same node by executing `vncserver -list`
(see also 
[List running VNC servers](./#list-running-vnc-servers)). If you get an empty list, it means that there is no VNC
server running on the login node.

**To set up the SSH tunnel required to connect to your VNC server, you will need to port forward the VNC port to your workstation.**

The *host* is `localhost`, which means "your own computer": we set up an
SSH tunnel that connects the VNC port on the login node to the same port
on your local computer.

### Determining the source/destination port 

The *destination port* is the port on which the VNC server is running
(on the login node), which is **the sum of `5900` and the partial port number** we noted down earlier (`6`); in the
running example, that is `5906`.

The *source port* is the port you will be connecting to with your VNC
client on your workstation. Although you can use any (free) port for
this, we strongly recommend to use the **same value as the destination port**.

So, in our running example, both the source and destination ports are
`5906`.

### Picking an intermediate port to connect to the right login node

In general, you have no control over which login node you will be on
when setting up the SSH tunnel from your workstation to `{{loginnode}}` (see [Setting up the SSH tunnel(s)](./#setting-up-the-ssh-tunnels)).

If the login node you end up on is a different one than the one where
your VNC server is running (i.e., `{{altloginhost}}` rather than `{{loginhost}}` in our running
example), you need to create a ***second* SSH tunnel** on the login node you are connected to,
in order to "patch through" to the correct port on the login node
where your VNC server is running.

In the remainder of these instructions, we will assume that we are
indeed connected to a different login node. Following these instructions
should always work, even if you happen to be connected to the correct
login node.

To set up the second SSH tunnel, you need to **pick an (unused) port on the login node you are connected to**, which will be used as an
*intermediate* port.

Now we have a chicken-egg situation: you need to pick a port before
setting up the SSH tunnel from your workstation to `{{loginhost}}`, but only after
starting the SSH tunnel will you be able to determine whether the port
you picked is actually free or not...

In practice, if you **pick a *random* number between $10000$ and $30000$**, you have a good chance that the port will not be
used yet.

We will proceed with $12345$ as intermediate port, but **you should pick another value that other people are not likely to pick**. If you need
some inspiration, run the following command on a Linux server (for
example on a login node): `echo $RANDOM` (but do not use a value lower
than $1025$).

### Setting up the SSH tunnel(s)

#### Setting up the first SSH tunnel from your workstation to {{loginnode}}

First, we will set up the SSH tunnel from our workstation to .

Use the settings specified in the sections above:

-   *source port*: the port on which the VNC server is running (see [Determining the source/destination port](./#determining-the-sourcedestination-port));

-   *destination host*: `localhost`;

-   *destination port*: use the intermediate port you picked (see [Picking an intermediate port to connect to the right login node](./#picking-an-intermediate-port-to-connect-to-the-right-login-node))

{% if OS == windows %}
See for detailed information on how to configure PuTTY to set up the SSH
tunnel, by entering the settings in the and fields in [SSH tunnel](../running_interactive_jobs/#ssh-tunnel).

{% else %}
Execute the following command to set up the SSH tunnel.

<pre><code>$ <b>ssh -L 5906:localhost:12345  {{userid}}@{{loginnode}}</b>
</code></pre>

**Replace the source port `5906`, destination port `12345` and user ID {{userid}} with your own!**

{% endif %}

With this, we have forwarded port `5906` on our workstation to port
`12345` on the login node we are connected to.

**Again, do *not* use `12345` as destination port, as this port will most likely be used by somebody else already; replace it with a port number you picked yourself, which is unlikely to be used already (see [Picking an intermediate port to connect to the right login node](./#picking-an-intermediate-port-to-connect-to-the-right-login-node)).**

#### Checking whether the intermediate port is available

Before continuing, it's good to check whether the intermediate port that
you have picked is actually still available (see [Picking an intermediate port to connect to the right login node](./#picking-an-intermediate-port-to-connect-to-the-right-login-node)).

You can check using the following command (**do not forget to replace `12345` the value you picked for your intermediate port):

<pre><code>$ <b>netstat -an | grep -i listen | grep tcp | grep 12345</b>
$
</code></pre>

If you see no matching lines, then the port you picked is still
available, and you can continue.

If you see one or more matching lines as shown below,
**you must disconnect the first SSH tunnel, pick a different intermediate port, and set up the first SSH tunnel again using the new value**.

<pre><code>$ <b>netstat -an | grep -i listen | grep tcp | grep 12345</b>
tcp        0      0 0.0.0.0:12345           0.0.0.0:*               LISTEN
tcp6       0      0 :::12345                :::*                    LISTEN
$
</code></pre>

#### Setting up the second SSH tunnel to the correct login node

In the session on the login node you created by setting up an SSH tunnel
from your workstation to `{{loginnode}}`, you now need to set up the second SSH
tunnel to "patch through" to the login node where your VNC server is
running (`{{loginhost}}` in our running example, see [Starting a VNC server](./#starting-a-vnc-server)).

To do this, run the following command:

<pre><code>$ <b>ssh -L 12345:localhost:5906 {{loginhost}}</b>
$ <b>hostname</b>
{{loginhost}}
</code></pre>

With this, we are forwarding port `12345` on the login node we are
connected to (which is referred to as `localhost`) through to port
`5906` on our target login node (`{{loginhost}}`).

Combined with the first SSH tunnel, port `5906` on our workstation is
now connected to port `5906` on the login node where our VNC server is
running (via the intermediate port `12345` on the login node we ended up
one with the first SSH tunnel).

**Do not forget to change the intermediate port (`12345`), destination port (`5906`),
and hostname of the login node (`{{loginhost}}`) in the command shown above!

As shown above, you can check again using the `hostname` command whether
you are indeed connected to the right login node. If so, you can go
ahead and connect to your VNC server (see [Connecting using a VNC client](./#connecting-using-a-vnc-client)).

### Connecting using a VNC client 

{% if OS == windows %}
You can download a free VNC client from
<https://sourceforge.net/projects/turbovnc/files/>. You can download the
latest version by clicking the top-most folder that has a version number
in it that doesn't also have `beta` in the version. Then download a file
that looks like `TurboVNC64-2.1.2.exe` (the version number can be
different, but the `64` should be in the filename) and execute it. 
{% endif %}
{% if OS == macos %}
You can download a free VNC client from
<https://sourceforge.net/projects/turbovnc/files/>. You can download the
latest version by clicking the top-most folder that has a version number
in it that doesn't also have `beta` in the version. Then download a file
ending in `TurboVNC64-2.1.2.dmg` (the version number can be different)
and execute it. 
{% endif %}
{% if OS == linux %}
Download and setup a VNC client. A good choice is
`tigervnc`. You can start it with the `vncviewer` command.
{% endif %}

Now start your VNC client and connect to `localhost:5906`. **Make sure you replace the port number `5906` with your own destination port (see [Determining the source/destination port](./#determining-the-sourcedestination-port)).

When prompted for a password, use the password you used to setup the VNC
server.

When prompted for default or empty panel, choose default.

If you have an empty panel, you can reset your settings with the
following commands:

<pre><code>$ <b>xfce4-panel --quit ; pkill xfconfd</b>
$ <b>mkdir ~/.oldxfcesettings</b>
$ <b>mv ~/.config/xfce4 ~/.oldxfcesettings</b>
$ <b>xfce4-panel</b>
</code></pre>

## Stopping the VNC server 

The VNC server can be killed by running

<pre><code>vncserver -kill :6
</code></pre>

where `6` is the port number we noted down earlier. If you forgot, you
can get it with `vncserver -list` (see [List running VNC servers](./#list-running-vnc-servers)).

## I forgot the password, what now?

You can reset the password by first stopping the VNC server (see ), then
removing the `.vnc/passwd` file (with `rm .vnc/passwd`) and then
starting the VNC server again (see [Starting a VNC server](./#starting-a-vnc-server)).
