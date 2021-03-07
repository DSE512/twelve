import numpy as np

from mpi4py import MPI
from sklearn import datasets
from argparse import ArgumentParser
from twelve.unsupervised.kmeans import Kmeans, kmeans_save


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--num_samples', type=int, default=100,
                        help='dataset size')
    parser.add_argument('--k', type=int, default=3,
                        help='number of clusters of k-means algoritm')
    parser.add_argument('--num_features', type=int, default=2,
                        help='number of clusters of k-means algoritm')
    parser.add_argument('--num_centers', type=int, default=3,
                        help='number of actual clusters in the data')
    parser.add_argument('--savepath', type=str, default="./results",
                        help='path to the save loss curves')
    parser.add_argument('--verbose', action="store_true",
                        help='print what is going on')
    return parser.parse_args()


def log(statement, rank=0):
    delim = "=" * 15
    print(f"{delim} Rank {rank} {delim}")
    print(f"{statement}\n")


def main():
    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    args = parse_args()

    if rank == 0:
        x_train, _ = datasets.make_blobs(
            n_samples=args.num_samples, 
            centers=args.num_centers, 
            n_features=args.num_features
        )

        subset_size = args.num_samples // size
        subset = np.zeros((subset_size, args.num_features), dtype=np.float64)
    else:
        subset_size = args.num_samples // size
        x_train = np.zeros((args.num_samples, args.num_features), dtype=np.float64)
        subset = np.zeros((subset_size, args.num_features), dtype=np.float64)

    comm.Scatter([x_train, MPI.DOUBLE], subset, root=0)

    if args.verbose:
        log(f"Received data of shape shape {subset.shape}", rank)


if __name__=="__main__":
    main()
