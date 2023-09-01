#!/bin/bash
#PBS -N AlphaFold-cpu-doduo
#PBS -l nodes=1:ppn=24
#PBS -l walltime=72:0:0

module load AlphaFold/2.3.1-foss-2022a 

export ALPHAFOLD_DATA_DIR=/arcanine/scratch/gent/apps/AlphaFold/20230310

WORKDIR=$VSC_SCRATCH/$PBS_JOBNAME-$PBS_JOBID
mkdir -p $WORKDIR

# download T1050.fasta via via https://www.predictioncenter.org/casp14/target.cgi?target=T1050&view=sequence
cp -a $PBS_O_WORKDIR/T1050.fasta $WORKDIR/

cd $WORKDIR

alphafold --fasta_paths=T1050.fasta --max_template_date=2020-05-14 --db_preset=full_dbs --output_dir=$PWD
echo "Output available in $WORKDIR"

