# Connecting to the HPC infrastructure

This text will help you to start using the HPC infrastructure at UGent.

Before you can really start using the {{ hpc }} clusters, there are several
things you need to do or know:

1. To work on the HPC infrastructure you need some basic knowledge of the [Linux]()
   operating system, using a [terminal]() and the [shell (bash)]().
   Make sure you understand these concepts before continuing.

1. To protect you, your data and the HPC infrastructure, access is limited, and
   connections must be encrypted (by using ssh and https)

1. You need to **log on to the HPC cluster** with your [VSC credentials]().  
   The connection is done by using an SSH client or the [**HPC web
   portal**](web_portal.md).
   If you do not have VSC credentials yet, fix this now.

1. Before you can do some work, you'll have to **transfer your files**
    that you need from your own computer to the HPC cluster. At the end
    of a job, you might want to transfer some files back.

1. Optionally, if you wish to use programs with a **graphical user
    interface**, you will need an X-server on your client system and log
    in to the login nodes with X-forwarding enabled.

1. Often several **versions** of software packages and libraries are
    installed, so you need to select the ones you need. To manage
    different versions efficiently, the VSC clusters use so-called
    **modules**, so you will need to select and load the modules that
    you need.

## Connection restrictions

For security reasons restrictions are in place that limit from where
you can connect to the VSC HPC infrastructure.

VSC login nodes are only directly accessible from within university
networks, and from (most) Belgian commercial internet providers.
$$$ ook eduroam?

All other IP domains are blocked by default. If you are connecting from
an IP address that is not allowed direct access, you have the following
options to get access to VSC login nodes:

- Use a VPN connection to connect to the {{ university }} network
  (recommended).
  See <https://helpdesk.ugent.be/vpn/en/> for more information.

