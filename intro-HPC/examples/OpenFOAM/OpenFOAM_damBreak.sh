#!/bin/bash
#PBS -l walltime=1:0:0
#PBS -l nodes=1:ppn=4
# check for more recent OpenFOAM modules with 'module avail OpenFOAM'
module load OpenFOAM/6-intel-2018a
source $FOAM_BASH
# purposely not specifying a particular version to use most recent mympirun
module load vsc-mympirun
# let mympirun pass down relevant environment variables to MPI processes
export MYMPIRUN_VARIABLESPREFIX=WM_PROJECT,FOAM,MPI
# set up working directory
# (uncomment one line defining $WORKDIR below)
#export WORKDIR=$VSC_SCRATCH/$PBS_JOBID  # for small multi-node jobs
#export WORKDIR=$VSC_SCRATCH_ARCANINE/$PBS_JOBID  # for large multi-node jobs (not on available victini)
export WORKDIR=$VSC_SCRATCH_NODE/$PBS_JOBID  # for single-node jobs
mkdir -p $WORKDIR
# damBreak tutorial, see also https://cfd.direct/openfoam/user-guide/dambreak
cp -r $FOAM_TUTORIALS/multiphase/interFoam/laminar/damBreak/damBreak $WORKDIR
cd $WORKDIR/damBreak
echo "working directory: $PWD"
# pre-processing: generate mesh
echo "start blockMesh: $(date)"
blockMesh &> blockMesh.out
# pre-processing: decompose domain for parallel processing
echo "start decomposePar: $(date)"
decomposePar &> decomposePar.out
# run OpenFOAM simulation in parallel
# note:
#  * the -parallel option is strictly required to actually run in parallel!
#    without it, the simulation is run N times on a single core...
#  * mympirun will use all available cores in the job by default,
#    you need to make sure this matches the number of subdomains!
echo "start interFoam: $(date)"
mympirun --output=interFoam.out interFoam -parallel
# post-processing: reassemble decomposed domain
echo "start reconstructPar: $(date)"
reconstructPar &> reconstructPar.out
# copy back results, i.e. all time step directories: 0, 0.05, ..., 1.0 and inputs
export RESULTS_DIR=$VSC_DATA/results/$PBS_JOBID
mkdir -p $RESULTS_DIR
cp -a *.out [0-9.]* constant system $RESULTS_DIR
echo "results copied to $RESULTS_DIR at $(date)"
# clean up working directory
cd $HOME
rm -rf $WORKDIR
