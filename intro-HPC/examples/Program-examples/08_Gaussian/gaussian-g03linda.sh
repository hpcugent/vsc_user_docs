#!/bin/sh

# about... 
#   - parallel run launching 8 processes (ppn=8) on 7 nodes (nodes=7)
#     linda will use 8x7 cores
#   - input file should start with %nprocl=8n (8n should be smaller than
#     or equal to number of processes times number of nodes, e.g.,
#     16, 24, 32, ..., or 14 (in case of 8x2), 21 (in case of 8x3), ...

#PBS -N g03l 
#PBS -q qlong
#PBS -l nodes=7:ppn=8 
#PBS -l walltime=72:00:00

module purge
module add Gaussian/g03_D1

# Needed to run on more than one node using Linda
export GAUSS_LFLAGS="-vv -nodelist '`cat $PBS_NODEFILE|sort|uniq`' -mp 8"

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

# Use g03l when using Linda
time g03l < jobname.com > jobname03.out

/bin/rm -R $GAUSS_SCRDIR
