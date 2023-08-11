# Uploading/downloading/editing files


## Uploading/downloading files
[//]: # (sec:uploading-files)

To transfer files from and to the HPC, see 
[the section about transferring files of the
HPC manual](https://docs.hpc.ugent.be/connecting/#transfer-files-tofrom-the-hpc)

### `dos2unix`
[//]: # (subsec:dos2unix)

After uploading files from Windows, you may experience some problems due to the difference
in line endings between Windows (*carriage return* + *line feed*) and Linux (*line feed* only),
see also <https://kuantingchen04.github.io/line-endings/>.

For example, you may see an error when submitting a job script that was edited on Windows:

```
sbatch: error: Batch script contains DOS line breaks (\r\n)
sbatch: error: instead of expected UNIX line breaks (\n).
```

To fix this problem, you should run the ``dos2unix`` command on the file:

<pre><code>$ <b>dos2unix filename</b>
</code></pre>

## Symlinks for data/scratch
[//]: # (sec:symlink-for-data)


As we end up in the home directory when connecting, it would be
convenient if we could access our data and VO storage. To facilitate
this we will create symlinks to them in our home directory. 
This will create 4 symbolic links {% if OS == windows %}
(they're like "shortcuts" on your desktop and they look like directories in WinSCP)
{% else %}
(they're like "shortcuts" on your desktop)
{% endif %} pointing to the respective storages:

<pre><code>$ <b>cd $HOME</b>
$ <b>ln -s $VSC_SCRATCH scratch</b>
$ <b>ln -s $VSC_DATA data</b>
$ <b>ls -l scratch data</b>
lrwxrwxrwx 1 vsc40000 vsc40000 31 Mar 27 2009 data ->
    /user/data/gent/vsc400/vsc40000
lrwxrwxrwx 1 vsc40000 vsc40000 34 Jun 5 2012 scratch ->
    /user/scratch/gent/vsc400/vsc40000
</code></pre>
 


##  Editing with `nano`

Nano is the simplest editor available on Linux. To open Nano, just type
`nano`. To edit a file, you use `nano the_file_to_edit.txt`. You will be
presented with the contents of the file and a menu at the bottom with
commands like `^O Write Out` The `^` is the Control key. So `^O` means
`Ctrl-O`. The main commands are:

1.  Open ("Read"): `^R`

2.  Save ("Write Out"): `^O`

3.  Exit: `^X`

More advanced editors (beyond the scope of this page) are `vim` and
`emacs`. A simple tutorial on how to get started with `vim` can be found
at <https://www.openvim.com/>.

## Copying faster with `rsync`
[//]: # (sec:rsync)

`rsync` is a fast and versatile copying tool. It can be much faster than
`scp` when copying large datasets. It's famous for its "delta-transfer
algorithm", which reduces the amount of data sent over the network by
only sending the differences between files.

You will need to run `rsync` from a computer where it is installed.
Installing `rsync` is the easiest on Linux: it comes pre-installed with
a lot of distributions.

For example, to copy a folder with lots of CSV files:
<pre><code>$ <b>rsync -rzv testfolder vsc40000@login.hpc.ugent.be:data/</b></code></pre>

will copy the folder `testfolder` and its contents to `$VSC_DATA` on the
, assuming the `data` symlink is present in your home directory, see 
[symlinks section](uploading_files.md#symlinks-for-datascratch).

The `-r` flag means "recursively", the `-z` flag means that compression
is enabled (this is especially handy when dealing with CSV files because
they compress well) and the `-v` enables more verbosity (more details
about what's going on).

To copy large files using `rsync`, you can use the `-P` flag: it enables
both showing of progress and resuming partially downloaded files.

To copy files from the to your local computer, you can also use `rsync`:
<pre><code>$ <b>rsync -rzv vsc40000@login.hpc.ugent.be:data/bioset local_folder</b></code></pre>
This will copy the folder `bioset` and its contents that on `$VSC_DATA`
of the to a local folder named `local_folder`.

See `man rsync` or <https://linux.die.net/man/1/rsync> for more
information about rsync.

## Exercises
1.  Download the file `/etc/hostname` to your local computer.

2.  Upload a file to a subdirectory of your personal `$VSC_DATA` space.

3.  Create a file named `hello.txt` and edit it using `nano`.

Now you have a basic understanding, see next [chapter](beyond_the_basics.md) for some more in depth concepts.
