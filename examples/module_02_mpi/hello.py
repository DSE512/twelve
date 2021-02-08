"""
hello.py

A Hello world for MPI programs.

Usage:
mpirun -n <procs> python hello.py

where <procs> is an integer number of processes.
"""
from mpi4py import MPI


def main():
    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    print(f"Hello from rank {rank} of size {size}")
    # Wait for everyone to sync up
    comm.Barrier()


if __name__=="__main__":
    main()
