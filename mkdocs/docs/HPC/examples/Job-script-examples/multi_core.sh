#!/bin/bash
#PBS -N mpi_hello             ## job name
#PBS -l nodes=2:ppn=all       ## 2 nodes, all cores per node
#PBS -l walltime=2:00:00      ## max. 2h of wall time
module load intel/2017b
module load vsc-mympirun      ## We don't use a version here, this is on purpose
# go to working directory, compile and run MPI hello world
cd $PBS_O_WORKDIR
mpicc mpi_hello.c -o mpi_hello
mympirun ./mpi_hello
