import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def run_kmeans(df, n_clusters):
    estimator = KMeans(n_clusters = n_clusters, random_state = 0)
    return estimator.fit(df)

def plot_elbow_curve(df, max_n_clusters = 10):
    # Create a plot of mean distance from cluster centroid as a function of
    # number of Kmeans clusters.
    from scipy.spatial.distance import cdist
    
    distortions = []
    for k in range(2, max_n_clusters + 1):
        km = run_kmeans(df, k)
        distortions.append(np.mean(np.min(cdist(df, km.cluster_centers_, 'euclidean'), axis=1)))
    plt.plot(range(2, max_n_clusters + 1), distortions)
    plt.xlabel("# Clusters")
    plt.ylabel("Mean distance from centroid")
