#!/bin/bash
#PBS -l walltime=1:0:0
#PBS -l nodes=1:ppn=32,gpus=4

module load PyTorch/1.2.0-fosscuda-2019.08-Python-3.7.2

# MPI-able TensorFlow
module load TensorFlow/1.14.0-fosscuda-2019.08-Python-3.7.2

# multi-node TensorFlow via Horovod
module load Horovod/0.18.1-fosscuda-2019.08-Python-3.7.2
