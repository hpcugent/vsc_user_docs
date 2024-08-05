#!/bin/bash
#PBS -l walltime=5:0:0
#PBS -l nodes=1:ppn=quarter:gpus=1

module load TensorFlow/2.11.0-foss-2022a-CUDA-11.7.0

cd $PBS_O_WORKDIR
python example.py
