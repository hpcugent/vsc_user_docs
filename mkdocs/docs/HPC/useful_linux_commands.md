# Useful Linux Commands

## Basic Linux Usage

All the {{hpc}} clusters run some variant of the "{{operatingsystembase}}" operating system. This means
that, when you connect to one of them, you get a command line interface,
which looks something like this:

<pre><code>{{userid}}@ln01[203] $
</code></pre>

When you see this, we also say you are inside a "shell". The shell will
accept your commands, and execute them.

<table>
    <tr>
        <td>
          ls
        </td>
        <td>
         Shows you a list of files in the current directory
        </td>
    </tr>
    <tr>
        <td>
          cd
        </td>
        <td>
          Change current working directory
        </td>
    </tr>
    <tr>
        <td>
          rm
        </td>
        <td>
         Remove file or directory
        </td>
    </tr>
{% if site == gent %}
    <tr>
        <td>
          nano
        </td>
        <td>
         Text editor
        </td>
    </tr>
{% else %}
   <tr>
        <td>
          joe
        </td>
        <td>
         Text editor
        </td>
    </tr>
{% endif %}
   <tr>
        <td>
          echo
        </td>
        <td>
         Prints its parameters to the screen
        </td>
    </tr>
</table>

Most commands will accept or even need parameters, which are placed
after the command, separated by spaces. A simple example with the "echo"
command:

<pre><code>$ <b>echo This is a test</b>
This is a test
</code></pre>

Important here is the "$" sign in front of the first line. This should
not be typed, but is a convention meaning "the rest of this line should
be typed at your shell prompt". The lines not starting with the "$"
sign are usually the feedback or output from the command.

More commands will be used in the rest of this text, and will be
explained then if necessary. If not, you can usually get more
information about a command, say the item or command "ls", by trying
either of the following:

<pre><code>$ <b>ls --help </b>
$ <b>man ls</b>
$ <b> info ls </b>
</code></pre>

(You can exit the last two "manuals" by using the "q" key.) For more
exhaustive tutorials about Linux usage, please refer to the following
sites: <http://www.linux.org/lessons/>
<http://linux.about.com/od/nwb_guide/a/gdenwb06.htm>

## How to get started with shell scripts

In a shell script, you will put the commands you would normally type at
your shell prompt in the same order. This will enable you to execute all
those commands at any time by only issuing one command: starting the
script.

Scripts are basically non-compiled pieces of code: they are just text
files. Since they don't contain machine code, they are executed by what
is called a "parser" or an "interpreter". This is another program that
understands the command in the script, and converts them to machine
code. There are many kinds of scripting languages, including Perl and
Python.

Another very common scripting language is shell scripting. In a shell
script, you will put the commands you would normally type at your shell
prompt in the same order. This will enable you to execute all those
commands at any time by only issuing one command: starting the script.

Typically in the following examples they'll have on each line the next
command to be executed although it is possible to put multiple commands
on one line. A very simple example of a script may be:

```bash
echo "Hello! This is my hostname:" 
hostname
```

You can type both lines at your shell prompt, and the result will be the
following:

<pre><code>$ <b>echo "Hello! This is my hostname:"</b>
Hello! This is my hostname:
$ <b>hostname</b>
{{loginhost}}
</code></pre>

Suppose we want to call this script "foo". You open a new file for
editing, and name it "foo", and edit it with your favourite editor

{% if site == gent %}
<pre><code>$ <b>nano foo</b>
</code></pre>
{% else %}
<pre><code>$ <b>vi foo</b>
</code></pre>
{% endif %}

or use the following commands:

<pre><code>$ <b>echo "echo Hello! This is my hostname:" > foo</b>
$ <b>echo hostname >> foo</b>
</code></pre>

The easiest ways to run a script is by starting the interpreter and pass
the script as parameter. In case of our script, the interpreter may
either be "sh" or "bash" (which are the same on the cluster). So start
the script:

