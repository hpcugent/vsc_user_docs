#!/bin/sh

#PBS -N pvm-test
#PBS -q qshort
#PBS -l nodes=18
#PBS -l walltime=1:00:00

module load PVM

cd $PBS_O_WORKDIR

#
#  Setup a virtual parallel machine.
#  Change both the path for executables (ep) and the
#  working directory (wd) to the current directory.
#
echo \* ep=`pwd` wd=`pwd` > hostlist
cat $PBS_NODEFILE >> hostlist
echo conf | pvm hostlist
rm hostlist

#
#  Start the (master) program
#
./master.x > out

#
# Shutdown PVM
#
echo halt | pvm
