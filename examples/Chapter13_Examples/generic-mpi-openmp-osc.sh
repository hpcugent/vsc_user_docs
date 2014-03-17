#!/bin/sh

## example hybrid OpenMP/MPI script for, e.g., OpenMX


#PBS -N name
#PBS -q qshort
#PBS -l nodes=X:ppn=Y:ib
#PBS -l walltime=1:00:00

#PBS -W x=nmatchpolicy:exactnode

module purge
module load <your package>
module load mpiexec

# $mpi_procs_per_node * OMP_NUM_THREADS worker threads will be created
# per node; this product should equal Y 

export OMP_NUM_THREADS=   # set the number of OpenMP threads per node
mpi_procs_per_node=       # set the number of MPI processes per node



cd $PBS_O_WORKDIR



mpiexec -npernode $mpi_procs_per_node <your executable> <your input files>