<pre><code>$ <b>bash foo</b>
Hello! This is my hostname:
{{loginhost}}
</code></pre>

Congratulations, you just created and started your first shell script!

A more advanced way of executing your shell scripts is by making them
executable by their own, so without invoking the interpreter manually.
The system can not automatically detect which interpreter you want, so
you need to tell this in some way. The easiest way is by using the so
called "shebang" notation, explicitly created for this function: you put
the following line on top of your shell script
"#!/path/to/your/interpreter".

You can find this path with the "which" command. In our case, since we
use bash as an interpreter, we get the following path:

<pre><code>$ <b>which bash</b>
/bin/bash
</code></pre>

We edit our script and change it with this information:

```bash
#!/bin/bash echo \"Hello! This is my hostname:\" hostname
```

Note that the "shebang" must be the first line of your script! Now the
operating system knows which program should be started to run the
script.

Finally, we tell the operating system that this script is now
executable. For this we change its file attributes:

<pre><code>$ <b> chmod +x foo</b>
</code></pre>

Now you can start your script by simply executing it:

<pre><code>$ <b>./foo</b>
Hello! This is my hostname:
{{loginhost}}
</code></pre>

The same technique can be used for all other scripting languages, like
Perl and Python.

Most scripting languages understand that lines beginning with "#" are
comments, and should be ignored. If the language you want to use does
not ignore these lines, you may get strange results ...

## Linux Quick reference Guide

### Archive Commands

<table>
    <tr>
        <td>
          tar
        </td>
        <td>
         An archiving program designed to store and extract files from an archive known as a tar file.
        </td>
    </tr>
    <tr>
        <td>
          tar -cvf foo.tar foo/
        </td>
        <td>
         compress the contents of foo folder to foo.tar
        </td>
    </tr>
    <tr>
        <td>
          tar -xvf foo.tar
        </td>
        <td>
         extract foo.tar
        </td>
    </tr>
    <tr>
        <td>
          tar -xvzf foo.tar.gz
        </td>
        <td>
         extract gzipped foo.tar.gz
        </td>
    </tr>
</table>

### Basic Commands

<table>
    <tr>
        <td>
          ls
        </td>
        <td>
         Shows you a list of files in the current directory
        </td>
    </tr>
    <tr>
        <td>
          cd
        </td>
        <td>
         Change the current directory
        </td>
    </tr>
    <tr>
        <td>
          rm
        </td>
        <td>
         Remove file or directory
        </td>
    </tr>
    <tr>
        <td>
          mv
        </td>
        <td>
         Move file or directory
        </td>
    </tr>
    <tr>
        <td>
          echo
        </td>
        <td>
         Display a line or text
        </td>
    </tr>
    <tr>
        <td>
          pwd
        </td>
        <td>
         Print working directory
        </td>
    </tr>
    <tr>
        <td>
          mkdir
        </td>
        <td>
         Create directories
        </td>
    </tr>
    <tr>
        <td>
          rmdir
        </td>
        <td>
         Remove directories
        </td>
    </tr>
</table>


### Editor

<table>
    <tr>
        <td>
          emacs
        </td>
        <td>
          
        </td>
    </tr>
    <tr>
        <td>
          nano
        </td>
        <td>
         Nano's ANOther editor, an enhanced free Pico clone
        </td>
    </tr>
    <tr>
        <td>
          vi
        </td>
        <td>
         A programmers text editor
        </td>
    </tr>
</table>

### File Commands

