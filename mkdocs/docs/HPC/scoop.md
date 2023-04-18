# SCOOP

SCOOP (Scalable COncurrent Operations in Python) is a distributed task
module allowing concurrent parallel programming on various environments,
from heterogeneous grids to supercomputers. It is an alternative to the
worker framework, see [Multi-job submission](../multi_job_submission/#multi-job-submission).

It can used for projects that require lots of (small) tasks to be
executed.

The `myscoop` script makes it very easy to use SCOOP, even in a
multi-node setup.

## Loading the module

Before using `myscoop`, you first need to load the `vsc-mympirun-scoop`
module. We don't specify a version here (this is an exception, for most
other modules you should, see [Using explicit version numbers](../running_batch_jobs/#using-explicit-version-numbers)) because newer versions might include
important bug fixes or performance improvements.

<pre><code>$ <b>module load vsc-mympirun-scoop</b>
</code></pre>

## Write a worker script

A Python worker script implements both the main program, and (typically)
the small task function that needs to be executed a large amount of
times.

This is done using the functionality provided by the `scoop` Python
module, for example `futures.map` (see also
<https://scoop.readthedocs.org/>).

First, the necessary imports need to be specified:

```python
import sys 
from scoop import futures
```

A Python function must be implemented for the core task, for example to
compute the square of a number:

```python
def square(x): 
    return x*x
```

The main function then applies this simple function to a range of values
specified as an argument. Note that it should be guarded by a
conditional (`if __name__ == "=__main__"`) to make sure it is only
executed when executing the script (and not when importing from it):

```python
f __name__ == "__main__":

    # obtain n from first command line argument 
    n = int(sys.argv[1])

    # compute the square of the first n numbers, in parallel using SCOOP functionality 
    squares = futures.map(square, range(n)) # note: returns an iterator

    print("First %d squares: %s" % (n, list(squares)))
```

## Executing the program

To execute the Python script implementing the task and main function in
a SCOOP environment, specify to the `python` command to use the `scoop`
module:

<pre><code>$ <b>python -m scoop squares.py 10000</b>
</code></pre>

## Using <tt>myscoop</tt>

To execute the SCOOP program in an multi-node environment, where workers
are spread across multiple physical systems, simply use `myscoop`: just
specify the name of the Python module in which the SCOOP program is
implemented, and specify further arguments on the command line.

You will need to make sure that the path to where the Python module is
located is listed in `$PYTHONPATH`.

This is an example of a complete job script executing the SCOOP program
in parallel in a multi-node job (i.e., 2 nodes with 8 cores each):

<center>-- squares_jobscript.pbs --</center>
```bash
{% include "./examples/SCOOP/squares_jobscript.pbs" %}
```

Note that you don't need to specify how many workers need to be used;
the `myscoop` command figures this out by itself. This is because
`myscoop` is a wrapper around `mympirun` (see [Mympirun](../mympirun/#mympirun)). In this example, 16
workers (one per available core) will be execute the 10000 tasks one by
one until all squares are computed.

To run the same command on the local system (e.g., a login node for
testing), add the `--sched=local` option to `myscoop`.

## Example: calculating π

A more practical example of a worker script is one to compute π
using a Monte-Carlo method (see also
<https://scoop.readthedocs.org/en/0.6/examples.html#computation-of>).

The `test` function implements a tiny task that is be executed `tries`
number of times by each worker. Afterwards, the number of successful
tests is determined using the Python `sum` function, and an approximate
value of π is computed and returned by `calcPi` so the main function
can print it out.

<center>-- picalc.py --</center>
```python
{% include "./examples/SCOOP/picalc.py" %}
```
<center>-- picalc_job_script.pbs --</center>
```bash
{% include "./examples/SCOOP/picalc_job_script.pbs" %}
```
