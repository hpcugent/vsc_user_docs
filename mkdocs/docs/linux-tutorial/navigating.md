Navigating
==========

Current directory: "pwd" and "\$PWD"
------------------------------------

To print the current directory, use `pwd` or `$PWD`:
<pre><code>$ <b>cd $HOME</b>
$ <b>pwd</b>
/user/home/gent/vsc400/vsc40000
$ <b>echo "The current directory is: $PWD"</b>
The current directory is: /user/home/gent/vsc400/vsc40000
</code></pre>

Listing files and directories: "ls"
-----------------------------------

A very basic and commonly used command is `ls`, which can be used to
list files and directories.

In it's basic usage, it just prints the names of files and directories
in the current directory. For example:
<pre><code>$ <b>ls</b>
afile.txt some_directory
</code></pre>

When provided an argument, it can be used to list the contents of a
directory:
<pre><code>$ <b>ls some_directory</b>
one.txt two.txt
</code></pre>


A couple of commonly used options include:

-   detailed listing using `ls -l`:
    <pre><code>$ <b>ls -l</b>
total 4224
-rw-rw-r-- 1 vsc40000 vsc40000 2157404 Apr 12 13:17 afile.txt
drwxrwxr-x 2 vsc40000 vsc40000 512 Apr 12 12:51 some_directory</code></pre>

-   To print the size information in human-readable form, use the `-h`
    flag:
    <pre><code>$ <b>ls -lh</b>
total 4.1M
-rw-rw-r-- 1 vsc40000 vsc40000 2.1M Apr 12 13:16 afile.txt
drwxrwxr-x 2 vsc40000 vsc40000 512 Apr 12 12:51 some_directory</code></pre>

-   also listing hidden files using the `-a` flag:

    <pre><code>$ <b>ls -lah</b>
total 3.9M
drwxrwxr-x 3 vsc40000 vsc40000 512 Apr 12 13:11 .
drwx------ 188 vsc40000 vsc40000 128K Apr 12 12:41 ..
-rw-rw-r-- 1 vsc40000 vsc40000 1.8M Apr 12 13:12 afile.txt
-rw-rw-r-- 1 vsc40000 vsc40000 0 Apr 12 13:11 .hidden_file.txt
drwxrwxr-x 2 vsc40000 vsc40000 512 Apr 12 12:51 some_directory</code></pre>

-   ordering files by the most recent change using `-rt`:

    <pre><code>$ <b>ls -lrth</b>
total 4.0M
drwxrwxr-x 2 vsc40000 vsc40000 512 Apr 12 12:51 some_directory
-rw-rw-r-- 1 vsc40000 vsc40000 2.0M Apr 12 13:15 afile.txt</code></pre>

If you try to use `ls` on a file that doesn't exist, you will get a
clear error message:
<pre><code>$ <b>ls nosuchfile</b>
ls: cannot access nosuchfile: No such file or directory
</code></pre>

Changing directory: "cd"
------------------------

To change to a different directory, you can use the `cd` command:
<pre><code>$ <b>cd some_directory</b></code></pre>
To change back to the previous directory you were in, there's a
shortcut: `cd -`

Using `cd` without an argument results in returning back to your home
directory:
<pre><code>$ <b>cd</b>
$<b> pwd</b>
/user/home/gent/vsc400/vsc40000
</code></pre>


Inspecting file type: "file"
----------------------------

The `file` command can be used to inspect what type of file you're
dealing with:
<pre><code>$ <b>file afile.txt</b>
afile.txt: ASCII text

$ <b>file some_directory</b>
some_directory: directory
</code></pre>

Absolute vs relative file paths
-------------------------------

An *absolute* filepath starts with `/` (or a variable which value starts
with `/`), which is also called the *root* of the filesystem.

Example: absolute path to your home directory: `/user/home/gent/vsc400/vsc40000`.

A *relative* path starts from the current directory, and points to
another location up or down the filesystem hierarchy.

Example: `some_directory/one.txt` points to the file `one.txt` that is
located in the subdirectory named `some_directory` of the current
directory.

There are two special relative paths worth mentioning:

-   `.` is a shorthand for the current directory

-   `..` is a shorthand for the parent of the current directory

You can also use `..` when constructing relative paths, for example:
<pre><code>$ <b>cd $HOME/some_directory</b>
$ <b>ls ../afile.txt</b>
../afile.txt
</code></pre>

Permissions
-----------

[//]: # (sec:permissions)

Each file and directory has particular *permissions* set on it, which
can be queried using `ls -l`.

For example:
<pre><code>$ <b>ls -l afile.txt</b>
-rw-rw-r-- 1 vsc40000 agroup 2929176 Apr 12 13:29 afile.txt
</code></pre>

The `-rwxrw-r--` specifies both the type of file (`-` for files, `d` for
directories (see first character)), and the permissions for
user/group/others:

1.  each triple of characters indicates whether the read (`r`), write
    (`w`), execute (`x`) permission bits are set or not

2.  the 1st part `rwx` indicates that the *owner* "vsc40000" of the file has all
    the rights

3.  the 2nd part `rw-` indicates the members of the *group* "agroup"
    only have read/write permissions (not execute)

4.  the 3rd part `r--` indicates that *other* users only have read
    permissions

The default permission settings for new files/directories are determined
by the so-called *umask* setting, and are by default:

1.  read-write permission on files for user/group (no execute),
    read-only for others (no write/execute)

2.  read-write-execute permission for directories on user/group,
    read/execute-only for others (no write)

See also [the chmod command](manipulating_files_and_directories.md#changing-permissions---chmod--sec--chmod) 
later in this manual.

Finding files/directories: "find"
---------------------------------

`find` will crawl a series of directories and lists files matching given
criteria.

For example, to look for the file named `one.txt`:
<pre><code>$ <b>cd $HOME</b>
$ <b>find . -name one.txt</b>
./some_directory/one.txt
</code></pre>

To look for files using incomplete names, you can use a wildcard `*`;
note that you need to escape the `*` to avoid that Bash *expands* it
into `afile.txt` by adding double quotes:
<pre><code>$ <b>find . -name "*.txt"</b>
./.hidden_file.txt
./afile.txt
./some_directory/one.txt
./some_directory/two.txt
</code></pre>

A more advanced use of the `find` command is to use the `-exec` flag to
perform actions on the found file(s), rather than just printing their
paths (see `man find`).

Exercises
---------

-   Go to `/tmp`, then back to your home directory. How many different
    ways to do this can you come up with?

-   When was your home directory created or last changed?

-   Determine the name of the last changed file in `/tmp`.

-   See how home directories are organised. Can you access the home
    directory of other users?