<table>
    <tr>
        <td>
          cat
        </td>
        <td>
          Read one or more files and print them to standard output
        </td>
    </tr>
    <tr>
        <td>
          cmp
        </td>
        <td>
         Compare two files byte by byte
        </td>
    </tr>
    <tr>
        <td>
          cp
        </td>
        <td>
         Copy files from a source to the same or different target(s)
        </td>
    </tr>
    <tr>
        <td>
          du
        </td>
        <td>
         Estimate disk usage of each file and recursively for directories
        </td>
    </tr>
    <tr>
        <td>
          find
        </td>
        <td>
         Search for files in directory hierarchy
        </td>
    </tr>
    <tr>
        <td>
          grep
        </td>
        <td>
         Print lines matching a pattern
        </td>
    </tr>
    <tr>
        <td>
          ls
        </td>
        <td>
         List directory contents
        </td>
    </tr>
    <tr>
        <td>
          mv
        </td>
        <td>
         Move file to different targets
        </td>
    </tr>
    <tr>
        <td>
          rm
        </td>
        <td>
         Remove files
        </td>
    </tr>
    <tr>
        <td>
          sort
        </td>
        <td>
         Sort lines of text files
        </td>
    </tr>
    <tr>
        <td>
          wc
        </td>
        <td>
         Print the number of new lines, words, and bytes in files
        </td>
    </tr>
</table>

### Help Commands

<table>
    <tr>
        <td>
          man
        </td>
        <td>
         Displays the manual page of a command with its name, synopsis, description, author, copyright etc.
        </td>
    </tr>
</table>

### Network Commands

<table>
    <tr>
        <td>
          hostname
        </td>
        <td>
         show or set the system's host name
        </td>
    </tr>
    <tr>
        <td>
          ifconfig
        </td>
        <td>
         Display the current configuration of the network interface. It is also useful to get the information about IP address, subnet mask, set remote IP address, netmask etc.
        </td>
    </tr>
    <tr>
        <td>
          ping
        </td>
        <td>
         send ICMP ECHO_REQUEST to network hosts, you will get back ICMP packet if the host responds. This command is useful when you are in a doubt whether your computer is connected or not.
        </td>
    </tr>
</table>      

### Other Commands

<table>
    <tr>
        <td>
          logname
        </td>
        <td>
         Print user's login name
        </td>
    </tr>
    <tr>
        <td>
          quota
        </td>
        <td>
         Display disk usage and limits
        </td>
    </tr>
    <tr>
        <td>
          which
        </td>
        <td>
         Returns the pathnames of the files that would be executed in the current environment
        </td>
    </tr>
    <tr>
        <td>
          whoami
        </td>
        <td>
         Displays the login name of the current effective user
        </td>
    </tr>
</table>

### Process Commands

<table>
    <tr>
        <td>
          &
        </td>
        <td>
         In order to execute a command in the background, place an ampersand (&) on the command line at the end of the command. A user job number (placed in brackets) and a system process number are displayed. A system process number is the number by which the system identifies the job whereas a user job number is the number by which the user identifies the job
        </td>
    </tr>
    <tr>
        <td>
          at
        </td>
        <td>
         executes commands at a specified time
        </td>
    </tr>
    <tr>
        <td>
          bg
        </td>
        <td>
         Places a suspended job in the background
        </td>
    </tr>
    <tr>
        <td>
          crontab
        </td>
        <td>
         crontab is a file which contains the schedule of entries to run at specified times
        </td>
    </tr>
    <tr>
        <td>
          fg
        </td>
        <td>
         A process running in the background will be processed in the foreground
        </td>
    </tr>
    <tr>
        <td>
          jobs
        </td>
        <td>
         Lists the jobs being run in the background
        </td>
    </tr>
    <tr>
        <td>
          kill
        </td>
        <td>
         Cancels a job running in the background, it takes argument either the user job number or the system process number
        </td>
    </tr>
    <tr>
        <td>
          ps
        </td>
        <td>
         Reports a snapshot of the current processes
        </td>
    </tr>
    <tr>
        <td>
          top
        </td>
        <td>
         Display Linux tasks
        </td>
    </tr>
</table>


### User Account Commands


<table>
    <tr>
        <td>
          chmod
        </td>
        <td>
         Modify properties for users
        </td>
    </tr>
</table>