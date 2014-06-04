#!/bin/sh

#PBS -N w2k-TiC
#PBS -q qshort
#PBS -l nodes=4:ppn=8
#PBS -l walltime=1:00:00

module load WIEN2k

cd $PBS_O_WORKDIR

echo '#' > .machines

# # example for an MPI parallel lapw0 
# echo -n 'lapw0:' >> .machines
# for line in `cat $PBS_NODEFILE`
# do
#   echo -n $line >> .machines
# done
# echo >> .machines


#example for k-point parallel lapw1/2
for line in `cat $PBS_NODEFILE`
do
  echo "1: $line" >> .machines
done
echo 'granularity:1' >>.machines
echo 'extrafine:1' >>.machines


#define here your WIEN2k command

run_lapw -p -i 20 -ec 0.00001
