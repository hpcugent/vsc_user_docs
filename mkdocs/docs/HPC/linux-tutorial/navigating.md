# Navigating

In its most basic form, the linux file system consists of directories and files. 
A directory can contain multiple files and subdirectories. 
In Linux, the current and parent directory are respectively denoted by `.` and `..`.

This chapter serves as a guide to navigating within a Linux shell.

## The current directory

To print the current directory, use the `pwd` (**p**rint **w**orking **d**irectory) command:

```bash
$ pwd
/user/home/gent/vsc400/{{ userid }}
```

`pwd` prints the working directory starting from the root directory (denoted by `/`). 
The root directory is the top-level directory in the filesystem hierarchy. 
After that, each directory is separated by a `/`.

## Absolute vs relative file paths

An *absolute* filepath starts with `/`, the *root* of the filesystem.

!!! example
    absolute path to your home directory: `/user/home/gent/vsc400/vsc40000`.

A *relative* path starts from the current directory, and points to
another location up or down the filesystem hierarchy.

!!! example
    `some_directory/one.txt` points to the file `one.txt` that is
    located in the subdirectory named `some_directory` of the current
    directory.

    `../file.txt` points to the file `file.txt` that is located in the
    parent directory of the current directory.


## Listing files and directories: "ls"

A very basic and commonly used command is `ls`, which can be
used to list files and directories.

In its basic usage, it just prints the names of files and directories
in the current directory. For example:
```bash
$ ls
afile.txt some_directory
```

When provided an argument, it can be used to list the contents of a directory:
```bash
$ ls some_directory
one.txt two.txt
```

In Linux, the semantics of commands can often be customized by adding *options* (or *flags*). 
Options are usually preceded by a `-` character.

Some common options for `ls` are:

-   detailed listing using `ls -l`:
    ```
    $ ls -l
    total 4224
    -rw-rw-r-- 1 vsc40000 vsc40000 2157404 Apr 12 13:17 afile.txt
    drwxrwxr-x 2 vsc40000 vsc40000 512 Apr 12 12:51 some_directory
    ```

-   printing the size information in human-readable form, using the `-h` flag:
    ```
    $ ls -lh
    total 4.1M
    -rw-rw-r-- 1 vsc40000 vsc40000 2.1M Apr 12 13:16 afile.txt
    drwxrwxr-x 2 vsc40000 vsc40000 512 Apr 12 12:51 some_directory
    ``` 

-   listing hidden files using the `-a` flag:

    ```
    $ ls -lah
    total 3.9M
    drwxrwxr-x 3 vsc40000 vsc40000 512 Apr 12 13:11 .
    drwx------ 188 vsc40000 vsc40000 128K Apr 12 12:41 ..
    -rw-rw-r-- 1 vsc40000 vsc40000 1.8M Apr 12 13:12 afile.txt
    -rw-rw-r-- 1 vsc40000 vsc40000 0 Apr 12 13:11 .hidden_file.txt
    drwxrwxr-x 2 vsc40000 vsc40000 512 Apr 12 12:51 some_directory
    ```
    
    !!! info
        In Linux, files and directories starting with a `.` are considered hidden files.

-   ordering files by the most recent change using `-t`:

    ```
    $ ls -lth
    total 4.0M
    -rw-rw-r-- 1 vsc40000 vsc40000 2.0M Apr 12 13:15 afile.txt
    drwxrwxr-x 2 vsc40000 vsc40000 512 Apr 12 12:51 some_directory
    ```

If you try to use `ls` on a file that doesn't exist, you will get a clear error message:

```bash
$ ls nosuchfile
ls: cannot access nosuchfile: No such file or directory
```

## Changing directory: "cd"

To change to a different directory, you can use the `cd` command:

```bash
$ cd some_directory
```

To change back to the previous directory you were in, use the shortcut: `cd -`

Using `cd` without an argument results in returning back to your home
directory:

```bash
$ cd
$ pwd
/user/home/gent/vsc400/vsc40000
```

## Inspecting files


The `file` command can be used to inspect what type of file you're dealing with:

```
$ file afile.txt
afile.txt: ASCII text

$ file some_directory 
some_directory: directory
```

## Finding files/directories: "find"

`find` will crawl a series of directories and lists files
matching given criteria.

For example, to look for the file named `one.txt` in the current directory and its subdirectories:

```
$ cd $HOME
find . -name one.txt
./some_directory/one.txt
```

To look for files using incomplete names, you can use a wildcard `*`;
note that you need to escape the `*` to avoid that Bash *expands* it
into `afile.txt` by adding double quotes:

```
$ find . -name "*.txt"
./.hidden_file.txt
./afile.txt
./some_directory/one.txt
./some_directory/two.txt
```

For more advanced uses of the `find` command, use `man find` to display its **man**ual.

## Exercises

??? abstract "Go to `/tmp`, then back to your home directory. How many different ways to do this can you come up with?"
    
    Some ways to go from the home directory to `/tmp` and back are:

    1. Using the `cd -` shortcut:
        ```bash
        $ cd /tmp
        $ cd -
        ```    

    2.  Using absolute paths:
        ```bash
        $ cd /tmp
        $ cd /user/home/gent/vsc400/vsc40000
        ```

    3. Using the `~` shortcut:
        ```bash
        $ cd /tmp
        $ cd ~
        ```

    4. Using variable expansion:
        ```bash
        $ cd /tmp
        $ cd $HOME
        ```
    
??? abstract "When was your home directory last changed?"
    
    To find out when your home directory was last changed, you can use the `ls` command,
    along with the `-l` flag to get a detailed listing and the `-a` flag to list hidden files:
    ```
    $ ls -al ~
    total 3.9M
    drwxrwxr-x 3 vsc40000 vsc40000 512 Apr 12 13:11 .
    ...
    ```

    Here, `.` denotes the home directory. The directory was last changed on April 12th at 13:11.


??? abstract "What is the name of the last changed file in `/tmp`?"
    
    The output of the `ls -lt /tmp` command will sort the files in `/tmp` by the time of last change. 
    Check the first letter of the line to determine if it is a file (`-`) or a directory (`d`).
    The first line with `-` is the last changed file in `/tmp`.

The [next](manipulating_files_and_directories.md) chapter will teach
you how to interact with files and directories.
