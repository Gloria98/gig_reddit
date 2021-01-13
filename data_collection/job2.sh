#!/bin/bash
#
#SBATCH --job-name=uberpeople
#SBATCH --output=uberpeople.out
#
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=1000
#
#SBATCH --array=0-22


python ./uberpeople.py $SLURM_ARRAY_TASK_ID