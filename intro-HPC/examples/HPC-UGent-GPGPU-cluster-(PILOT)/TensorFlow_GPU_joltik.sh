#!/bin/bash
#PBS -l walltime=1:0:0
#PBS -l nodes=1:ppn=32,gpus=4

module load TensorFlow/1.14.0-fosscuda-2019.08-Python-3.7.2

cd $PBS_O_WORKDIR
python example.py
