import numpy as np
from mpi4py import MPI


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()


    if rank == 0:
        data = np.arange(10_000, dtype=np.int64)
        comm.Send([data, MPI.INT], dest=1, tag=77)
    elif rank == 1:
        data = np.empty(10_000, dtype=np.int64)
        comm.Recv([data, MPI.INT], source=0, tag=77)
        print(f"Rank {rank} received {data}")


if __name__=="__main__":
    main()
