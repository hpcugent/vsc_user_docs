#!/bin/sh

#PBS -N pqs
#PBS -q qshort

#PBS -l nodes=1:ppn=4
#PBS -l walltime=1:00:00



module purge
module load PQS
module load OpenMPI/1.4.1

slaves=$(( `wc -l ${PBS_NODEFILE} | cut -f1 -d" " ` - 1 ))

cd $PBS_O_WORKDIR

pqs water $slaves -f $PBS_NODEFILE -ompi

