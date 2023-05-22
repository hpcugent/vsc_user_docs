#!/bin/bash

module swap cluster/donphan
export SLURM_CLUSTERS="donphan"
/usr/libexec/jobcli/qsub ~/job_scripts/test.sh >& ~/job.out
