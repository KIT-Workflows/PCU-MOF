#! /bin/bash

module purge

export PARA_ARCH=SMP
export TM_PAR_OMP=on

module load turbomole/7.4.1

python run_tm.py

t2x coord > final_structure.xyz

exit 0
