import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram

def load_data(file):
    data = []
    with open(file, encoding='utf-8') as csvfile:
        read_data = csv.DictReader(csvfile)
        for row in read_data:
            data.append(dict(row))
    return data

def calc_features(row):
    #converting each stat to float for xi, as stated in directions.
    x1 = float(row['Population'])
    x2 = float(row['Net migration'])
    x3 = float(row['GDP ($ per capita)'])
    x4 = float(row['Literacy (%)'])
    x5 = float(row['Phones (per 1000)'])
    x6 = float(row['Infant mortality (per 1000 births)'])
    features = np.array([x1, x2, x3, x4, x5, x6], dtype=np.float64)
    return features

def hac(features):
    n = len(features)
    distances = np.zeros((n, n)) #initializing empty distance matrix with size n x n to contain distances between all data points.
    
    #calculating the distances between all data points.
    for i in range(n):
        for j in range(i + 1, n):
            distances[i, j] = np.linalg.norm(features[i] - features[j])  #euclidian distance
            distances[j, i] = distances[i, j]   #distance is the same, no matter the order of the two points. 
    
    Z = np.zeros((n - 1, 4))  #initializing Z as an (n − 1) × 4 array.

    sizes_of_clusters = {}
    for i in range(n):
        sizes_of_clusters[i] = 1 #clusters start as 1 data point.

    current_clusters = {}
    for i in range(n):
        current_clusters[i] = i
    
    for iteration in range(n - 1):
        #using single-linkage, "the shortest distance from any item in one cluster to any item in the other cluster" as described in lecture.
        min_distance = np.inf  #start with infinite distance.
        two_clusters = (-1, -1)
        for i in current_clusters.keys():
            for j in current_clusters.keys():
                if i >= j:  
                    continue
                if distances[i, j] < min_distance:
                    min_distance = distances[i, j]
                    two_clusters = (i, j)
                elif distances[i, j] == min_distance:  #tie-breaking by picking pair with smallest first index and smallest second index.
                    if i < two_clusters[0] or (i == two_clusters[0] and j < two_clusters[1]):
                        two_clusters = (i, j)
        
        #merging the clusters.
        i, j = two_clusters
        Z[iteration, 0] = min(i, j) #indices of the two clusters merged in the ith iteration. 
        Z[iteration, 1] = max(i, j)
        Z[iteration, 2] = min_distance #single linkage distance between two clusters.
        Z[iteration, 3] = sizes_of_clusters[i] + sizes_of_clusters[j]
        new_cluster = n + iteration #making a new cluster.
        sizes_of_clusters[new_cluster] = sizes_of_clusters[i] + sizes_of_clusters[j] #updating the size of each cluster.
        
        #adding a column and row at the end to store the distances to the new cluster
        #Model: ChatGPT (GPT-4) 
        #Prompt: How can I add an additional row and column to a NumPy array? 
        updated_distances = np.zeros((distances.shape[0] + 1, distances.shape[1] + 1))
        updated_distances[:distances.shape[0], :distances.shape[1]] = distances
        
        #updating distances.
        for k in current_clusters.keys():
            if k == i or k == j:  #skipping the merged clusters.
                continue
            updated_distances[new_cluster, k] = min(distances[i, k], distances[j, k])
            updated_distances[k, new_cluster] = updated_distances[new_cluster, k]

        #removing the two old clusters and adding the new one.
        del current_clusters[i]
        del current_clusters[j]
        current_clusters[new_cluster] = new_cluster 
        distances = updated_distances
    
    return Z

def fig_hac(Z, names):
    fig = plt.figure()
    dendrogram(Z, labels=names, leaf_rotation=90) #leaf_rotation=90 turns the country names 90 degrees to match the example shown in the directions.
    fig.tight_layout()
    return fig

def normalize_features(features):
    x = np.array(features)
    col_min = np.min(x, axis=0) #axis=0 gets minimum column-wise
    col_max = np.max(x, axis=0) #axis=0 gets maximum column-wise
    normalized_features = (x - col_min) / (col_max - col_min) #equation given by directions to calculate normalized feature values for each point. 
    return normalized_features.tolist()

