# TORQUE options

## TORQUE Submission Flags: common and useful directives

Below is a list of the most common and useful directives.

| Option | System type | Description|
|:------:|:-----------:|:----------|
| -k  | All | Send "stdout" and/or "stderr" to your home directory when the job runs <br> **#PBS -k o** or **#PBS -k e** or **#PBS -koe**</br> |
| -l | All | Precedes a resource request, e.g., processors, wallclock |
| -M | All | Send an e-mail messages to an alternative e-mail address <br> **#PBS -M me@mymail.be**</br> |
| -m | All | Send an e-mail address when a job **b**egins execution and/or **e**nds or **a**borts <br> **#PBS -m b** or **#PBS -m be** or **#PBS -m ba** |
| mem | Shared Memory | Memory & Specifies the amount of memory you need for a job. <br>**#PBS -I mem=90gb** |
| mpiproces | Clusters | Number of processes per node on a cluster. This should equal number of processors on a node in most cases. <br> **#PBS -l mpiprocs=4** |
| -N | All | Give your job a unique name <br>**#PBS -N galaxies1234**</br> |
| -ncpus | Shared Memory | The number of processors to use for a shared memory job. <br>**#PBS ncpus=4**</br> |
| -r | All | ontrol whether or not jobs should automatically re-run from the start if the system crashes or is rebooted. Users with check points might not wish this to happen. <br>**#PBS -r n**</br><br>**#PBS -r y**</br> |
| select | Clusters | Number of compute nodes to use. Usually combined with the mpiprocs directive <br>**#PBS -l select=2**</br>|
| -V | All | Make sure that the environment in which the job **runs** is the same as the environment in which it was **submitted <br> #PBS -V</br>**
| Walltime | All | The maximum time a job can run before being stopped. If not used a default of a few minutes is used. Use this flag to prevent jobs that go bad running for hundreds of hours. Format is HH:MM:SS <br>**#PBS -l walltime=12:00:00**</br> | 

## Environment Variables in Batch Job Scripts

TORQUE-related environment variables in batch job scripts.

```bash
# Using PBS - Environment Variables:
# When a batch job starts execution, a number of environment variables are
# predefined, which include:
#
#      Variables defined on the execution host.
#      Variables exported from the submission host with
#                -v (selected variables) and -V (all variables).
#      Variables defined by PBS.
#
# The following reflect the environment where the user ran qsub:
# PBS_O_HOST    The host where you ran the qsub command.
# PBS_O_LOGNAME Your user ID where you ran qsub.
# PBS_O_HOME    Your home directory where you ran qsub.
# PBS_O_WORKDIR The working directory where you ran qsub.
#
# These reflect the environment where the job is executing:
# PBS_ENVIRONMENT       Set to PBS_BATCH to indicate the job is a batch job,
#         or to PBS_INTERACTIVE to indicate the job is a PBS interactive job.
# PBS_O_QUEUE   The original queue you submitted to.
# PBS_QUEUE     The queue the job is executing from.
# PBS_JOBID     The job's PBS identifier.
# PBS_JOBNAME   The job's name.
```

***IMPORTANT!!*** All PBS directives MUST come before the first line of executable code in
your script, otherwise they will be ignored.

When a batch job is started, a number of environment variables are
created that can be used in the batch job script. A few of the most
commonly used variables are described here.

| Variable | Description |
|:--------:|:-----------|
|  PBS_ENVIRONMENT |  set to PBS_BATCH to indicate that the job is a batch job; otherwise, set to PBS_INTERACTIVE to indicate that the job is a PBS interactive job. |
|  PBS_JOBID |        the job identifier assigned to the job by the batch system. This is the same number you see when you do *qstat*. |
|  PBS_JOBNAME    |   the job name supplied by the user |
|  PBS_NODEFILE   |   the name of the file that contains the list of the nodes assigned to the job . Useful for Parallel jobs if you want to refer the node, count the node etc. |
|  PBS_QUEUE      |   the name of the queue from which the job is executed
|  PBS_O_HOME     |  value of the HOME variable in the environment in which *qsub* was executed |
|  PBS_O_LANG   |    value of the LANG variable in the environment in which *qsub* was executed |
|  PBS_O_LOGNAME  |  value of the LOGNAME variable in the environment in which *qsub* was executed |
|  PBS_O_PATH    |   value of the PATH variable in the environment in which *qsub* was executed |
|  PBS_O_MAIL   |    value of the MAIL variable in the environment in which *qsub* was executed |
|  PBS_O_SHELL   |   value of the SHELL variable in the environment in which *qsub* was executed |
|  PBS_O_TZ      |   value of the TZ variable in the environment in which *qsub* was executed |
|  PBS_O_HOST    |   the name of the host upon which the *qsub* command is running |
|  PBS_O_QUEUE  |    the name of the original queue to which the job was submitted |
|  PBS_O_WORKDIR  |  the absolute path of the current working directory of the *qsub* command. This is the most useful. Use it in every job script. The first thing you do is, cd $PBS_O_WORKDIR after defining the resource list. This is because, pbs throw you to your $HOME directory. |
|  PBS_VERSION   |    Version Number of TORQUE, e.g., TORQUE-2.5.1 |
|  PBS_MOMPORT    |   active port for mom daemon |
|  PBS_TASKNUM    |   number of tasks requested |
|  PBS_JOBCOOKIE   |  job cookie |
|  PBS_SERVER    |    Server Running TORQUE |
