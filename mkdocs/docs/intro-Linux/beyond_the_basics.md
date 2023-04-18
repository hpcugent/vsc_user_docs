{% import 'macros/nb.md' as nb %}
# Beyond the basics

Now that you've seen some of the more basic commands, let's take a look
at some of the deeper concepts and commands.

## Input/output


To redirect output to files, you can use the redirection operators: `>`,
`>>`, `&>`, and `<`.

First, it's important to make a distinction between two different output
channels:

1.  `stdout`: standard output channel, for regular output

2.  `stderr`: standard error channel, for errors and warnings

### Redirecting `stdout`

`>` writes the (`stdout`) output of a command to a file and *overwrites*
whatever was in the file before.
<pre><code>$ <b>echo hello > somefile</b>
$ <b>cat somefile</b>
hello
$ <b>echo hello2 > somefile</b>
$ <b>cat somefile</b>
hello2
</code></pre>

`>>` appends the (`stdout`) output of a command to a file; it does not
clobber whatever was in the file before:
<pre><code>$ <b>echo hello > somefile</b>
$ <b>cat somefile</b> 
hello
$ <b>echo hello2 >> somefile</b>
$ cat somefile
hello
hello2
</code></pre>

### Reading from `stdin`

`<` reads a file from standard input (piped or typed input). So you
would use this to simulate typing into a terminal. `< somefile.txt` is
largely equivalent to `cat somefile.txt | `.

One common use might be to take the results of a long-running
command and store the results in a file, so you don't have to repeat it
while you refine your command line. For example, if you have a large
directory structure you might save a list of all the files you're
interested in and then reading in the file list when you are done:
<pre><code>$ <b>find . -name .txt > files</b>
$ <b>xargs grep banana < files</b>
</code></pre>

### Redirecting `stderr`

To redirect the `stderr` output (warnings, messages), you can use `2>`,
just like `>`
<pre><code>$ <b>ls one.txt nosuchfile.txt 2> errors.txt</b>
one.txt
$ <b>cat errors.txt</b>
ls: nosuchfile.txt: No such file or directory
</code></pre>

### Combining `stdout` and `stderr`

To combine both output channels (`stdout` and `stderr`) and redirect
them to a single file, you can use `&>`
<pre><code>$ <b>ls one.txt nosuchfile.txt &> ls.out</b>
$ <b>cat ls.out</b>
ls: nosuchfile.txt: No such file or directory
one.txt
</code></pre>

## Command piping

Part of the power of the command line is to string multiple commands
together to create useful results. The core of these is the pipe: `|`.
For example, to see the number of files in a directory, we can pipe the
(`stdout`) output of `ls` to `wc` (**w**ord **c**ount, but can also be used to
count the number of lines with the `-l` flag).
<pre><code>$ <b>ls | wc -l</b>
    42
</code></pre>

A common pattern is to pipe the output of a command to `less` so you
can examine or search the output:
<pre><code>$ <b>find . | less</b></code></pre>

Or to look through your command history:
<pre><code>$ <b>history | less</b></code></pre>

You can put multiple pipes in the same line. For example, which `cp`
commands have we run?
<pre><code>$ <b>history | grep cp | less</b></code></pre>

## Shell expansion

The shell will expand certain things, including:

1.  `*` wildcard: for example `ls t*txt` will list all files starting
    with 't' and ending in 'txt'

2.  tab completion: hit the `<tab>` key to make the shell complete your
    command line; works for completing file names, command names, etc.

3.  `$...` or `${...}`: environment variables will be replaced with
    their value; example: `echo "I am $USER"` or `echo "I am ${USER}"`

4.  square brackets can be used to list a number of options for a
    particular characters; {{nb.nb("example: `ls *.[oe][0-9]`.")}} This will list all
    files starting with whatever characters (`*`), then a dot (`.`),
    then either an 'o' or an 'e' (`[oe]`), then a character from '0' to
    '9' (so any digit) (`[0-9]`). So this filename will match:
    `anything.o5`, but this one won't: `anything.o52`.

## Process information

### `ps` and `pstree`

`ps` lists processes running. By default, it will only show you the
processes running in the local shell. To see all of your processes
running on the system, use:
<pre><code>$ <b>ps -fu $USER</b></code></pre>

