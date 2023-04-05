#!/bin/bash

module swap cluster/slaking 
export SLURM_CLUSTERS="slaking"
/usr/libexec/jobcli/qsub ~/job_scripts/test.sh >& ~/job.out
