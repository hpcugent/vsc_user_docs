#!/bin/bash
#PBS -N timeout_example
#PBS -l nodes=1:ppn=1         ## single-node job, single core
#PBS -l walltime=20:00:00     ## max. 20h of wall time

# go to temporary working directory (on local disk)
cd $TMPDIR
# This command will take too long (1400 minutes is longer than our walltime)
# $PBS_O_WORKDIR/example_program.sh 1400 output.txt

# So we put it after a timeout command
# We have a total of 60 * 20 minutes (=1200 minutes), but we only give it
#  1150 minutes, so we have 50 minutes left to copy files back. This should
#  be more than enough.
timeout 1150m $PBS_O_WORKDIR/example_program.sh 1400 output.txt
# copy back output data, ensure unique filename using $PBS_JOBID
cp output.txt $VSC_DATA/output_${PBS_JOBID}.txt
