# Getting Started

To get started with the HPC-UGent infrastructure, you need to obtain a
VSC account, see [HPC manual](../account.md). 
Details on connecting to the HPC infrastructure are available in

## Getting help

To get help:

1.  use the documentation available on the system, through the
    `help`, `info` and `man` commands (use `q` to exit).
    ``` 
    help cd 
    info ls 
    man cp 
    ```
2.  use Google

3. contact <a href="mailto:{{hpcinfo}}">{{hpcinfo}}</a> in case
of problems or questions (even for basic things!)

### Errors

Sometimes when executing a command, an error occurs. Most likely there
will be error output or a message explaining you this. Read this
carefully and try to act on it. Try googling the error first to find any
possible solution, but if you can't come up with something in 15
minutes, don't hesitate to mail 
<a href="mailto:{{hpcinfo}}">{{hpcinfo}}</a>.

## Basic terminal usage

The basic interface is the so-called shell prompt, typically ending with
`$` (for `bash` shells).

You use the shell by executing commands, and hitting
`<enter>`. For example: 
<pre><code>$<b> echo hello 
</b> hello </code></pre>

You can go to the start or end of the command line using
`Ctrl-A` or `Ctrl-E`.

To go through previous commands, use `<up>` and
`<down>`, rather than retyping them.

### Command history

A powerful feature is that you can "search" through your command
history, either using the `history` command, or using
`Ctrl-R`: 
<pre><code>$<b> history</b>
    1 echo hello

# hit Ctrl-R, type 'echo' 
(reverse-i-search)`echo': echo hello
</code></pre>

### Stopping commands

If for any reason you want to stop a command from executing, press
`Ctrl-C`. For example, if a command is taking too long, or
you want to rerun it with different arguments.

## Variables

At the prompt we also have access to *shell variables*, which have both a
*name* and a *value*.

They can be thought of as placeholders for things we need to remember.

For example, to print the path to your home directory, we can use the
shell variable named `HOME`:

<pre><code>$<b> echo $HOME</b> 
/user/home/gent/vsc400/vsc40000
</code></pre>

This prints the value of this variable.

There are several variables already defined for you when you start your
session, such as `$HOME` which contains the path to your
home directory.

For a full overview of defined environment variables in your current
session, you can use the `env` command. You can sort this
output with `sort` to make it easier to search in:

<pre><code>$<b> env | sort</b> 
...
HOME=/user/home/gent/vsc400/vsc40000 
... </code></pre>

!!! info
    In Linux, the pipe operator (`|`) is used to pass output from one command as input to another. 
    This is known as a pipeline. Here, `env | sort` will take the output of `env` and use it as the input for `sort`. 
    This can be extremely useful for chaining together commands and processing data.

You can also use the `grep` command to search for a piece of text. The
following command will output all VSC-specific variable names and their
values:

<pre><code>$ <b>env | sort | grep VSC</b></code></pre>

### Defining variables

It is also possible to define your own variables. this is done with the `export` command:

<pre><code>$ <b>export MYVARIABLE="value"</b></code></pre>


!!! note
    Notice the lack of the `$` sign and spaces around the `=` sign. 
    By convention, variables should be all-caps.


If we then do 
<pre><code>$ <b>echo $MYVARIABLE</b></code></pre>

this will output `value`. Note that the quotes are not
included, they were only used when defining the variable to escape
potential spaces in the value.

### Restoring your default environment

If you've made a mess of your environment, you shouldn't waste too much
time trying to fix it. Just log out and log in again, and you will be
given a pristine environment.

## Basic system information

Basic information about the system you are logged into can be obtained
in a variety of ways.

We limit ourselves to determining the hostname: 
<pre><code>$ <b>hostname</b> 
gligar01.gligar.os

$ <b>echo $HOSTNAME</b> 
gligar01.gligar.os 
</code></pre>

And querying some basic information about the Linux kernel:
<pre><code>$ <b>uname -a </b>
Linux gligar01.gligar.os 2.6.32-573.8.1.el6.ug.x86_64 #1 SMP Mon Nov 16 15:12:09
    CET 2015 x86_64 x86_64 x86_64 GNU/Linux
</code></pre>



## Exercises

??? abstract "Print the full path to your home directory"
    ```bash
    $ echo $HOME
    ```

??? abstract "Determine the name of the environment variable to your personal scratch directory"
    ```bash
    $ env | grep SCRATCH
    ```

??? abstract "What's the name of the system you're logged into? Is it the same for everyone?"
    ```bash
    $ hostname
    ```
    
    Not everyone will be logged in to the same node, so the output will differ.

??? abstract "Figure out how to print the value of a variable without including a newline"
    
    We can use the `man` command to find relevant information on the echo command with:

    ```bash
    $ man echo
    ```

    We find the following line in the manual:

    ```
    -n     do not output the trailing newline
    ```
    
    So we can use the `-n` flag to suppress the newline:
    
    ```bash
    $ echo -n $HOME
    ```

??? abstract "How do you get help on using the `man` command?"
    
    ```bash
    $ man man
    ```

Next [chapter](navigating.md) teaches you how to navigate the filesystem.
