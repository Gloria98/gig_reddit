#!/bin/bash
#
#SBATCH --job-name=action
#SBATCH --output=action.out
#
#SBATCH --ntasks=1
#SBATCH --time=2:00:00
#SBATCH --mem-per-cpu=2000




python ./topic_modeling.py 