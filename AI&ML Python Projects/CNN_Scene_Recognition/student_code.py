# python imports
import os
from tqdm import tqdm

# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F #From https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html


#LeNet class modeled after tutorial on this page https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html

class LeNet(nn.Module):
    def __init__(self, input_shape=(32, 32), num_classes=100):
        super(LeNet, self).__init__ ()
        # certain definitions
        #First convolutional layer: inputting 3 channels for RGB, outputting 6 channels.
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=5, stride=1) #Kernel size 5 and stride 1

        self.pool = nn.MaxPool2d(kernel_size=2, stride=2) #2D Max Pool to be used on both convolutional layers.

        #Second convolutional layer: inputting 6 channels from last layer, outputting 16 channels.
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5, stride=1) #Kernel size 5 and stride 1

        self.flattened = 16 * 5 * 5 #Flattening to convert 3D tensor to 1D.

        #Three linear layers with outputting appropriate dimensions from instructions. 
        self.lin1 = nn.Linear(self.flattened, 256) #Taking in dimensions after flatten layer, output dim 256. 
        self.lin2 = nn.Linear(256, 128) #Output dim 128. 
        self.lin3 = nn.Linear(128, num_classes) #Third linear layer where the output dimension is the # of classes.

    def forward(self, x):
        shape_dict = {}
        # certain operations
        #Updating x for each layer and operation performed. 
        x = F.relu(self.conv1(x)) #ReLU activation using torch functional following the first convolutional layer. 
        x = F.max_pool2d(x, (2, 2)) #Applying 2d Max Pool operation using torch functional.
        shape_dict[1] = list(x.shape)

        x = F.relu(self.conv2(x)) #ReLU activation following the second convolutional layer. 
        x = F.max_pool2d(x, (2, 2)) #Applying the 2d Max Pool operation using torch functional. 
        shape_dict[2] = list(x.shape)

        x = torch.flatten(x, 1)  #Converting tensor from 3d to 1d using torch as shown in the tutorial.  
        shape_dict[3] = list(x.shape)

        x = F.relu(self.lin1(x)) #First two linear layers have ReLU activation applied. 
        shape_dict[4] = list(x.shape)
        x = F.relu(self.lin2(x))
        shape_dict[5] = list(x.shape)
        output = self.lin3(x) #Last layer, output. 
        shape_dict[6] = list(output.shape)
        
        return output, shape_dict

def count_model_params():
    '''
    return the number of trainable parameters of LeNet.
    '''
    model = LeNet()
    model_params = 0.0
    for name, parameter in model.named_parameters():
        if parameter.requires_grad: #Check if the parameter is trainable. 
            model_params += parameter.numel() #Adding total number of parameters. 
            
    return model_params / 1e6 #Returning result in millions. 

def train_model(model, train_loader, optimizer, criterion, epoch):
    """
    model (torch.nn.module): The model created to train
    train_loader (pytorch data loader): Training data loader
    optimizer (optimizer.*): A instance of some sort of optimizer, usually SGD
    criterion (nn.CrossEntropyLoss) : Loss function used to train the network
    epoch (int): Current epoch number
    """
    model.train()
    train_loss = 0.0
    for input, target in tqdm(train_loader, total=len(train_loader)):
        # 1) zero the parameter gradients
        optimizer.zero_grad()
        # 2) forward + backward + optimize
        output, _ = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        # Update the train_loss variable
        # .item() detaches the node from the computational graph
        train_loss += loss.item()

    train_loss /= len(train_loader)
    print('[Training set] Epoch: {:d}, Average loss: {:.4f}'.format(epoch+1, train_loss))

    return train_loss

def test_model(model, test_loader, epoch):
    model.eval()
    correct = 0
    with torch.no_grad():
        for input, target in test_loader:
            output, _ = model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_acc = correct / len(test_loader.dataset)
    print('[Test set] Epoch: {:d}, Accuracy: {:.2f}%\n'.format(
        epoch+1, 100. * test_acc))

    return test_acc
