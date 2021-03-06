import numpy as np

from mpi4py import MPI
from pathlib import Path
from sklearn import datasets
from argparse import ArgumentParser

from twelve.unsupervised import (
    kmeans_save, KmeansDistributed
)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--num_samples", type=int, default=100, 
                        help="dataset size")
    parser.add_argument("--k", type=int, default=3, 
                        help="number of clusters of k-means algoritm")
    parser.add_argument("--num_features", type=int, default=2,
                        help="number of clusters of k-means algoritm")
    parser.add_argument("--num_centers", type=int, default=3,
                        help="number of actual clusters in the data")
    parser.add_argument("--savepath", type=str, default="./results", 
                        help="path to the save loss curves")
    parser.add_argument("--verbose", action="store_true", 
                        help="print what is going on")
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
        x_train, y_train = datasets.make_blobs(
            n_samples=args.num_samples,
            centers=args.num_centers,
            n_features=args.num_features,
        )

        subset_size = args.num_samples // size
        x_subset = np.zeros((subset_size, args.num_features), dtype=np.float64)
        y_subset = np.zeros((subset_size,), dtype=np.float64)
    else:
        subset_size = args.num_samples // size
        x_train = np.zeros((args.num_samples, args.num_features), dtype=np.float64)
        y_train = np.zeros((args.num_samples, args.num_features), dtype=np.float64)
        x_subset = np.zeros((subset_size, args.num_features), dtype=np.float64)
        y_subset = np.zeros((subset_size,), dtype=np.float64)

    comm.Scatter([x_train, MPI.DOUBLE], x_subset, root=0)
    comm.Scatter([y_train, MPI.INT], y_subset, root=0)

    if args.verbose:
        log(f"Received data, labels of shape {x_subset.shape}, {y_subset.shape}", rank)

    model = KmeansDistributed(comm, rank, args.k)
    predictions, centroids = model.predict(x_subset)

    kmeans_save(
        data=x_subset,
        target=y_subset,
        predictions=predictions,
        centroids=centroids,
        path=Path(args.savepath).joinpath(f'save_rank{rank}.pt')
    )


if __name__ == "__main__":
    main()
