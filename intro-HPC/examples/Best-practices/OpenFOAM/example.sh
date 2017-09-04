#!/bin/bash

# set up environment for using OpenFOAM
# check for more recent OpenFOAM modules with 'module avail OpenFOAM'
module load OpenFOAM/4.0-intel-2016b
source $FOAM_BASH

# also load module required for mympirun
# purposely not specifying a particular version to use most recent
module load vsc-mympirun

# let mympirun pass down relevant environment variables to MPI processes
export MYMPIRUN_VARIABLESPREFIX=WM_PROJECT,FOAM,MPI
