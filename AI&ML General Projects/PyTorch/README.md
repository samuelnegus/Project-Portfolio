# HW6: Introduction to PyTorch

This project introduces the PyTorch framework for deep learning by implementing, training, and evaluating a neural network to classify images from the Fashion-MNIST dataset.

---

## Assignment Goals

1. **Setup a Virtual Environment**: Learn to manage Python environments using `venv`.
2. **Build and Train a Neural Network**: Create a simple neural network with PyTorch for image classification.
3. **Model Evaluation and Predictions**: Test model performance on unseen data and predict labels for specific images.
4. **Understand PyTorch Basics**: Familiarize yourself with PyTorch utilities such as `DataLoader`, `nn.Module`, and `optim`.

---

## Dataset

The dataset used is **Fashion-MNIST**, which consists of grayscale images of size 28×28, each belonging to one of 10 classes:

- `T-shirt/top`
- `Trouser`
- `Pullover`
- `Dress`
- `Coat`
- `Sandal`
- `Shirt`
- `Sneaker`
- `Bag`
- `Ankle Boot`

The dataset is automatically downloaded using PyTorch utilities.

---

## Implemented Features

### 1. **Data Loading**
The function `get_data_loader(training=True)` returns a `DataLoader` object for either the training set (60,000 images) or the test set (10,000 images), with:
- **Batch Size**: 64
- **Transformations**:
  - Conversion to tensor.
  - Normalization using mean = 0.1307 and std = 0.3081.

### 2. **Model Architecture**
The model is a simple feedforward neural network with three layers:
1. **Flatten**: Converts 2D images into 1D arrays.
2. **Dense Layer 1**: 128 neurons with ReLU activation.
3. **Dense Layer 2**: 64 neurons with ReLU activation.
4. **Output Layer**: 10 neurons (one for each class).

### 3. **Model Training**
The `train_model` function trains the model using:
- **Criterion**: Cross-Entropy Loss.
- **Optimizer**: Stochastic Gradient Descent (SGD) with:
  - Learning Rate = 0.001
  - Momentum = 0.9
- **Output**: Training loss and accuracy after every epoch.

### 4. **Model Evaluation**
The `evaluate_model` function tests the model on the test dataset and reports:
- Accuracy (formatted to 2 decimal places).
- Average loss (formatted to 4 decimal places, if `show_loss=True`).

### 5. **Label Prediction**
The `predict_label` function predicts the top 3 most likely labels for a given test image. It displays:
- Label names.
- Probabilities (formatted to 2 decimal places).

