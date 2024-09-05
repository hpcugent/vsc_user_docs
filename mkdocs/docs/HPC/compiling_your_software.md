{% set exampledir="examples/Compiling-and-testing-your-software-on-the-HPC" %}
# Compiling and testing your software on the HPC

All nodes in the {{hpc}} cluster are running the "{{operatingsystem}}" 
Operating system, which is a specific version of {{operatingsystembase}}. This means that all the 
software programs
(executable) that the end-user wants to run on the {{hpc}} first must be
compiled for {{operatingsystem}}. It also means that you first have to install all the
required external software packages on the {{hpc}}.

Most commonly used compilers are already pre-installed on the {{hpc}} and can be
used straight away. Also, many popular external software packages, which
are regularly used in the scientific community, are also pre-installed.

## Check the pre-installed software on the {{hpc}}

In order to check all the available modules and their version numbers,
which are pre-installed on the {{hpc}} enter:
{% include "sites/available_modules.md" %}


When your required application is not available on the {{hpc}} please contact
any {{hpc}} member. Be aware of potential "License Costs". "Open Source"
software is often preferred.

## Porting your code

To **port** a software-program is to translate it from the operating system in
which it was developed (e.g., Windows 7) to another operating system
(e.g., {{operatingsystembase}} on our {{hpc}}) so that it can be used there. Porting implies some
degree of effort, but not nearly as much as redeveloping the program in
the new environment. It all depends on how "portable" you wrote your
code.

In the simplest case the file or files may simply be copied from one
machine to the other. However, in many cases the software is installed
on a computer in a way, which depends upon its detailed hardware,
software, and setup, with device drivers for particular devices, using
installed operating system and supporting software components, and using
different directories.

In some cases software, usually described as "portable software" is
specifically designed to run on different computers with compatible
operating systems and processors without any machine-dependent
installation; it is sufficient to transfer specified directories and
their contents. Hardware- and software-specific information is often
stored in configuration files in specified locations (e.g., the registry
on machines running MS Windows).

Software, which is not portable in this sense, will have to be
transferred with modifications to support the environment on the
destination machine.

Whilst programming, it would be wise to stick to certain standards
(e.g., ISO/ANSI/POSIX). This will ease the porting of your code to other
platforms.

Porting your code to the {{operatingsystem}} platform is the responsibility of the end-user.

## Compiling and building on the {{hpc}}

Compiling refers to the process of translating code written in some
programming language, e.g., Fortran, C, or C++, to machine code.
Building is similar, but includes gluing together the machine code
resulting from different source files into an executable (or library).
The text below guides you through some basic problems typical for small
software projects. For larger projects it is more appropriate to use
makefiles or even an advanced build system like CMake.

All the {{hpc}} nodes run the same version of the Operating System, i.e. {{operatingsystem}}. So,
it is sufficient to compile your program on any compute node. Once you
have generated an executable with your compiler, this executable should
be able to run on any other compute-node.

A typical process looks like:

1.  Copy your software to the login-node of the {{hpc}}

2.  Start an interactive session on a compute node;

3.  Compile it;

4.  Test it locally;

5.  Generate your job scripts;

6.  Test it on the {{hpc}}

7.  Run it (in parallel);

We assume you've copied your software to the {{hpc}}. The next step is to request
your private compute node.

```bash
$ qsub -I
qsub: waiting for job {{jobid}} to start
```


### Compiling a sequential program in C

