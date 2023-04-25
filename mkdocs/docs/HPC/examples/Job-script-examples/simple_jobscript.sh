#!/bin/bash

# Basic parameters
#PBS -N jobname           ## Job name
#PBS -l nodes=1:ppn=2     ## 1 node, 2 processors per node (ppn=all to get a full node)
#PBS -l walltime=01:00:00 ## Max time your job will run (no more than 72:00:00)

# Situational parameters: remove one '#' at the front to use
##PBS -l gpus=1            ## GPU amount (only on accelgor or joltik)
##PBS -l mem=32gb          ## If not used, memory will be available proportional to the max amount
##PBS -m abe               ## Email notifications (abe=aborted, begin and end)
##PBS -M -email_address-   ## ONLY if you want to use a different email than your VSC address
##PBS -A -project-         ## Project name when credits are required (only Tier 1)

##PBS -o -filename-        ## Output log
##PBS -e -filename-        ## Error log


module load [module]
module load [module]

cd $PBS_O_WORKDIR         # Change working directory to the location where the job was submmitted

[commands]
