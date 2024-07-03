#!/bin/sh

#PBS -N name
#PBS -q qshort
#PBS -l nodes=2:ppn=8:ib
#PBS -l walltime=1:00:00

module load <your package>

cd $PBS_O_WORKDIR


n_proc=$(cat $PBS_NODEFILE | wc -l)
n_node=$(cat $PBS_NODEFILE | uniq | wc -l)

mpirun -r ssh -n ${n_proc} <your executable> <your input files>
