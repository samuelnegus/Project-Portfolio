# HW7: Implementing LeNet-5 and Training on MiniPlaces Dataset

This project involves implementing and training LeNet-5, a convolutional neural network (CNN), on the MiniPlaces scene recognition dataset. Additionally, the project explores the impact of different hyperparameter configurations on training performance.

---

## Assignment Goals

1. **Implement LeNet-5**: Develop a CNN based on the LeNet-5 architecture using PyTorch.
2. **Count Trainable Parameters**: Calculate the number of trainable parameters in the model.
3. **Hyperparameter Tuning**: Train LeNet-5 under various hyperparameter configurations to evaluate its performance.
4. **Scene Recognition**: Classify scenes in the MiniPlaces dataset with high accuracy.

---

## Dataset

### MiniPlaces Dataset
The MiniPlaces dataset contains:
- **Training Set**: 100,000 images
- **Validation Set**: 10,000 images
- **Test Set**: 10,000 images

Each image is resized to **32×32 pixels** and belongs to one of **100 scene categories**.

---

## Implementation Details

### 1. **LeNet-5 Architecture**
The `LeNet` class implements the following architecture:
1. **Conv Layer 1**: 6 output channels, kernel size = 5, stride = 1, followed by ReLU and Max Pool (kernel size = 2, stride = 2).
2. **Conv Layer 2**: 16 output channels, kernel size = 5, stride = 1, followed by ReLU and Max Pool (kernel size = 2, stride = 2).
3. **Flatten Layer**: Converts the 3D tensor into a 1D tensor.
4. **Fully Connected Layer 1**: Input size = 400, output size = 256, followed by ReLU.
5. **Fully Connected Layer 2**: Input size = 256, output size = 128, followed by ReLU.
6. **Output Layer**: Input size = 128, output size = 100 (number of scene classes).

**Output**: 
- `output`: Model predictions for the input batch.
- `shape_dict`: Dictionary containing the shape of intermediate outputs for debugging and visualization.

### 2. **Counting Trainable Parameters**
The `count_model_params` function calculates the total number of trainable parameters in the LeNet-5 model:
- Iterates through all trainable parameters in the model using `model.named_parameters()`.
- Returns the parameter count in **millions (1e6)**.

### 3. **Training and Testing**
#### `train_model`:
- Trains the model for a given number of epochs.
- Uses the **Cross-Entropy Loss** as the loss function.
- Optimizes using **Stochastic Gradient Descent (SGD)** with adjustable learning rate and momentum.
- Outputs average training loss per epoch.

#### `test_model`:
- Evaluates the trained model on the test/validation set.
- Computes the accuracy of predictions.

---

## Training Configurations

The model was trained under the following configurations:

| **Configuration** | **Batch Size** | **Learning Rate** | **Epochs** |
|--------------------|----------------|--------------------|------------|
| Default            | 64             | 0.001              | 10         |
| Configuration 1    | 8              | 0.001              | 10         |
| Configuration 2    | 16             | 0.001              | 10         |
| Configuration 3    | 64             | 0.05               | 10         |
| Configuration 4    | 64             | 0.01               | 10         |
| Configuration 5    | 64             | 0.001              | 20         |
| Configuration 6    | 64             | 0.001              | 5          |


