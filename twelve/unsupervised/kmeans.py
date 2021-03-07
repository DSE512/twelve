import torch
import numpy as np


def euclidean_distance(x1, x2):
    """Squared distance

    We are ignoring the sqrt here to since it
    does not affect k-means, and we gain a bit
    of speed. 

    Note:
        While k-means is unaffected by using the 
        squared distance, other clustering 
        algorithms, like hierarchical clustering,
        are affected. Instead, you should use the 
        regular Euclidean distance.
    """
    return np.sum(np.square(x1 - x2))


class Kmeans:
    """Clustering around k centroids"""

    def __init__(self, k=2, num_iterations=100):
        self.k = k
        self.num_iterations = num_iterations

    def initialize_centroids(self, data):
        """Randomly initialize centroids

        Randomly choose points in our data to be the
        positions of our centroids
        """
        num_samples, _ = data.shape

        idx = np.random.choice(
            num_samples, (self.k,), replace=False
        )

        return data[idx, :]

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
        centroids = self.initialize_centroids(data)

        for idx in range(self.num_iterations):
            clusters = self.assign_clusters(data, centroids)
            centroids = self.update_centroids(data, clusters)

        cluster_assignments = self.cluster_assignments(data, clusters)

        return cluster_assignments, centroids


def kmeans_save(data, target, predictions, centroids, path):
    """Save both the data and our predictions"""
    torch.save({
        "data": data,
        "target": target,
        "predictions": predictions,
        "centroids": centroids
    }, path)


if __name__ == "__main__":
    from sklearn import datasets

    data, _ = datasets.make_blobs(n_features=10)
    print(f"blobs: {data.shape}")

    model = Kmeans(k=10)
    assignments, _ = model.predict(data)

    print(assignments.shape)
    print(assignments)

