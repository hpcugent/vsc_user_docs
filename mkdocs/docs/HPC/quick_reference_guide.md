# HPC Quick Reference Guide

Remember to substitute the usernames, login nodes, file names, ...for
your own.

| **Login**         |                                         |
|-------------------|-----------------------------------------|
| Login             | `ssh {{userid}}@{{loginnode}}`          |
| Where am I?       | `hostname`                              |
| Copy to {{hpc}}   | `scp foo.txt {{userid}}@{{loginnode}}:` |
| Copy from {{hpc}} | `scp {{userid}}@{{loginnode}}:foo.txt`  |
| Setup ftp session | `sftp {{userid}}@{{loginnode}}`         |


| **Modules**                |                       |
|----------------------------|-----------------------|
| List all available modules | Module avail          |
| List loaded modules        | module list           |
| Load module                | module load example   |
| Unload module              | module unload example |
| Unload all modules         | module purge          |
| Help on use of module      | module help           |

| Command                                       | Description                                             |
|-----------------------------------------------|---------------------------------------------------------|
| `qsub script.pbs`                            | Submit job with job script `script.pbs`                |
| `qstat 12345`                                | Status of job with ID 12345                            |
{% if site != (gent or brussel) %} | `showstart 12345`                           | Possible start time of job with ID 12345 (not available everywhere) |
| `checkjob 12345`                            | Check job with ID 12345 (not available everywhere)    |
{% endif %} | `qstat -n 12345`                            | Show compute node of job with ID 12345                 |
| `qdel 12345`                                | Delete job with ID 12345                               |
| `qstat`                                     | Status of all your jobs                                |
| `qstat -na`                                 | Detailed status of your jobs + a list of nodes they are running on |
{% if site != (gent or brussel) %} | `showq`                                     | Show all jobs on queue (not available everywhere)      |
{% endif %} | `qsub -I`                                  | Submit Interactive job                                 |


| **Disk quota**                                |                                                 |
|-----------------------------------------------|-------------------------------------------------|
{% if site == gent %} | Check your disk quota                         | see [https://account.vscentrum.be](https://account.vscentrum.be) |
{% else %} | Check your disk quota                         | `mmlsquota`                                     |
| Check your disk quota nice                    | `show_quota.py`                                 |
{% endif %} | Disk usage in current directory (`.`)         | `du -h`                                         |



| **Worker Framework**                    |                                                                                                                                    |
|-----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Load worker module                      | `module load worker/1.6.13-iimpi-2023a`  Don't forget to specify a version. To list available versions, use `module avail worker/` |
| Submit parameter sweep                  | `wsub -batch weather.pbs -data data.csv`                                                                                           |
| Submit job array                        | `wsub -t 1-100 -batch test_set.pbs`                                                                                                |
| Submit job array with prolog and epilog | `wsub -prolog pre.sh -batch test_set.pbs -epilog post.sh -t 1-100`                                                                 |
