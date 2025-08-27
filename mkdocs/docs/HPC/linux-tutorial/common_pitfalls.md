# Common Pitfalls

This page highlights common pitfalls in Linux usage, offering insights into potential challenges users might face. 
By understanding these pitfalls, you can avoid unnecessary hurdles.

### Location

If you receive an error message which contains something like the
following:
```shell
No such file or directory
```

It probably means that you haven't placed your files in the correct
directory, or you have mistyped the file name or path.

Try and figure out the correct location using `ls`, `cd` and using the
different `$VSC_*` variables.

### Spaces

Filenames should **not** contain any spaces! If you have a long filename you
should use underscores or dashes (e.g., `very_long_filename`).
```
$ cat some file
No such file or directory 'some'
```

Spaces are permitted, however they result in surprising behaviour. To
cat the file `'some file'` as above, you can escape the space with a
backslash ("`\ `") or you can put the filename in quotes:
```
$ cat some\ file
...
$ cat "some file"
...
```

This is especially error-prone if you are piping results of `find`:
```
$ find . -type f | xargs cat
No such file or directory name ’some’
No such file or directory name ’file’
```

This can be worked around using the `-print0` flag:
```
$ find . -type f -print0 | xargs -0 cat
...
```

But, this is tedious, and you can prevent errors by simply colouring
within the lines and not using spaces in filenames.

### Missing/mistyped environment variables
If you use a command like `rm -r` with environment variables you need to
be careful to make sure that the environment variable exists. If you
mistype an environment variable then it will resolve into a blank string.
This means the following resolves to `rm -r ~/*` which will remove every
file in your home directory!
```
$ rm -r ~/$PROJETC/*
```

### Typing dangerous commands
A good habit when typing dangerous commands is to precede the line with
`#`, the comment character. This will let you type out the command
without fear of accidentally hitting enter and running something
unintended.
```
$ #rm -r ~/$POROJETC/*
```
Then you can go back to the beginning of the line (`Ctrl-A`) and remove
the first character (`Ctrl-D`) to run the command. You can also just
press enter to put the command in your history so you can come back to
it later (e.g., while you go check the spelling of your environment
variables).

{% if OS==windows %}

### Copying files with WinSCP

After copying files from a windows machine, a file might look funny when
looking at it on the cluster.
```
$ cat script.sh
#!/bin/bash^M
#PBS -l nodes^M
...
```

Or you can get errors like:
```
$ qsub fibo.pbs
qsub: script is written in DOS/Windows text format
```

See section [dos2unix](uploading_files.md#dos2unix) to fix these errors with `dos2unix`.

{% endif %}

### Permissions
```
$ ls -l script.sh # File with correct permissions
-rwxr-xr-x 1 vsc40000 vsc40000 2983 Jan 30 09:13 script.sh
$ ls -l script.sh # File with incorrect permissions
-rw-r--r-- 1 vsc40000 vsc40000 2983 Jan 30 09:13 script.sh
```

Before submitting the script, you'll need to add execute permissions to
make sure it can be executed:
```
$ chmod +x script_name.sh
```

## Help

If you stumble upon an error, don't panic! Read the error output, it
might contain a clue as to what went wrong. You can copy the error
message into Google (selecting a small part of the error without
filenames). It can help if you surround your search terms in double
quotes (for example `"No such file or directory"`), that way Google will
consider the error as one thing, and won't show results just containing
these words in random order.

If you need help about a certain command, you should consult its so-called "man page":
```
$ man command
```

This will open the manual of this command. This manual contains detailed
explanation of all the options the command has. Exiting the manual is
done by pressing 'q'.

**Don't be afraid to contact <{{hpcinfo}}>. They are here to help and will do so for even the 
smallest of problems!**

# More information

1.  [Unix Power Tools - A **fantastic ** book about most of these
    tools](https://web.archive.org/web/20081219192620/http://docstore.mik.ua/orelly/unix/upt/index.htm) 

2.  <https://linuxcommand.org/>: A great place to start with many
    examples. There is an associated book which gets a lot of good
    reviews

3.  [The Linux Documentation Project](https://www.tldp.org/guides.html): More guides on various topics relating to the Linux command line

4.  [basic shell
    usage](https://linuxcommand.org/lc3_learning_the_shell.php)

5.  [Bash for
    beginners](https://www.tldp.org/LDP/Bash-Beginners-Guide/html/Bash-Beginners-Guide.html)

6.  [MOOC](https://www.edx.org/learn/linux/the-linux-foundation-introduction-to-linux)

Please don't hesitate to contact in case of questions or problems.
