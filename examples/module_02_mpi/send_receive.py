from mpi4py import MPI


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        data = {'hello': 0, 'world!': 1}
        comm.send(data, dest=1)
    elif rank == 1:
        data = comm.recv(source=0)


if __name__=="__main__":
    main()


