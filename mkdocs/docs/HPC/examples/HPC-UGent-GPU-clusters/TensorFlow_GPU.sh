#!/bin/bash
#PBS -l walltime=5:0:0
#PBS -l nodes=1:ppn=quarter:gpus=1

module load TensorFlow/2.6.0-foss-2021a-CUDA-11.3.1

cd $PBS_O_WORKDIR
python example.py
