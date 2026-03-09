from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    dataset = np.load(filename)
    dataset_mean = np.mean(dataset, axis=0)
    dataset_centered = dataset - dataset_mean
    return dataset_centered

def get_covariance(dataset):
    covariance_matrix = np.dot(np.transpose(dataset), dataset) / (dataset.shape[0]-1)
    return covariance_matrix

def get_eig(S, k):
    eigen_values, eigen_vectors = eigh(S)
    sorted_indices = np.argsort(eigen_values)[::-1]
    
    k_indices = sorted_indices[:k]
    k_largest_eigen_values = eigen_values[k_indices]
    
    lam = np.diag(k_largest_eigen_values)
    U = eigen_vectors[:, k_indices]
    return lam, U

def get_eig_prop(S, prop):
    eigen_values, eigen_vectors = eigh(S)
    sorted_indices = np.argsort(eigen_values)[::-1]
    sorted_eigenvalues = eigen_values[sorted_indices]
    sorted_eigenvectors = eigen_vectors[:, sorted_indices]
    
    total_variance = np.sum(sorted_eigenvalues)
    explained_variance_props = sorted_eigenvalues / total_variance
    
    indices_to_use = np.where(explained_variance_props >= prop)[0] #using all eigenvalues/eigenvectors that explain more than a proportion (prop) of the variance.
    eigenvalues_to_use = sorted_eigenvalues[indices_to_use]
    lam = np.diag(eigenvalues_to_use)
    U = sorted_eigenvectors[:, indices_to_use]
    
    return lam, U

def project_image(image, U):
    proj = np.dot(np.transpose(U), image)
    return np.dot(U, proj)
    
def display_image(orig, proj):
    orig_image = orig.reshape(64, 64)
    proj_image = proj.reshape(64, 64)
    
    fig, (ax1, ax2) = plt.subplots(figsize=(9, 3), ncols=2) #desired format 

    ax1.imshow(orig_image)
    ax1.set_title('Original')
    plt.colorbar(ax1.imshow(orig_image), ax=ax1)
    
    ax2.imshow(proj_image)
    ax2.set_title('Projection')
    plt.colorbar(ax2.imshow(proj_image), ax=ax2)
    
    return fig, ax1, ax2

def perturb_image(image, U, sigma):
    proj = np.dot(np.transpose(U), image)
    gaussian_distribution = np.random.normal(0, sigma, size=proj.shape) #mean of 0, S.D. of sigma
    perturb_proj = proj + gaussian_distribution #"Perturbed weights are addition of original weights and perturbation."
    return np.dot(U, perturb_proj)

def display_perturbed_image(orig, perturb): #Similar to display_image, just notes that the image is perturbed as show in directions. 
    orig_image = orig.reshape(64, 64)
    perturb_image = perturb.reshape(64, 64)
    
    fig, (ax1, ax2) = plt.subplots(figsize=(9, 3), ncols=2) 

    ax1.imshow(perturb_image)
    ax1.set_title('Original')
    plt.colorbar(ax1.imshow(orig_image), ax=ax1)
    
    ax2.imshow(proj_image)
    ax2.set_title('Perturbed')
    plt.colorbar(ax2.imshow(perturb_image), ax=ax2)
    
    return fig, ax1, ax2

def combine_image(image1, image2, U, lam):
    proj_image1 = np.dot(np.transpose(U), image1)
    proj_image2 = np.dot(np.transpose(U), image2)
    proj_combined = lam * proj_image1 + (1 - lam) * proj_image2 #lambda * a1 + (1 - lambda) * a2
    return np.dot(U, proj_combined)

def display_image_combo(image1, image2, combined_image): #adapted from display_image() to take in 3 arguments
    image1 = image1.reshape(64, 64)
    image2 = image2.reshape(64, 64)
    combined_image = combined_image.reshape(64, 64)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
    
    ax1.imshow(image1)
    ax1.set_title("Image 1")
    plt.colorbar(ax1.imshow(image1), ax=ax1)
    
    ax2.imshow(image2)
    ax2.set_title("Image 2")
    plt.colorbar(ax2.imshow(image2), ax=ax2)
    
    ax3.imshow(combined_image)
    ax3.set_title("Combined Image")
    plt.colorbar(ax3.imshow(combined_image), ax=ax3)
    
    return fig, ax1, ax2, ax3
    