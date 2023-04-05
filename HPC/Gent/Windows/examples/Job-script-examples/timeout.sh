#!/bin/bash
#PBS -N timeout_example
#PBS -l nodes=1:ppn=1        ## single-node job, single core
#PBS -l walltime=2:00:00     ## max. 2h of wall time

# go to temporary working directory (on local disk)
cd $TMPDIR
# This command will take too long (1400 minutes is longer than our walltime)
# $PBS_O_WORKDIR/example_program.sh 1400 output.txt

# So we put it after a timeout command
# We have a total of 120 minutes (2 x 60) and we instruct the script to run for
# 100 minutes, but timeout after 90 minute,
# so we have 30 minutes left to copy files back. This should
#  be more than enough.
timeout -s SIGKILL 90m $PBS_O_WORKDIR/example_program.sh 100 output.txt
# copy back output data, ensure unique filename using $PBS_JOBID
cp output.txt $VSC_DATA/output_${PBS_JOBID}.txt
