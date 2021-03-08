import torch
import numpy as np

from twelve.unsupervised.kmeans import (
    Kmeans, euclidean_distance
)


class KmeansDistributed(Kmeans):
    """Clustering around k centroids"""

    def __init__(self, comm, rank, k=2, num_iterations=100):
        super().__init__(k, num_iterations)
        self.comm = comm
        self.rank = rank

    def initialize_centroids(self, data):
        """Randomly initialize centroids

        Randomly choose points in our data to be the
        positions of our centroids
        """
        num_samples, num_features = data.shape

        if self.rank == 0:
            idx = np.random.choice(
                num_samples, (self.k,), replace=False
            )

            centroids = data[idx, :]
        else:
            centroids = np.zeros(
                (self.k, num_features), dtype=np.float64
            )

        self.comm.bcast(centroids, root=0)

    def nearest_centroid(self, sample, centroids):
        """Find the nearest centroid for a data point

        Args:
            sample: np.array of shape (1, num_features),
                    a single data point
            centroids: current centroid positions
        """
        nearest = None
        nearest_distance = np.inf

        for idx, centroid in enumerate(centroids):
            distance = euclidean_distance(sample, centroid)
            if distance < nearest_distance:
                nearest = idx
                nearest_distance = distance

        return nearest

    def assign_clusters(self, data, centroids):
        """Assign the data to the nearest centroids"""
        num_samples, _ = data.shape

        clusters = [[] for _ in range(self.k)]

        for idx, sample in enumerate(data):
            nearest_centroid = self.nearest_centroid(sample, centroids)
            clusters[nearest_centroid].append(idx)

        return clusters

    def cluster_assignments(self, data, clusters):
        """Get which cluster each sample is assigned to"""
        num_samples, _ = data.shape

        assignments = np.zeros(num_samples)
        for idx, cluster in enumerate(clusters):
            for sample in cluster:
                assignments[sample] = idx

        return assignments

    def update_centroids(self, data, clusters):
        """Set the centroids to be the mean of the samples in each cluster"""
        _, num_features = data.shape

        centroids = np.zeros((self.k, num_features))

        for idx, cluster in enumerate(clusters):
            centroid = np.mean(data[cluster], axis=0)
            centroids[idx] = centroid

        return centroids

    def predict(self, data):
        """K-means clustering over data"""
        self.initialize_centroids(data)

        for idx in range(self.num_iterations):
            clusters = self.assign_clusters(data, centroids)
            centroids = self.update_centroids(data, clusters)

        cluster_assignments = self.cluster_assignments(data, clusters)

        return cluster_assignments, centroids

