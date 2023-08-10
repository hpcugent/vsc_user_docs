{% set exampledir="examples/Program-examples" %}
# Program examples { #ch:program-examples}

If you have **not done so already** copy our examples to your home directory by running the following command:
<pre><code><b> cp -r {{ examplesdir }} ~/</b></code></pre>
<sub>`~`(tilde) refers to your home directory, the directory you arrive by default when you login.</sub>

Go to our examples:
<pre><code><b>cd ~/{{exampledir}}</b></code></pre>

Here, we just have put together a number of examples for your
convenience. We did an effort to put comments inside the source files,
so the source code files are (should be) self-explanatory.

1.  01_Python

2.  02_C_C++

3.  03_Matlab

4.  04_MPI_C

5.  05a_OMP_C

6.  05b_OMP_FORTRAN

7.  06_NWChem

8.  07_Wien2k

9.  08_Gaussian

10. 09_Fortran

11. 10_PQS

The above 2 OMP directories contain the following examples:

| C Files                                                                                                                                               | Fortran Files                                                                                                                                                  | Description                           |
|-------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| omp_hello.c                                                                                                                                           | omp_hello.f                                                                                                                                                    | Hello world                           |
| omp_workshare1.c                                                                                                                                      | omp_workshare1.f                                                                                                                                               | Loop work-sharing                     |
| omp_workshare2.c                                                                                                                                      | omp_workshare2.f                                                                                                                                               | Sections work-sharing                 |
| omp_reduction.c                                                                                                                                       | omp_reduction.f                                                                                                                                                | Combined parallel loop reduction      |
| omp_orphan.c                                                                                                                                          | omp_orphan.f                                                                                                                                                   | Orphaned parallel loop reduction      |
| omp_mm.c                                                                                                                                              | omp_mm.f                                                                                                                                                       | Matrix multiply                       |
| omp_getEnvInfo.c                                                                                                                                      | omp_getEnvInfo.f                                                                                                                                               | Get and print environment information |
| omp_bug1.c<br/>omp_bug1fix.c<br/> omp_bug2.c<br/>  omp_bug3.c<br/>  omp_bug4.c<br/>  omp_bug4fix<br/>  omp_bug5.c<br/>  omp_bug5fix.c<br/> omp_bug6.c | omp_bug1.f<br/>  omp_bug1fix.f<br/>  omp_bug2.f<br/>  omp_bug3.f<br/>  omp_bug4.f<br/>  omp_bug4fix<br/>  omp_bug5.f<br/>  omp_bug5fix.f<br/>  omp_bug6.f<br/> | Programs with bugs and their solution |

Compile by any of the following commands:
<table>
    <tr>
        <th>C:</th>
        <td>icc -openmp omp_hello.c -o hello\newline pgcc -mp omp_hello.c -o hello\newline gcc -fopenmp omp_hello.c -o hello</td>
    </tr>
    <tr>
        <th>Fortran:</th>
        <td>ifort -openmp omp_hello.f -o hello\newline pgf90 -mp omp_hello.f -o hello\newline gfortran -fopenmp omp_hello.f -o hello</td>
    </tr>
</table>

Be invited to explore the examples.
