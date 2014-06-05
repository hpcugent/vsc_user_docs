#!/bin/sh

#PBS -N benchNW-1
#PBS -q qxlong
#PBS -l nodes=16:ppn=8:ib
#PBS -l walltime=168:00:00

module purge
module load NWChem/6.0-ictce-3.2.2.u2
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
 
mpiexec nwchem $job.nw 

/bin/rm -R $NWCHEM_SCRDIR
