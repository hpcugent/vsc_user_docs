#!/bin/bash


  # "name" of the job (optional)
#PBS -N my_serial_job         


  # requested running time (required!)
#PBS -l walltime=01:00:00

  # specification (required!)
  #   nodes=   number of nodes; 1 for serial; 1 or more for parallel
  #   ppn=     number of processors per node; 1 for serial; up to 8
  #   if you want your "private" node: ppn=8
  #   mem=     memory required
#PBS -l nodes=1:ppn=1

  # if you want to be sure to get your private node, simply claim all memory ;-)
#  #PBS -l pvmem=16000m


  # send mail notification (optional); may be combined, e.g., -m abe
  #   a        when job is aborted
  #   b        when job begins
  #   e        when job ends
#PBS -m e

  #   M        specify alternate e-mailaddress; default is your institute address
# #PBS -M my.other.address@mail.com


  # redirect standard output (-o) and error (-e) (optional)
  # if omitted, the name of the job (specified by -N) or
  # a generic name (name of the script followed by .o or .e and 
  # job number) will be used
#PBS -o stdout
#PBS -e stderr


  # go to the (current) working directory (optional, if this is the
  # directory where you submitted the job)
cd $PBS_O_WORKDIR  


  # the program itself
echo Start Job
date
hostname
echo End Job
