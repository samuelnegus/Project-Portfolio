# HW3: Principal Component Analysis (PCA) and Image Manipulation

This project explores Principal Component Analysis (PCA) for dimensionality reduction and visualization, using the Label Faces in the Wild dataset. The goal is to implement PCA-related functions, manipulate image projections, and create visually meaningful results.

## Assignment Goals
- Understand and implement PCA using Python and related libraries.
- Apply PCA to facial images for dimensionality reduction and reconstruction.
- Explore the effects of perturbations and combinations of PCA projections.

## Dataset
- **Source**: Processed subset of the Label Faces in the Wild dataset.
- **Size**: 13,233 grayscale images, each 64×64 pixels.
- Each image is represented as a 4,096-dimensional feature vector.
- Dataset file: `face_dataset.npy`.

## Features

### PCA Functions
1. **Load and Center Dataset**: Centers the dataset around the origin by subtracting the mean.
2. **Covariance Matrix**: Computes the covariance matrix of the dataset.
3. **Eigendecomposition**:
   - Retrieves the top `k` eigenvalues and eigenvectors.
   - Optionally, retrieves eigenvalues/eigenvectors explaining more than a specified proportion of variance.
4. **Image Projection**: Projects an image into a lower-dimensional subspace spanned by eigenvectors.
5. **Image Reconstruction**:
   - Reconstructs images using PCA projections.
   - Supports visual comparison of original and reconstructed images.
6. **Perturbed Images**: Adds Gaussian noise to projection weights and reconstructs the perturbed image.
7. **Combined Images**: Creates a hybrid image by combining projection weights of two images.

### Visualization
- Uses Matplotlib to display images with side-by-side comparisons (e.g., original vs. projection, perturbed, or hybrid images).
- Colorbars enhance visual clarity.
