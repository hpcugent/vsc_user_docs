#!/bin/bash

#PBS -l nodes=1:ppn=1
#PBS -l walltime=1:00:00

## name of the executable
name=magicsquare
## arguments to pass to the executable ("" is no options)
opts="5"
## directory where the executable and script can be found
## PBS_O_WORKDIR variable points to the directory you are submitting from
dir=$PBS_O_WORKDIR
#dir=/path/to/dir

## version: version of MATLAB
version=2018a

## Size of MATLAB cache in memory
cache_size=1024M
#################################################################
###  Don't change things below unless you know what you are doing
#################################################################

module load MATLAB/${version}

if [ ! -d $dir ]
then
  echo "Directory $dir is not a directory"
  exit 1
fi

cd $dir

if [ ! -x $name ]
then
  echo "No executable $name found."
  exit 2
fi
script=run_${name}.sh
if [ ! -x  $script ]
then
  echo "No run script $script found"
  exit 3
fi

## make cache dir
## /dev/shm is memory, so this should be really fast

cdir=$(mktemp -d -p /dev/shm)
if [ ! -d $cdir ]
then
  echo "No tempdir $cdir found."
  exit 1
fi

## set dir
export MCR_CACHE_ROOT=$cdir
## 1GB cache (more then large enough)
export MCR_CACHE_SIZE=$cache_size
## real running
./$script $EBROOTMATLAB $opts
