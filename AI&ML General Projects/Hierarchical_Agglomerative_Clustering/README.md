# HW4: Hierarchical Agglomerative Clustering of Socioeconomic Data

This project performs **Hierarchical Agglomerative Clustering (HAC)** to group countries based on socioeconomic statistics, allowing visualization of similarities between countries. The clustering is implemented from scratch, avoiding the use of `scipy.cluster.hierarchy.linkage`.

---

## Assignment Goals
1. **Process Real-World Data**: Work with socioeconomic data for various countries.
2. **Implement Hierarchical Clustering**: Use single-linkage HAC with Euclidean distance.
3. **Normalize Data**: Ensure fair contributions from all features by normalizing values.
4. **Visualize Clustering**: Generate dendrograms to depict the clustering hierarchy.

---

## Dataset

The dataset (`countries.csv`) contains various statistics for multiple countries. Each country is represented by six key socioeconomic features:

1. `Population`
2. `Net migration`
3. `GDP ($ per capita)`
4. `Literacy (%)`
5. `Phones (per 1000)`
6. `Infant mortality (per 1000 births)`

---

## Functions

### 1. `load_data(filepath)`
- **Input**: Path to the dataset (`countries.csv`).
- **Output**: List of dictionaries, where each dictionary corresponds to a row in the dataset with column headers as keys.

### 2. `calc_features(row)`
- **Input**: A dictionary representing one country.
- **Output**: A NumPy array (`shape = (6,)`) containing the six feature values for the country as `float64`.

### 3. `hac(features)`
- **Input**: List of NumPy arrays representing feature vectors for all countries.
- **Output**: A NumPy array (`shape = (n-1, 4)`) detailing the clustering process:
  - Columns:
    1. Indices of the two merged clusters.
    2. Distance between the merged clusters.
    3. Number of countries in the merged cluster.
- **Description**: Implements single-linkage HAC with a distance matrix. Includes tie-breaking rules based on indices.

### 4. `fig_hac(Z, names)`
- **Input**: Clustering array `Z` (output of `hac`) and a list of country names.
- **Output**: A matplotlib figure showing the dendrogram of the clustering.

### 5. `normalize_features(features)`
- **Input**: List of feature vectors (NumPy arrays).
- **Output**: Normalized feature vectors where all values are scaled to the range [0, 1].

---
