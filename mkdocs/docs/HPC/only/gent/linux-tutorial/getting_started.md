Getting Started
===============

Logging in
----------

To get started with the HPC-UGent infrastructure, you need to obtain a
VSC account, see [HPC manual](https://docs.hpc.ugent.be/account/).
**Keep in mind that you must keep your private key to yourself!**

You can look at your public/private key pair as a lock and a key: you
give us the lock (your public key), we put it on the door, and then you
can use your key to open the door and get access to the HPC
infrastructure. **Anyone who has your key can use your VSC account!**

Details on connecting to the HPC infrastructure are available in
[HPC manual connecting section](https://docs.hpc.ugent.be/connecting/).

Getting help
------------

To get help:

1.  use the documentation available on the system, through the `help`,
    `info` and `man` commands (use `q` to exit).
    ```
    help cd
    info ls
    man cp
    ```

2.  use Google

3.  contact <a href="mailto:{{hpcinfo}}">{{hpcinfo}}</a> in case 
of problems or questions (even for basic things!)

### Errors

Sometimes when executing a command, an error occurs. Most likely there
will be error output or a message explaining you this. Read this
carefully and try to act on it. Try googling the error first to find any
possible solution, but if you can't come up with something in 15
minutes, don't hesitate to mail <a href="mailto:{{hpcinfo}}">{{hpcinfo}}</a>.

Basic terminal usage
--------------------

The basic interface is the so-called shell prompt, typically ending with
`$` (for `bash` shells).

You use the shell by executing commands, and hitting `<enter>`. For
example:
<pre><code>$<b> echo hello</b>
hello
</code></pre>

You can go to the start or end of the command line using `Ctrl-A` or
`Ctrl-E`.

To go through previous commands, use `<up>` and `<down>`, rather than
retyping them.

### Command history

A powerful feature is that you can "search" through your command
history, either using the `history` command, or using `Ctrl-R`:
<pre><code>$<b> history</b>
    1 echo hello

# hit Ctrl-R, type 'echo' 
(reverse-i-search)`echo': echo hello
</code></pre>

### Stopping commands

If for any reason you want to stop a command from executing, press
`Ctrl-C`. For example, if a command is taking too long, or you want to
rerun it with different arguments.

Variables
---------
[//]: # (sec:environment-variables())

At the prompt we also have access to shell variables, which have both a
*name* and a *value*.

They can be thought of as placeholders for things we need to remember.

For example, to print the path to your home directory, we can use the
shell variable named `HOME`:

<pre><code>$<b> echo $HOME</b>
/user/home/gent/vsc400/vsc40000
</code></pre>

This prints the value of this variable.

### Defining variables

There are several variables already defined for you when you start your
session, such as `$HOME` which contains the path to your home directory.

For a full overview of defined environment variables in your current
session, you can use the `env` command. You can sort this output with
`sort` to make it easier to search in:

<pre><code>$<b> env | sort</b>
...
HOME=/user/home/gent/vsc400/vsc40000
...
</code></pre>

You can also use the `grep` command to search for a piece of text. The
following command will output all VSC-specific variable names and their
values:

<pre><code>$ <b>env | sort | grep VSC</b></code></pre>

But we can also define our own. this is done with the `export` command
(note: variables are always all-caps as a convention):

<pre><code>$ <b>export MYVARIABLE="value"</b></code></pre>

It is important you don't include spaces around the `=` sign. Also note
the lack of `$` sign in front of the variable name.

If we then do
<pre><code>$ <b>echo $MYVARIABLE</b></code></pre>

this will output `value`. Note that the quotes are not included, they
were only used when defining the variable to escape potential spaces in
the value.

#### Changing your prompt using `$PS1`

You can change what your prompt looks like by redefining the
special-purpose variable `$PS1`.

For example: to include the current location in your prompt:
<pre><code>$ <b>export PS1='\w $'</b>
~ $ cd test
~/test $
</code></pre>

Note that `~` is short representation of your home directory.

To make this persistent across session, you can define this custom value
for `$PS1` in your `.profile` startup script:
<pre><code>$ <b>echo 'export PS1="\w $ " ' >> ~/.profile</b></code></pre>

### Using non-defined variables

One common pitfall is the (accidental) use of non-defined variables.
Contrary to what you may expect, this does *not* result in error
messages, but the variable is considered to be *empty* instead.

This may lead to surprising results, for example:
<pre><code>$ <b>export WORKDIR=/tmp/test</b>
$ <b>pwd</b>
/user/home/gent/vsc400/vsc40000
$ <b>echo $HOME</b>
/user/home/gent/vsc400/vsc40000
</code></pre>

To understand what's going on here, see the section on `cd` below.

The moral here is: **be very careful to not use empty variables unintentionally**.

**Tip for job scripts: use `set -e -u` to avoid using empty variables accidentally.**

The `-e` option will result in the script getting stopped if any command
fails.

The `-u` option will result in the script getting stopped if empty
variables are used. (see <https://ss64.com/bash/set.html> for a more
detailed explanation and more options)

More information can be found at <http://www.tldp.org/LDP/abs/html/variables.html>.

### Restoring your default environment

If you've made a mess of your environment, you shouldn't waste too much
time trying to fix it. Just log out and log in again and you will be
given a pristine environment.

Basic system information
------------------------

Basic information about the system you are logged into can be obtained
in a variety of ways.

We limit ourselves to determining the hostname:
<pre><code>$ <b>hostname</b>
gligar01.gligar.os

$ <b>echo $HOSTNAME</b>
gligar01.gligar.os
</code></pre>

And querying some basic information about the Linux kernel:
<pre><code>$ <b>uname -a</b>
Linux gligar01.gligar.os 2.6.32-573.8.1.el6.ug.x86_64 #1 SMP Mon Nov 16 15:12:09
    CET 2015 x86_64 x86_64 x86_64 GNU/Linux
</code></pre>



Exercises
---------

-   Print the full path to your home directory

-   Determine the name of the environment variable to your personal
    scratch directory

-   What's the name of the system you're logged into? Is it the same for
    everyone?

-   Figure out how to print the value of a variable without including a
    newline

-   How do you get help on using the `man` command?
