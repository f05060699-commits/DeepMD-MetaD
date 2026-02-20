#!/bin/bash
#SBATCH -J lammps-DCU
#SBATCH -p xahdnormal
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --gres=dcu:4

##SBATCH -c 8
##SBATCH --ntasks-per-node=4

module purge
source /work/home/baoergen22b/apprepo/lammps/2Aug2023-dtk23.10_hpcx274/scripts/env.sh
export UCX_IB_ADDR_TYPE="ib_global"
export UCX_NET_DEVICES="mlx5_0:1,mlx5_1:1,mlx5_2:1,mlx5_3:1"
export UCX_IB_PCI_BW="mlx5_0:50Gbs,mlx5_1:50Gbs,mlx5_2:50Gbs,mlx5_3:50Gbs"

mpirun -np 4 lmp_mpi -sf gpu -pk gpu 4 -in  in.rigid >lmp.out 2>lmp.err 
