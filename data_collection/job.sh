#!/bin/bash
#
#SBATCH --job-name=2019turk
#SBATCH --output=2019turk.out
#
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=1000



python ./reddit_api.py 