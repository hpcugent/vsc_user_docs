#!/bin/sh

#PBS -N nwchem-h2o
#PBS -q qshort
#PBS -l nodes=3:ppn=8:ib
#PBS -l walltime=1:00:00

module purge
module load NWChem/5.1.1-LINUX64-RHELWS4-ifort-MPICH2-EM64T 
module load mpiexec

job=h2o

echo "job = $job"
base=$PBS_O_WORKDIR

export NWCHEM_SCRDIR=${VSC_SCRATCH}/nwchem/$job.$PBS_JOBID
if [ ! -d $NWCHEM_SCRDIR ]
then
  mkdir -p $NWCHEM_SCRDIR
fi

cd $NWCHEM_SCRDIR

cp $PBS_O_WORKDIR/$job.nw .
 

mpiexec nwchem $job.nw > $base/$job.out

/bin/rm -R $NWCHEM_SCRDIR
