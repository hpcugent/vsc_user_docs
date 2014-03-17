#!/bin/sh

## example MPI script that can be used for MPI programs not compiled
## with the OpenMPI environment, e.g., ABINIT, CPMD, Quantum Espresso,
## OpenMX, vasp and "generic" MPI programs

## it replaces the "mpirun -r ssh -genv I_MPI_FABRICS ..." or
## "mympirun" scripts

## Wien2K, Gaussian, Molpro, pvm have their own example scripts


#PBS -N name
#PBS -q qshort

## node specification: Y is at most 8 for harpertown, or 24 for westmere
#PBS -l nodes=X:ppn=Y:ib

#PBS -l walltime=1:00:00

## to enforce the node specification, add the following line 
#PBS -W x=nmatchpolicy:exactnode

## if, in addition, you want to avoid that other jobs of you also could
## use this node, also add
#PBS -l naccesspolicy=singlejob

## another way is to specify the amount of memory needed per core,
## i.e., Y as defined on the node specification line.  Take into
## account that installed memory in harpertown nodes is 16 GB, in
## westmere nodes 24 GB

#PBS -l pmem=8G

## other options can be found on
## http://www.adaptivecomputing.com/resources/docs/mwm/13.3rmextensions.php
## http://www.adaptivecomputing.com/resources/docs/mwm/5.3nodeaccess.php


module purge
module load <your Intel MPI/MPICH based package>
   # e.g., ictce, ABINIT/6.6.1-ictce-3.2.2.u3

module load mpiexec


cd $PBS_O_WORKDIR

mpiexec <your executable> <your input files>
