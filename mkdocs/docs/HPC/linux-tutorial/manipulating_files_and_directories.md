# Manipulating files and directories

Being able to manage your data is an important part of using the HPC
infrastructure. The bread and butter commands for doing this are
mentioned here. It might seem annoyingly terse at first, but with
practice you will realise that it's very practical to have such common
commands short to type.

## File contents: "cat", "head", "tail", "less", "more"

To print the contents of an entire file, you can use `cat`; to only see
the first or last N lines, you can use `head` or `tail`:
<pre><code>$ <b>cat one.txt</b>
1
2
3
4
5

$ <b>head -2 one.txt</b>
1
2

$ <b>tail -2 one.txt</b>
4
5
</code></pre>

To check the contents of long text files, you can use the `less` or
`more` commands which support scrolling with "&lt;up&gt;", "&lt;down&gt;",
"&lt;space&gt;", etc.

## Copying files: "cp"

<pre><code>$ <b>cp source target</b>
</code></pre>

This is the `cp` command, which copies a file from source to target. To
copy a directory, we use the `-r` option:
<pre><code>$ <b>cp -r sourceDirectory target</b>
</code></pre>

A last more complicated example:
<pre><code>$ <b>cp -a sourceDirectory target</b>
</code></pre>

Here we used the same `cp` command, but instead we gave it the `-a`
option which tells cp to copy all the files and keep timestamps and
permissions.

## Creating directories: "mkdir"

<pre><code>$ <b>mkdir directory</b>
</code></pre>

which will create a directory with the given name inside the current
directory.

## Renaming/moving files: "mv"

<pre><code>$ <b>mv source target</b>
</code></pre>

`mv` will move the source path to the destination path. Works for both
directories as files.

## Removing files: "rm"

<pre><code>$ <b>rm filename</b>
</code></pre>
`rm` will remove a file or directory. (`rm -rf directory` will remove every file inside a given directory).

!!! danger
    There are NO backups, there is no 'trash bin'. If you remove files/directories, they are gone.

## Permissions

Each file and directory has particular *permissions* set on it, which
can be queried using `ls -l`.

For example:

```
$ ls -l afile.txt
-rwxrw-r-- 1 vsc40000 agroup 2929176 Apr 12 13:29 afile.sh
```

Here, the output `-rwxrw-r--` indicates the permissions of the file. It can be broken down into 4 parts:

| type                               | permissions user              | permissions group     | permissions others |
|------------------------------------|-------------------------------|-----------------------|--------------------|
| `-`: is a file (`d` for directory) | `rwx`: can read/write/execute | `rw-`: can read/write | `r--`: can read    |

In this example, the file `afile.sh` is a regular file, and the owner `vsc40000` has read/write/execute permissions, 
users in the group `agroup` have read/write permissions, 
and all others only have read permissions.

The default permission settings for new files/directories are determined
by the so-called *umask* setting, and are by default `rw-rw-r--` for files and `rwxrwxr-x` for directories.

## Changing permissions: "chmod"

<pre><code>$ <b>ls -l</b>
total 1
-rw-r--r--. 1 vsc40000 mygroup 4283648 Apr 12 15:13 articleTable.csv
drwxr-x---. 2 vsc40000 mygroup 40 Apr 12 15:00 Project_GoldenDragon
</code></pre>

We use `chmod` to change the modifiers to the directory to
let people in the group write to the directory:
<pre><code>$ <b>chmod g+w Project_GoldenDragon</b>
$ <b>ls -l</b>
total 1
-rw-r--r--. 1 vsc40000 mygroup 4283648 Apr 12 15:13 articleTable.csv
drwxrwx---. 2 vsc40000 mygroup 40 Apr 12 15:00 Project_GoldenDragon
</code></pre>

The syntax used here is `g+x` which means group was given write
permission. To revoke it again, we use `g-w`. The other roles are `u`
for user and `o` for other.

You can put multiple changes on the same line:
`chmod o-rwx,g-rxw,u+rx,u-w somefile` will take everyone's permission
away except the user's ability to read or execute the file.

You can also use the `-R` flag to affect all the files within a
directory, but this is dangerous. It's best to refine your search using
`find` and then pass the resulting list to `chmod` since it's not usual
for all files in a directory structure to have the same permissions.

### Access control lists (ACLs)

However, this means that all users in `mygroup` can add or remove files.
This could be problematic if you only wanted one person to be allowed to
help you administer the files in the project. We need a new group. To do
this in the HPC environment, we need to use access control lists (ACLs):
<pre><code>$ <b>setfacl -m u:otheruser:w Project_GoldenDragon</b>
$ <b>ls -l Project_GoldenDragon</b>
drwxr-x---+ 2 vsc40000 mygroup 40 Apr 12 15:00 Project_GoldenDragon
</code></pre>

This will give the **u**ser `otheruser` permissions to **w**rite to
`Project_GoldenDragon`