- Add your IP address automatically to the list of trusted IP addresses.
  Go to the [VSC firewall](https://firewall.vscentrum.be) and log in with your
  {{ university }} account.

    -   While this web connection is active new SSH sessions can be
        started.
    -   Active SSH sessions will remain active even when this web page
        is closed.

- Contact your HPC support team (via {{ hpcinfo }}) and ask them to add your
    IP range (e.g., for industry access, automated processes) to the list of
    trusted IP addresses.

Trying to establish an SSH connection from an unknown IP address
will give an error message like this one:

```ABNF
ssh_exchange_identification: read: Connection reset by peer
```

## First Time connection to the HPC infrastructure

The remaining content in this text is primarily focused for people utilizing
a terminal with SSH.

If you want to use the web portal, read following page:
[Using the HPC web portal](web_portal.md).

If you have any issues connecting to the {{ hpc }} after you've followed these
steps, see [Issues connecting to login
node](../troubleshooting/#issues-connecting-to-login-node) to troubleshoot.
steps, see [Issues connecting to login
node](troubleshooting.md#issues-connecting-to-login-node) to troubleshoot.

### Connect

Open up a terminal and enter the following command to connect to the {{ hpc }}.

```bash
ssh {{ userid }}@{{ loginnode }}
```

Here, user {{ userid }} wants to make a connection to the "{{ hpcname }}"
cluster at {{ university }} via the login node "{{ loginnode }}", so replace {{
userid }} with your own VSC id in the above command.

The first time you make a connection to the login node, you will be asked to
verify the authenticity of the login node.

> The authenticity of host 'login.hpc.ugent.be (157.193.252.74)' can't be
> established.  
ED25519 key fingerprint is SHA256:8AJg3lPN27y6i+um7rFx3xoy42U8ZgqNe4LsEycHILA.  
This key is not known by any other names.  
Are you sure you want to continue connecting (yes/no/[fingerprint])?  

Please check ["Warning message when first connecting to new
host"](../troubleshooting/#warning-message-when-first-connecting-to-new-host) on
how to handle this.

$$$ dit hoort in troubleshootig doc
A possible error message you can get if you previously saved your
private key somewhere else than the default location
(`$HOME/.ssh/id_rsa`):

> Permission denied (publickey,gssapi-keyex,gssapi-with-mic).

In this case, use the `-i` option for the `ssh` command to specify the
location of your private key. For example:

```bash
ssh -i /home/example/my_keys
```

## Congratulations, you're on the {{ hpc }} infrastructure now

To find out where you have landed you can **p**rint the current **w**orking
**d**irectory:

```bash
$ pwd
{{ homedir }}
```

Your new private home directory is "{{ homedir }}". Here you can create your
own subdirectory structure, copy and prepare your applications, compile and
test them and submit your jobs on the {{ hpc }}.

```bash
$ cd {{ tutorialdir }}
$ ls
Intro-HPC/
```

This directory currently contains all training material for the ***Introduction
to the {{ hpc }}***. More relevant training material to work with the {{ hpc }}
can always be added later in this directory.

You can now explore the content of this directory with the "ls -l"
(**l**ist**s** **l**ong) and the "cd" (**c**hange **d**irectory) commands:

As we are interested in the use of the ***HPC***, move further to
***Intro-HPC*** and explore the contents up to 2 levels deep (-L 2):

```bash
$ cd Intro-HPC
$ tree -L 2
.
'-- examples
    |-- Compiling-and-testing-your-software-on-the-HPC
    |-- Fine-tuning-Job-Specifications
    |-- Multi-core-jobs-Parallel-Computing
    |-- Multi-job-submission
    |-- Program-examples
    |-- Running-batch-jobs
    |-- Running-jobs-with-input
    |-- Running-jobs-with-input-output-data
    |-- example.pbs
    '-- example.sh
9 directories, 5 files
```

This directory contains:

1. This ***HPC Tutorial***
2. An ***examples*** subdirectory, containing all the examples that you need in
   this Tutorial, as well as examples that might be useful for your specific
   applications.

```bash
$ cd examples
```

!!! tip
    Typing `cd ex` followed by ++tab++ (the Tab-key) will generate the `cd
    examples` command. **Command-line completion** (also **tab completion**)
    is a common feature of the bash command line interpreter, in which the
    program automatically fills in partially typed commands.

!!! tip
    For more exhaustive tutorials about Linux usage, see Appendix [Useful Linux
    Commands](../useful_linux_commands)

The first action is to copy the contents of the {{ hpc }} examples directory to
your home directory, so that you have your own personal copy and that you can
start using the examples. The "-r" option of the copy command will also copy
the contents of the sub-directories "**r**ecursively".

```bash
cp -r {{ examplesdir }} ~/
```

Go to your home directory, check your own private examples directory, ... and
start working.

```bash
cd
ls -l
```

Upon connecting you will see a login message containing your last login time
stamp and a basic overview of the current cluster utilisation.

```bash
Last login: Thu Mar 18 13:15:09 2026 from gligarha02.gastly.os

 STEVIN HPC-UGent infrastructure status on Mon, 19 Apr 2026 10:00:01
      cluster         - full - free -  part - total - running - queued
                        nodes  nodes   free   nodes   jobs      jobs
 -------------------------------------------------------------------------
           joltik           6      0      1      10        29       18
            doduo          22      0     75     128      1397    11933
         accelgor           4      3      2       9        18        1
          donphan           0      0     16      16        16       13
          gallade           2      0      5      16        19      136


For a full view of the current loads and queues see:
https://hpc.ugent.be/clusterstate/
Updates on current system status and planned maintenance can be found on
https://www.ugent.be/hpc/en/infrastructure/status
```

You can exit the connection at anytime by entering:

```bash
$ exit
logout
Connection to {{ loginnode }} closed.
```

## Transfer Files to/from the HPC

Before you can do some work, you'll have to **transfer the files** you need
from your desktop or department to the cluster. At the end of a job, you might
want to transfer some files back.

The preferred way to transfer files is by using an scp or sftp via the secure
OpenSSH protocol. All operating systems ship with an implementation of OpenSSH,
so you don't need to install any third-party software to use it. Just open a
terminal window and jump in!

### Using a GUI

If you want a graphical user interface (GUI) please consider using the [web portal]().

If you prefer a graphical user interface (GUI) to transfer files back and forth
to the {{ hpc }}, you can use a file manager. Open your file manager and press
++"Ctrl"+"l"++ if you are on Linux or ++cmd+"k"++ if you are using MacOS.

This should open up a address bar where you can enter a URL.
Alternatively, look for the "connect to server" option in your file
managers menu.

Enter: **`sftp://{{ userid }}@{{ loginnode }}/`** and press enter.

You should now be able to browse files on the {{ hpc }} in your file browser.

### Using scp

**Secure copy** or **SCP** is a tool (command) for securely transferring files
between a local host (= your computer) and a remote host (the {{ hpc }}). It is
based on the Secure Shell (SSH) protocol. The **scp** command is the equivalent
of the **cp** (i.e., **c**o**p**y) command, but can copy files to or from
remote machines.

It's easier to copy files directly to `$VSC_DATA` and `$VSC_SCRATCH` if you
have **symlinks** to them in your home directory.  
See [symlinks](/linux-tutorial/uploading_files/#symlinks-for-datascratch) on
how to create symlinks.

Open an additional terminal window and check that you're working on your
local machine. The command hostname should give you the name of **your** pc.

```bash
$ hostname
<local-machine-name>
```

If you're still using the terminal that is connected to the {{ hpc }}, close the
connection by typing "exit" in the terminal window.

#### Example: copy a file to the hpc cluster

We will copy the (local) file "*localfile.txt*" from your pc to your
home directory on the (remote) {{ hpc }} cluster.

Note the **#**-signs are used to indicate comments, you do not need to type the
comments.

First we generate a small dummy file "*localfile.txt*", which contains the word
"Hello". To create this file we use the tool "echo", which shows some text on
the screen. We can redirect the output of a command to a file with the **>**-symbol.

```bash
$ echo "Hello"  # show the word Hello on the screen
Hello
$ echo "Hello" > localfile.txt # create the file
$ ls -l                        # verify if the file exists
...
-rw-r--r-- 1 user  staff   6 Sep 18 09:37 localfile.txt
$ cat localfile.txt # verify the contents of the file
Hello
```

Use your own VSC account, which is something like "{{ userid }}".

Don't forget the colon (**:**) at the end. If you forget it, it will just
create a file named {{ userid }}@{{ loginnode }} on your local filesystem. You
can even specify where to save the file on the remote filesystem by putting a
path after the colon.

```bash
$ scp localfile.txt {{ userid }}@{{ loginnode }}:
localfile.txt     100%   6     0.0KB/s     00:00
```

Connect to the {{ hpc }} via another terminal, print the working directory (to
make sure you're in the home directory) and check whether the file has
arrived:

```bash
$ pwd
{{ homedir }}
$ ls -l 
total 1536
drwxrwxr-x 2
drwxrwxr-x 2
drwxrwxr-x 10
-rw-r--r-- 1
$ cat localfile.txt
Hello
```

The **scp** command can also be used to copy files from the cluster to your
local machine. Let us copy the remote file "intro-HPC.pdf" from your "docs"
subdirectory on the cluster to your local computer.

First, we will confirm that the file is indeed in the "docs" subdirectory. In
the terminal on the login node, enter:

```bash
$ cd ~/docs
$ ls -l
total 1536
-rw-r--r-- 1 {{ userid }} Sep 11 09:53 intro-HPC.pdf
```

Now we will copy the file to the local machine. On the terminal on your
own local computer, enter:

```bash
$ scp {{ userid }}@{{ loginnode }}:./docs/intro-HPC.pdf .
intro-HPC.pdf 100% 725KB 724.6KB/s 00:01
$ ls -l
total 899
-rw-r--r-- 1 user staff 741995 Sep 18 09:53
-rw-r--r-- 1 user staff      6 Sep 18 09:37 localfile.txt
```

The file has been copied from the HPC to your local computer.

It's also possible to copy entire directories (and their contents) with
the `-r` flag. For example, if we want to copy the local directory
`dataset` to `$VSC_SCRATCH`, we can use the following command (assuming
you've created the `scratch` symlink):

```bash
scp -r dataset {{ userid }}@{{ loginnode }}:scratch
```

If you don't use the `-r` option to copy a directory, you will run into
the following error:

```bash
$ scp dataset {{ userid }}@{{ loginnode }}:scratch
dataset: not a regular file
```

### Using sftp

The **SSH File Transfer Protocol** (also **Secure File Transfer Protocol**, or
**SFTP**) is a network protocol that provides file access, file transfer and
file management functionalities over any reliable data stream.
Compared to scp the sftp tool provides a more interactive way of doing file transfers.

One easy way of starting a sftp session is

```bash
sftp {{ userid }}@{{ loginnode }}
```

After the sftp program is started you get a prompt and you can issue commands.

Typical and popular commands inside an sftp session are:

| Command                   | What the command does                                                                |
|:--------------------------|:-------------------------------------------------------------------------------------|
| **?**                     | Show a list of commands                                                              |
| **bye**                   | Quit the sftp session                                                                |
| **ls**                    | Get a list of the files in the current directory on the {{ hpc }}.                   |
| **lls**                   | Get **l**ocal directory listing (i.e. on your computer).                             |
| **cd ~/exmples/fibo**     | Move to the examples/fibo subdirectory on the remote machine (i.e., the {{ hpc }})   |
| **get fibo.py**           | Copy the file "fibo.py" from the {{ hpc }} to your computer                          |
| **get tutorial/HPC.pdf**  | Copy the file "HPC.pdf" from the {{ hpc }}, which is in the "tutorial" subdirectory. |
| **lcd test**              | Move to the "test" subdirectory on your **l**ocal machine.                           |
| **lcd ..**                | Move up one level in the **l**ocal directory.                                        |
| **put test.py**           | Copy the local file test.py to the {{ hpc }}.                                        |
| **put test1.py test2.py** | Copy the local file test1.py to the and rename it to test2.py.                       |
| **mget *.cc**             | Copy all the remote files with extension ".cc" to the local directory.               |
| **mput *.h**              | Copy all the local files with extension ".h" to the {{ hpc }}.                       |

### Fast file transfer for large datasets

$$$ rsync can resume jobs
$$$ filesender??
See [the section on `rsync` in the Linux
intro](../linux-tutorial/uploading_files/#copying-faster-with-rsync).

## Changing login nodes

It can be useful to have control over which login node you are on.

However, when you connect to the HPC (High-Performance Computing) system, you
are directed to a *random* login node, which might not be the one where you
already have an active session. To address this, there is a way to manually
switch your active login node.

For instance, if you want to switch to the login node named `{{loginhost}}`,
you can use the following command while you are connected to the
`{{altloginhost}}` login node on the HPC:

```bash
ssh {{loginhost}}
```

This is also possible the other way around.

If you want to find out which login host you are connected to, you can use the
`hostname` command.

```bash
$ hostname
{{loginhost}}
$ ssh {{altloginhost}}

$ hostname
{{altloginhost}}
```

Rather than always starting a new session on the HPC, you can also use a
terminal multiplexer like `screen` or `tmux`.
These can make sessions that 'survives' across disconnects.

You can find more information on how to use these tools here (or on other
online sources):

- [screen](https://www.howtogeek.com/662422/how-to-use-linuxs-screen-command/)
- [tmux](https://www.howtogeek.com/671422/how-to-use-tmux-on-linux-and-why-its-better-than-screen/)
