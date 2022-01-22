#!/bin/bash
. /etc/profile.d/lmod.sh
set -e
module purge
module load   gulp 
module load prun

prun gulp < mof.gin | tee gulp.out
mv fort.20 mof.cif

