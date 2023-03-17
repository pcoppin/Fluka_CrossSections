#!/bin/bash
#SBATCH --partition=private-dpnc-cpu
#SBATCH --ntasks=1
#SBATCH --job-name=SelectMC
#SBATCH --mem=2G
#SBATCH --time=12:00:00
#SBATCH --array=0-9
#SBATCH --output=/srv/beegfs/scratch/users/c/coppinp/Simu_vary_cross_section/OUT/log-%A_%a.out

echo $(date) - This is $(hostname), executing task

echo "Sourcing Software"
source /cvmfs/dampe.cern.ch/centos7/etc/setup.sh
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/9.2.0/x86_64-centos7/setup.sh

cd /srv/beegfs/scratch/users/c/coppinp/temp/$SLURM_ARRAY_TASK_ID
python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka.py $SLURM_ARRAY_TASK_ID

echo $(date) - All done.