Now there is a `+` at the end of the line. This means there is an ACL
attached to the directory. `getfacl Project_GoldenDragon` will print the
ACLs for the directory.

Note: most people don't use ACLs, but it's sometimes the right thing and
you should be aware it exists.

See <https://linux.die.net/man/1/setfacl> for more information.

## Zipping: "gzip"/"gunzip", "zip"/"unzip"

Files should usually be stored in a compressed file if they're not being
used frequently. This means they will use less space and thus you get
more out of your quota. Some types of files (e.g., CSV files with a lot
of numbers) compress as much as 9:1. The most commonly used compression
format on Linux is gzip. To compress a file using gzip, we use:
<pre><code>$ <b>ls -lh myfile</b>
-rw-r--r--. 1 vsc40000 vsc40000 4.1M Dec 2 11:14 myfile
$ <b>gzip myfile</b>
$ <b>ls -lh myfile.gz</b>
-rw-r--r--. 1 vsc40000 vsc40000 1.1M Dec 2 11:14 myfile.gz
</code></pre>

!!! note 
    If you zip a file, the original file will be removed. If you unzip
    a file, the compressed file will be removed. To keep both, we send the
    data to `stdout` and redirect it to the target file:
    <pre><code>$ <b>gzip -c myfile > myfile.gz</b>
    $ <b>gunzip -c myfile.gz > myfile</b>
    </code></pre>

### "zip" and "unzip"

Windows and macOS seem to favour the zip file format, so it's also
important to know how to unpack those. We do this using unzip:
<pre><code>$ <b>unzip myfile.zip</b>
</code></pre>

If we would like to make our own zip archive, we use zip:
<pre><code>$ <b>zip myfiles.zip myfile1 myfile2 myfile3</b>
</code></pre>

## Working with tarballs: "tar"

Tar stands for "tape archive" and is a way to bundle files together in a
bigger file.

You will normally want to unpack these files more often than you make
them. To unpack a `.tar` file you use:
<pre><code>$ <b>tar -xf tarfile.tar</b>
</code></pre>

Often, you will find `gzip` compressed `.tar` files on the web. These
are called tarballs. You can recognize them by the filename ending in
`.tar.gz`. You can uncompress these using `gunzip` and then unpacking
them using `tar`. But `tar` knows how to open them using the `-z`
option:
<pre><code>$ <b>tar -zxf tarfile.tar.gz</b>
$ <b>tar -zxf tarfile.tgz</b>
</code></pre>

### Order of arguments

Note: Archive programs like `zip`, `tar`, and `jar` use arguments in the
"opposite direction" of copy commands.
<pre><code># cp, ln: &lt;source(s)&gt; &lt;target&gt;
$ <b>cp source1 source2 source3 target</b>
$ <b>ln -s source target</b>

# zip, tar: &lt;target&gt; &lt;source(s)&gt;
$ <b>zip zipfile.zip source1 source2 source3</b>
$ <b>tar -cf tarfile.tar source1 source2 source3</b>
</code></pre>


If you use `tar` with the source files first then the first file will be
overwritten. You can control the order of arguments of `tar` if it helps
you remember:

<pre><code>$ <b>tar -c source1 source2 source3 -f tarfile.tar</b></code></pre>

## Exercises


??? abstract "Create a subdirectory in your home directory named `test` containing a single, empty file named `one.txt`."
    ```bash
    mkdir ~/test
    touch ~/test/one.txt
    ```

??? abstract "Copy `/etc/hostname` into the `test` directory and then check what's in it. Rename the file to `hostname.txt`."
    ```bash
    cp /etc/hostname ~/test/
    cat ~/test/hostname
    mv ~/test/hostname ~/test/hostname.txt
    ```

??? abstract "Make a new directory named `another` and copy the entire `test` directory to it. `another/test/one.txt` should then be an empty file."
    ```bash
    mkdir ~/another
    cp -r ~/test ~/another/
    ```

??? abstract "Remove the `another/test` directory with a single command."
    ```bash
    rm -r ~/another/test
    ```

??? abstract "Rename `test` to `test2`. Move `test2/hostname.txt` to your home directory."
    ```bash
    mv ~/test ~/test2
    mv ~/test2/hostname.txt ~/
    ```

??? abstract "Change the permission of `test2` so only you can access it."
    ```bash
    chmod u+rwx ~/test2  # Add read, write, and execute permissions for the user (owner)
    chmod go-rwx ~/test2  # Remove read, write, and execute permissions for the group and others
    ```

??? abstract "Create an empty job script named `job.sh`, and make it executable."
    ```bash
    touch ~/job.sh
    chmod +x ~/job.sh
    ```

??? abstract "gzip `hostname.txt`, see how much smaller it becomes, then unzip it again."
    ```bash
    gzip ~/hostname.txt
    ls -lh ~/hostname.txt.gz
    gunzip ~/hostname.txt.gz
    ```

The next [chapter](uploading_files.md) is on uploading files, especially important when using HPC-infrastructure.
