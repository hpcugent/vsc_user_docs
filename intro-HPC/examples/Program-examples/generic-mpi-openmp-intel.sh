#!/bin/sh

#PBS -N name
#PBS -q qshort
#PBS -l nodes=4:ppn=8
#PBS -l walltime=1:00:00

#PBS -W x=nmatchpolicy:exactnode

module purge
module load <your package>

# assume 32 processes in total, divided over 4 nodes
# => #PBS -l nodes=4:ppn=8
#
# on every node, we want to run 2 MPI processes,
# each running 4 OpenMP instances
# => mpirun -ppn 2 -n 8
# meaning: start 2 MPI instances per node;
# the total number of MPI instances is given by -n,
# namely: number of nodes on the #PBS line multiplied by
# the value of ppn on the mpirun line
#
# more info:
# http://software.intel.com/en-us/articles/hybrid-applications-intelmpi-openmp/ 
# https://support.scinet.utoronto.ca/wiki/index.php/GPC_Quickstart#Hybrid_MPI.2FOpenMP_jobs



mpi_procs_per_node=       # set the number of MPI processes per node
mpi_procs_total=          # set the total number of MPI processes


cd $PBS_O_WORKDIR


mpirun -r ssh -ppn ${mpi_procs_per_node} -n ${mpi_procs_total} <your executable> <your input files>

