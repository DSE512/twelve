"""
scatter_pather.py

Scatter values to all ranks and gather them back!
"""
import numpy as np

from mpi4py import MPI


def banner(comm=MPI.COMM_WORLD):
    """Print a banner of run info"""
    if comm.rank == 0:
        print(f"Running on {comm.size} ranks")


def main():
    comm = MPI.COMM_WORLD
    rank = comm.rank

    if rank == 0:
        data = [x for x in range(comm.size)]
        print(f"Rank {rank} scattering {data}")
    else:
        data = None

    data = comm.scatter(data, root=0)
    print(f"Rank {rank} after scatter has {data}")

    comm.Barrier()

    if rank == 0:
        print(f"****Gathering!****")

    data = comm.gather(data, root=0)
    print(f"Rank {rank} after gather has {data}")


if __name__=="__main__":
    main()