To see all the processes:
<pre><code>$ <b>ps -elf</b></code></pre>

To see all the processes in a forest view, use:
<pre><code>$ <b>ps auxf</b></code></pre>

The last two will spit out a lot of data, so get in the habit of piping
it to `less`.

`pstree` is another way to dump a tree/forest view. It looks better than
`ps auxf` but it has much less information so its value is limited.

`pgrep` will find all the processes where the name matches the pattern
and print the process IDs (PID). This is used in piping the processes
together as we will see in the next section.

### `kill`

`ps` isn't very useful unless you can manipulate the processes. We do
this using the `kill` command. Kill will send a message
([SIGINT](https://en.wikipedia.org/wiki/Unix_signal#POSIX_signals)) to
the process to ask it to stop.
<pre><code>$ <b>kill 1234</b>
$ <b>kill $(pgrep misbehaving_process)</b>
</code></pre>

Usually, this ends the process, giving it the opportunity to flush data
to files, etc. However, if the process ignored your signal, you can send
it a different message
([SIGKILL](https://en.wikipedia.org/wiki/Unix_signal#POSIX_signals))
which the OS will use to unceremoniously terminate the process:
<pre><code>$ <b>kill -9 1234</b>
</code></pre>

### `top`

`top` is a tool to see the current status of the system. You've probably
used something similar in Task Manager on Windows or Activity Monitor in
macOS. `top` will update every second and has a few interesting
commands.

To see only your processes, type `u` and your username after starting
`top`, (you can also do this with {{nb.nb("`top -u $USER`")}}). The default is to
sort the display by `%CPU`. To change the sort order, use `<` and `>`
like arrow keys.

There are a lot of configuration options in `top`, but if you're
interested in seeing a nicer view, you can run `htop` instead. Be aware
that it's not installed everywhere, while `top` is.

To exit `top`, use `q` (for 'quit').

For more information, see [Brendan Gregg's excellent site dedicated to
performance analysis](http://brendangregg.com).

### ulimit

`ulimit` is a utility to get or set user limits on the machine. For
example, you may be limited to a certain number of processes. To see all
the limits that have been set, use:
<pre><code>$ <b>ulimit -a</b></code></pre>

## Counting: `wc`

To count the number of lines, words, and characters (or bytes) in a file, use `wc` (**w**ord ount):
<pre><code>$ <b>wc example.txt</b>
      90     468     3189   example.txt
</code></pre>

The output indicates that the file named `example.txt` contains 90
lines, 468 words, and 3189 characters/bytes.

To only count the number of lines, use `wc -l`:
<pre><code>$ <b>wc -l example.txt</b>
      90    example.txt
</code></pre>

## Searching file contents: `grep`

`grep` is an important command. It was originally an abbreviation for
"globally search a regular expression and print" but it's entered the
common computing lexicon and people use 'grep' to mean searching for
anything. To use grep, you give a pattern and a list of files.
<pre><code>$ <b>grep banana fruit.txt</b>
$ <b>grep banana fruit_bowl1.txt fruit_bowl2.txt</b>
$ <b>grep banana fruit*txt</b>
</code></pre>

`grep` also lets you search for [Regular
Expressions](https://en.wikipedia.org/wiki/Regular_expression), but
these are not in scope for this introductory text.

## `cut`

`cut` is used to pull fields out of files or pipes streams. It's a
useful glue when you mix it with `grep` because `grep` can find the
lines where a string occurs and `cut` can pull out a particular field.
For example, to pull the first column (`-f 1`, the first **f**ield) from (an
unquoted) CSV (comma-separated values, so `-d ','`: **d**elimited by `,`)
file, you can use the following:
<pre><code>$ <b>cut -f 1 -d ',' mydata.csv</b></code></pre>

## `sed`

`sed` is the stream editor. It is used to replace text in a file or
piped stream. In this way, it works like grep, but instead of just
searching, it can also edit files. This is like "Search and Replace" in
a text editor. `sed` has a lot of features, but almost everyone uses the
extremely basic version of string replacement:
<pre><code>$ <b>sed 's/oldtext/newtext/g' myfile.txt</b></code></pre>

By default, sed will just print the results. If you want to edit the
file inplace, use `-i`, but be very careful that the results will be
what you want before you go around **destroying your data**!

## `awk`


`awk` is a basic language that builds on `sed` to do much more advanced
stream editing. Going in depth is far out of scope of this tutorial, but
there are two examples that are worth knowing.

First, `cut` is very limited in pulling fields apart based on
whitespace. For example, if you have padded fields then
`cut -f 4 -d ' '` will almost certainly give you a headache as there
might be an uncertain number of spaces between each field. `awk` does
better whitespace splitting. So, pulling out the fourth field in a
whitespace delimited file is as follows:
<pre><code>$ <b>awk '{print $4}' mydata.dat</b></code></pre>

You can use `-F ':'` to change the delimiter (F for field separator).

The next example is used to sum numbers from a field:
<pre><code>$ <b>awk -F ',' '{sum += $1} END {print sum}' mydata.csv</b></code></pre>
## Basic Shell Scripting

The basic premise of a script is to execute automate the execution of
multiple commands. If you find yourself repeating the same commands over
and over again, you should consider writing one script to do the same. A
script is nothing special, it is just a text file like any other. Any
commands you put in there will be executed from the top to bottom.

However, there are some rules you need to abide by.

Here is a [very detailed guide](http://www.tldp.org/LDP/Bash-Beginners-Guide/html/) should you
need more information.

### Shebang

The first line of the script is the so-called shebang (`#` is sometimes
called hash and `!` is sometimes called bang). This line tells the shell
which command should execute the script. In most cases, this will
simply be the shell itself. The line itself looks a bit weird, but you
can copy-paste this line as you need not worry about it further. It is
however very important this is the very first line of the script! These
are all valid shebangs, but you should only use one of them:

```shell
#!/bin/sh
```
```shell
#!/bin/bash
```
```shell
#!/usr/bin/env bash
```

### Conditionals

Sometimes you only want certain commands to be executed when a certain
condition is met. For example, only move files to a directory if that
directory exists. The syntax:
```shell
if [ -d directory ] && [ -f file ]
then 
  mv file directory 
fi

Or you only want to do something if a file exists:

if [ -f filename ] 
then 
  echo "it exists" 
fi
```
Or only if a certain variable is bigger than one:
```shell
if [ $AMOUNT -gt 1 ]
then
  echo "More than one"
  # more commands
fi
```
Several pitfalls exist with this syntax. You need spaces surrounding the
brackets, the **then** needs to be at the beginning of a line. It is best to just
copy this example and modify it.

In the initial example, we used `-d` to test if a directory existed.
There are [several more checks](http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html).

Another useful example, is to test if a variable contains a value (so it's
not empty):
```shell
if [ -z $PBS_ARRAYID ]
then
  echo "Not an array job, quitting."
  exit 1
fi
```

the `-z` will check if the length of the variable's value is greater than zero.

## Loops

Are you copy-pasting commands? Are you doing the same thing with just different
options? You most likely can simplify your script by using a loop.

Let's look at a simple example:
```shell
for i in 1 2 3
do
  echo $i
done
```

### Subcommands

Subcommands are used all the time in shell scripts. What they
do is storing the output of a command in a variable. So this can later
be used in a conditional or a loop for example.
<pre><code>CURRENTDIR=`pwd`  # using backticks
CURRENTDIR=$(pwd)  # recommended (easier to type)
</code></pre>

In the above example you can see the 2 different methods of using a
subcommand. `pwd` will output the current working directory, and its
output will be stored in the CURRENTDIR variable. The recommended way to
use subcommands is with the `$()` syntax.

### Errors

Sometimes some things go wrong and a command or script you ran causes an
error. How do you properly deal with these situations?

Firstly a useful thing to know for debugging and testing is that you can
run any command like this:
<pre><code>command 2>&1 output.log   # one single output file, both output and errors</code></pre>

If you add `2>&1 output.log` at the end of any command, it will combine
`stdout` and `stderr`, outputting it into a single file named
`output.log`.

If you want regular and error output separated you can use:
<pre><code>command > output.log 2> output.err  # errors in a separate file</code></pre>

this will write regular output to `output.log` and error output to
`output.err`.

You can then look for the errors with `less` or search for specific text
with `grep`.

In scripts, you can use:
<pre><code>set -e</code></pre>


This will tell the shell to stop executing any subsequent commands when
a single command in the script fails. This is most convenient as most
likely this causes the rest of the script to fail as well.

#### Advanced error checking

Sometimes you want to control all the error checking yourself, this is
also possible. Everytime you run a command, a special variable `$?` is
used to denote successful completion of the command. A value other than
zero signifies something went wrong. So an example use case:
```shell
command_with_possible_error
exit_code=$?  # capture exit code of last command
if [ $exit_code -ne 0 ]
then
  echo "something went wrong"
fi
```

## `.bashrc` login script
[//]: # (sec:bashrc-login-script)

If you have certain commands executed every time you log in (which
includes every time a job starts), you can add them to your
`$HOME/.bashrc` file. This file is a shell script that gets executed
every time you log in.

Examples include:

-   modifying your `$PS1` (to tweak your shell prompt)

-   printing information about the current/jobs environment (echoing
    environment variables, etc.)

-   selecting a specific cluster to run on with
    `module swap cluster/...`

Some recommendations:

-   Avoid using `module load` statements in your `$HOME/.bashrc` file

-   Don't directly edit your `.bashrc` file: if there's an error in your
    `.bashrc` file, you might not be able to log in again. To
    prevent that, use another file to test your changes, then copy them
    over when you tested the script.

## Scripting for the cluster
When writing scripts to be submitted on the cluster there are some
tricks you need to keep in mind.

### Example job script
```shell
#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -N FreeSurfer_per_subject-time-longitudinal
#PBS -l walltime=48:00:00
#PBS -q long
#PBS -m abe
#PBS -j oe
export DATADIR=$VSC_DATA/example
# $PBS_JOBID is unique for each job, so this creates a unique directory
export WORKDIR=$VSC_SCRATCH_NODE/$PBS_JOBID
mkdir -p $WORKDIR
# copy files to local storage
cp -a $DATADIR/workfiles $WORKDIR/

# load software we need
module load FreeSurfer
cd $WORKDIR
# recon-all ... &> output.log  # this command takes too long, let's show a more practical example
echo $PBS_ARRAYID > $WORKDIR/$PBS_ARRAYID.txt
# create results directory if necessary
mkdir -p $DATADIR/results
# copy work files back
cp $WORKDIR/$PBS_ARRAYID.txt $DATADIR/results/
```
### PBS pragmas

The scheduler needs to know about the requirements of the script, for
example: how much memory will it use, and how long will it run. These
things can be specified inside a script with what we call PBS pragmas.

This pragma (a pragma is a special comment) tells PBS to use 1 node and core:
```shell
#PBS -l nodes=1:ppn=1 # single-core
```

For parallel software, you can request multiple cores (OpenMP) and/or
multiple nodes (MPI). *Only use this when the software you
use is capable of working in parallel*. Here is an example:
```shell
#PBS -l nodes=1:ppn=16  # single-node, multi-core
#PBS -l nodes=5:ppn=16  # multi-node
```

We intend to submit it on the long queue:
```shell
#PBS -q long
```

We request a total running time of 48 hours (2 days).
```shell
#PBS -l walltime=48:00:00
```

We specify a desired name of our job:
```shell
#PBS -N FreeSurfer_per_subject-time-longitudinal
```
This specifies mail options:
```shell
#PBS -m abe
```

1.  `a` means mail is sent when the job is aborted.

2.  `b` means mail is sent when the job begins.

3.  `e` means mail is sent when the job ends.

Joins error output with regular output:
```shell
#PBS -j oe
```

All of these options can also be specified on the command-line and will
overwrite any pragmas present in the script.

## Exercises

1.  Create a file that contains this message: "Hello, I am &lt;user&gt;",
    where `<user>` is replaced by your username. Don't cheat by using an
    editor, use a command to create the file.

2.  Use another command to add this line to the same file: "I am on
    system &lt;hostname&gt; in directory &lt;current&nbsp;directory&gt;". Words
    between `<>` should be replaced with their value (hint: use
    environment variables).

3.  How many files and directories are in `/tmp`?

4.  What's the name of the 5th file/directory in alphabetical order in
    `/tmp`?

5.  List all files that start with `t` in `/tmp`.

6.  Create a file containing "My home directory &lt;home&gt; is available
    using $HOME". `<home>` should be replaced with your home directory,
    but `$HOME` should remain as-is.

7.  How many processes are you currently running? How many are you
    allowed to run? Where are they coming from?
