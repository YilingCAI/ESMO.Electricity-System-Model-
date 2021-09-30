#!/bin/bash
#PBS -q xlongp
#PBS -l nodes=1:ppn=1
#PBS -l mem=40gb
#PBS -l vmem=60gb

module load python/3.6
source activate my_python

export PYTHONPATH="${PYTHONPATH}:/home/users/ylcai/.conda/envs/my_python/lib/python3.7/site-packages"
export PATH="/home/users/ylcai/opt/ibm/ILOG/CPLEX_Studio1210/cplex/bin/x86-64_linux:$PATH"

cd /home/users/ylcai/model_development/ESMO_test

python runscenario_A1.py "A1"

# python runscenario_A2.py "A2"


