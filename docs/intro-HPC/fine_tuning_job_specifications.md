# Fine-tuning Job Specifications
[//]: # (ch:fine-tuning-job-specifications)

As {{hpc}} system administrators, we often observe that the {{hpc}} resources are not
optimally (or wisely) used. For example, we regularly notice that
several cores on a computing node are not utilised, due to the fact that
one sequential program uses only one core on the node. Or users run I/O
intensive applications on nodes with "slow" network connections.

Users often tend to run their jobs without specifying specific PBS Job
parameters. As such, their job will automatically use the default
parameters, which are not necessarily (or rarely) the optimal ones. This
can slow down the run time of your application, but also block {{hpc}} resources
for other users.

Specifying the "optimal" Job Parameters requires some knowledge of your
application (e.g., how many parallel threads does my application uses,
is there a lot of inter-process communication, how much memory does my
application need) and also some knowledge about the {{hpc}} infrastructure
(e.g., what kind of multi-core processors are available, which nodes
have InfiniBand).

There are plenty of monitoring tools on Linux available to the user,
which are useful to analyse your individual application. The {{hpc}} environment
as a whole often requires different techniques, metrics and time goals,
which are not discussed here. We will focus on tools that can help to
optimise your Job Specifications.

Determining the optimal computer resource specifications can be broken
down into different parts. The first is actually determining which
metrics are needed and then collecting that data from the hosts. Some of
the most commonly tracked metrics are CPU usage, memory consumption,
network bandwidth, and disk I/O stats. These provide different
indications of how well a system is performing, and may indicate where
there are potential problems or performance bottlenecks. Once the data
have actually been acquired, the second task is analysing the data and
adapting your PBS Job Specifications.

Another different task is to monitor the behaviour of an application at
run time and detect anomalies or unexpected behaviour. Linux provides a
large number of utilities to monitor the performance of its components.

This chapter shows you how to measure:

1.  Walltime
2.  Memory usage
3.  CPU usage
4.  Disk (storage) needs
5.  Network bottlenecks

First, we allocate a compute node and move to our relevant directory:
<pre><code>$ <b>qsub -I</b>
$ <b>cd ~/examples/Fine-tuning-Job-Specifications</b></code></pre>

## Specifying Walltime
[//]: # (sec:specifying-walltime-requirements)

One of the most important and also easiest parameters to measure is the
duration of your program. This information is needed to specify the
*walltime*.

The *time* utility **executes** and **times** your application. You can just add the time
command in front of your normal command line, including your command
line options. After your executable has finished, **time** writes the total time
elapsed, the time consumed by system overhead, and the time used to
execute your executable to the standard error stream. The calculated
times are reported in seconds.

Test the time command:
<pre><code>$ <b>time sleep 75</b>
real 1m15.005s
user 0m0.001s
sys 0m0.002s</code></pre>

It is a good practice to correctly estimate and specify the run time
(duration) of an application. Of course, a margin of 10% to 20% can be
taken to be on the safe side.

It is also wise to check the walltime on different compute nodes or to
select the "slowest" compute node for your walltime tests. Your estimate
should appropriate in case your application will run on the "slowest"
(oldest) compute nodes.

The walltime can be specified in a job scripts as:
<pre><code>#PBS -l walltime=3:00:00:00</code></pre>

or on the command line
<pre><code>$ <b>qsub -l walltime=3:00:00:00</b></code></pre>

It is recommended to always specify the walltime for a job.

## Specifying memory requirements
[//]: # (sec:specifying-memory-requirements)

In many situations, it is useful to monitor the amount of memory an
application is using. You need this information to determine the
characteristics of the required compute node, where that application
should run on. Estimating the amount of memory an application will use
during execution is often non-trivial, especially when one uses
third-party software.

{% if site!=gent %}
The "eat_mem" application in the HPC examples directory just consumes
and then releases memory, for the purpose of this test. It has one
parameter, the amount of gigabytes of memory which needs to be
allocated.

First compile the program on your machine and then test it for 1 GB:
<pre><code>$ <b>gcc -o eat_mem eat_mem.c</b>
$ <b>./eat_mem 1</b>
Consuming 1 gigabyte of memory.</code></pre>
{% endif %}

### Available Memory on the machine

The first point is to be aware of the available free memory in your
computer. The "*free*" command displays the total amount of free and
used physical and swap memory in the system, as well as the buffers used
by the kernel. We also use the options "-m" to see the results expressed
in Mega-Bytes and the "-t" option to get totals.
<pre><code>$ <b>free -m -t</b>
                total   used   free  shared  buffers  cached
Mem:            16049   4772  11277       0      107     161
-/+ buffers/cache:      4503  11546
Swap:           16002   4185  11816
Total:          32052   8957  23094</code></pre>

Important is to note the total amount of memory available in the machine
(i.e., 16 GB in this example) and the amount of used and free memory
(i.e., 4.7 GB is used and another 11.2 GB is free here).

It is not a good practice to use swap-space for your computational
applications. A lot of "swapping" can increase the execution time of
your application tremendously.
{% if site==gent %}
On the UGent clusters, there is no swap space available for jobs, you
can only use physical memory, even though "*free*" will show swap.
{% endif %}

### Checking the memory consumption
{% if site!=gent %}
The "Monitor" tool monitors applications in terms of memory and CPU
usage, as well as the size of temporary files. Note that currently only
single node jobs are supported, MPI support may be added in a future
release.

To start using monitor, first load the appropriate module. Then we study
the "eat_mem.c" program and compile it:
<pre><code>$ <b>module load monitor</b>
$ <b>cat eat_mem.c</b>
$ <b>gcc -o eat_mem eat_mem.c</b>
</code></pre>

Starting a program to monitor is very straightforward; you just add the
"monitor" command before the regular command line.
<pre><code>$ <b>monitor ./eat_mem 3</b>
time (s) size (kb) %mem %cpu
Consuming 3 gigabyte of memory.
5  252900 1.4 0.6
10  498592 2.9 0.3
15  743256 4.4 0.3
20  988948 5.9 0.3
25  1233612 7.4 0.3
30  1479304 8.9 0.2
35  1723968 10.4 0.2
40  1969660 11.9 0.2
45  2214324 13.4 0.2
50  2460016 14.9 0.2
55  2704680 16.4 0.2
60  2950372 17.9 0.2
65  3167280 19.2 0.2
70  3167280 19.2 0.2
75  9264  0 0.5
80  9264  0 0.4
</code></pre>

Whereby:

1.  The first column shows you the elapsed time in seconds. By default,
    all values will be displayed every 5&nbsp;seconds.
2.  The second column shows you the used memory in kb. We note that the
    memory slowly increases up to just over 3&nbsp;GB (3GB is 3,145,728&nbsp;KB),
    and is released again.
3.  The third column shows the memory utilisation, expressed in
    percentages of the full available memory. At full memory
    consumption, 19.2% of the memory was being used by our application.
    With the *"free"* command, we have previously seen that we had a
    node of 16&nbsp;GB in this example. 3&nbsp;GB is indeed more or less 19.2% of
    the full available memory.
4.  The fourth column shows you the CPU utilisation, expressed in
    percentages of a full CPU load. As there are no computations done in
    our exercise, the value remains very low (i.e.&nbsp;0.2%).

Monitor will write the CPU usage and memory consumption of simulation to
standard error.

This is the rate at which monitor samples the program's metrics. Since
monitor's output may interfere with that of the program to monitor, it
is often convenient to use a&nbsp;log file. The latter can be specified as
follows:
<pre><code>$ <b>monitor -l test1.log eat_mem 2</b>
Consuming 2 gigabyte of memory.
$ <b>cat test1.log</b></code></pre>

For long-running programs, it may be convenient to limit the output to,
e.g., the last minute of the programs' execution. Since monitor provides
metrics every 5 seconds, this implies we want to limit the output to the
last 12 values to cover a minute:
<pre><code>$ <b>monitor -l test2.log -n 12 eat_mem 4</b>
Consuming 4 gigabyte of memory.</code></pre>

Note that this option is only available when monitor writes its metrics
to a&nbsp;log file, not when standard error is used.

The interval at&nbsp;which monitor will show the metrics can be modified by
specifying delta, the sample rate:
<pre><code>$ <b>monitor -d 1 ./eat_mem</b>
Consuming 3 gigabyte of memory.</code></pre>

Monitor will now print the program's metrics every second. Note that the&nbsp;minimum delta value is 1&nbsp;second.
{% endif %}

{% if site==gent %}
To monitor the memory consumption of a running application, you can use the "*top*" or the "*htop*" command.
{% else %}
Alternative options to monitor the memory consumption are the "*top*" or the "*htop*" command.
{% endif %}

top

:   provides an ongoing look at processor activity in real time. It
    displays a listing of the most CPU-intensive tasks on the system,
    and can provide an interactive interface for manipulating processes.
    It can sort the tasks by memory usage, CPU usage and run time.

htop

:   is similar to top, but shows the CPU-utilisation for all the CPUs in
    the machine and allows to scroll the list vertically and
    horizontally to see all processes and their full command lines.

<pre><code>$ <b>top</b>
$ <b>htot</b></code></pre>

### Setting the memory parameter {: #pbs_mem }

Once you gathered a good idea of the overall memory consumption of your
application, you can define it in your job script. It is wise to foresee
a margin of about 10%.

{% if site==gent %}
The maximum amount of physical memory used by the job per node can be
specified in a job script as:
{% else %}
<u>Sequential or single-node applications:</u>

The maximum amount of physical memory used by the job can be specified in a job script as:
{% endif %}
<pre><code>#PBS -l mem=4gb</code></pre>

or on the command line
<pre><code>$ <b>qsub -l mem=4gb</b></code></pre>

{% if site!=gent %}
This setting is ignored if the number of nodes is not&nbsp;1.

<u>Parallel or multi-node applications:</u>

When you are running a parallel application over multiple cores, you can
also specify the memory requirements per processor (pmem). This
directive specifies the maximum amount of physical memory used by any
process in the job.

For example, if the job would run four processes and each would use up
to 2 GB (gigabytes) of memory, then the memory directive would read:
<pre><code>#PBS -l pmem=2gb</code></pre>

or on the command line
<pre><code>$ <b>qsub -l pmem=2gb</b></code></pre>

(and of course this would need to be combined with a CPU cores directive
such as nodes=1:ppn=4). In this example, you request 8&nbsp;GB of memory in
total on the node.
{% endif %}

## Specifying processors requirements

Users are encouraged to fully utilise all the available cores on a
certain compute node. Once the required numbers of cores and nodes are
decently specified, it is also good practice to monitor the CPU
utilisation on these cores and to make sure that all the assigned nodes
are working at full load.

### Number of processors

The number of core and nodes that a user shall request fully depends on
the architecture of the application. Developers design their
applications with a strategy for parallelisation in mind. The
application can be designed for a certain fixed number or for a
configurable number of nodes and cores. It is wise to target a specific
set of compute nodes (e.g., Westmere, Harpertown) for your computing
work and then to configure your software to nicely fill up all
processors on these compute nodes.

The */proc/cpuinfo* stores info about your CPU architecture like number
of CPUs, threads, cores, information about CPU caches, CPU family, model
and much more. So, if you want to detect how many cores are available on
a specific machine:
<pre><code>$ <b>less /proc/cpuinfo</b>
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 23
model name      : Intel(R) Xeon(R) CPU  E5420  @ 2.50GHz
stepping        : 10
cpu MHz         : 2500.088
cache size      : 6144 KB
...</code></pre>

Or if you want to see it in a more readable format, execute:
<pre><code>$ <b>grep processor /proc/cpuinfo</b>
processor : 0
processor : 1
processor : 2
processor : 3
processor : 4
processor : 5
processor : 6
processor : 7</code></pre>

<u>Remark</u>: Unless you want information of the login nodes, you'll have to issue
these commands on one of the workernodes. This is most easily achieved
in an interactive job, see the chapter on Running interactive jobs.

In order to specify the number of nodes and the number of processors per
node in your job script, use:
<pre><code>#PBS -l nodes=N:ppn=M</code></pre>

or with equivalent parameters on the command line
<pre><code>$ <b>qsub -l nodes=N:ppn=M</b></code></pre>

This specifies the number of nodes (nodes=N) and the number of
processors per node (ppn=M) that the job should use. PBS treats a
processor core as a processor, so a system with eight cores per compute
node can have ppn=8 as its maximum ppn request.
{% if site !=antwerpen %}
You can also use this statement in your job script:

<pre><code>#PBS -l nodes=N:ppn=all</code></pre>

to request all cores of a node, or

<pre><code>#PBS -l nodes=N:ppn=half</code></pre>

to request half of them.
{% endif %}

Note that unless a job has some inherent parallelism of its own through
something like MPI or OpenMP, requesting more than a single processor on
a single node is usually wasteful and can impact the job start time.

### Monitoring the CPU-utilisation
{% if site != gent %}
The previously used "monitor" tool also shows the overall CPU-load. The
"eat_cpu" program performs a multiplication of 2 randomly filled a
\(1500 \times 1500\) matrices and is just written to consume a lot of
"*cpu*".

We first load the monitor modules, study the "eat_cpu.c" program and
compile it:
<pre><code>$ <b>module load monitor</b>
$ <b>cat eat_cpu.c</b>
$ <b>gcc -o eat_cpu eat_cpu.c</b></code></pre>

And then start to monitor the *eat_cpu* program:
<pre><code>$ <b>monitor -d 1 ./eat_cpu</b>
time  (s) size (kb) %mem %cpu
1  52852  0.3 100
2  52852  0.3 100
3  52852  0.3 100
4  52852  0.3 100
5  52852  0.3  99
6  52852  0.3 100
7  52852  0.3 100
8  52852  0.3 100</code></pre>

We notice that it the program keeps its CPU nicely busy at 100%.

Some processes spawn one or more sub-processes. In that case, the
metrics shown by monitor are aggregated over the process and all of its
sub-processes (recursively). The reported CPU usage is the sum of all
these processes, and can thus exceed 100%.

Some (well, since this is a {{hpc}} Cluster, we hope most) programs use more
than one core to perform their computations. Hence, it should not come
as a surprise that the CPU usage is reported as larger than 100%. When
programs of this type are running on a computer with n cores, the CPU
usage can go up to \(\text{n} \times 100\%\).
{% endif %}
This could also be monitored with the _**htop**_ command:
<pre><code>$ <b>htop</b></code></pre>
```
{% include "examples/Fine-tuning-Job-Specifications/htop-output" %}
```


The advantage of htop is that it shows you the cpu utilisation for all
processors as well as the details per application. A nice exercise is to
start 4 instances of the "cpu_eat" program in 4 different terminals, and
inspect the cpu utilisation per processor with monitor and htop.

If _**htop**_ reports that your program is taking 75% CPU on a certain processor,
it means that 75% of the samples taken by top found your process active
on the CPU. The rest of the time your application was in a wait. (It is
important to remember that a CPU is a discrete state machine. It really
can be at only 100%, executing an instruction, or at 0%, waiting for
something to do. There is no such thing as using 45% of a CPU. The CPU
percentage is a function of time.) However, it is likely that your
application's rest periods include waiting to be dispatched on a CPU and
not on external devices. That part of the wait percentage is then very
relevant to understanding your overall CPU usage pattern.

### Fine-tuning your executable and/or job script

It is good practice to perform a number of run time stress tests, and to
check the CPU utilisation of your nodes. We (and all other users of the
{{hpc}}) would appreciate that you use the maximum of the CPU resources that
are assigned to you and make sure that there are no CPUs in your node
who are not utilised without reasons.

But how can you maximise?

1.  Configure your software. (e.g., to exactly use the available amount
    of processors in a node)
2.  Develop your parallel program in a smart way.
3.  Demand a specific type of compute node (e.g., Harpertown, Westmere),
    which have a specific number of cores.
4.  Correct your request for CPUs in your job script.

## The system load

On top of the CPU utilisation, it is also important to check the **system load**.
The system **load** is a measure of the amount of computational work that a computer
system performs.

The system load is the number of applications running or waiting to run
on the compute node. In a system with for example four CPUs, a load
average of 3.61 would indicate that there were, on average, 3.61
processes ready to run, and each one could be scheduled into a CPU.

The load averages differ from CPU percentage in two significant ways:

1.  "*load averages*" measure the trend of processes waiting to be run
    (and not only an instantaneous snapshot, as does CPU percentage);
    and
2.  "*load averages*" include all demand for all resources, e.g., CPU
    and also I/O and network (and not only how much was active at the
    time of measurement).

### Optimal load

What is the "*optimal load*" rule of thumb?

The load averages tell us whether our physical CPUs are over- or
under-utilised. The **point of perfect utilisation**, meaning that the CPUs are always busy and, yet, no
process ever waits for one, is **the
average matching the number of CPUs**. Your load should not exceed the number
of cores available. E.g., if there are four CPUs on a machine and the
reported one-minute load average is 4.00, the machine has been utilising
its processors perfectly for the last 60 seconds. The "100% utilisation"
mark is 1.0 on a single-core system, 2.0 on a dual-core, 4.0 on a
quad-core, etc. The optimal load shall be between 0.7 and 1.0 per
processor.

In general, the intuitive idea of load averages is the higher they rise
above the number of processors, the more processes are waiting and doing
nothing, and the lower they fall below the number of processors, the
more untapped CPU capacity there is.

*Load averages* do include any processes or threads waiting on I/O,
networking, databases or anything else not demanding the CPU. This means
that the optimal *number of applications* running on a system at the
same time, might be more than one per processor.

The "**optimal number of applications**" running on one machine at the same time depends on the type of
the applications that you are running.

1.  When you are running **computational intensive applications**, one application per processor will generate
    the optimal load.
2.  For **I/O intensive applications** (e.g., applications which perform a lot of disk-I/O), a higher
    number of applications can generate the optimal load. While some
    applications are reading or writing data on disks, the processors
    can serve other applications.

The optimal number of applications on a machine could be empirically
calculated by performing a number of stress tests, whilst checking the
highest throughput. There is however no manner in the {{hpc}} at the moment to
specify the maximum number of applications that shall run per core
dynamically. The {{hpc}} scheduler will not launch more than one process per
core.

The manner how the cores are spread out over CPUs does not matter for
what regards the load. Two quad-cores perform similar to four
dual-cores, and again perform similar to eight single-cores. It's all
eight cores for these purposes.

### Monitoring the load

The **load average** represents the average system load over a period of time. It
conventionally appears in the form of three numbers, which represent the
system load during the last **one**-, **five**-, and **fifteen**-minute periods.

The **uptime** command will show us the average load
<pre><code>$ <b>uptime</b>
10:14:05 up 86 days, 12:01, 11 users, load average: 0.60, 0.41, 0.41
</code></pre>

Now, start a few instances of the "*eat_cpu*" program in the background,
and check the effect on the load again:
<pre><code>$ <b>./eat_cpu&</b>
$ <b>./eat_cpu&</b>
$ <b>./eat_cpu&</b>
$ <b>uptime</b>
10:14:42 up 86 days, 12:02, 11 users, load average: 2.60, 0.93, 0.58
</code></pre>
You can also read it in the **htop** command.

### Fine-tuning your executable and/or job script

It is good practice to perform a number of run time stress tests, and to
check the system load of your nodes. We (and all other users of the {{hpc}})
would appreciate that you use the maximum of the CPU resources that are
assigned to you and make sure that there are no CPUs in your node who
are not utilised without reasons.

But how can you maximise?

1.  Profile your software to improve its performance.
2.  Configure your software (e.g., to exactly use the available amount
    of processors in a node).
3.  Develop your parallel program in a smart way, so that it fully
    utilises the available processors.
4.  Demand a specific type of compute node (e.g., Harpertown, Westmere),
    which have a specific number of cores.
5.  Correct your request for CPUs in your job script.

And then check again.

## Checking File sizes & Disk I/O

### Monitoring File sizes during execution

Some programs generate intermediate or output files, the size of which
may also be a useful metric.

Remember that your available disk space on the {{hpc}} online storage is
limited, and that you have environment variables which point to these
directories available (i.e., *$VSC_DATA*, *$VSC_SCRATCH* and
*$VSC_DATA*). On top of those, you can also access some temporary
storage (i.e., the /tmp directory) on the compute node, which is defined
by the *$VSC_SCRATCH_NODE* environment variable.

{% if site != gent %}
We first load the monitor modules, study the "eat_disk.c" program and
compile it:
<pre><code>$ <b>module load monitor</b>
$ <b>cat eat_disk.c</b>
$ <b>gcc -o eat_disk eat_disk.c</b>
</code></pre>

The *monitor* tool provides an option (-f) to display the size of one or
more files:
<pre><code>$ <b>monitor -f $VSC_SCRATCH/test.txt ./eat_disk</b>
time (s) size (kb) %mem %cpu
5  1276  0 38.6 168820736
10  1276  0 24.8 238026752
15  1276  0 22.8 318767104
20  1276  0 25 456130560
25  1276  0 26.9 614465536
30  1276  0 27.7 760217600
...
</code></pre>

Here, the size of the file "*test.txt*" in directory $VSC_SCRATCH will
be monitored. Files can be specified by absolute as well as relative
path, and multiple files are separated by ",".
{% endif %}

It is important to be aware of the sizes of the file that will be
generated, as the available disk space for each user is limited. We
refer to section 
[How much disk space do I get?](running_jobs_with_input_output_data.md#how-much-disk-space-do-i-get) on [Quotas](running_jobs_with_input_output_data.md#quota) to check your
quota and tools to find which files consumed the "quota".

Several actions can be taken, to avoid storage problems:

1.  Be aware of all the files that are generated by your program. Also
    check out the hidden files.
2.  Check your quota consumption regularly.
3.  Clean up your files regularly.
4.  First work (i.e., read and write) with your big files in the local
    /tmp directory. Once finished, you can move your files once to the
    VSC_DATA directories.
5.  Make sure your programs clean up their temporary files after
    execution.
6.  Move your output results to your own computer regularly.
7.  Anyone can request more disk space to the {{hpc}} staff, but you will have
    to duly justify your request.

## Specifying network requirements

Users can examine their network activities with the htop command. When
your processors are 100% busy, but you see a lot of red bars and only
limited green bars in the htop screen, it is mostly an indication that
they lose a lot of time with inter-process communication.

Whenever your application utilises a lot of inter-process communication
(as is the case in most parallel programs), we strongly recommend to
request nodes with an "InfiniBand" network. The InfiniBand is a
specialised high bandwidth, low latency network that enables large
parallel jobs to run as efficiently as possible.

The parameter to add in your job script would be:
<pre><code>#PBS -l ib</code></pre>

If for some other reasons, a user is fine with the gigabit Ethernet
network, he can specify:
<pre><code>#PBS -l gbe</code></pre>

{% if site!=gent %}
## Some more tips on the Monitor tool

### Command Lines arguments

Many programs, e.g., MATLAB, take command line options. To make sure
these do not interfere with those of monitor and vice versa, the program
can for instance be started in the following way:
<pre><code>$ <b>monitor -delta 60 -- matlab -nojvm -nodisplay computation.m</b></code></pre>

The use of `--` will ensure that monitor does not get confused by
MATLAB's `-nojvm` and `-nodisplay` options.

### Exit Code

Monitor will propagate the exit code of the program it is watching.
Suppose the latter ends normally, then monitor's exit code will be 0. On
the other hand, when the program terminates abnormally with a non-zero
exit code, e.g., 3, then this will be monitor's exit code as well.

When monitor terminates in an abnormal state, for instance if it can't
create the log file, its exit code will be 65. If this interferes with
an exit code of the program to be monitored, it can be modified by
setting the environment variable MONITOR_EXIT_ERROR to a more suitable
value.

### Monitoring a running process

It is also possible to "attach" monitor to a program or process that is
already running. One simply determines the relevant process ID using the
ps command, e.g., 18749, and starts monitor:
<pre><code>$ <b>monitor -p 18749</b></code></pre>

Note that this feature can be (ab)used to monitor specific sub-processes.
{% endif %}
