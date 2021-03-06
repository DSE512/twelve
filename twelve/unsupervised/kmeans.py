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
    return np.sum(np.square(x1, x2))


class Kmeans:
    """Clustering around k centroids"""

    def __init__(self, k=2, max_iterations=100):
        self.k = k
        self.max_iterations = max_iterations

    def initialize_centroids(self, data):
        """Randomly initialize centroids

        Randomly choose points in our data to be the
        positions of our centroids
        """
        #TODO(Todd): write this
        raise NotImplementedError()
