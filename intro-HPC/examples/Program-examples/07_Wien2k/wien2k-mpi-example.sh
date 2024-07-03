#!/bin/bash -login

#PBS -N test
#PBS -l nodes=2:ppn=4
#PBS -l walltime=1:00:00
#PBS -W x=nmatchpolicy:exactnode
#PBS -q qshort

######################
# Wien2k script by Matthias Zschornak (matthias.zschornak@physik.tu-dresden.de)
#   modified by Stefan Becuwe (stefan.becuwe@ua.ac.be) to deal with a "bug"
#   in the lapw*_para files: FQDN host names are not taken into account,
#   so we modify the machines in this script (look for "turing")
#

######################
# IMPORTANT!!! 
#   define here the number of processors you like to use for fine grid
#   mpi-parallelization per k-bundle

NPROCSMPI=4

#######################
# setting up MPI environment and WIEN2k
#
# put the following line in your ~/.bashrc:
#   module load WIEN2k/10.1-MPICH-1.2.7p1-ictce-3.2.1.015.u1
#
# it will load WIEN2k variables, and modify PATH, LD_LIBRARY_PATH


######################
# collects environment info, feedback in .cn_info

NPROCS=`wc -l < $PBS_NODEFILE`
SCR_DIR=$PBS_JOBID
JOBNAME=$PBS_JOBNAME
HOSTNAME=$PBS_O_HOST
HDIR=$PBS_O_WORKDIR

rm $HDIR/.cn_nodes $HDIR/.cn_amount $HDIR/.cn_info
echo `cat $PBS_NODEFILE` >> $HDIR/.cn_nodes
echo $NPROCS > $HDIR/.cn_amount
module list >& $HDIR/.cn_info
echo $WIENROOT >>$HDIR/.cn_info
echo "WIEN_MPIRUN: $WIEN_MPIRUN" >>$HDIR/.cn_info
echo "USE_REMOTE: $USE_REMOTE" >>$HDIR/.cn_info
echo "MPI_REMOTE: $MPI_REMOTE" >>$HDIR/.cn_info
echo "PATH: $PATH" >>$HDIR/.cn_info
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH" >>$HDIR/.cn_info
which mpirun >>$HDIR/.cn_info
which lapw1_mpi >>$HDIR/.cn_info
which lapw1c_mpi >>$HDIR/.cn_info
which lapw1 >>$HDIR/.cn_info
which lapw1c >>$HDIR/.cn_info

SCRATCH=/scratch/sbecuwe/wien2k-scratch

######################
# changes into your working directory

cd $HDIR

######################
# creates a machines file for WIEN2k

rm .machines
mach=`cat $PBS_NODEFILE|sort -u`
echo -n "lapw0: " > .machines
for n in $mach; do
    cpucnt=`grep "^$n$" $PBS_NODEFILE|wc -l`
    n=`echo $n | sed -e 's/.turing.antwerpen.vsc//'`
    echo -n "$n:$cpucnt " >> .machines
done
echo >> .machines
for n in $mach; do
    cpucnt=`grep "^$n$" $PBS_NODEFILE|wc -l`
    while [ "$cpucnt" -gt "$NPROCSMPI" ]; do
        n=`echo $n | sed -e 's/.turing.antwerpen.vsc//'`
        echo "1: $n:$NPROCSMPI" >> .machines
        cpucnt=$(($cpucnt - $NPROCSMPI))
    done
    n=`echo $n | sed -e 's/.turing.antwerpen.vsc//'`
    echo "1: $n:$cpucnt" >> .machines
done
echo granularity:1 >> .machines
echo extrafine:1 >> .machines

######################
#    WIEN commands
clean_lapw -s
x dstart
x dstart -up
x dstart -dn
runsp_lapw -I -p -ec 0.0001

#clean_lapw -s
#x dstart
#run_lapw -p -it -ec 0.0001
#x dstart
#x lapw0 -p
#x lapw1 
#x lapw2 -p

##runsp_lapw -I -i 100 -p -it -ec 0.0001 -orb
##min -NI -s 1 -j 'runsp_lapw -I -i 100 -p -it -fc 2.0 -orb'
#min -NI -s 1 -j 'runsp_lapw -NI -i 40 -fc 2.0 -p -it -orb '.
#min -s 1 -j 'runsp_lapw -I -i 100 -fc 2.0 -p -it -orb'.
#run_lapw -p -ec 0.00001 -i 50 -in1new 1.
#run_lapw -p -ec 0.0001.
#optimize.job
#x lapw2 -p -qtl
#x tetra


######################

