#!/bin/bash
#SBATCH --partition=shared-bigmem
#SBATCH --ntasks=1
#SBATCH --job-name=FlukaCrossSection
#SBATCH --mem=2G
#SBATCH --time=12:00:00
#SBATCH --array=0-9
#SBATCH --output=/srv/beegfs/scratch/users/c/coppinp/Simu_vary_cross_section/OUT/log-%A_%a.out

echo $(date) - This is $(hostname), executing task

echo "Sourcing Software"
source /cvmfs/dampe.cern.ch/centos7/etc/setup.sh
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/9.2.0/x86_64-centos7/setup.sh

mkdir /srv/beegfs/scratch/users/c/coppinp/temp/${SLURM_JOB_ID}_$SLURM_ARRAY_TASK_ID
cd /srv/beegfs/scratch/users/c/coppinp/temp/${SLURM_JOB_ID}_$SLURM_ARRAY_TASK_ID

### For proton and helium
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka.py $SLURM_ARRAY_TASK_ID 0
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka.py $SLURM_ARRAY_TASK_ID 1
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka.py $SLURM_ARRAY_TASK_ID 2

# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 3 6 Li6
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 3 7 Li7

# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 4 7 Be7
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 4 9 Be9
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 4 10 Be10

# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 5 9 B9
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 5 10 B10
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 5 11 B11

# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 6 12 C12
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 6 13 C13

# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 8 16 O16

# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 10 20 Ne20
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 12 24 Mg24
# python /dpnc/beegfs/users/coppinp/FLUKA/Development/ExtractOverEnergyRange/ParsingFluka-ions.py $SLURM_ARRAY_TASK_ID 26 56 Fe56

echo $(date) - All done.