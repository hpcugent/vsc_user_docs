#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=1:0:0
#
# Example (single-core) MATLAB job script
# see http://hpcugent.github.io/vsc_user_docs/
#

# make sure the MATLAB version matches with the one used to compile the MATLAB program!
module load MATLAB/2018a

# use temporary directory (not $HOME) for (mostly useless) MATLAB log files
# subdir in $TMPDIR (if defined, or /tmp otherwise)
export MATLAB_LOG_DIR=$(mktemp -d -p  ${TMPDIR:-/tmp})

# configure MATLAB Compiler Runtime cache location & size (1GB)
# use a temporary directory in /dev/shm (i.e. in memory) for performance reasons
export MCR_CACHE_ROOT=$(mktemp -d -p /dev/shm)
export MCR_CACHE_SIZE=1024MB

# change to directory where job script was submitted from
cd $PBS_O_WORKDIR

# run compiled example MATLAB program 'example', provide '5' as input argument to the program
# $EBROOTMATLAB points to MATLAB installation directory
./run_example.sh $EBROOTMATLAB 5
