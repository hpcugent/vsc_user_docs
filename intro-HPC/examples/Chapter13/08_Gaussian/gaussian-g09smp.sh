#!/bin/sh

# about ...
#   - smp run on 1 node (nodes=1): requesting all memory (pvm=16000m)
#     has the same effect as requesting all processors in 1 node (ppn=8)
#   - input file should start with %nproc=8

#PBS -N g09smp
#PBS -q qlong
#PBS -l nodes=1
#PBS -l pvmem=16000m
#PBS -l pmem=14400m
#PBS -l walltime=72:00:00

module purge
module load Gaussian/g09_A1

# If you need more than 100 GB of scratch, use /scratch  (global scratch)
export GAUSS_SCRDIR=${VSC_SCRATCH}/gaussian/$job.$PBS_JOBID

# otherwise use /tmp  (local scratch on node)
export GAUSS_SCRDIR=${VSC_SCRATCH_NODE}/gaussian/$job.$PBS_JOBID

# choose the correct GAUSS_SCRDIR line above!

if [ ! -d $GAUSS_SCRDIR ]
then
  mkdir -p $GAUSS_SCRDIR
fi


# Assume that the job file are located in the submit directory
cd $PBS_O_WORKDIR
time g09 < halo12.com > halo12.log

/bin/rm -R $GAUSS_SCRDIR
