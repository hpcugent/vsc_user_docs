#!/bin/sh

# about...
#   - serial run launching 1 processes (ppn=1) on 1 node (nodes=1)

#PBS -N g09 
#PBS -q qreg  
#PBS -l nodes=1:ppn=1 
#PBS -l walltime=1:00:00

module purge
module add Gaussian/g09_A1

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

time g09 < test.com > test.log           

/bin/rm -R $GAUSS_SCRDIR