Go to the examples for chapter 
[Compiling and testing your software on the HPC](compiling_your_software.md#compiling-and-building-on-the-hpc) and load the 
foss module:
```
cd ~/{{exampledir}}
module load foss
```

We now list the directory and explore the contents of the "*hello.c*"
program:
```
$ ls -l
total 512
-rw-r--r-- 1 {{userid}} 214 Sep 16 09:42 hello.c
-rw-r--r-- 1 {{userid}} 130 Sep 16 11:39 hello.pbs*
-rw-r--r-- 1 {{userid}} 359 Sep 16 13:55 mpihello.c
-rw-r--r-- 1 {{userid}} 304 Sep 16 13:55 mpihello.pbs
```

```shell title="hello.c"
{% include "examples/Compiling-and-testing-your-software-on-the-HPC/hello.c" %}
```

The "hello.c" program is a simple source file, written in C. It'll print
500 times "Hello #&lt;num&gt;", and waits one second between 2 printouts.

We first need to compile this C-file into an executable with the
gcc-compiler.

First, check the command line options for *"gcc" (GNU C-Compiler)*, then
we compile. the `O2` option enables a moderate level of optimization when compiling the code. 
It instructs the compiler to optimize the code for better performance without significantly increasing compilation time.
Finally, list the contents of the directory again:
```
$ gcc -help
$ gcc -O2 -o hello hello.c
$ ls -l
total 512
-rwxrwxr-x 1 {{userid}} 7116 Sep 16 11:43 hello*
-rw-r--r-- 1 {{userid}}  214 Sep 16 09:42 hello.c
-rwxr-xr-x 1 {{userid}}  130 Sep 16 11:39 hello.pbs*
```

A new file "hello" has been created. Note that this file has "execute"
rights, i.e., it is an executable. More often than not, calling gcc --
or any other compiler for that matter -- will provide you with a list of
errors and warnings referring to mistakes the programmer made, such as
typos, syntax errors. You will have to correct them first in order to
make the code compile. Warnings pinpoint less crucial issues that may
relate to performance problems, using unsafe or obsolete language
features, etc. It is good practice to remove all warnings from a
compilation process, even if they seem unimportant so that a code change
that produces a warning does not go unnoticed.

Let's test this program on the local compute node, which is at your
disposal after the `qsub --I` command:
```
$ ./hello
Hello #0
Hello #1
Hello #2
Hello #3
Hello #4
...
```

It seems to work, now run it on the {{hpc}}
```
qsub hello.pbs
```

### Compiling a parallel program in C/MPI
```
cd ~/{{exampledir}}
```

List the directory and explore the contents of the "*mpihello.c*"
program:
```
$ ls -l
total 512
total 512
-rw-r--r-- 1 {{userid}} 214 Sep 16 09:42 hello.c
-rw-r--r-- 1 {{userid}} 130 Sep 16 11:39 hello.pbs*
-rw-r--r-- 1 {{userid}} 359 Sep 16 13:55 mpihello.c
-rw-r--r-- 1 {{userid}} 304 Sep 16 13:55 mpihello.pbs
```

```shell title="mpihello.c"
{% include "examples/Compiling-and-testing-your-software-on-the-HPC/mpihello.c" %}
```

The "mpi_hello.c" program is a simple source file, written in C with MPI
library calls.

Then, check the command line options for *"mpicc" (GNU C-Compiler with
MPI extensions)*, then we compile and list the contents of the directory
again:

```
mpicc --help
mpicc -o mpihello mpihello.c
ls -l
```

A new file "hello" has been created. Note that this program has
"execute" rights.

Let's test this program on the "login" node first:

```
$ ./mpihello
Hello World from Node 0.
```

It seems to work, now run it on the {{hpc}}.

```
qsub mpihello.pbs
```

### Compiling a parallel program in Intel Parallel Studio Cluster Edition

We will now compile the same program, but using the Intel Parallel
Studio Cluster Edition compilers. We stay in the examples directory for
this chapter:

```
cd ~/{{exampledir}}
```


We will compile this C/MPI -file into an executable with the Intel
Parallel Studio Cluster Edition. First, clear the modules (purge) and
then load the latest "intel" module:

```
module purge
module load intel
```

Then, compile and list the contents of the directory again. The Intel
equivalent of mpicc is mpiicc.
```
mpiicc -o mpihello mpihello.c
ls -l
```

Note that the old "mpihello" file has been overwritten. Let's test this
program on the "login" node first:
```
$ ./mpihello
Hello World from Node 0.
```

It seems to work, now run it on the {{hpc}}.

```
qsub mpihello.pbs
```

Note: The {{association}} only has a license for the Intel Parallel Studio Cluster
Edition for a fixed number of users. As such, it might happen that you
have to wait a few minutes before a floating license becomes available
for your use.

Note: The Intel Parallel Studio Cluster Edition contains equivalent
compilers for all GNU compilers. Hereafter the overview for C, C++ and
Fortran compilers.

|             | **Sequential Program** |           | **Parallel Program (with MPI)** |           |
|-------------|------------------------|-----------|---------------------------------|-----------|
|             | **GNU**                | **Intel** | **GNU**                         | **Intel** |
| **C**       | gcc                    | icc       | mpicc                           | mpiicc    |
| **C++**     | g++                    | icpc      | mpicxx                          | mpiicpc   |
| **Fortran** | gfortran               | ifort     | mpif90                          | mpiifort  |
