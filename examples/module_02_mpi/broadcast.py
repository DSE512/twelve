"""
broadcast.py

Usage:
mpirun -n <procs> python broadcast.py
"""
import numpy as np

from mpi4py import MPI


def main():
    comm = MPI.COMM_WORLD
    rank = comm.rank

    if rank == 0:
        x = np.random.randn(4)
    else:
        x = np.empty(4, dtype=np.float64)

    print(f"Rank {rank} before broadcast has {x}")
    comm.Bcast([x, MPI.DOUBLE])
    print(f"Rank {rank} after broadcast has {x}\n")


if __name__=="__main__":
    main()
