"""
all_pather.py

Scatter values to all ranks and gather them back! Note that
the number of values to be scattered equal the number of ranks
that you are scattering to.

Usage:
mpirun -n <procs> python all_gather.py
"""
import numpy as np

from mpi4py import MPI


def banner(comm=MPI.COMM_WORLD):
    """Print a banner of run info"""
    if comm.rank == 0:
        print("="*18)
        print(f"Running on {comm.size} ranks")
        print("="*18)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    banner()

    if rank == 0:
        data = [x for x in range(size)]
        print(f"\nRank {rank} scattering {data}")
    else:
        data = None

    data = comm.scatter(data, root=0)
    print(f"Rank {rank} after scatter has {data}")

    comm.Barrier()

    if rank == 0:
        print(f"\n****Gathering!****\n")

    # Note that we no longer specify the root here!
    data = comm.allgather(data)
    print(f"Rank {rank} after gather has {data}\n")


if __name__=="__main__":
    main()
