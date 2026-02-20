#!/bin/bash
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -J dp
#SBATCH -p xahdnormal #队列
#SBATCH --gres=dcu:4

module purge
source /work/home/baoergen22b/apprepo/deepmd/v2.2.9-dtk23.10/scripts/env.sh
export OMP_NUM_THREADS=8
export TF_INTRA_OP_PARALLELISM_THREADS=8
export TF_INTER_OP_PARALLELISM_THREADS=4
#这个是给dp传参，必须要的，如果每个节点一张卡那么传一个数字，每个节点两张卡可以写0,1，每节点4张卡写0,1,2,3
export CUDA_VISIBLE_DEVICES=0,1,2,3

#执行命令 -np 是总共的进程数量（N * ntasks-per-node）

mpirun -np 4 dp train --mpi-log=workers input.json

